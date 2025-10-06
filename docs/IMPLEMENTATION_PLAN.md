# Mini AI Pilot - Implementation Plan

**Document Version:** 1.0  
**Created:** 2025-01-27  
**Project:** Mini AI Pilot - CSV → Prediction → Prioritized Dispatch  

---

## 1. Implementation Overview

### 1.1 Project Timeline
- **Total Duration**: 48 hours (2 days)
- **Development Approach**: Agile sprint methodology
- **Delivery Method**: Incremental with daily milestones

### 1.2 Implementation Strategy
- **Primary Platform**: Google Colab
- **Backup Platform**: Jupyter Notebook
- **Code Quality**: Clean, commented, reproducible
- **Testing**: Continuous validation throughout development

---

## 2. Phase-by-Phase Implementation

### Phase 1: Environment Setup & Data Preparation
**Duration**: Day 1 Morning (4 hours)  
**Priority**: Critical  

#### 2.1.1 Tasks
- [ ] **Setup Google Colab Environment**
  - Create new notebook: `mini_ai_pilot_colab.ipynb`
  - Configure runtime settings
  - Test basic Python functionality

- [ ] **Install Required Libraries**
  ```python
  # Core libraries
  import pandas as pd
  import numpy as np
  import matplotlib.pyplot as plt
  from sklearn.model_selection import train_test_split
  from sklearn.ensemble import RandomForestRegressor
  from sklearn.metrics import mean_absolute_error, r2_score
  ```

- [ ] **Create Data Loading Functions**
  ```python
  def load_and_validate_csv(file_path):
      """Load CSV and validate schema"""
      df = pd.read_csv(file_path)
      validate_input_data(df)
      return df
  ```

- [ ] **Implement Data Validation**
  - Schema validation
  - Data type checking
  - Range validation
  - Missing value handling

- [ ] **Test with Sample Data**
  - Load `gbfs_template.csv`
  - Validate data structure
  - Test error handling

#### 2.1.2 Deliverables
- Working Colab notebook with data loading
- Data validation functions
- Sample data test results

#### 2.1.3 Success Criteria
- [ ] Notebook runs without errors
- [ ] Data validation passes
- [ ] Sample data loads correctly

---

### Phase 2: Machine Learning Model Development
**Duration**: Day 1 Afternoon (4 hours)  
**Priority**: Critical  

#### 2.2.1 Tasks
- [ ] **Implement Train/Test Split**
  ```python
  def prepare_training_data(df):
      features = ['soc_now', 'hour', 'day_of_week', 'demand_zone_score']
      X = df[features].values
      y = df['minutes_to_empty'].values
      return train_test_split(X, y, test_size=0.25, random_state=0)
  ```

- [ ] **Develop RandomForestRegressor Model**
  ```python
  def train_model(X_train, y_train):
      model = RandomForestRegressor(
          n_estimators=200,
          random_state=0
      )
      model.fit(X_train, y_train)
      return model
  ```

- [ ] **Implement Model Evaluation**
  ```python
  def evaluate_model(model, X_test, y_test):
      predictions = model.predict(X_test)
      mae = mean_absolute_error(y_test, predictions)
      r2 = r2_score(y_test, predictions)
      return mae, r2, predictions
  ```

- [ ] **Create Feature Importance Visualization**
  ```python
  def plot_feature_importance(model, feature_names):
      importances = model.feature_importances_
      plt.figure(figsize=(10, 6))
      plt.bar(range(len(importances)), importances)
      plt.xticks(range(len(importances)), feature_names)
      plt.title("Feature Importances")
      plt.savefig('feature_importance.png')
      plt.show()
  ```

- [ ] **Validate Performance Metrics**
  - Ensure MAE ≤ 35 minutes
  - Ensure R² ≥ 0.55
  - Document model performance

#### 2.2.2 Deliverables
- Trained RandomForest model
- Model evaluation metrics
- Feature importance chart (PNG)
- Performance validation report

#### 2.2.3 Success Criteria
- [ ] Model trains successfully
- [ ] MAE ≤ 35 minutes achieved
- [ ] R² ≥ 0.55 achieved
- [ ] Feature importance chart generated

---

