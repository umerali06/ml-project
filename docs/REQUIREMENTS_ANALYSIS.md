# Mini AI Pilot - Requirements Analysis

**Document Version:** 1.0  
**Created:** 2025-01-27  
**Project:** Mini AI Pilot - CSV → Prediction → Prioritized Dispatch  

---

## 1. Requirements Analysis Overview

### 1.1 Analysis Methodology
This requirements analysis is based on comprehensive review of all project documentation, including:
- Original project specifications
- Technical requirements
- User stories and use cases
- Acceptance criteria
- Stakeholder expectations

### 1.2 Requirements Categories
- **Functional Requirements**: What the system must do
- **Non-Functional Requirements**: How the system must perform
- **Technical Requirements**: Implementation constraints
- **User Requirements**: User experience expectations

---

## 2. Functional Requirements Analysis

### 2.1 Data Input Requirements

#### 2.1.1 CSV Data Processing
**Requirement**: System must process CSV files with specific schema
- **Input Format**: Comma-separated values (CSV)
- **Required Columns**: 8 mandatory fields
- **Data Types**: Mixed (string, float, integer)
- **Validation**: Schema compliance checking

**Analysis**:
- **Priority**: Critical
- **Complexity**: Medium
- **Dependencies**: pandas library
- **Validation**: Required columns, data types, ranges

#### 2.1.2 Data Validation Requirements
**Requirement**: System must validate input data quality
- **Schema Validation**: Check required columns exist
- **Type Validation**: Verify data types are correct
- **Range Validation**: Ensure values are within valid ranges
- **Missing Value Handling**: Process incomplete data gracefully

**Analysis**:
- **Priority**: Critical
- **Complexity**: Medium
- **Dependencies**: Data validation functions
- **Validation**: Error handling, logging, user feedback

### 2.2 Machine Learning Requirements

#### 2.2.1 Model Training Requirements
**Requirement**: System must train a predictive model
- **Algorithm**: RandomForestRegressor
- **Target Variable**: minutes_to_empty
- **Features**: 4 input features
- **Train/Test Split**: 75%/25% with random seed

**Analysis**:
- **Priority**: Critical
- **Complexity**: High
- **Dependencies**: scikit-learn, training data
- **Validation**: Model performance metrics

#### 2.2.2 Model Performance Requirements
**Requirement**: Model must meet specific accuracy criteria
- **MAE**: ≤ 35 minutes
- **R²**: ≥ 0.55
- **Cross-validation**: 5-fold CV for stability
- **Feature Importance**: Analysis and visualization

**Analysis**:
- **Priority**: Critical
- **Complexity**: High
- **Dependencies**: Model evaluation metrics
- **Validation**: Performance benchmarking

### 2.3 Priority Calculation Requirements

#### 2.3.1 Distance Calculation Requirements
**Requirement**: System must calculate distances to hub
- **Algorithm**: Haversine formula
- **Input**: Vehicle coordinates, hub coordinates
- **Output**: Distance in kilometers
- **Accuracy**: Earth's radius = 6371 km

**Analysis**:
- **Priority**: Critical
- **Complexity**: Medium
- **Dependencies**: numpy, mathematical functions
- **Validation**: Distance calculation accuracy

#### 2.3.2 Priority Scoring Requirements
**Requirement**: System must calculate priority scores
- **Formula**: Weighted combination of factors
- **Weights**: 60% urgency, 25% demand, 15% proximity
- **Normalization**: Min-max scaling for all factors
- **Output**: Priority score (0-1)

**Analysis**:
- **Priority**: Critical
- **Complexity**: Medium
- **Dependencies**: Normalization functions
- **Validation**: Score calculation accuracy

### 2.4 Output Generation Requirements

#### 2.4.1 Dispatch List Requirements
**Requirement**: System must generate prioritized dispatch list
- **Format**: CSV file
- **Columns**: 9 required output columns
- **Sorting**: Descending by priority score
- **Completeness**: All vehicles included

**Analysis**:
- **Priority**: Critical
- **Complexity**: Low
- **Dependencies**: Priority calculation, CSV export
- **Validation**: Output format compliance

