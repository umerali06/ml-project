# Mini AI Pilot System - Product Requirements Document (PRD)

**Document Version:** 1.0  
**Created:** 2025-01-27  
**Project:** Mini AI Pilot - CSV → Prediction → Prioritized Dispatch  

---

## 1. System Overview

### 1.1 Project Name
**Mini AI Pilot: CSV → Prediction → Prioritized Dispatch System**

### 1.2 System Purpose
The Mini AI Pilot is a proof-of-concept system designed to transform raw vehicle fleet data (CSV format) into actionable prioritized dispatch lists for urban electric mobility operations. The system predicts battery depletion times and creates optimized dispatch priorities for fleet management.

### 1.3 Target Audience
- **Primary**: Fleet operators and urban mobility managers
- **Secondary**: Data scientists and analysts working in electric vehicle operations
- **Tertiary**: Beginners with no coding background (via Google Sheets implementation)

### 1.4 Business Objectives
- **Primary**: Optimize electric vehicle fleet dispatch operations
- **Secondary**: Reduce operational costs through predictive maintenance
- **Tertiary**: Demonstrate AI/ML capabilities for urban mobility solutions

---

## 2. System Requirements

### 2.1 Functional Requirements

#### 2.1.1 Data Input Requirements
- **Input Format**: CSV files with specific schema
- **Required Columns**:
  - `vehicle_id`: Unique vehicle identifier
  - `zone_name`: Geographic zone name
  - `latitude`: Vehicle latitude coordinate
  - `longitude`: Vehicle longitude coordinate
  - `soc_now`: Current State of Charge (0.0-1.0)
  - `hour`: Hour of day (0-23)
  - `day_of_week`: Day of week (0-6)
  - `demand_zone_score`: Demand score for the zone

#### 2.1.2 Core Processing Requirements
1. **Data Validation & Preprocessing**
   - Load and validate CSV data
   - Handle missing values and data type validation
   - Basic statistical analysis

2. **Machine Learning Model**
   - Train RandomForestRegressor model
   - Predict `minutes_to_empty` based on features
   - Achieve performance metrics: MAE ≤ 35 minutes, R² ≥ 0.55

3. **Feature Engineering**
   - Calculate `pred_minutes_to_20pct` from predictions
   - Compute `dist_km_to_hub` using Haversine formula
   - Normalize features for priority scoring

4. **Priority Calculation**
   - Apply weighted priority formula:
     - 60% weight: Urgency (time to 20% SOC)
     - 25% weight: Demand zone score
     - 15% weight: Proximity to hub
   - Generate priority scores for all vehicles

5. **Output Generation**
   - Create prioritized dispatch list
   - Generate Top-50 subset
   - Export results to CSV format

#### 2.1.3 Output Requirements
- **Primary Output**: `dispatch_list.csv` with columns:
  - `vehicle_id`, `zone_name`, `soc_now`
  - `pred_minutes_to_20pct`, `demand_zone_score`
  - `dist_km_to_hub`, `priority_score`
  - `hour`, `day_of_week`
- **Secondary Output**: Top-50 prioritized vehicles
- **Supporting Outputs**: Feature importance chart, model metrics

### 2.2 Non-Functional Requirements

#### 2.2.1 Performance Requirements
- **Model Performance**: MAE ≤ 35 minutes, R² ≥ 0.55
- **Processing Time**: Complete end-to-end execution in < 5 minutes
- **Scalability**: Handle datasets up to 10,000 vehicles

#### 2.2.2 Usability Requirements
- **Ease of Use**: One-click execution ("Run all" in Colab)
- **Accessibility**: No-code option via Google Sheets
- **Documentation**: Clear README and 1-page report

#### 2.2.3 Technical Requirements
- **Platform**: Google Colab (free tier)
- **Dependencies**: Only free, open-source libraries
- **Reproducibility**: Deterministic results with same input
- **Compatibility**: Works with any CSV matching template schema

#### 2.2.4 Quality Requirements
- **Reliability**: 100% success rate on valid input data
- **Maintainability**: Clean, commented code
- **Extensibility**: Easy to modify hub coordinates and priority weights

---

## 3. System Design Phase

### 3.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Mini AI Pilot System Architecture            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    │
│  │   Input     │    │   Processing │    │     Output      │    │
│  │   Layer     │    │    Layer     │    │     Layer       │    │
│  │             │    │              │    │                 │    │
│  │ CSV Data    │───▶│ Data Prep    │───▶│ Dispatch List   │    │
│  │ Template    │    │ ML Model     │    │ Top-50 List     │    │
│  │ Validation  │    │ Priority     │    │ Metrics Report  │    │
│  │             │    │ Calculation  │    │ Charts          │    │
│  └─────────────┘    └──────────────┘    └─────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Implementation Options                         ││
│  │                                                             ││
│  │  Option 1: Google Colab Notebook (Primary)                 ││
│  │  Option 2: Google Sheets Formulas (No-code)                 ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Data Flow Design

```
Input CSV → Data Validation → Feature Engineering → ML Training → 
Prediction → Priority Calculation → Output Generation → Dispatch List
```

### 3.3 Component Design

#### 3.3.1 Data Processing Component
- **Input Handler**: CSV loader with schema validation
- **Data Cleaner**: Missing value handling, type conversion
- **Feature Engineer**: Distance calculation, normalization

#### 3.3.2 Machine Learning Component
- **Model Trainer**: RandomForestRegressor with train/test split
- **Predictor**: Time-to-empty prediction
- **Evaluator**: MAE and R² calculation

