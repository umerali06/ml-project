from flask import Flask, render_template, request, send_file, redirect, url_for
import pandas as pd
import plotly.express as px
import plotly
import json
import os

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
    app.run(host='0.0.0.0', port=5000, debug=True)


