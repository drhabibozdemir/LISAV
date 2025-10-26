"""
Statistics Module
Handles statistical analysis of laboratory data
"""
import pandas as pd
import numpy as np


class Statistics:
    """Class for statistical analysis of laboratory data"""
    
    def calculate_descriptive_stats(self, df):
        """
        Calculate descriptive statistics for a test
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame: Descriptive statistics
        """
        if 'test_value' not in df.columns:
            return pd.DataFrame()
        
        stats_dict = {
            'Mean': [df['test_value'].mean()],
            'Median': [df['test_value'].median()],
            'Std Dev': [df['test_value'].std()],
            'Min': [df['test_value'].min()],
            'Max': [df['test_value'].max()],
            '25th Percentile': [df['test_value'].quantile(0.25)],
            '75th Percentile': [df['test_value'].quantile(0.75)],
            'Count': [len(df)],
            'Normal Count': [len(df[df['test_flag'] == 'N'])],
            'High Count': [len(df[df['test_flag'] == 'H'])],
            'Low Count': [len(df[df['test_flag'] == 'L'])]
        }
        
        return pd.DataFrame(stats_dict).round(3)
    
    def get_complete_summary(self, df):
        """
        Get complete statistical summary for all tests
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame: Complete statistical summary
        """
        summary_data = []
        
        for test_name in df['test_name'].unique():
            test_data = df[df['test_name'] == test_name]
            
            summary_data.append({
                'Test Name': test_name,
                'Count': len(test_data),
                'Mean': test_data['test_value'].mean(),
                'Median': test_data['test_value'].median(),
                'Std': test_data['test_value'].std(),
                'Min': test_data['test_value'].min(),
                'Max': test_data['test_value'].max(),
                'Normal Count': len(test_data[test_data['test_flag'] == 'N']),
                'High Count': len(test_data[test_data['test_flag'] == 'H']),
                'Low Count': len(test_data[test_data['test_flag'] == 'L']),
                'Abnormal Rate': f"{(len(test_data[test_data['test_flag'].isin(['H','L'])]) / len(test_data) * 100):.2f}%"
            })
        
        return pd.DataFrame(summary_data).round(3)
    
    def calculate_percentiles(self, df, percentiles=[10, 25, 50, 75, 90]):
        """
        Calculate percentiles for test values
        
        Args:
            df: Input DataFrame
            percentiles: List of percentiles to calculate
            
        Returns:
            DataFrame: Percentile values
        """
        percentile_dict = {}
        
        for p in percentiles:
            percentile_dict[f'{p}th Percentile'] = [df['test_value'].quantile(p/100)]
        
        return pd.DataFrame(percentile_dict).round(3)
    
    def get_abnormal_rate(self, df):
        """
        Calculate abnormal rate for each test
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame: Abnormal rate by test
        """
        abnormal_data = []
        
        for test_name in df['test_name'].unique():
            test_data = df[df['test_name'] == test_name]
            total = len(test_data)
            abnormal = len(test_data[test_data['test_flag'].isin(['H', 'L'])])
            
            abnormal_data.append({
                'Test Name': test_name,
                'Total Tests': total,
                'Abnormal Tests': abnormal,
                'Abnormal Rate (%)': (abnormal / total * 100) if total > 0 else 0,
                'Normal Tests': total - abnormal
            })
        
        result_df = pd.DataFrame(abnormal_data)
        result_df = result_df.sort_values('Abnormal Rate (%)', ascending=False)
        
        return result_df.round(3)
    
    def compare_with_reference_range(self, df):
        """
        Compare actual values with reference ranges
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame: Comparison with reference ranges
        """
        comparison_data = []
        
        for test_name in df['test_name'].unique():
            test_data = df[df['test_name'] == test_name]
            
            if len(test_data) == 0:
                continue
            
            ref_min = test_data['reference_min'].iloc[0]
            ref_max = test_data['reference_max'].iloc[0]
            
            comparison_data.append({
                'Test Name': test_name,
                'Reference Min': ref_min,
                'Reference Max': ref_max,
                'Actual Min': test_data['test_value'].min(),
                'Actual Max': test_data['test_value'].max(),
                'Actual Mean': test_data['test_value'].mean(),
                'Within Range': len(test_data[test_data['test_value'].between(ref_min, ref_max)]),
                'Out of Range': len(test_data[~test_data['test_value'].between(ref_min, ref_max)]),
                'Total': len(test_data)
            })
        
        return pd.DataFrame(comparison_data).round(3)
    
    def get_patient_summary(self, df, patient_id):
        """
        Get statistical summary for a specific patient
        
        Args:
            df: Input DataFrame
            patient_id: Patient ID
            
        Returns:
            DataFrame: Patient summary
        """
        patient_data = df[df['patient_id'] == patient_id]
        
        if len(patient_data) == 0:
            return pd.DataFrame()
        
        summary_data = []
        
        for test_name in patient_data['test_name'].unique():
            test_data = patient_data[patient_data['test_name'] == test_name]
            
            summary_data.append({
                'Test Name': test_name,
                'Count': len(test_data),
                'Latest Value': test_data['test_value'].iloc[-1],
                'Mean': test_data['test_value'].mean(),
                'Trend': self._calculate_trend(test_data),
                'Abnormal Flags': len(test_data[test_data['test_flag'].isin(['H', 'L'])])
            })
        
        return pd.DataFrame(summary_data)
    
    def _calculate_trend(self, test_data):
        """Helper method to calculate trend"""
        if len(test_data) < 2:
            return 'N/A'
        
        test_data = test_data.sort_values('sample_lab_admission_time')
        first = test_data['test_value'].iloc[0]
        last = test_data['test_value'].iloc[-1]
        
        if last > first * 1.1:
            return 'Increasing'
        elif last < first * 0.9:
            return 'Decreasing'
        else:
            return 'Stable'
    
    def identify_outliers(self, df, method='iqr'):
        """
        Identify outlier values using various methods
        
        Args:
            df: Input DataFrame
            method: Method to use ('iqr', 'zscore')
            
        Returns:
            DataFrame: Outlier values
        """
        if method == 'iqr':
            outliers = []
            
            for test_name in df['test_name'].unique():
                test_data = df[df['test_name'] == test_name]
                
                Q1 = test_data['test_value'].quantile(0.25)
                Q3 = test_data['test_value'].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                test_outliers = test_data[
                    (test_data['test_value'] < lower_bound) | 
                    (test_data['test_value'] > upper_bound)
                ]
                
                if len(test_outliers) > 0:
                    outliers.append(test_outliers)
            
            if outliers:
                return pd.concat(outliers)
            else:
                return pd.DataFrame()
        
        elif method == 'zscore':
            outliers = []
            
            for test_name in df['test_name'].unique():
                test_data = df[df['test_name'] == test_name].copy()
                
                z_scores = np.abs((test_data['test_value'] - test_data['test_value'].mean()) / 
                                 test_data['test_value'].std())
                
                test_outliers = test_data[z_scores > 3]
                
                if len(test_outliers) > 0:
                    outliers.append(test_outliers)
            
            if outliers:
                return pd.concat(outliers)
            else:
                return pd.DataFrame()