#### 3.3.3 Priority Engine Component
- **Distance Calculator**: Haversine formula implementation
- **Score Calculator**: Weighted priority formula
- **Ranker**: Sort by priority score

#### 3.3.4 Output Generator Component
- **CSV Exporter**: Dispatch list generation
- **Chart Generator**: Feature importance visualization
- **Report Generator**: Metrics and analysis

---

## 4. Implementation Plan

### 4.1 Development Phases

#### Phase 1: Environment Setup & Data Preparation (Day 1 - Morning)
- [ ] Set up Google Colab environment
- [ ] Install required libraries (pandas, scikit-learn, matplotlib, numpy)
- [ ] Create data loading and validation functions
- [ ] Implement CSV template validation
- [ ] Test with synthetic data

#### Phase 2: Machine Learning Model Development (Day 1 - Afternoon)
- [ ] Implement train/test split
- [ ] Develop RandomForestRegressor baseline
- [ ] Add model evaluation metrics (MAE, R²)
- [ ] Create feature importance visualization
- [ ] Validate model performance against acceptance criteria

#### Phase 3: Priority Calculation & Dispatch Logic (Day 2 - Morning)
- [ ] Implement Haversine distance calculation
- [ ] Develop priority scoring algorithm
- [ ] Create dispatch list generation
- [ ] Implement Top-50 subset creation
- [ ] Test priority logic with sample data

#### Phase 4: Output Generation & Documentation (Day 2 - Afternoon)
- [ ] Generate dispatch_list.csv output
- [ ] Create feature importance chart (PNG)
- [ ] Write comprehensive README
- [ ] Prepare 1-page technical report
- [ ] Final testing and validation

### 4.2 Technical Implementation Details

#### 4.2.1 Core Algorithm Implementation
```python
# Priority Score Formula
priority_score = (
    0.60 * (1 - normalized_minutes_to_20pct) +
    0.25 * normalized_demand_score +
    0.15 * (1 - normalized_distance_to_hub)
)
```

#### 4.2.2 Key Functions to Implement
1. **Data Loading**: `load_and_validate_csv(file_path)`
2. **Model Training**: `train_random_forest(X, y)`
3. **Distance Calculation**: `haversine_distance(lat1, lon1, lat2, lon2)`
4. **Priority Calculation**: `calculate_priority_score(row)`
5. **Output Generation**: `generate_dispatch_list(df)`

### 4.3 Quality Assurance Plan

#### 4.3.1 Testing Strategy
- **Unit Tests**: Individual function validation
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Model accuracy validation
- **User Acceptance Tests**: One-click execution verification

#### 4.3.2 Acceptance Criteria Validation
- [ ] Notebook runs in free Colab without errors
- [ ] MAE ≤ 35 minutes achieved
- [ ] R² ≥ 0.55 achieved
- [ ] Correct priority logic implemented
- [ ] Required output columns present
- [ ] Reproducible results with same input

### 4.4 Deliverables Checklist

#### 4.4.1 Primary Deliverables
- [ ] `mini_ai_pilot_colab.ipynb` - Complete notebook
- [ ] `dispatch_list.csv` - Prioritized dispatch list
- [ ] `synthetic_gbfs.csv` - Sample input data
- [ ] Feature importance chart (PNG)
- [ ] README.md - User guide
- [ ] Technical report (1-page)

#### 4.4.2 Optional Deliverables
- [ ] Top-50 subset CSV
- [ ] Model metrics text file
- [ ] Google Sheets template
- [ ] Extended documentation

### 4.5 Risk Mitigation

#### 4.5.1 Technical Risks
- **Model Performance**: Fallback to simpler models if RandomForest fails
- **Data Quality**: Robust validation and error handling
- **Platform Issues**: Alternative implementation in Jupyter

#### 4.5.2 Timeline Risks
- **Scope Creep**: Strict adherence to defined requirements
- **Quality Issues**: Built-in testing and validation
- **Integration Problems**: Modular design for easy debugging

---

## 5. Success Metrics

### 5.1 Technical Success Criteria
- Model accuracy: MAE ≤ 35 minutes, R² ≥ 0.55
- System reliability: 100% success rate on valid inputs
- Performance: Complete execution in < 5 minutes
- Usability: One-click execution capability

### 5.2 Business Success Criteria
- Demonstrates AI/ML capability for fleet management
- Provides actionable insights for dispatch operations
- Reduces manual prioritization effort
- Enables data-driven decision making

### 5.3 User Experience Success Criteria
- Intuitive operation for non-technical users
- Clear documentation and instructions
- Reproducible results across different datasets
- Professional output quality

---

## 6. Appendices

### 6.1 Data Schema Reference
```csv
vehicle_id,zone_name,latitude,longitude,soc_now,hour,day_of_week,demand_zone_score
V-1001,Zone_A,48.866,2.400,0.45,14,2,1.2
```

### 6.2 Priority Formula Details
```
Priority Score = 0.60 × (1 - norm(minutes_to_20pct)) 
                + 0.25 × norm(demand_zone_score) 
                + 0.15 × (1 - norm(dist_to_hub))
```

### 6.3 Acceptance Criteria Summary
- **Performance**: MAE ≤ 35 min, R² ≥ 0.55
- **Platform**: Free Google Colab execution
- **Output**: Complete dispatch list with required columns
- **Usability**: One-click "Run all" functionality
- **Documentation**: README + 1-page report

---

**Document Status**: Complete  
**Next Steps**: Begin Phase 1 implementation  
**Review Date**: 2025-01-28

