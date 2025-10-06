# Mini AI Pilot - Technical Specification Document

**Document Version:** 1.0  
**Created:** 2025-01-27  
**Project:** Mini AI Pilot - CSV → Prediction → Prioritized Dispatch  

---

## 1. Technical Overview

### 1.1 System Architecture
The Mini AI Pilot system follows a modular architecture with clear separation of concerns:

- **Data Layer**: CSV input processing and validation
- **Processing Layer**: Machine learning and priority calculation
- **Output Layer**: Dispatch list generation and reporting

### 1.2 Technology Stack
- **Platform**: Google Colab (Python 3.8+)
- **Core Libraries**: 
  - pandas (data manipulation)
  - scikit-learn (machine learning)
  - numpy (numerical computing)
  - matplotlib (visualization)
- **Optional**: XGBoost, geopy (if available in free tier)

---

## 2. Data Specifications

### 2.1 Input Data Schema
```csv
vehicle_id,zone_name,latitude,longitude,soc_now,hour,day_of_week,demand_zone_score
```

#### Field Descriptions:
- **vehicle_id** (string): Unique identifier for each vehicle
- **zone_name** (string): Geographic zone name
- **latitude** (float): Vehicle latitude coordinate (-90 to 90)
- **longitude** (float): Vehicle longitude coordinate (-180 to 180)
- **soc_now** (float): Current State of Charge (0.0 to 1.0)
- **hour** (integer): Hour of day (0 to 23)
- **day_of_week** (integer): Day of week (0=Monday to 6=Sunday)
- **demand_zone_score** (float): Demand score for the zone (>0)

### 2.2 Data Validation Rules
```python
def validate_input_data(df):
    """Validate input CSV data against schema requirements"""
    required_columns = [
        'vehicle_id', 'zone_name', 'latitude', 'longitude',
        'soc_now', 'hour', 'day_of_week', 'demand_zone_score'
    ]
    
    # Check required columns exist
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Validate data types and ranges
    assert df['latitude'].between(-90, 90).all(), "Latitude must be between -90 and 90"
    assert df['longitude'].between(-180, 180).all(), "Longitude must be between -180 and 180"
    assert df['soc_now'].between(0, 1).all(), "SOC must be between 0 and 1"
    assert df['hour'].between(0, 23).all(), "Hour must be between 0 and 23"
    assert df['day_of_week'].between(0, 6).all(), "Day of week must be between 0 and 6"
    assert (df['demand_zone_score'] > 0).all(), "Demand score must be positive"
    
    return True
```

---

## 3. Machine Learning Specifications

### 3.1 Model Architecture
- **Algorithm**: RandomForestRegressor
- **Target Variable**: `minutes_to_empty`
- **Features**: `['soc_now', 'hour', 'day_of_week', 'demand_zone_score']`
- **Train/Test Split**: 75%/25% with random_state=0

### 3.2 Model Configuration
```python
model_config = {
    'n_estimators': 200,
    'random_state': 0,
    'max_depth': None,
    'min_samples_split': 2,
    'min_samples_leaf': 1,
    'max_features': 'sqrt'
}
```

### 3.3 Performance Requirements
- **Mean Absolute Error (MAE)**: ≤ 35 minutes
- **R-squared (R²)**: ≥ 0.55
- **Cross-validation**: 5-fold CV for stability assessment

### 3.4 Feature Engineering Pipeline
```python
def engineer_features(df):
    """Create derived features for model training"""
    # Calculate minutes to 20% SOC
    df['pred_minutes_to_20pct'] = np.maximum(
        0.0, 
        df['pred_minutes_to_empty'] * (df['soc_now'] - 0.20) / np.maximum(df['soc_now'], 1e-6)
    )
    
    # Calculate distance to hub using Haversine formula
    df['dist_km_to_hub'] = haversine_distance(
        HUB_LAT, HUB_LON, 
        df['latitude'], df['longitude']
    )
    
    return df
```

---

## 4. Priority Calculation Specifications

### 4.1 Haversine Distance Formula
```python
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    R = 6371.0  # Earth's radius in kilometers
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return R * c
```

### 4.2 Priority Score Algorithm
```python
def calculate_priority_score(df):
    """Calculate priority score for each vehicle"""
    
    def normalize(series):
        """Min-max normalization"""
        return (series - series.min()) / (series.max() - series.min() + 1e-9)
    
    # Normalize components
    norm_minutes_to_20pct = normalize(df['pred_minutes_to_20pct'])
    norm_demand_score = normalize(df['demand_zone_score'])
    norm_distance = normalize(df['dist_km_to_hub'])
    
    # Calculate weighted priority score
    priority_score = (
        0.60 * (1 - norm_minutes_to_20pct) +  # Urgency (higher = more urgent)
        0.25 * norm_demand_score +            # Demand (higher = more demand)
        0.15 * (1 - norm_distance)           # Proximity (closer = higher score)
    )
    
    return priority_score
```

### 4.3 Hub Configuration
```python
# Default hub coordinates (Paris, France)
HUB_LAT = 48.866
HUB_LON = 2.400

# Configurable via parameters
def set_hub_location(latitude, longitude):
    """Set hub location for distance calculations"""
    global HUB_LAT, HUB_LON
    HUB_LAT = latitude
    HUB_LON = longitude
```

---

## 5. Output Specifications

### 5.1 Dispatch List Schema
```csv
vehicle_id,zone_name,soc_now,pred_minutes_to_20pct,demand_zone_score,dist_km_to_hub,priority_score,hour,day_of_week
```

