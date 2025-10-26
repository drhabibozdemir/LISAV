"""
Laboratory Information System (LIS) - Main Application
Version 1.0.2
"""
import streamlit as st
import pandas as pd
from streamlit_tree_select import tree_select
from modules.data_loader import DataLoader
from modules.data_filter import DataFilter
from modules.config_manager import ConfigManager
from modules.approval_engine import ApprovalEngine

# Page configuration
st.set_page_config(
    page_title="Laboratory Information System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'filtered_data' not in st.session_state:
        st.session_state.filtered_data = None
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'config_manager' not in st.session_state:
        st.session_state.config_manager = ConfigManager()
    if 'approval_engine' not in st.session_state:
        st.session_state.approval_engine = ApprovalEngine(st.session_state.config_manager)
    
    # Sidebar
    with st.sidebar:
        # Header in sidebar - moved to top
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 1rem; border-bottom: 3px solid #1f77b4; margin-bottom: 1.5rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 0.5rem;'>
            <h1 style='color: #1f77b4; margin: 0; font-size: 2.2rem; font-weight: bold;'>🔬 LIS</h1>
            <p style='color: #2c3e50; margin: 0.5rem 0; font-size: 1rem; font-weight: 600;'>TBD Uluslararası Laboratuvar Tıbbı Zirvesi</p>
            <p style='color: #34495e; margin: 0.3rem 0; font-size: 0.9rem;'>28 Ekim - 31 Ekim</p>
            <p style='color: #666; margin: 0.5rem 0; font-size: 0.9rem;'>Laboratory Information System v1.0.2</p>
            <p style='color: #888; margin: 0; font-size: 0.8rem; font-style: italic;'>Dr. Habib ÖZDEMİR</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu (only if data is loaded)
        if st.session_state.data is not None:
            st.subheader("🧭 Navigation")
            
            # Navigation buttons
            pages = [
                "📋 Overview",
                "🔍 Data Explorer",
                "⚙️ Configuration",
                "✅ Approval System"
            ]
            
            current = st.session_state.get('current_page', "📋 Overview")
            
            for page in pages:
                if st.button(page, use_container_width=True, 
                           type="primary" if page == current else "secondary",
                           key=f"nav_{page}"):
                    st.session_state.current_page = page
                    st.rerun()
            
            st.divider()
        
        st.header("📊 Data Management")
        
        # Auto-load sample data on first run
        if not st.session_state.data_loaded:
            try:
                with st.spinner("Loading sample data..."):
                    data_loader = DataLoader()
                    df = data_loader.load_sample_data()
                    
                    # Process approval system
                    with st.spinner("Processing approval system..."):
                        approval_engine = st.session_state.approval_engine
                        df_with_approval = approval_engine.process_test_results(df)
                    
                    st.session_state.data = df_with_approval
                    st.session_state.filtered_data = df_with_approval
                    st.session_state.data_loaded = True
                    st.success(f"✅ Sample data loaded! ({len(df)} rows)")
                    st.rerun()
            except FileNotFoundError as e:
                st.warning(f"⚠️ Sample data file not found: {e}")
                st.info("Please upload a CSV file manually")
            except ValueError as e:
                st.error(f"❌ Error in sample data: {e}")
                st.info("Please upload a CSV file manually")
            except Exception as e:
                st.error(f"❌ Unexpected error loading sample data: {str(e)}")
                st.info("Please upload a CSV file manually")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload CSV File",
            type=['csv'],
            help="Upload your laboratory data in CSV format"
        )
        
        if uploaded_file is not None:
            try:
                with st.spinner("Loading uploaded file..."):
                    data_loader = DataLoader()
                    df = data_loader.load_csv(uploaded_file)
                    
                    # Process approval system
                    with st.spinner("Processing approval system..."):
                        approval_engine = st.session_state.approval_engine
                        df_with_approval = approval_engine.process_test_results(df)
                    
                    st.session_state.data = df_with_approval
                    st.session_state.filtered_data = df_with_approval
                    st.session_state.data_loaded = True
                    st.success(f"✅ Data loaded successfully! ({len(df)} rows)")
                    st.rerun()
            except ValueError as e:
                st.error(f"❌ Error in file format: {e}")
            except FileNotFoundError as e:
                st.error(f"❌ File not found: {e}")
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
        
        # Reload sample data button
        if st.button("📂 Reload Sample Data", use_container_width=True):
            try:
                with st.spinner("Reloading sample data..."):
                    data_loader = DataLoader()
                    df = data_loader.load_sample_data()
                    
                    # Process approval system
                    with st.spinner("Processing approval system..."):
                        approval_engine = st.session_state.approval_engine
                        df_with_approval = approval_engine.process_test_results(df)
                    
                    st.session_state.data = df_with_approval
                    st.session_state.filtered_data = df_with_approval
                    st.session_state.data_loaded = True
                    st.success(f"✅ Sample data reloaded! ({len(df)} rows)")
                    st.rerun()
            except FileNotFoundError as e:
                st.error(f"❌ Sample data file not found: {e}")
            except ValueError as e:
                st.error(f"❌ Error in sample data: {e}")
            except Exception as e:
                st.error(f"❌ Error reloading sample data: {str(e)}")
        
        st.divider()
        
        # Data info
        if st.session_state.data is not None:
            st.subheader("📈 Dataset Info")
            st.info(f"""
            - Total Patients: {st.session_state.data['patient_id'].nunique()}
            - Total Samples: {st.session_state.data['sample_id'].nunique()}
            - Total Tests: {len(st.session_state.data)}
            - Test Names: {st.session_state.data['test_name'].nunique()}
            """)
    
    # Main content area
    if st.session_state.data is not None:
        # Initialize navigation state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "📋 Overview"
        
        # Show page content based on selection
        if st.session_state.current_page == "📋 Overview":
            show_overview()
        elif st.session_state.current_page == "🔍 Data Explorer":
            show_data_explorer()
        elif st.session_state.current_page == "⚙️ Configuration":
            show_configuration()
        elif st.session_state.current_page == "✅ Approval System":
            show_approval_system()
    else:
        # Welcome screen
        show_welcome_screen()