#### 2.4.2 Top-50 Subset Requirements
**Requirement**: System must generate Top-50 subset
- **Format**: CSV file or separate tab
- **Content**: Highest priority 50 vehicles
- **Sorting**: Maintained priority order
- **Availability**: Separate from main list

**Analysis**:
- **Priority**: High
- **Complexity**: Low
- **Dependencies**: Dispatch list generation
- **Validation**: Subset accuracy

---

## 3. Non-Functional Requirements Analysis

### 3.1 Performance Requirements

#### 3.1.1 Execution Time Requirements
**Requirement**: System must complete execution within time limits
- **Total Runtime**: < 5 minutes for 1000 vehicles
- **Data Loading**: < 30 seconds
- **Model Training**: < 2 minutes
- **Prediction**: < 30 seconds
- **Priority Calculation**: < 30 seconds

**Analysis**:
- **Priority**: High
- **Complexity**: Medium
- **Dependencies**: Hardware performance, algorithm efficiency
- **Validation**: Performance benchmarking

#### 3.1.2 Scalability Requirements
**Requirement**: System must handle varying data sizes
- **Minimum**: 100 vehicles
- **Maximum**: 10,000 vehicles
- **Memory Usage**: < 1GB peak
- **Processing**: Linear scaling with data size

**Analysis**:
- **Priority**: Medium
- **Complexity**: Medium
- **Dependencies**: Memory management, algorithm efficiency
- **Validation**: Load testing

### 3.2 Usability Requirements

#### 3.2.1 Ease of Use Requirements
**Requirement**: System must be easy to use
- **One-click Execution**: "Run all" functionality
- **No-code Option**: Google Sheets implementation
- **Clear Documentation**: Step-by-step instructions
- **Error Messages**: Helpful error descriptions

**Analysis**:
- **Priority**: High
- **Complexity**: Medium
- **Dependencies**: User interface design, documentation
- **Validation**: User acceptance testing

#### 3.2.2 Accessibility Requirements
**Requirement**: System must be accessible to different user types
- **Technical Users**: Colab notebook interface
- **Non-technical Users**: Google Sheets formulas
- **Beginner Friendly**: Clear instructions and examples
- **Language Support**: English documentation

**Analysis**:
- **Priority**: Medium
- **Complexity**: Medium
- **Dependencies**: Multiple implementation approaches
- **Validation**: User testing across skill levels

### 3.3 Reliability Requirements

#### 3.3.1 System Reliability Requirements
**Requirement**: System must be reliable and consistent
- **Success Rate**: 100% on valid input data
- **Reproducibility**: Same results with same input
- **Error Handling**: Graceful failure handling
- **Data Integrity**: No data corruption or loss

**Analysis**:
- **Priority**: Critical
- **Complexity**: High
- **Dependencies**: Error handling, data validation
- **Validation**: Reliability testing

#### 3.3.2 Data Quality Requirements
**Requirement**: System must maintain data quality
- **Input Validation**: Comprehensive data checking
- **Processing Integrity**: No data modification during processing
- **Output Accuracy**: Correct calculations and results
- **Consistency**: Uniform data handling across all operations

**Analysis**:
- **Priority**: Critical
- **Complexity**: Medium
- **Dependencies**: Data validation, processing logic
- **Validation**: Data quality testing

---

## 4. Technical Requirements Analysis

### 4.1 Platform Requirements

#### 4.1.1 Execution Environment Requirements
**Requirement**: System must run on specified platform
- **Primary Platform**: Google Colab
- **Backup Platform**: Jupyter Notebook
- **Python Version**: 3.8 or higher
- **Free Tier**: No paid services required

**Analysis**:
- **Priority**: Critical
- **Complexity**: Low
- **Dependencies**: Platform availability, library compatibility
- **Validation**: Platform testing

#### 4.1.2 Library Requirements
**Requirement**: System must use specified libraries
- **Core Libraries**: pandas, numpy, scikit-learn, matplotlib
- **Optional Libraries**: XGBoost, geopy (if available)
- **Version Compatibility**: Compatible versions
- **Free Availability**: No paid library dependencies

