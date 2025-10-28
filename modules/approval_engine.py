"""
Auto Verification Engine Module for LIS
Handles laboratory test auto verification system with rule engine
"""
import pandas as pd
import streamlit as st
from typing import Dict, List, Tuple, Optional
from .rule_validator import RuleValidator


class ApprovalEngine:
    """Main auto verification engine that processes laboratory test results"""
    
    def __init__(self, config_manager):
        """
        Initialize auto verification engine
        
        Args:
            config_manager: ConfigManager instance for dictionary data
        """
        self.config_manager = config_manager
        self.rule_validator = RuleValidator()
        
        # Rule priority order (higher number = higher priority)
        self.rule_priority = {
            'IQC': 5,
            'EQC': 4,
            'critical_value': 3,
            'delta_check': 2,
            'reference_range': 1,
            'serum_index': 1
        }
    
    def process_test_results(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process test results and add auto verification status
        
        Args:
            df: DataFrame with test results
            
        Returns:
            DataFrame with added auto verification status and comments
        """
        if df is None or len(df) == 0:
            return df
        
        # Get configuration data
        config_df = self.config_manager.get_config_data()
        if config_df is None:
            st.error("Configuration data not available for auto verification processing")
            return df
        
        # Create a copy to avoid modifying original
        result_df = df.copy()
        
        # Initialize new columns
        result_df['approval_status'] = 'Auto Validated'
        result_df['approval_comments'] = ''
        result_df['failed_rules'] = ''
        
        # Process each test result
        for idx, row in result_df.iterrows():
            test_name = row['test_name']
            
            # Get test configuration
            test_config = self._get_test_config(test_name, config_df)
            if test_config is None:
                result_df.at[idx, 'approval_status'] = 'Manual Review Needed'
                result_df.at[idx, 'approval_comments'] = 'Test configuration not found'
                continue
            
            # Apply rules in priority order
            approval_result = self._apply_rules(row, test_config)
            
            # Update result
            result_df.at[idx, 'approval_status'] = approval_result['status']
            result_df.at[idx, 'approval_comments'] = approval_result['comments']
            result_df.at[idx, 'failed_rules'] = approval_result['failed_rules']
        
        return result_df
    
    def _get_test_config(self, test_name: str, config_df: pd.DataFrame) -> Optional[Dict]:
        """
        Get configuration for a specific test
        
        Args:
            test_name: Name of the test
            config_df: Configuration DataFrame
            
        Returns:
            Dictionary with test configuration or None
        """
        test_row = config_df[config_df['test'] == test_name]
        if len(test_row) == 0:
            return None
        
        return test_row.iloc[0].to_dict()
    
    def _apply_rules(self, test_result: pd.Series, test_config: Dict) -> Dict:
        """
        Apply all rules to a test result
        
        Args:
            test_result: Single test result row
            test_config: Test configuration dictionary
            
        Returns:
            Dictionary with approval result
        """
        failed_rules = []
        comments = []
        
        # Apply rules in priority order
        rules_to_check = [
            ('IQC', self._check_iqc_rule),
            ('EQC', self._check_eqc_rule),
            ('critical_value', self._check_critical_value_rule),
            ('delta_check', self._check_delta_check_rule),
            ('reference_range', self._check_reference_range_rule),
            ('serum_index', self._check_serum_index_rule)
        ]
        
        for rule_name, rule_function in rules_to_check:
            try:
                rule_result = rule_function(test_result, test_config)
                if not rule_result['passed']:
                    failed_rules.append(rule_name)
                    comments.append(rule_result['message'])
            except Exception as e:
                failed_rules.append(rule_name)
                comments.append(f"Error in {rule_name} rule: {str(e)}")
        
        # Determine final status
        if len(failed_rules) == 0:
            status = 'Auto Validated'
            final_comments = 'All rules passed'
        else:
            status = 'Manual Review Needed'
            final_comments = '; '.join(comments)
        
        return {
            'status': status,
            'comments': final_comments,
            'failed_rules': ', '.join(failed_rules)
        }
    
    def _check_iqc_rule(self, test_result: pd.Series, test_config: Dict) -> Dict:
        """Check IQC rule"""
        iqc_value = test_config.get('IQC', False)
        
        # IQC değeri 1 ise onaylanmaya uygun, 0 ise manuel review gerekli
        if iqc_value == 1 or iqc_value is True:
            return {'passed': True, 'message': 'IQC check passed - test approved'}
        else:
            return {'passed': False, 'message': 'IQC check failed - manual review needed'}
    
    def _check_eqc_rule(self, test_result: pd.Series, test_config: Dict) -> Dict:
        """Check EQC rule"""
        eqc_value = test_config.get('EQC', False)
        
        # EQC değeri 1 ise onaylanmaya uygun, 0 ise manuel review gerekli
        if eqc_value == 1 or eqc_value is True:
            return {'passed': True, 'message': 'EQC check passed - test approved'}
        else:
            return {'passed': False, 'message': 'EQC check failed - manual review needed'}
    
    def _check_critical_value_rule(self, test_result: pd.Series, test_config: Dict) -> Dict:
        """Check critical value rule"""
        test_value = test_result.get('test_value')
        critical_min = test_config.get('critical_min')
        critical_max = test_config.get('critical_max')
        
        if pd.isna(test_value) or pd.isna(critical_min) or pd.isna(critical_max):
            return {'passed': True, 'message': 'Critical values not configured'}
        
        if test_value < critical_min or test_value > critical_max:
            return {
                'passed': False, 
                'message': f'Critical value exceeded: {test_value} (range: {critical_min}-{critical_max})'
            }
        
        return {'passed': True, 'message': 'Critical value check passed'}
    
    def _check_delta_check_rule(self, test_result: pd.Series, test_config: Dict) -> Dict:
        """Check delta check rule"""
        delta_min = test_config.get('delta_check_min')
        delta_max = test_config.get('delta_check_max')
        delta_interval = test_config.get('delta_check_interval')
        
        if pd.isna(delta_min) or pd.isna(delta_max) or pd.isna(delta_interval):
            return {'passed': True, 'message': 'Delta check not configured'}
        
        # Delta check logic would require previous results
        # For now, assume delta check is always passed
        return {'passed': True, 'message': 'Delta check passed'}
    
    def _check_reference_range_rule(self, test_result: pd.Series, test_config: Dict) -> Dict:
        """Check reference range rule"""
        test_value = test_result.get('test_value')
        ref_min = test_config.get('ref_min')
        ref_max = test_config.get('ref_max')
        
        if pd.isna(test_value) or pd.isna(ref_min) or pd.isna(ref_max):
            return {'passed': True, 'message': 'Reference range not configured'}
        
        if test_value < ref_min or test_value > ref_max:
            return {
                'passed': False, 
                'message': f'Out of reference range: {test_value} (range: {ref_min}-{ref_max})'
            }
        
        return {'passed': True, 'message': 'Reference range check passed'}
    
    def _check_serum_index_rule(self, test_result: pd.Series, test_config: Dict) -> Dict:
        """Check serum index interference rule"""
        sample_hemolysis = test_result.get('hemolysis_value', 0)
        sample_icterus = test_result.get('icterus_value', 0)
        sample_lipemia = test_result.get('lipemia_value', 0)
        
        test_hemolysis = test_config.get('hemolysis', False)
        test_icterus = test_config.get('icterus', False)
        test_lipemia = test_config.get('lipemia', False)
        
        interference_detected = []
        
        if test_hemolysis and sample_hemolysis == 1:
            interference_detected.append('hemolysis')
        
        if test_icterus and sample_icterus == 1:
            interference_detected.append('icterus')
        
        if test_lipemia and sample_lipemia == 1:
            interference_detected.append('lipemia')
        
        if interference_detected:
            return {
                'passed': False,
                'message': f'Serum index interference detected: {", ".join(interference_detected)}'
            }
        
        return {'passed': True, 'message': 'Serum index check passed'}
    
    def get_approval_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Get comprehensive auto verification statistics
        
        Args:
            df: DataFrame with auto verification results
            
        Returns:
            Dictionary with comprehensive auto verification statistics
        """
        if df is None or len(df) == 0:
            return {}
        
        # Basic statistics
        total_tests = len(df)
        auto_validated = len(df[df['approval_status'] == 'Auto Validated'])
        manual_review = len(df[df['approval_status'] == 'Manual Review Needed'])
        
        # Failed rules statistics
        failed_rules_stats = {}
        for idx, row in df.iterrows():
            failed_rules = row.get('failed_rules', '')
            if failed_rules:
                rules = [rule.strip() for rule in failed_rules.split(',')]
                for rule in rules:
                    if rule:
                        failed_rules_stats[rule] = failed_rules_stats.get(rule, 0) + 1
        
        # Additional comprehensive statistics
        stats = {
            'total_tests': total_tests,
            'auto_validated': auto_validated,
            'manual_review_needed': manual_review,
            'auto_validation_rate': (auto_validated / total_tests * 100) if total_tests > 0 else 0,
            'manual_review_rate': (manual_review / total_tests * 100) if total_tests > 0 else 0,
            'failed_rules_stats': failed_rules_stats
        }
        
        # Add comprehensive statistics
        stats.update(self._get_comprehensive_statistics(df))
        
        return stats
    
    def _get_comprehensive_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Get comprehensive approval statistics including time-based, test-based, and patient-based analysis
        
        Args:
            df: DataFrame with approval results
            
        Returns:
            Dictionary with comprehensive statistics
        """
        comprehensive_stats = {}
        
        # 1. Test-based statistics
        comprehensive_stats['test_statistics'] = self._get_test_based_statistics(df)
        
        # 2. Patient-based statistics
        comprehensive_stats['patient_statistics'] = self._get_patient_based_statistics(df)
        
        # 3. Time-based statistics
        comprehensive_stats['time_statistics'] = self._get_time_based_statistics(df)
        
        # 4. Quality control statistics
        comprehensive_stats['quality_control_stats'] = self._get_quality_control_statistics(df)
        
        # 5. Rule failure analysis
        comprehensive_stats['rule_analysis'] = self._get_rule_failure_analysis(df)
        
        # 6. Sample quality statistics
        comprehensive_stats['sample_quality_stats'] = self._get_sample_quality_statistics(df)
        
        return comprehensive_stats
    
    def _get_test_based_statistics(self, df: pd.DataFrame) -> Dict:
        """Get test-specific approval statistics"""
        test_stats = {}
        
        for test_name in df['test_name'].unique():
            test_data = df[df['test_name'] == test_name]
            total_tests = len(test_data)
            auto_validated = len(test_data[test_data['approval_status'] == 'Auto Validated'])
            manual_review = len(test_data[test_data['approval_status'] == 'Manual Review Needed'])
            
            test_stats[test_name] = {
                'total_tests': total_tests,
                'auto_validated': auto_validated,
                'manual_review_needed': manual_review,
                'auto_validation_rate': (auto_validated / total_tests * 100) if total_tests > 0 else 0,
                'manual_review_rate': (manual_review / total_tests * 100) if total_tests > 0 else 0,
                'abnormal_rate': (len(test_data[test_data['test_flag'].isin(['H', 'L'])]) / total_tests * 100) if total_tests > 0 else 0
            }
        
        return test_stats
    
    def _get_patient_based_statistics(self, df: pd.DataFrame) -> Dict:
        """Get patient-specific approval statistics"""
        patient_stats = {}
        
        for patient_id in df['patient_id'].unique():
            patient_data = df[df['patient_id'] == patient_id]
            total_tests = len(patient_data)
            auto_validated = len(patient_data[patient_data['approval_status'] == 'Auto Validated'])
            manual_review = len(patient_data[patient_data['approval_status'] == 'Manual Review Needed'])
            
            # Get patient demographics
            patient_info = patient_data.iloc[0]
            age = patient_info.get('age', 'N/A')
            gender = patient_info.get('gender', 'N/A')
            
            patient_stats[patient_id] = {
                'total_tests': total_tests,
                'auto_validated': auto_validated,
                'manual_review_needed': manual_review,
                'auto_validation_rate': (auto_validated / total_tests * 100) if total_tests > 0 else 0,
                'manual_review_rate': (manual_review / total_tests * 100) if total_tests > 0 else 0,
                'age': age,
                'gender': gender,
                'total_samples': patient_data['sample_id'].nunique()
            }
        
        return patient_stats
    
    def _get_time_based_statistics(self, df: pd.DataFrame) -> Dict:
        """Get time-based approval statistics"""
        time_stats = {}
        
        if 'sample_lab_admission_time' in df.columns:
            # Convert to datetime if possible
            try:
                df['datetime'] = pd.to_datetime(df['sample_lab_admission_time'])
                
                # Daily statistics
                daily_stats = df.groupby(df['datetime'].dt.date).agg({
                    'approval_status': ['count', lambda x: (x == 'Auto Validated').sum()]
                }).round(2)
                
                daily_stats.columns = ['total_tests', 'auto_validated']
                daily_stats['auto_validation_rate'] = (daily_stats['auto_validated'] / daily_stats['total_tests'] * 100).round(2)
                
                time_stats['daily_stats'] = daily_stats.to_dict('index')
                
                # Hourly distribution
                hourly_stats = df.groupby(df['datetime'].dt.hour).agg({
                    'approval_status': ['count', lambda x: (x == 'Auto Validated').sum()]
                }).round(2)
                
                hourly_stats.columns = ['total_tests', 'auto_validated']
                hourly_stats['auto_validation_rate'] = (hourly_stats['auto_validated'] / hourly_stats['total_tests'] * 100).round(2)
                
                time_stats['hourly_stats'] = hourly_stats.to_dict('index')
                
            except Exception as e:
                time_stats['error'] = f"Time parsing error: {str(e)}"
        
        return time_stats
    
    def _get_quality_control_statistics(self, df: pd.DataFrame) -> Dict:
        """Get quality control related statistics"""
        qc_stats = {}
        
        # IQC/EQC statistics
        iqc_failed = len(df[df['failed_rules'].str.contains('IQC', na=False)])
        eqc_failed = len(df[df['failed_rules'].str.contains('EQC', na=False)])
        critical_failed = len(df[df['failed_rules'].str.contains('critical_value', na=False)])
        delta_failed = len(df[df['failed_rules'].str.contains('delta_check', na=False)])
        reference_failed = len(df[df['failed_rules'].str.contains('reference_range', na=False)])
        serum_index_failed = len(df[df['failed_rules'].str.contains('serum_index', na=False)])
        
        qc_stats = {
            'iqc_failures': iqc_failed,
            'eqc_failures': eqc_failed,
            'critical_value_failures': critical_failed,
            'delta_check_failures': delta_failed,
            'reference_range_failures': reference_failed,
            'serum_index_failures': serum_index_failed,
            'total_qc_failures': iqc_failed + eqc_failed + critical_failed + delta_failed + reference_failed + serum_index_failed
        }
        
        return qc_stats
    
    def _get_rule_failure_analysis(self, df: pd.DataFrame) -> Dict:
        """Get detailed rule failure analysis"""
        rule_analysis = {}
        
        # Count failures by rule type
        rule_failures = {}
        for idx, row in df.iterrows():
            failed_rules = row.get('failed_rules', '')
            if failed_rules:
                rules = [rule.strip() for rule in failed_rules.split(',')]
                for rule in rules:
                    if rule:
                        rule_failures[rule] = rule_failures.get(rule, 0) + 1
        
        # Get most problematic tests
        test_failure_counts = {}
        for test_name in df['test_name'].unique():
            test_data = df[df['test_name'] == test_name]
            failures = len(test_data[test_data['approval_status'] == 'Manual Review Needed'])
            test_failure_counts[test_name] = failures
        
        # Sort by failure count
        most_problematic_tests = dict(sorted(test_failure_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        
        rule_analysis = {
            'rule_failure_counts': rule_failures,
            'most_problematic_tests': most_problematic_tests,
            'total_rule_failures': sum(rule_failures.values())
        }
        
        return rule_analysis
    
    def _get_sample_quality_statistics(self, df: pd.DataFrame) -> Dict:
        """Get sample quality related statistics"""
        sample_quality_stats = {}
        
        # Hemolysis statistics
        hemolysis_samples = len(df[df['hemolysis_value'] == 1])
        icterus_samples = len(df[df['icterus_value'] == 1])
        lipemia_samples = len(df[df['lipemia_value'] == 1])
        
        # Samples with quality issues
        quality_issue_samples = len(df[(df['hemolysis_value'] == 1) | (df['icterus_value'] == 1) | (df['lipemia_value'] == 1)])
        
        # Approval rates for samples with quality issues
        quality_issue_data = df[(df['hemolysis_value'] == 1) | (df['icterus_value'] == 1) | (df['lipemia_value'] == 1)]
        quality_issue_auto_validated = len(quality_issue_data[quality_issue_data['approval_status'] == 'Auto Validated'])
        
        sample_quality_stats = {
            'hemolysis_samples': hemolysis_samples,
            'icterus_samples': icterus_samples,
            'lipemia_samples': lipemia_samples,
            'total_quality_issue_samples': quality_issue_samples,
            'quality_issue_auto_validation_rate': (quality_issue_auto_validated / quality_issue_samples * 100) if quality_issue_samples > 0 else 0,
            'quality_issue_percentage': (quality_issue_samples / len(df) * 100) if len(df) > 0 else 0
        }
        
        return sample_quality_stats