### Phase 3: Priority Calculation & Dispatch Logic
**Duration**: Day 2 Morning (4 hours)  
**Priority**: Critical  

#### 2.3.1 Tasks
- [ ] **Implement Haversine Distance Calculation**
  ```python
  def haversine_distance(lat1, lon1, lat2, lon2):
      """Calculate distance between two points"""
      R = 6371.0  # Earth's radius in kilometers
      lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
      dlat = lat2 - lat1
      dlon = lon2 - lon1
      a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
      c = 2 * np.arcsin(np.sqrt(a))
      return R * c
  ```

- [ ] **Calculate Minutes to 20% SOC**
  ```python
  def calculate_minutes_to_20pct(df):
      """Calculate predicted minutes to 20% SOC"""
      df['pred_minutes_to_20pct'] = np.maximum(
          0.0, 
          df['pred_minutes_to_empty'] * (df['soc_now'] - 0.20) / np.maximum(df['soc_now'], 1e-6)
      )
      return df
  ```

- [ ] **Implement Priority Scoring Algorithm**
  ```python
  def calculate_priority_score(df):
      """Calculate priority score for each vehicle"""
      def normalize(series):
          return (series - series.min()) / (series.max() - series.min() + 1e-9)
      
      priority_score = (
          0.60 * (1 - normalize(df['pred_minutes_to_20pct'])) +
          0.25 * normalize(df['demand_zone_score']) +
          0.15 * (1 - normalize(df['dist_km_to_hub']))
      )
      return priority_score
  ```

- [ ] **Generate Dispatch List**
  ```python
  def generate_dispatch_list(df):
      """Generate prioritized dispatch list"""
      dispatch_columns = [
          'vehicle_id', 'zone_name', 'soc_now',
          'pred_minutes_to_20pct', 'demand_zone_score',
          'dist_km_to_hub', 'priority_score',
          'hour', 'day_of_week'
      ]
      
      dispatch_list = df[dispatch_columns].sort_values(
          'priority_score', ascending=False
      ).reset_index(drop=True)
      
      return dispatch_list
  ```

- [ ] **Create Top-50 Subset**
  ```python
  def generate_top_50(dispatch_list):
      """Generate Top-50 prioritized vehicles"""
      return dispatch_list.head(50)
  ```

#### 2.3.2 Deliverables
- Priority calculation functions
- Dispatch list generation
- Top-50 subset
- Priority logic validation

#### 2.3.3 Success Criteria
- [ ] Distance calculation works correctly
- [ ] Priority scores calculated properly
- [ ] Dispatch list sorted by priority
- [ ] Top-50 subset generated

---

### Phase 4: Output Generation & Documentation
**Duration**: Day 2 Afternoon (4 hours)  
**Priority**: High  

#### 2.4.1 Tasks
- [ ] **Generate Final Outputs**
  ```python
  # Save dispatch list
  dispatch_list.to_csv('dispatch_list.csv', index=False)
  
  # Save Top-50 subset
  top_50.to_csv('top_50_dispatch.csv', index=False)
  
  # Save synthetic data
  df.to_csv('synthetic_gbfs.csv', index=False)
  ```