#### Output Field Descriptions:
- **vehicle_id**: Original vehicle identifier
- **zone_name**: Original zone name
- **soc_now**: Current State of Charge
- **pred_minutes_to_20pct**: Predicted minutes until 20% SOC
- **demand_zone_score**: Original demand score
- **dist_km_to_hub**: Distance to hub in kilometers
- **priority_score**: Calculated priority score (0-1)
- **hour**: Hour of day
- **day_of_week**: Day of week

### 5.2 Output Generation Process
```python
def generate_dispatch_list(df):
    """Generate prioritized dispatch list"""
    
    # Calculate priority scores
    df['priority_score'] = calculate_priority_score(df)
    
    # Define output columns
    dispatch_columns = [
        'vehicle_id', 'zone_name', 'soc_now',
        'pred_minutes_to_20pct', 'demand_zone_score',
        'dist_km_to_hub', 'priority_score',
        'hour', 'day_of_week'
    ]
    
    # Sort by priority score (descending)
    dispatch_list = df[dispatch_columns].sort_values(
        'priority_score', 
        ascending=False
    ).reset_index(drop=True)
    
    return dispatch_list
```

### 5.3 Top-50 Subset Generation
```python
def generate_top_50(df):
    """Generate Top-50 prioritized vehicles"""
    return df.head(50)
```

---

## 6. Visualization Specifications

### 6.1 Feature Importance Chart
```python
def create_feature_importance_chart(model, feature_names):
    """Create feature importance visualization"""
    import matplotlib.pyplot as plt
    
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(10, 6))
    plt.title("Feature Importances")
    plt.bar(range(len(importances)), importances[indices])
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices])
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    plt.show()
```

### 6.2 Model Performance Visualization
```python
def plot_model_performance(y_true, y_pred):
    """Create model performance visualization"""
    import matplotlib.pyplot as plt
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Actual vs Predicted scatter plot
    ax1.scatter(y_true, y_pred, alpha=0.6)
    ax1.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
    ax1.set_xlabel('Actual Minutes to Empty')
    ax1.set_ylabel('Predicted Minutes to Empty')
    ax1.set_title('Actual vs Predicted')
    
    # Residuals plot
    residuals = y_true - y_pred
    ax2.scatter(y_pred, residuals, alpha=0.6)
    ax2.axhline(y=0, color='r', linestyle='--')
    ax2.set_xlabel('Predicted Minutes to Empty')
    ax2.set_ylabel('Residuals')
    ax2.set_title('Residuals Plot')
    
    plt.tight_layout()
    plt.savefig('model_performance.png', dpi=300, bbox_inches='tight')
    plt.show()
```

---

## 7. Error Handling Specifications

### 7.1 Data Validation Errors
```python
class DataValidationError(Exception):
    """Custom exception for data validation errors"""
    pass

def handle_data_errors(df):
    """Handle common data validation issues"""
    try:
        validate_input_data(df)
    except ValueError as e:
        raise DataValidationError(f"Data validation failed: {str(e)}")
    
    # Handle missing values
    if df.isnull().any().any():
        print("Warning: Missing values detected. Filling with defaults.")
        df = df.fillna({
            'soc_now': 0.5,
            'hour': 12,
            'day_of_week': 0,
            'demand_zone_score': 1.0
        })
    
    return df
```

### 7.2 Model Training Errors
```python
def safe_model_training(X, y):
    """Train model with error handling"""
    try:
        model = RandomForestRegressor(**model_config)
        model.fit(X, y)
        return model
    except Exception as e:
        print(f"Model training failed: {str(e)}")
        # Fallback to simpler model
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(X, y)
        return model
```

---

## 8. Performance Specifications

### 8.1 Execution Time Requirements
- **Total Runtime**: < 5 minutes for 1000 vehicles
- **Data Loading**: < 30 seconds
- **Model Training**: < 2 minutes
- **Prediction**: < 30 seconds
- **Priority Calculation**: < 30 seconds
- **Output Generation**: < 30 seconds

### 8.2 Memory Requirements
- **Minimum RAM**: 2GB
- **Recommended RAM**: 4GB
- **Peak Memory Usage**: < 1GB for 1000 vehicles

### 8.3 Scalability Limits
- **Maximum Vehicles**: 10,000 per execution
- **Maximum Zones**: 100 unique zones
- **Maximum Features**: 20 features per model

---

## 9. Configuration Parameters

### 9.1 Model Parameters
```python
MODEL_CONFIG = {
    'n_estimators': 200,
    'random_state': 0,
    'test_size': 0.25,
    'cv_folds': 5
}
```

### 9.2 Priority Weights
```python
PRIORITY_WEIGHTS = {
    'urgency': 0.60,      # Minutes to 20% SOC
    'demand': 0.25,       # Demand zone score
    'proximity': 0.15     # Distance to hub
}
```

### 9.3 Hub Configuration
```python
HUB_CONFIG = {
    'latitude': 48.866,
    'longitude': 2.400,
    'name': 'Paris Hub'
}
```

---

## 10. Testing Specifications

### 10.1 Unit Test Coverage
- Data validation functions: 100%
- Distance calculation: 100%
- Priority calculation: 100%
- Output generation: 100%

### 10.2 Integration Test Scenarios
1. **End-to-end workflow**: Complete pipeline execution
2. **Data edge cases**: Missing values, invalid ranges
3. **Model performance**: Accuracy metrics validation
4. **Output validation**: Schema compliance check

### 10.3 Performance Test Cases
- Small dataset (100 vehicles)
- Medium dataset (1000 vehicles)
- Large dataset (5000 vehicles)
- Edge case dataset (10 vehicles)

---

**Document Status**: Complete  
**Review Date**: 2025-01-28  
**Next Review**: After Phase 1 completion