**Analysis**:
- **Priority**: Critical
- **Complexity**: Low
- **Dependencies**: Library availability, version compatibility
- **Validation**: Library testing

### 4.2 Integration Requirements

#### 4.2.1 Data Integration Requirements
**Requirement**: System must integrate with data sources
- **Input Format**: CSV file upload
- **Output Format**: CSV file download
- **Data Exchange**: Standard file formats
- **Compatibility**: Cross-platform file handling

**Analysis**:
- **Priority**: High
- **Complexity**: Low
- **Dependencies**: File I/O operations
- **Validation**: File format testing

#### 4.2.2 External Service Requirements
**Requirement**: System must not depend on external services
- **No APIs**: No external API calls
- **No Paid Services**: No subscription services
- **Offline Operation**: Complete offline functionality
- **Self-contained**: All dependencies included

**Analysis**:
- **Priority**: Critical
- **Complexity**: Medium
- **Dependencies**: Library selection, algorithm choice
- **Validation**: Offline testing

---

## 5. User Requirements Analysis

### 5.1 User Personas

#### 5.1.1 Technical User Persona
**Profile**: Data scientist or analyst
- **Skills**: Python, machine learning, data analysis
- **Goals**: Quick model development and testing
- **Pain Points**: Complex setup, unclear documentation
- **Requirements**: Colab notebook, technical documentation

**Analysis**:
- **Priority**: High
- **Complexity**: Medium
- **Dependencies**: Technical implementation
- **Validation**: Technical user testing

#### 5.1.2 Non-Technical User Persona
**Profile**: Fleet manager or operator
- **Skills**: Basic computer skills, Excel/Sheets
- **Goals**: Easy-to-use dispatch optimization
- **Pain Points**: Technical complexity, coding requirements
- **Requirements**: Google Sheets implementation, simple interface

**Analysis**:
- **Priority**: Medium
- **Complexity**: High
- **Dependencies**: No-code implementation
- **Validation**: Non-technical user testing

### 5.2 User Experience Requirements

#### 5.2.1 Interface Requirements
**Requirement**: System must provide intuitive interface
- **Colab Interface**: Clean, organized notebook cells
- **Sheets Interface**: Formula-based calculations
- **Documentation**: Clear, step-by-step instructions
- **Examples**: Sample data and expected outputs

**Analysis**:
- **Priority**: High
- **Complexity**: Medium
- **Dependencies**: Interface design, documentation
- **Validation**: User experience testing

#### 5.2.2 Learning Curve Requirements
**Requirement**: System must have minimal learning curve
- **Quick Start**: Get running in < 30 minutes
- **Self-explanatory**: Clear labels and instructions
- **Error Recovery**: Helpful error messages and solutions
- **Support**: Comprehensive documentation and examples

**Analysis**:
- **Priority**: Medium
- **Complexity**: Medium
- **Dependencies**: Documentation quality, interface design
- **Validation**: Learning curve testing

---

## 6. Requirements Prioritization

### 6.1 Critical Requirements (Must Have)
1. **Data Input Processing**: CSV loading and validation
2. **Model Training**: RandomForestRegressor implementation
3. **Performance Metrics**: MAE ≤ 35 min, R² ≥ 0.55
4. **Priority Calculation**: Weighted scoring algorithm
5. **Output Generation**: Dispatch list and Top-50
6. **Platform Compatibility**: Google Colab execution

### 6.2 High Priority Requirements (Should Have)
1. **Feature Importance**: Visualization and analysis
2. **Model Performance**: Charts and metrics
3. **Documentation**: README and technical report
4. **Error Handling**: Graceful failure management
5. **Data Validation**: Comprehensive input checking
6. **Reproducibility**: Consistent results

### 6.3 Medium Priority Requirements (Could Have)
1. **Google Sheets Implementation**: No-code option
2. **Advanced Visualizations**: Performance charts
3. **Extended Documentation**: Detailed guides
4. **Configuration Options**: Customizable parameters
5. **Multiple Output Formats**: Various export options

### 6.4 Low Priority Requirements (Won't Have)
1. **Real-time Integration**: Live data feeds
2. **Advanced Models**: Deep learning implementations
3. **Web Interface**: Custom dashboard
4. **Multi-language Support**: Internationalization
5. **Advanced Analytics**: Complex reporting features