- [ ] **Create Model Performance Visualization**
  ```python
  def plot_model_performance(y_true, y_pred):
      """Create performance visualization"""
      fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
      
      # Actual vs Predicted
      ax1.scatter(y_true, y_pred, alpha=0.6)
      ax1.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--')
      ax1.set_xlabel('Actual Minutes to Empty')
      ax1.set_ylabel('Predicted Minutes to Empty')
      ax1.set_title('Actual vs Predicted')
      
      # Residuals
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

- [ ] **Write Comprehensive README**
  - Installation instructions
  - Usage guide
  - Parameter configuration
  - Troubleshooting guide

- [ ] **Prepare Technical Report**
  - Model performance summary
  - Key findings
  - Limitations and recommendations
  - Next steps

- [ ] **Final Testing and Validation**
  - End-to-end workflow test
  - Output validation
  - Performance verification

#### 2.4.2 Deliverables
- Complete dispatch_list.csv
- Top-50 subset CSV
- Feature importance chart (PNG)
- Model performance chart (PNG)
- Comprehensive README.md
- Technical report (1-page)

#### 2.4.3 Success Criteria
- [ ] All outputs generated successfully
- [ ] README is clear and complete
- [ ] Technical report is comprehensive
- [ ] Final validation passes

---

## 3. Implementation Details

### 3.1 Code Structure
```
mini_ai_pilot_colab.ipynb
├── Cell 1: Imports and Setup
├── Cell 2: Data Loading Functions
├── Cell 3: Data Validation
├── Cell 4: Model Training
├── Cell 5: Model Evaluation
├── Cell 6: Feature Engineering
├── Cell 7: Priority Calculation
├── Cell 8: Output Generation
├── Cell 9: Visualization
└── Cell 10: Documentation
```

### 3.2 Key Functions Implementation

#### 3.2.1 Data Processing Functions
```python
def load_and_validate_csv(file_path):
    """Load CSV and validate schema"""
    df = pd.read_csv(file_path)
    
    # Validate required columns
    required_columns = [
        'vehicle_id', 'zone_name', 'latitude', 'longitude',
        'soc_now', 'hour', 'day_of_week', 'demand_zone_score'
    ]
    
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Validate data ranges
    assert df['latitude'].between(-90, 90).all(), "Invalid latitude"
    assert df['longitude'].between(-180, 180).all(), "Invalid longitude"
    assert df['soc_now'].between(0, 1).all(), "Invalid SOC"
    assert df['hour'].between(0, 23).all(), "Invalid hour"
    assert df['day_of_week'].between(0, 6).all(), "Invalid day of week"
    assert (df['demand_zone_score'] > 0).all(), "Invalid demand score"
    
    return df
```

#### 3.2.2 Model Training Functions
```python
def train_and_evaluate_model(df):
    """Train model and evaluate performance"""
    features = ['soc_now', 'hour', 'day_of_week', 'demand_zone_score']
    X = df[features].values
    y = df['minutes_to_empty'].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )
    
    model = RandomForestRegressor(n_estimators=200, random_state=0)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"MAE: {mae:.2f} minutes")
    print(f"R²: {r2:.3f}")
    
    return model, mae, r2, predictions
```

#### 3.2.3 Priority Calculation Functions
```python
def calculate_priority_scores(df, hub_lat=48.866, hub_lon=2.400):
    """Calculate priority scores for all vehicles"""
    
    # Calculate distance to hub
    df['dist_km_to_hub'] = haversine_distance(
        hub_lat, hub_lon, df['latitude'], df['longitude']
    )
    
    # Calculate minutes to 20% SOC
    df['pred_minutes_to_20pct'] = np.maximum(
        0.0, 
        df['pred_minutes_to_empty'] * (df['soc_now'] - 0.20) / np.maximum(df['soc_now'], 1e-6)
    )
    
    # Normalize features
    def normalize(series):
        return (series - series.min()) / (series.max() - series.min() + 1e-9)
    
    # Calculate priority score
    df['priority_score'] = (
        0.60 * (1 - normalize(df['pred_minutes_to_20pct'])) +
        0.25 * normalize(df['demand_zone_score']) +
        0.15 * (1 - normalize(df['dist_km_to_hub']))
    )
    
    return df
```

### 3.3 Testing Strategy

#### 3.3.1 Unit Testing
```python
def test_data_validation():
    """Test data validation functions"""
    # Test with valid data
    valid_df = pd.DataFrame({
        'vehicle_id': ['V1', 'V2'],
        'latitude': [48.866, 48.867],
        'longitude': [2.400, 2.401],
        'soc_now': [0.5, 0.6],
        'hour': [12, 13],
        'day_of_week': [1, 2],
        'demand_zone_score': [1.2, 1.3]
    })
    
    result = load_and_validate_csv(valid_df)
    assert result is not None
    
    # Test with invalid data
    invalid_df = pd.DataFrame({
        'vehicle_id': ['V1'],
        'latitude': [100],  # Invalid latitude
        'longitude': [2.400],
        'soc_now': [0.5],
        'hour': [12],
        'day_of_week': [1],
        'demand_zone_score': [1.2]
    })
    
    try:
        load_and_validate_csv(invalid_df)
        assert False, "Should have raised an error"
    except AssertionError:
        pass  # Expected behavior
