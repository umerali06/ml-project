from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
import pandas as pd
import plotly.express as px
import plotly
import json
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

app = Flask(__name__)


def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dispatch_path = os.path.join(base_dir, 'dispatch_list.csv')
    top50_path = os.path.join(base_dir, 'top_50_dispatch.csv')
    synth_path = os.path.join(base_dir, 'synthetic_gbfs.csv')

    dispatch = pd.read_csv(dispatch_path) if os.path.exists(dispatch_path) else pd.DataFrame()
    top50 = pd.read_csv(top50_path) if os.path.exists(top50_path) else pd.DataFrame()
    synth = pd.read_csv(synth_path) if os.path.exists(synth_path) else pd.DataFrame()
    return dispatch, top50, synth


def recompute_priority(dispatch: pd.DataFrame, synth: pd.DataFrame | None,
                       hub_lat: float, hub_lon: float,
                       w_urg: float, w_dem: float, w_prox: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    import numpy as np

    # Haversine distance
    def hav(lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1; dlon = lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
        return 2*R*np.arcsin(np.sqrt(a))

    # Compute distance
    if 'latitude' in dispatch and 'longitude' in dispatch:
        dispatch['dist_km_to_hub'] = hav(hub_lat, hub_lon, dispatch['latitude'], dispatch['longitude'])

    # Ensure pred_minutes_to_20pct exists
    if 'pred_minutes_to_20pct' not in dispatch:
        if synth is not None and not synth.empty and 'pred_minutes_to_20pct' in synth:
            dispatch = dispatch.merge(synth[['vehicle_id','pred_minutes_to_20pct']], on='vehicle_id', how='left')
        elif 'minutes_to_empty' in dispatch and 'soc_now' in dispatch:
            dispatch['pred_minutes_to_20pct'] = np.maximum(
                0.0,
                dispatch['minutes_to_empty'] * (dispatch['soc_now'] - 0.20) / np.maximum(dispatch['soc_now'], 1e-6)
            )

    # Normalize helper
    def norm(s):
        s = s.astype(float)
        return (s - s.min()) / (s.max() - s.min() + 1e-9)

    if set(['pred_minutes_to_20pct','demand_zone_score','dist_km_to_hub']).issubset(dispatch.columns):
        dispatch['priority_score'] = (
            w_urg * (1 - norm(dispatch['pred_minutes_to_20pct'])) +
            w_dem * norm(dispatch['demand_zone_score']) +
            w_prox * (1 - norm(dispatch['dist_km_to_hub']))
        ).clip(0,1)
        dispatch = dispatch.sort_values('priority_score', ascending=False).reset_index(drop=True)
        if 'rank' in dispatch:
            dispatch['rank'] = range(1, len(dispatch)+1)
    top50 = dispatch.head(50).copy() if not dispatch.empty else pd.DataFrame()
    return dispatch, top50


def generate_synthetic_data(n_vehicles=200, random_seed=42):
    """Generate synthetic vehicle fleet data for testing"""
    if random_seed is not None:
        np.random.seed(random_seed)
    
    zones = [
        ("Villepinte", 48.97, 2.55, 1.2),
        ("Viry-Chatillon", 48.67, 2.38, 1.0),
        ("Roissy-en-Brie", 48.79, 2.65, 1.1),
        ("Malakoff", 48.82, 2.29, 1.05),
        ("Bobigny", 48.92, 2.43, 1.15)
    ]
    
    rows = []
    for i in range(n_vehicles):
        name, zlat, zlon, dbase = zones[np.random.choice(len(zones))]
        lat = zlat + np.random.normal(0, 0.01)
        lon = zlon + np.random.normal(0, 0.015)
        hour = np.random.randint(6, 23)
        dow = np.random.randint(0, 7)
        peak = 1.0 + (0.45 if (7 <= hour <= 9 or 17 <= hour <= 20) else 0)
        weekend = 1 if dow in [5, 6] else 0
        demand = dbase * peak * (1.15 if weekend else 1.0)
        soc = np.clip(np.random.normal(0.45, 0.18), 0.10, 0.95)
        base_minutes_full = 420
        minutes_to_empty = base_minutes_full * (1.0 / demand) * soc + np.random.normal(0, 20)
        minutes_to_empty = max(5, minutes_to_empty)
        
        rows.append({
            'vehicle_id': f"{name[:3].upper()}-{1000+i}",
            'zone_name': name,
            'latitude': lat,
            'longitude': lon,
            'soc_now': round(float(soc), 3),
            'hour': hour,
            'day_of_week': dow,
            'demand_zone_score': round(float(demand), 3),
            'minutes_to_empty': round(float(minutes_to_empty), 1)
        })
    
    return pd.DataFrame(rows)


def run_ml_simulation(random_seed=42):
    """Run the complete ML simulation pipeline"""
    try:
        # Generate synthetic data
        df = generate_synthetic_data(n_vehicles=200, random_seed=random_seed)
        
        # Train ML model
        features = ['soc_now', 'hour', 'day_of_week', 'demand_zone_score']
        X = df[features].values
        y = df['minutes_to_empty'].values
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
        
        model = RandomForestRegressor(n_estimators=200, random_state=0)
        model.fit(X_train, y_train)
        
        # Make predictions
        df['pred_minutes_to_empty'] = model.predict(df[features].values)
        
        # IMPORTANT: Calculate pred_minutes_to_20pct from MODEL predictions, not ground truth
        df['pred_minutes_to_20pct'] = np.maximum(
            0.0,
            df['pred_minutes_to_empty'] * (df['soc_now'] - 0.20) / np.maximum(df['soc_now'], 1e-6)
        )
        
        # Calculate metrics
        y_pred_test = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred_test)
        r2 = r2_score(y_test, y_pred_test)
        
        # Calculate priority scores (now using ML predictions)
        hub_lat, hub_lon = 48.866, 2.400
        w_urg, w_dem, w_prox = 0.60, 0.25, 0.15
        
        df, top50 = recompute_priority(df, None, hub_lat, hub_lon, w_urg, w_dem, w_prox)
        
        # Add rank column
        df.insert(0, 'rank', range(1, len(df) + 1))
        top50.insert(0, 'rank', range(1, len(top50) + 1))
        
        # Save to CSV
        df.to_csv('dispatch_list.csv', index=False)
        top50.to_csv('top_50_dispatch.csv', index=False)
        
        # Save full dataset with predictions
        synth_df = df.copy()
        synth_df.to_csv('synthetic_gbfs.csv', index=False)
        
        return {
            'success': True,
            'mae': round(mae, 2),
            'r2': round(r2, 3),
            'vehicles': len(df),
            'seed': random_seed
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@app.route('/run_simulation', methods=['POST'])
def trigger_simulation():
    """Endpoint to trigger new simulation"""
    try:
        seed_type = request.form.get('seed_type', 'fixed')
        
        if seed_type == 'random':
            seed = None
        else:
            seed = int(request.form.get('seed_value', 42))
        
        result = run_ml_simulation(random_seed=seed)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f"✅ Simulation complete! MAE: {result['mae']} min, R²: {result['r2']}",
                'mae': result['mae'],
                'r2': result['r2'],
                'vehicles': result['vehicles'],
                'seed': 'Random' if seed is None else seed
            })
        else:
            return jsonify({
                'success': False,
                'message': f"❌ Simulation failed: {result['error']}"
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"❌ Error: {str(e)}"
        }), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    dispatch, top50, synth = load_data()
    # Defaults
    hub_lat = 48.866
    hub_lon = 2.400
    w_urg, w_dem, w_prox = 0.60, 0.25, 0.15

    if request.method == 'POST':
        # Read from form
        hub_lat = float(request.form.get('hub_lat') or hub_lat)
        hub_lon = float(request.form.get('hub_lon') or hub_lon)
        w_urg = float(request.form.get('w_urgency') or w_urg)
        w_dem = float(request.form.get('w_demand') or w_dem)
        w_prox = float(request.form.get('w_proximity') or w_prox)

        file = request.files.get('csv')
        if file and file.filename.lower().endswith('.csv'):
            try:
                dispatch = pd.read_csv(file)
            except Exception:
                pass

        if dispatch is not None and not dispatch.empty:
            dispatch, top50 = recompute_priority(dispatch, synth, hub_lat, hub_lon, w_urg, w_dem, w_prox)
    else:
        # GET with query params
        q_hub_lat = request.args.get('hub_lat', type=float)
        q_hub_lon = request.args.get('hub_lon', type=float)
        q_w_urg = request.args.get('w_urgency', type=float)
        q_w_dem = request.args.get('w_demand', type=float)
        q_w_prox = request.args.get('w_proximity', type=float)

        if any(v is not None for v in [q_hub_lat, q_hub_lon, q_w_urg, q_w_dem, q_w_prox]):
            hub_lat = q_hub_lat if q_hub_lat is not None else hub_lat
            hub_lon = q_hub_lon if q_hub_lon is not None else hub_lon
            w_urg = q_w_urg if q_w_urg is not None else w_urg
            w_dem = q_w_dem if q_w_dem is not None else w_dem
            w_prox = q_w_prox if q_w_prox is not None else w_prox
            if dispatch is not None and not dispatch.empty:
                dispatch, top50 = recompute_priority(dispatch, synth, hub_lat, hub_lon, w_urg, w_dem, w_prox)

    # Summary KPIs
    total = len(dispatch)
    zones = dispatch['zone_name'].nunique() if not dispatch.empty else 0
    avg_soc = dispatch['soc_now'].mean() if not dispatch.empty else 0
    avg_dist = dispatch['dist_km_to_hub'].mean() if 'dist_km_to_hub' in dispatch else 0

    # Charts
    figs = {}
    if not dispatch.empty:
        # Priority distribution
        fig_priority = px.histogram(dispatch, x='priority_score', nbins=30, title='Priority Score Distribution',
                                    opacity=0.85, color_discrete_sequence=['#60a5fa'])
        fig_priority.update_traces(marker_line_color='#0b1220', marker_line_width=1)
        fig_priority.update_layout(
            template='plotly_dark', font=dict(family='Inter, Segoe UI, system-ui', size=13, color='#e5e7eb'),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#0f172a',
            margin=dict(l=30, r=20, t=40, b=40),
            xaxis=dict(gridcolor='#1f2937'), yaxis=dict(gridcolor='#1f2937')
        )
        figs['priority'] = json.dumps(fig_priority, cls=plotly.utils.PlotlyJSONEncoder)

        # SOC vs Priority
        fig_soc = px.scatter(
            dispatch, x='soc_now', y='priority_score', color='zone_name',
            title='SOC vs Priority by Zone', opacity=0.8, color_discrete_sequence=px.colors.qualitative.Set2,
            labels={'soc_now':'SOC (0-1)'}
        )
        fig_soc.update_traces(marker=dict(size=7, line=dict(color='#0b1220', width=1)))
        fig_soc.update_layout(
            template='plotly_dark', font=dict(family='Inter, Segoe UI, system-ui', size=13, color='#e5e7eb'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#0f172a',
            margin=dict(l=30, r=20, t=60, b=40),
            xaxis=dict(gridcolor='#1f2937'), yaxis=dict(gridcolor='#1f2937')
        )
        figs['soc_priority'] = json.dumps(fig_soc, cls=plotly.utils.PlotlyJSONEncoder)

        # Distance vs Priority
        if 'dist_km_to_hub' in dispatch:
            fig_dist = px.scatter(
                dispatch, x='dist_km_to_hub', y='priority_score', color='soc_now',
                title='Distance to Hub vs Priority (colored by SOC)', color_continuous_scale='RdYlGn'
            )
            fig_dist.update_traces(marker=dict(size=7, line=dict(color='#0b1220', width=1)))
            fig_dist.update_layout(
                template='plotly_dark', font=dict(family='Inter, Segoe UI, system-ui', size=13, color='#e5e7eb'),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#0f172a',
                margin=dict(l=30, r=20, t=60, b=40),
                xaxis=dict(gridcolor='#1f2937'), yaxis=dict(gridcolor='#1f2937')
            )
            figs['dist_priority'] = json.dumps(fig_dist, cls=plotly.utils.PlotlyJSONEncoder)

        # Zone composition in Top-50
        if not top50.empty:
            zone_counts = top50['zone_name'].value_counts().reset_index()
            zone_counts.columns = ['zone_name', 'count']
            fig_zone = px.pie(zone_counts, names='zone_name', values='count', title='Top-50 Zone Composition',
                               color_discrete_sequence=px.colors.qualitative.Set2, hole=0.35)
            fig_zone.update_layout(
                template='plotly_dark', font=dict(family='Inter, Segoe UI, system-ui', size=13, color='#e5e7eb'),
                paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=60, b=20)
            )
            figs['top50_zones'] = json.dumps(fig_zone, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', dispatch=dispatch, top50=top50, synth=synth,
                           total=total, zones=zones, avg_soc=avg_soc, avg_dist=avg_dist,
                           figs=figs)


@app.route('/download/<name>')
def download(name: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, name)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return ('Not found', 404)


if __name__ == '__main__':
    # Production settings for Hostinger
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)


