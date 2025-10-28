# Laboratory Information System (LIS) v1.0.2

A modular web-based laboratory information system for managing and analyzing laboratory test data.

## 📋 Features

- **Data Upload & Management**: Load CSV files with laboratory test results
- **Advanced Filtering**: Filter data by patient, sample, test, date, and more
- **Interactive Visualizations**: Charts and graphs for data analysis
- **Statistical Analysis**: Comprehensive statistics and summaries
- **Data Exploration**: Browse and search through test results
- **Export Functionality**: Download filtered data as CSV
- **⚙️ Configuration Management**: Complete laboratory test configuration system

## 🚀 Quick Start

### Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

This will install all dependencies including:
- streamlit
- pandas
- plotly
- streamlit-tree-select (for interactive tree views)
- openpyxl (for Excel file support)
- xlrd (for legacy Excel file support)

### Running the Application

```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

## 📊 Data Format

The CSV file should contain the following columns:

- `patient_id`: Patient identifier
- `sample_id`: Sample identifier
- `age`: Patient age
- `gender`: Patient gender (M/F)
- `sample_lab_admission_time`: Sample collection date/time
- `hemolysis_value`: Hemolysis indicator (0/1)
- `icterus_value`: Icterus indicator (0/1)
- `lipemia_value`: Lipemia indicator (0/1)
- `test_name`: Test name
- `test_value`: Test result value
- `test_flag`: Test result flag (N/L/H)
- `reference_min`: Minimum reference value
- `reference_max`: Maximum reference value

## 🏗️ Architecture

### Modular Design

```
LIS/
├── main.py                 # Main application entry point
├── modules/
│   ├── __init__.py
│   ├── data_loader.py     # Data loading functionality
│   ├── data_filter.py     # Data filtering and querying
│   ├── data_visualizer.py # Visualization creation
│   ├── statistics.py      # Statistical analysis
│   └── config_manager.py  # Configuration management
├── requirements.txt
└── README.md
```

### Modules

1. **Data Loader**: Handles loading CSV and Excel files and sample data
2. **Data Filter**: Provides filtering capabilities for querying data
3. **Data Visualizer**: Creates interactive charts and graphs
4. **Statistics**: Performs statistical analysis on data
5. **Config Manager**: Manages laboratory test configuration dictionary

## 💡 Usage

### 1. Upload Data

- Click on the file uploader in the sidebar
- Select your CSV or Excel file
- Or load sample data using the "Load Sample Data" button

### 2. Explore Data

#### Overview Tab
- View key metrics and summary statistics
- See test distribution
- Preview data

#### Data Explorer Tab
- **Tree View**: Expandable view with patient statistics and sample details
- **Tree Select View**: Interactive checkbox tree for selecting patients, samples, and tests
- **Table View**: Filter data by patients, tests, or abnormal values
- Download filtered data

**Tree Select Features:**
- ☑️ Select individual patients, samples, or specific tests
- 🌳 Hierarchical tree structure (Patient → Sample → Test)
- 📊 See selected items and their details
- 💾 Export selected data as CSV

#### ⚙️ Configuration Tab
- **📊 Editable Configuration Table**: Direct editing of laboratory test parameters
- **☑️ Checkbox Controls**: For boolean values (hemolysis, icterus, lipemia, IQC, EQC, analyzer_flag)
- **📝 Text/Number Inputs**: For test names, reference ranges, critical values, and units
- **➕ Add New Tests**: Form-based interface to add new test configurations
- **📤📥 Import/Export**: Support for both Excel (.xlsx) and CSV formats
- **🔄 Auto-Loading**: Automatically loads `dictionary_v14.0.0.xlsx` on startup
- **📈 Summary Statistics**: Overview of configuration data

**Configuration Features:**
- ✅ Automatic Excel file detection and loading
- ✅ Real-time editing with immediate visual feedback
- ✅ Support for all laboratory test parameters
- ✅ Export to Excel or CSV format
- ✅ Import from Excel or CSV files
- ✅ Add/remove test configurations dynamically

#### Visualizations Tab
- View test value distributions
- Analyze patient trends
- Examine test flags
- Analyze time series data

#### Statistics Tab
- View descriptive statistics
- Analyze by test type
- Compare with reference ranges
- Get patient summaries

#### Settings Tab
- View application configuration
- Check dataset information

## 🔧 Configuration

You can customize the application by modifying:

- `main.py`: Add new tabs or features
- `modules/data_loader.py`: Add support for other file formats
- `modules/data_filter.py`: Add new filtering options
- `modules/data_visualizer.py`: Add new chart types
- `modules/statistics.py`: Add new statistical methods

## 📝 Requirements

- Python 3.8+
- streamlit >= 1.28.0
- pandas >= 1.5.0
- numpy >= 1.24.0
- plotly >= 5.14.0
- matplotlib >= 3.6.0
- streamlit-tree-select >= 1.2.0
- openpyxl >= 3.0.0 (for Excel file support)
- xlrd >= 2.0.0 (for legacy Excel file support)

## 🎯 Future Enhancements

- Database integration
- User authentication
- PDF report generation
- Email notifications
- Real-time data updates
- API integration
- Multi-language support

## 📄 License

This project is provided as-is for laboratory data management purposes.

## 🤝 Support

For issues or questions, please refer to the project documentation or contact the development team.

## 📚 Version History

### v1.0.2 (Current)
- **🔧 Bug Fixes & Improvements**:
  - Enhanced error handling for data loading
  - Improved file path detection for dictionary files
  - Better memory management for large datasets
  - Optimized tree select performance
  - Fixed minor UI inconsistencies
- **📊 Enhanced User Experience**:
  - Smoother navigation between tabs
  - Better error messages and user feedback
  - Improved data formatting and display
  - Enhanced configuration management stability
- **🔧 Technical Improvements**:
  - Code optimization and cleanup
  - Better exception handling
  - Improved data validation
  - Enhanced file I/O operations

### v1.0.1
- **🆕 New Configuration Management System**:
  - Complete laboratory test configuration interface
  - Editable table with checkboxes for boolean values and text inputs for numeric values
  - Automatic loading of `dictionary_v14.0.0.xlsx` file
  - Support for both Excel (.xlsx) and CSV file formats
  - Import/export functionality for configuration data
  - Add new test configurations dynamically
  - Real-time editing with immediate visual feedback
- **📊 Enhanced User Interface**:
  - Streamlined configuration tab with minimal design
  - Direct access to editable configuration table
  - Clean import/export section at the bottom
- **🔧 Technical Improvements**:
  - Added `ConfigManager` module for configuration handling
  - Excel file support with `openpyxl` and `xlrd` dependencies
  - Smart file path detection for dictionary files
  - Improved data type handling for boolean and numeric values
- **📈 Existing Features**:
  - Improved tree select view with spacing
  - Enhanced data display with patient/sample separation
  - Optimized performance

### v1.0.0
- Initial release
- Data upload and management
- Basic filtering and visualization
- Statistical analysis
- Data export functionality