```

#### 3.3.2 Integration Testing
```python
def test_end_to_end_workflow():
    """Test complete workflow"""
    # Load sample data
    df = load_and_validate_csv('synthetic_gbfs.csv')
    
    # Train model
    model, mae, r2, predictions = train_and_evaluate_model(df)
    
    # Validate performance
    assert mae <= 35, f"MAE {mae} exceeds threshold of 35"
    assert r2 >= 0.55, f"R² {r2} below threshold of 0.55"
    
    # Calculate priorities
    df_with_priorities = calculate_priority_scores(df)
    
    # Generate dispatch list
    dispatch_list = generate_dispatch_list(df_with_priorities)
    
    # Validate output
    assert 'priority_score' in dispatch_list.columns
    assert dispatch_list['priority_score'].is_monotonic_decreasing
    
    print("End-to-end test passed!")
```

---

## 4. Risk Management

### 4.1 Technical Risks

#### 4.1.1 Model Performance Risk
- **Risk**: Model fails to meet performance criteria
- **Mitigation**: 
  - Implement fallback models (LinearRegression, DecisionTree)
  - Tune hyperparameters if needed
  - Use cross-validation for stability

#### 4.1.2 Data Quality Risk
- **Risk**: Input data has quality issues
- **Mitigation**:
  - Robust data validation
  - Missing value handling
  - Outlier detection and handling

#### 4.1.3 Platform Risk
- **Risk**: Google Colab issues or limitations
- **Mitigation**:
  - Backup Jupyter implementation
  - Local testing capability
  - Alternative cloud platforms

### 4.2 Timeline Risks

#### 4.2.1 Scope Creep Risk
- **Risk**: Additional requirements added during development
- **Mitigation**:
  - Strict adherence to defined requirements
  - Clear change control process
  - Regular stakeholder communication

#### 4.2.2 Quality Risk
- **Risk**: Rushing to meet deadline compromises quality
- **Mitigation**:
  - Built-in testing and validation
  - Code review process
  - Incremental delivery approach

---

## 5. Quality Assurance

### 5.1 Code Quality Standards
- **Documentation**: All functions documented with docstrings
- **Comments**: Complex logic explained with inline comments
- **Naming**: Descriptive variable and function names
- **Structure**: Modular, reusable code components

### 5.2 Testing Requirements
- **Unit Tests**: All core functions tested
- **Integration Tests**: End-to-end workflow validated
- **Performance Tests**: Model accuracy verified
- **User Acceptance Tests**: One-click execution confirmed

### 5.3 Validation Checklist
- [ ] Notebook runs without errors
- [ ] All required outputs generated
- [ ] Performance metrics meet criteria
- [ ] Code is clean and documented
- [ ] README is comprehensive
- [ ] Technical report is complete

---

## 6. Delivery Plan

### 6.1 Daily Milestones

#### Day 1 Milestones
- [ ] Environment setup complete
- [ ] Data loading and validation working
- [ ] Model training and evaluation complete
- [ ] Performance metrics validated

#### Day 2 Milestones
- [ ] Priority calculation implemented
- [ ] Dispatch list generation working
- [ ] All outputs generated
- [ ] Documentation complete
- [ ] Final validation passed

### 6.2 Final Deliverables
1. **mini_ai_pilot_colab.ipynb** - Complete notebook
2. **dispatch_list.csv** - Prioritized dispatch list
3. **top_50_dispatch.csv** - Top-50 subset
4. **synthetic_gbfs.csv** - Sample input data
5. **feature_importance.png** - Feature importance chart
6. **model_performance.png** - Model performance visualization
7. **README.md** - User guide
8. **technical_report.md** - 1-page technical report

### 6.3 Handover Process
1. **Code Review**: Complete code walkthrough
2. **Testing**: Final validation of all components
3. **Documentation**: Review of all documentation
4. **Training**: Brief user training session
5. **Support**: 1 revision included for bug fixes

---

**Document Status**: Complete  
**Next Steps**: Begin Phase 1 implementation  
**Review Date**: 2025-01-28