def show_welcome_screen():
    """Display welcome screen when no data is loaded"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h2>Welcome to Laboratory Information System</h2>
            <p style='font-size: 1.2rem; color: #666;'>
                Please upload a CSV file or load sample data from the sidebar to get started.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### ✨ Features:
        - **Data Upload & Management**: Load CSV files with laboratory test results
        - **Advanced Filtering**: Filter data by patient, sample, test, date, and more
        - **Interactive Visualizations**: Charts and graphs for data analysis
        - **Statistical Analysis**: Comprehensive statistics and summaries
        - **Data Exploration**: Browse and search through test results
        
        ### 📋 Expected Data Format:
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
        """)

def show_overview():
    """Display data overview"""
    df = st.session_state.filtered_data
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Patients", df['patient_id'].nunique())
    
    with col2:
        st.metric("🧪 Total Samples", df['sample_id'].nunique())
    
    with col3:
        st.metric("📝 Total Tests", len(df))
    
    with col4:
        st.metric("🔬 Unique Test Types", df['test_name'].nunique())
    
    st.divider()
    
    # Summary statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Test Distribution")
        test_counts = df['test_name'].value_counts()
        st.bar_chart(test_counts)
    
    with col2:
        st.subheader("🚨 Abnormal Values")
        abnormal = df[df['test_flag'].isin(['H', 'L'])]
        if len(abnormal) > 0:
            abnormal_counts = abnormal['test_flag'].value_counts()
            st.bar_chart(abnormal_counts)
        else:
            st.info("No abnormal values found")
    
    st.divider()
    
    # Data validation summary
    st.subheader("🔍 Data Quality Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        missing_values = df.isnull().sum().sum()
        st.metric("Missing Values", missing_values)
    
    with col2:
        duplicate_tests = df.duplicated(subset=['patient_id', 'sample_id', 'test_name']).sum()
        st.metric("Duplicate Tests", duplicate_tests)
    
    with col3:
        invalid_flags = len(df[~df['test_flag'].isin(['N', 'L', 'H'])])
        st.metric("Invalid Flags", invalid_flags)
    
    with col4:
        out_of_range = len(df[(df['test_value'] < df['reference_min']) | (df['test_value'] > df['reference_max'])])
        st.metric("Out of Range", out_of_range)
    
    # Show warnings if data quality issues exist
    if missing_values > 0 or duplicate_tests > 0 or invalid_flags > 0:
        st.warning("⚠️ Data quality issues detected. Please review the data before analysis.")
    
    st.divider()

def show_data_explorer():
    """Display data explorer with tree structure for patients and samples"""
    df = st.session_state.data
    
    # Set filtered data
    st.session_state.filtered_data = df
    
    # Show only Tree Select View
    show_tree_select_view(df)

def show_tree_view(df):
    """Display data in tree structure: Patients -> Samples -> Tests"""
    
    st.subheader("🌳 Patient & Sample Tree View")
    
    # Get unique patients
    patients = sorted(df['patient_id'].unique())
    
    # Patient info summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", len(patients))
    
    with col2:
        st.metric("Total Samples", df['sample_id'].nunique())
    
    with col3:
        st.metric("Total Tests", len(df))
    
    with col4:
        abnormal = len(df[df['test_flag'].isin(['H', 'L'])])
        st.metric("Abnormal Values", abnormal)
    
    st.divider()
    
    # Display patients in tree structure
    if len(patients) == 0:
        st.warning("No patients found matching the criteria")
        return
    
    # Patient containers with expanders
    with st.container():
        for idx, patient_id in enumerate(patients):
            patient_data = df[df['patient_id'] == patient_id]
            
            # Get patient info
            patient_info = patient_data.iloc[0]
            age = patient_info.get('age', 'N/A')
            gender = patient_info.get('gender', 'N/A')
            
            # Calculate statistics for this patient
            total_samples = patient_data['sample_id'].nunique()
            total_tests = len(patient_data)
            abnormal_tests = len(patient_data[patient_data['test_flag'].isin(['H', 'L'])])
            
            # Initialize session state for patient expand
            patient_key = f"patient_{patient_id}"
            if patient_key not in st.session_state:
                st.session_state[patient_key] = False
            
            # Patient header with toggle button
            col1, col2 = st.columns([8, 1])
            with col1:
                patient_title = f"👤 {patient_id} | Age: {age} | Gender: {gender} | Samples: {total_samples} | Tests: {total_tests}"
                if abnormal_tests > 0:
                    patient_title += " 🚨"
                st.markdown(f"### {patient_title}")
            
            with col2:
                # Toggle button for patient
                toggle_label = "🔽 Collapse" if st.session_state[patient_key] else "▶️ Expand"
                if st.button(toggle_label, key=f"toggle_{patient_id}"):
                    st.session_state[patient_key] = not st.session_state[patient_key]
            
            # Show patient data if expanded
            if st.session_state[patient_key]:
                st.markdown("---")
                
                # Patient statistics
                stat_col1, stat_col2, stat_col3 = st.columns(3)
                with stat_col1:
                    st.metric("Total Samples", total_samples)
                with stat_col2:
                    st.metric("Total Tests", total_tests)
                with stat_col3:
                    st.metric("Abnormal Tests", abnormal_tests)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Get unique samples for this patient
                samples = sorted(patient_data['sample_id'].unique())
                
                for sample_idx, sample_id in enumerate(samples):
                    sample_data = patient_data[patient_data['sample_id'] == sample_id]
                    
                    # Initialize session state for sample expand
                    sample_key = f"sample_{sample_id}"
                    if sample_key not in st.session_state:
                        st.session_state[sample_key] = False
                    
                    # Get sample info
                    if 'sample_lab_admission_time' in sample_data.columns:
                        sample_time = sample_data.iloc[0]['sample_lab_admission_time']
                        if isinstance(sample_time, str):
                            sample_date = sample_time.split()[0] if ' ' in sample_time else sample_time
                        else:
                            sample_date = str(sample_time).split()[0]
                    else:
                        sample_date = "N/A"
                    
                    # Sample statistics
                    sample_tests = len(sample_data)
                    sample_abnormal = len(sample_data[sample_data['test_flag'].isin(['H', 'L'])])
                    
                    # Sample header
                    sample_col1, sample_col2 = st.columns([9, 1])
                    with sample_col1:
                        sample_title = f"🧪 {sample_id} | Date: {sample_date} | Tests: {sample_tests}"
                        if sample_abnormal > 0:
                            sample_title += " 🚨"
                        st.markdown(f"**{sample_title}**")
                    
                    with sample_col2:
                        # Toggle button for sample
                        toggle_sample_label = "🔽" if st.session_state[sample_key] else "▶️"
                        if st.button(toggle_sample_label, key=f"toggle_sample_{sample_id}"):
                            st.session_state[sample_key] = not st.session_state[sample_key]
                    
                    # Show sample data if expanded
                    if st.session_state[sample_key]:
                        st.markdown("**Sample Details**")
                        
                        # Sample quality indicators
                        if len(sample_data) > 0:
                            sample_info = sample_data.iloc[0]
                            hemolysis = sample_info.get('hemolysis_value', 0)
                            icterus = sample_info.get('icterus_value', 0)
                            lipemia = sample_info.get('lipemia_value', 0)
                            
                            quality_col1, quality_col2, quality_col3 = st.columns(3)
                            with quality_col1:
                                st.write(f"🔴 Hemolysis: {'Yes' if hemolysis == 1 else 'No'}")
                            with quality_col2:
                                st.write(f"🟡 Icterus: {'Yes' if icterus == 1 else 'No'}")
                            with quality_col3:
                                st.write(f"⚪ Lipemia: {'Yes' if lipemia == 1 else 'No'}")
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Display tests for this sample
                        st.markdown(f"**📝 Test Results ({sample_tests})**")
                        
                        # Create table for tests
                        test_table = sample_data[[
                            'test_name', 'test_value', 'test_flag', 
                            'reference_min', 'reference_max'
                        ]].copy()
                        
                        # Add color coding based on test flag
                        def style_test_flag(val):
                            if val == 'H':
                                return 'background-color: #ffcccc'
                            elif val == 'L':
                                return 'background-color: #fff4cc'
                            else:
                                return 'background-color: #ccffcc'
                        
                        styled_table = test_table.style.applymap(style_test_flag, subset=['test_flag'])
                        st.dataframe(
                            styled_table,
                            use_container_width=True,
                            height=min(300, len(test_table) * 35 + 50),
                            hide_index=True
                        )
                        st.markdown("<br>", unsafe_allow_html=True)
                    
                    st.markdown("---")
                
                st.markdown("<br><br>", unsafe_allow_html=True)
            
            st.markdown("---")

def show_table_view(df):
    """Display data in table format with filters"""
    
    st.subheader("📊 Data Table View")
    
    # Additional filters for table view
    col1, col2 = st.columns(2)
    
    with col1:
        selected_tests = st.multiselect(
            "Select Tests",
            options=sorted(df['test_name'].unique()),
            default=df['test_name'].unique()
        )
    
    with col2:
        selected_patients = st.multiselect(
            "Select Patients",
            options=sorted(df['patient_id'].unique()),
            default=sorted(df['patient_id'].unique())[:20] if len(df['patient_id'].unique()) > 20 else sorted(df['patient_id'].unique())
        )
    
    # Apply filters
    table_df = df.copy()
    
    if selected_tests:
        table_df = table_df[table_df['test_name'].isin(selected_tests)]
    
    if selected_patients:
        table_df = table_df[table_df['patient_id'].isin(selected_patients)]
    
    # Display table
    st.dataframe(
        table_df,
        use_container_width=True,
        height=600
    )
    
    # Download button
    st.divider()
    csv = table_df.to_csv(index=False)
    st.download_button(
        label="💾 Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_lab_data.csv",
        mime="text/csv",
        use_container_width=True
    )

def show_tree_select_view(df):
    """Display data using streamlit-tree-select with checkbox tree"""
    
    st.subheader("🌳 Patient & Sample Tree Select")
    
    # Build tree structure (Patient -> Sample only, no tests in tree)
    nodes = []
    patients = sorted(df['patient_id'].unique())
    
    for patient_id in patients:
        patient_data = df[df['patient_id'] == patient_id]
        
        # Get patient info
        patient_info = patient_data.iloc[0]
        age = patient_info.get('age', 'N/A')
        gender = patient_info.get('gender', 'N/A')
        
        # Get samples for this patient
        samples = sorted(patient_data['sample_id'].unique())
        sample_children = []
        
        for sample_id in samples:
            sample_data = patient_data[patient_data['sample_id'] == sample_id]
            
            # Get sample info
            if 'sample_lab_admission_time' in sample_data.columns:
                sample_time = sample_data.iloc[0]['sample_lab_admission_time']
                # Show full datetime
                sample_date = str(sample_time)
            else:
                sample_date = "N/A"
            
            sample_tests = len(sample_data)
            sample_abnormal = len(sample_data[sample_data['test_flag'].isin(['H', 'L'])])
            
            # Only add sample to tree, not individual tests
            sample_label = f"{sample_id} - Date: {sample_date} - Tests: {sample_tests}"
            if sample_abnormal > 0:
                sample_label += " 🚨"
            
            sample_children.append({
                "label": sample_label,
                "value": sample_id
            })
        
        patient_label = f"👤 {patient_id} - Age: {age} - Gender: {gender}"
        patient_node = {
            "label": patient_label,
            "value": patient_id,
            "children": sample_children
        }
        nodes.append(patient_node)
    
    # Two column layout: Tree on left (narrower), Test Results on right (wider)
    tree_col, detail_col = st.columns([1.5, 4.5])
    
    with tree_col:
        st.markdown("### Select Samples")
        result = tree_select(nodes)
    
    with detail_col:
        st.markdown("### Test Results for Selected Samples")
        
        # Get selected samples
        selected_samples = []
        if result and result.get('checked'):
            selected_samples = [item for item in result['checked'] if item in df['sample_id'].values]
        
        # Show test results for selected samples
        if selected_samples:
            # Show sample quality indicators
            st.markdown("**Sample Quality Indicators:**")
            quality_col1, quality_col2, quality_col3 = st.columns(3)
            
            for sample_id in selected_samples:
                sample_data = df[df['sample_id'] == sample_id]
                if len(sample_data) > 0:
                    sample_info = sample_data.iloc[0]
                    hemolysis = sample_info.get('hemolysis_value', 0)
                    icterus = sample_info.get('icterus_value', 0)
                    lipemia = sample_info.get('lipemia_value', 0)
                    
                    with quality_col1:
                        st.write(f"🔴 **{sample_id}** - Hemolysis: {'Yes' if hemolysis == 1 else 'No'}")
                    with quality_col2:
                        st.write(f"🟡 **{sample_id}** - Icterus: {'Yes' if icterus == 1 else 'No'}")
                    with quality_col3:
                        st.write(f"⚪ **{sample_id}** - Lipemia: {'Yes' if lipemia == 1 else 'No'}")
            
            st.markdown("---")
            
            # Get data for selected samples
            selected_df = pd.DataFrame()
            for sample_id in selected_samples:
                selected_df = pd.concat([selected_df, df[df['sample_id'] == sample_id]])
            
            if len(selected_df) > 0:
                # Display selected columns (excluding hemolysis, icterus, lipemia)
                columns_to_show = ['patient_id', 'sample_id', 'test_name', 'test_value', 'test_flag', 'reference_min', 'reference_max', 'approval_status']
                display_df = selected_df[columns_to_show].copy()
                
                # Format float columns to 2 decimal places
                numeric_cols = display_df.select_dtypes(include=['float64', 'float32']).columns
                for col in numeric_cols:
                    if col in display_df.columns:
                        display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) and isinstance(x, (int, float)) else x)
                
                # Add spacing rows between samples and patients
                spaced_df = pd.DataFrame()
                current_patient = None
                current_sample = None
                
                for idx, row in display_df.iterrows():
                    # Check if this is a new patient
                    if current_patient != row['patient_id']:
                        if current_patient is not None:
                            # Add 2 empty rows between patients
                            empty_rows = pd.DataFrame([[''] * len(columns_to_show)] * 2, columns=columns_to_show)
                            spaced_df = pd.concat([spaced_df, empty_rows], ignore_index=True)
                        current_patient = row['patient_id']
                        current_sample = None
                    
                    # Check if this is a new sample
                    if current_sample != row['sample_id']:
                        if current_sample is not None:
                            # Add 1 empty row between samples
                            empty_row = pd.DataFrame([[''] * len(columns_to_show)], columns=columns_to_show)
                            spaced_df = pd.concat([spaced_df, empty_row], ignore_index=True)
                        current_sample = row['sample_id']
                    
                    # Add the actual data row
                    spaced_df = pd.concat([spaced_df, row.to_frame().T], ignore_index=True)
                
                # Add color coding based on test flag
                def style_row(row):
                    # Skip styling for empty rows
                    if row['patient_id'] == '':
                        return [''] * len(row)
                    
                    flag_col_idx = list(spaced_df.columns).index('test_flag') if 'test_flag' in spaced_df.columns else 4
                    flag_val = row.iloc[flag_col_idx] if flag_col_idx < len(row) else row['test_flag']
                    
                    if str(flag_val) == 'H':
                        return ['background-color: #ffcccc'] * len(row)
                    elif str(flag_val) == 'L':
                        return ['background-color: #fff4cc'] * len(row)
                    else:
                        return ['background-color: #ccffcc'] * len(row)
                
                styled_df = spaced_df.style.apply(style_row, axis=1)
                
                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    height=600,
                    hide_index=True
                )
                
                # Summary statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Tests", len(display_df))
                with col2:
                    st.metric("Normal", len(display_df[display_df['test_flag'] == 'N']))
                with col3:
                    st.metric("High 🚨", len(display_df[display_df['test_flag'] == 'H']))
                with col4:
                    st.metric("Low ⚠️", len(display_df[display_df['test_flag'] == 'L']))
                
                # Download button
                st.markdown("---")
                csv = selected_df.to_csv(index=False)
                st.download_button(
                    label="💾 Download Selected Test Data as CSV",
                    data=csv,
                    file_name="selected_lab_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("No test data available")
        else:
            st.info("Please select samples from the tree to view test results")

def show_configuration():
    """Display configuration management interface"""
    
    config_manager = st.session_state.config_manager
    
    # Load dictionary data
    if config_manager.get_config_data() is None:
        st.error("Failed to load dictionary configuration")
        return
    
    df = config_manager.get_config_data()
    column_info = config_manager.get_column_info()
    
    # Display configuration table
    st.markdown("### 📊 Test Configuration Table")
    st.markdown("*Edit values directly in the table below. Checkboxes for 0/1 values, text inputs for other values.*")
    
    # Create editable dataframe
    edited_df = st.data_editor(
        df,
        column_config={
            col: st.column_config.CheckboxColumn(
                col,
                help=column_info[col]['description'],
                default=False
            ) if column_info[col]['type'] == 'checkbox' else
            st.column_config.NumberColumn(
                col,
                help=column_info[col]['description'],
                format="%.2f"
            ) if column_info[col]['type'] == 'number' else
            st.column_config.TextColumn(
                col,
                help=column_info[col]['description']
            )
            for col in df.columns if col in column_info
        },
        use_container_width=True,
        num_rows="dynamic",
        key="config_editor"
    )
    
    # Update session state with edited data
    if edited_df is not None:
        config_manager.config_data = edited_df
    
    # Add new row functionality
    st.markdown("### ➕ Add New Test Configuration")
    
    with st.form("add_test_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_test = st.text_input("Test Name", key="new_test_name")
            new_age = st.text_input("Age Group", value="Adult", key="new_age")
            new_units = st.text_input("Units", key="new_units")
        
        with col2:
            new_ref_min = st.number_input("Reference Min", key="new_ref_min")
            new_ref_max = st.number_input("Reference Max", key="new_ref_max")
            new_critical_min = st.number_input("Critical Min", key="new_critical_min")
            new_critical_max = st.number_input("Critical Max", key="new_critical_max")
        
        # Boolean flags
        st.markdown("**Quality Control Flags:**")
        col3, col4, col5, col6, col7 = st.columns(5)
        
        with col3:
            new_hemolysis = st.checkbox("Hemolysis", key="new_hemolysis")
        with col4:
            new_icterus = st.checkbox("Icterus", key="new_icterus")
        with col5:
            new_lipemia = st.checkbox("Lipemia", key="new_lipemia")
        with col6:
            new_iqc = st.checkbox("IQC", key="new_iqc")
        with col7:
            new_eqc = st.checkbox("EQC", key="new_eqc")
        
        # Delta check values
        st.markdown("**Delta Check Values:**")
        col8, col9, col10 = st.columns(3)
        
        with col8:
            new_delta_min = st.number_input("Delta Check Min", key="new_delta_min")
        with col9:
            new_delta_max = st.number_input("Delta Check Max", key="new_delta_max")
        with col10:
            new_delta_interval = st.number_input("Delta Check Interval", key="new_delta_interval")
        
        new_analyzer_flag = st.checkbox("Analyzer Flag", key="new_analyzer_flag")
        
        if st.form_submit_button("➕ Add Test Configuration", use_container_width=True):
            if new_test:
                # Create new row
                new_row = {
                    'test': new_test,
                    'age': new_age,
                    'hemolysis': new_hemolysis,
                    'icterus': new_icterus,
                    'lipemia': new_lipemia,
                    'IQC': new_iqc,
                    'EQC': new_eqc,
                    'ref_min': new_ref_min,
                    'ref_max': new_ref_max,
                    'delta_check_min': new_delta_min,
                    'delta_check_max': new_delta_max,
                    'analyzer_flag': new_analyzer_flag,
                    'units': new_units,
                    'critical_min': new_critical_min,
                    'critical_max': new_critical_max,
                    'delta_check_interval': new_delta_interval
                }
                
                # Add to dataframe
                new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                config_manager.config_data = new_df
                st.success(f"Added new test configuration: {new_test}")
                st.rerun()
            else:
                st.error("Please enter a test name")
    
    # Summary statistics
    st.divider()
    st.markdown("### 📈 Configuration Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tests", len(df))
    
    with col2:
        hemolysis_count = df['hemolysis'].sum() if 'hemolysis' in df.columns else 0
        st.metric("Hemolysis Tests", int(hemolysis_count))
    
    with col3:
        icterus_count = df['icterus'].sum() if 'icterus' in df.columns else 0
        st.metric("Icterus Tests", int(icterus_count))
    
    with col4:
        lipemia_count = df['lipemia'].sum() if 'lipemia' in df.columns else 0
        st.metric("Lipemia Tests", int(lipemia_count))
    
    # Import/Export Section at the bottom
    st.divider()
    st.markdown("### 📤📥 Import & Export Configuration")
    
    col_import, col_export = st.columns(2)
    
    with col_import:
        st.markdown("#### 📥 Import Configuration")
        uploaded_file = st.file_uploader(
            "Upload Excel/CSV File",
            type=['csv', 'xlsx', 'xls'],
            help="Upload an Excel or CSV file to replace current configuration",
            key="config_upload"
        )
        
        if uploaded_file is not None:
            new_df = config_manager.import_config(uploaded_file)
            if new_df is not None:
                st.success("Configuration imported successfully!")
                st.rerun()
    
    with col_export:
        st.markdown("#### 📤 Export Configuration")
        
        # Export buttons
        col_csv, col_excel = st.columns(2)
        
        with col_csv:
            # Export CSV
            csv_data = config_manager.export_config(df)
            st.download_button(
                label="📤 Export CSV",
                data=csv_data,
                file_name="dictionary_config.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_excel:
            # Export Excel
            excel_data = config_manager.export_excel(df)
            st.download_button(
                label="📤 Export Excel",
                data=excel_data,
                file_name="dictionary_config.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

def show_approval_system():
    """Display approval system interface"""
    df = st.session_state.data
    
    if df is None:
        st.error("No data available for approval processing")
        return
    
    st.subheader("✅ Laboratory Approval System")
    st.markdown("*Automated validation system using laboratory rules and configuration*")
    
    # Approval statistics
    approval_engine = st.session_state.approval_engine
    stats = approval_engine.get_approval_statistics(df)
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tests", stats['total_tests'])
        
        with col2:
            st.metric("Auto Validated", stats['auto_validated'], 
                     delta=f"{stats['auto_validation_rate']:.1f}%")
        
        with col3:
            st.metric("Manual Review", stats['manual_review_needed'],
                     delta=f"{stats['manual_review_rate']:.1f}%")
        
        with col4:
            success_rate = stats['auto_validation_rate']
            st.metric("Success Rate", f"{success_rate:.1f}%")
        
        st.divider()
        
        # Approval status distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Approval Status Distribution")
            approval_counts = df['approval_status'].value_counts()
            
            # Create pie chart
            import plotly.express as px
            fig = px.pie(values=approval_counts.values, 
                        names=approval_counts.index,
                        title="Approval Status Distribution",
                        color_discrete_map={
                            'Auto Validated': '#28a745',
                            'Manual Review Needed': '#ffc107'
                        })
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🚨 Failed Rules Analysis")
            failed_rules_stats = stats.get('failed_rules_stats', {})
            
            if failed_rules_stats:
                failed_df = pd.DataFrame(list(failed_rules_stats.items()), 
                                       columns=['Rule', 'Count'])
                failed_df = failed_df.sort_values('Count', ascending=False)
                
                fig = px.bar(failed_df, x='Rule', y='Count',
                           title="Most Common Failed Rules",
                           color='Count',
                           color_continuous_scale='Reds')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No failed rules detected")
        
        st.divider()
        
        # Detailed approval results
        st.subheader("📋 Detailed Approval Results")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            status_filter = st.selectbox(
                "Filter by Approval Status",
                options=["All", "Auto Validated", "Manual Review Needed"],
                key="approval_status_filter"
            )
        
        with col2:
            test_filter = st.multiselect(
                "Filter by Test Name",
                options=sorted(df['test_name'].unique()),
                default=[],
                key="approval_test_filter"
            )
        
        # Apply filters
        filtered_df = df.copy()
        
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['approval_status'] == status_filter]
        
        if test_filter:
            filtered_df = filtered_df[filtered_df['test_name'].isin(test_filter)]
        
        # Display filtered results
        if len(filtered_df) > 0:
            # Show summary
            st.info(f"Showing {len(filtered_df)} results")
            
            # Pagination controls
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                rows_per_page = st.selectbox(
                    "Rows per page",
                    options=[50, 100, 200, 500, 1000],
                    index=1,  # Default to 100
                    key="approval_rows_per_page"
                )
            
            with col2:
                total_pages = (len(filtered_df) + rows_per_page - 1) // rows_per_page
                if total_pages > 1:
                    page = st.selectbox(
                        "Page",
                        options=list(range(1, total_pages + 1)),
                        key="approval_page"
                    )
                else:
                    page = 1
            
            # Calculate start and end indices
            start_idx = (page - 1) * rows_per_page
            end_idx = min(start_idx + rows_per_page, len(filtered_df))
            
            with col3:
                st.write(f"Page {page} of {total_pages}")
                st.write(f"Showing {start_idx + 1}-{end_idx} of {len(filtered_df)}")
            
            # Get page data
            page_df = filtered_df.iloc[start_idx:end_idx]
            
            # Display table with approval information
            display_columns = ['patient_id', 'sample_id', 'test_name', 'test_value', 
                             'test_flag', 'approval_status', 'approval_comments']
            
            display_df = page_df[display_columns].copy()
            
            # Add color coding for approval status
            def style_approval_status(val):
                if val == 'Auto Validated':
                    return 'background-color: #d4edda; color: #155724'
                elif val == 'Manual Review Needed':
                    return 'background-color: #fff3cd; color: #856404'
                else:
                    return ''
            
            styled_df = display_df.style.applymap(style_approval_status, subset=['approval_status'])
            
            st.dataframe(
                styled_df,
                use_container_width=True,
                height=min(1000, len(display_df) * 35 + 50),
                hide_index=True
            )
            
            # Download buttons
            col_download1, col_download2 = st.columns(2)
            
            with col_download1:
                # Download current page
                csv_page = page_df.to_csv(index=False)
                st.download_button(
                    label="💾 Download Current Page",
                    data=csv_page,
                    file_name=f"approval_results_page_{page}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_download2:
                # Download all filtered results
                csv_all = filtered_df.to_csv(index=False)
                st.download_button(
                    label="💾 Download All Results",
                    data=csv_all,
                    file_name="approval_results_all.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.warning("No results match the selected filters")
    
    else:
        st.error("Unable to generate approval statistics")


if __name__ == "__main__":
    main()

