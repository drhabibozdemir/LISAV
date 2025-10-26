# LIS v1.0.2 Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Navigate to the LIS directory:**
   ```bash
   cd LIS/v.1.0.2
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run main.py
   ```

4. **Open your browser:**
   The application will automatically open at `http://localhost:8501`

## 📊 Using the Application

### 1. Data Loading
- **Sample Data**: Automatically loads sample data on first run
- **Upload CSV**: Use the file uploader in the sidebar to upload your own data
- **Reload Sample**: Click "Reload Sample Data" to refresh sample data

### 2. Navigation
The application has three main sections:
- **📋 Overview**: Data summary, metrics, and quality checks
- **🔍 Data Explorer**: Interactive tree view for exploring patient/sample data
- **⚙️ Configuration**: Laboratory test configuration management

### 3. Data Explorer Features
- **Tree Select View**: Hierarchical patient → sample → test structure
- **Sample Selection**: Check/uncheck samples to view specific test results
- **Quality Indicators**: View hemolysis, icterus, and lipemia flags
- **Export Data**: Download selected test results as CSV

### 4. Configuration Management
- **Edit Configuration**: Modify test parameters directly in the table
- **Add New Tests**: Use the form to add new test configurations
- **Import/Export**: Support for Excel (.xlsx) and CSV formats
- **Auto-Loading**: Automatically loads dictionary configuration files

## 🔧 Troubleshooting

### Common Issues

1. **Sample data not loading:**
   - Check if the data file exists in the correct path
   - Verify file permissions
   - Try uploading your own CSV file

2. **Dictionary file not found:**
   - Ensure dictionary files are in the correct directory
   - Check file naming conventions
   - Use the import feature to upload configuration files

3. **CSV upload errors:**
   - Verify CSV format matches expected columns
   - Check for missing required columns
   - Ensure proper data types

### Required CSV Columns
Your CSV file must contain these columns:
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

## 📈 New in v1.0.2

### Enhanced Error Handling
- Better error messages for file loading issues
- Improved validation of data formats
- More informative error notifications

### Performance Improvements
- Faster tree select rendering
- Optimized memory usage
- Smoother navigation

### Data Quality Features
- Data quality summary in Overview tab
- Missing value detection
- Duplicate test identification
- Invalid flag detection
- Out-of-range value alerts

### UI/UX Improvements
- Better loading indicators
- Enhanced error feedback
- Improved data formatting
- Smoother transitions

## 🆘 Support

For technical support or feature requests:
- Check the README.md for detailed documentation
- Review RELEASE_NOTES.md for version information
- Contact the development team

---

**Version**: 1.0.2  
**Developer**: Dr. Habib ÖZDEMİR  
**Release Date**: October 26, 2025