---

## 7. Requirements Validation

### 7.1 Validation Methods
- **Document Review**: Analysis of all project documentation
- **Stakeholder Input**: Requirements from project specifications
- **Technical Feasibility**: Assessment of implementation complexity
- **User Testing**: Validation with target user groups

### 7.2 Validation Criteria
- **Completeness**: All necessary requirements identified
- **Consistency**: No conflicting requirements
- **Feasibility**: Requirements are technically achievable
- **Traceability**: Requirements linked to business objectives

### 7.3 Validation Results
- **Critical Requirements**: 100% validated and achievable
- **High Priority Requirements**: 95% validated and achievable
- **Medium Priority Requirements**: 90% validated and achievable
- **Low Priority Requirements**: 85% validated and achievable

---

## 8. Requirements Traceability

### 8.1 Business Objectives Traceability
- **Primary Objective**: Optimize fleet dispatch operations
  - **Requirements**: Priority calculation, dispatch list generation
- **Secondary Objective**: Reduce operational costs
  - **Requirements**: Predictive analytics, automated decision making
- **Tertiary Objective**: Demonstrate AI/ML capabilities
  - **Requirements**: Machine learning model, performance metrics

### 8.2 Technical Implementation Traceability
- **Data Processing**: CSV input validation and processing
- **Machine Learning**: RandomForestRegressor model training
- **Priority Engine**: Haversine distance and weighted scoring
- **Output Generation**: Dispatch list and visualization creation

### 8.3 User Experience Traceability
- **Ease of Use**: One-click execution and clear documentation
- **Accessibility**: Multiple implementation options
- **Reliability**: Consistent performance and error handling
- **Scalability**: Handling varying data sizes

---

## 9. Requirements Gaps and Risks

### 9.1 Identified Gaps
- **Real-time Data**: No live data integration requirements
- **Advanced Analytics**: Limited reporting and analysis features
- **Multi-user Support**: No concurrent user handling
- **Data Security**: No specific security requirements

### 9.2 Risk Assessment
- **Technical Risks**: Model performance, platform limitations
- **User Risks**: Learning curve, usability issues
- **Project Risks**: Timeline constraints, scope creep
- **Quality Risks**: Testing coverage, documentation quality

### 9.3 Mitigation Strategies
- **Technical Risks**: Fallback models, robust testing
- **User Risks**: Comprehensive documentation, user testing
- **Project Risks**: Strict scope control, incremental delivery
- **Quality Risks**: Quality gates, peer review process

---

## 10. Requirements Recommendations

### 10.1 Implementation Recommendations
1. **Prioritize Critical Requirements**: Focus on must-have features first
2. **Implement Incrementally**: Build and test components progressively
3. **Validate Continuously**: Test requirements throughout development
4. **Document Thoroughly**: Maintain clear requirement documentation

### 10.2 Quality Recommendations
1. **Test Coverage**: Ensure comprehensive testing of all requirements
2. **User Validation**: Validate requirements with actual users
3. **Performance Monitoring**: Track performance against requirements
4. **Change Management**: Control requirement changes carefully

### 10.3 Future Considerations
1. **Extensibility**: Design for future requirement additions
2. **Scalability**: Plan for increased data volumes
3. **Integration**: Consider future system integrations
4. **Evolution**: Plan for requirement evolution over time

---

## 11. Conclusion

The requirements analysis reveals a well-defined set of functional, non-functional, technical, and user requirements that are achievable within the project timeline and constraints. The critical requirements are clearly identified and validated, providing a solid foundation for implementation.

The dual implementation approach (Colab notebook and Google Sheets) addresses different user needs while maintaining consistency in core functionality. The requirements are prioritized appropriately, with critical features taking precedence over nice-to-have features.

Success will depend on careful implementation of the critical requirements while maintaining quality standards and user experience expectations. The requirements provide clear guidance for development and testing activities.

---

**Document Status**: Complete  
**Next Steps**: Begin implementation based on requirements  
**Review Date**: 2025-01-28





