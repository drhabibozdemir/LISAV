"""
Data Filter Module
Handles filtering and querying of laboratory data
"""
import pandas as pd
from datetime import datetime


class DataFilter:
    """Class for filtering laboratory data"""
    
    def filter_data(self, df, patients=None, samples=None, tests=None, 
                    abnormal_only=False, date_range=None, gender=None,
                    flag_type=None):
        """
        Apply filters to the dataframe
        
        Args:
            df: Input DataFrame
            patients: List of patient IDs to filter
            samples: List of sample IDs to filter
            tests: List of test names to filter
            abnormal_only: If True, only return abnormal values
            date_range: Tuple of (start_date, end_date)
            gender: Gender filter (M/F)
            flag_type: Test flag filter (N/L/H)
            
        Returns:
            DataFrame: Filtered data
        """
        filtered_df = df.copy()
        
        # Filter by patients
        if patients and len(patients) > 0:
            filtered_df = filtered_df[filtered_df['patient_id'].isin(patients)]
        
        # Filter by samples
        if samples and len(samples) > 0:
            filtered_df = filtered_df[filtered_df['sample_id'].isin(samples)]
        
        # Filter by tests
        if tests and len(tests) > 0:
            filtered_df = filtered_df[filtered_df['test_name'].isin(tests)]
        
        # Filter abnormal values only
        if abnormal_only:
            filtered_df = filtered_df[filtered_df['test_flag'].isin(['H', 'L'])]
        
        # Filter by date range
        if date_range and len(date_range) == 2:
            if 'sample_lab_admission_time' in filtered_df.columns:
                start_date = pd.to_datetime(date_range[0])
                end_date = pd.to_datetime(date_range[1])
                mask = (filtered_df['sample_lab_admission_time'] >= start_date) & \
                       (filtered_df['sample_lab_admission_time'] <= end_date)
                filtered_df = filtered_df[mask]
        
        # Filter by gender
        if gender and 'gender' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['gender'] == gender]
        
        # Filter by flag type
        if flag_type and 'test_flag' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['test_flag'] == flag_type]
        
        return filtered_df
    
    def search_patients(self, df, search_term):
        """
        Search for patients by ID
        
        Args:
            df: Input DataFrame
            search_term: Search term for patient ID
            
        Returns:
            DataFrame: Filtered data
        """
        return df[df['patient_id'].str.contains(search_term, case=False, na=False)]
    
    def get_patient_history(self, df, patient_id):
        """
        Get complete test history for a patient
        
        Args:
            df: Input DataFrame
            patient_id: Patient ID
            
        Returns:
            DataFrame: Patient's complete test history
        """
        patient_data = df[df['patient_id'] == patient_id].copy()
        
        # Sort by date if available
        if 'sample_lab_admission_time' in patient_data.columns:
            patient_data = patient_data.sort_values('sample_lab_admission_time')
        
        return patient_data
    
    def get_recent_tests(self, df, n_days=30):
        """
        Get recent tests from last n days
        
        Args:
            df: Input DataFrame
            n_days: Number of days to look back
            
        Returns:
            DataFrame: Recent tests
        """
        if 'sample_lab_admission_time' not in df.columns:
            return df
        
        df = df.copy()
        df['sample_lab_admission_time'] = pd.to_datetime(df['sample_lab_admission_time'])
        
        cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=n_days)
        
        return df[df['sample_lab_admission_time'] >= cutoff_date]
    
    def count_abnormal_values(self, df, patient_id=None):
        """
        Count abnormal values in the dataset
        
        Args:
            df: Input DataFrame
            patient_id: Optional patient ID to filter
            
        Returns:
            int: Count of abnormal values
        """
        if patient_id:
            df = df[df['patient_id'] == patient_id]
        
        return len(df[df['test_flag'].isin(['H', 'L'])])
    
    def get_critical_values(self, df, deviation_factor=2):
        """
        Get critical values that are significantly outside reference ranges
        
        Args:
            df: Input DataFrame
            deviation_factor: Factor by which value deviates from reference
            
        Returns:
            DataFrame: Critical values
        """
        df = df.copy()
        
        # Calculate deviation from reference range
        df['deviation'] = 0
        
        # For high values
        high_mask = df['test_value'] > df['reference_max']
        df.loc[high_mask, 'deviation'] = (df.loc[high_mask, 'test_value'] - df.loc[high_mask, 'reference_max']) / \
                                         df.loc[high_mask, 'reference_max']
        
        # For low values
        low_mask = df['test_value'] < df['reference_min']
        df.loc[low_mask, 'deviation'] = (df.loc[low_mask, 'reference_min'] - df.loc[low_mask, 'test_value']) / \
                                       df.loc[low_mask, 'reference_min']
        
        # Filter by deviation factor
        critical = df[abs(df['deviation']) >= deviation_factor]
        
        return critical.sort_values('deviation', ascending=False)

