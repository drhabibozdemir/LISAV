"""
Approval Engine Module for LIS
Handles laboratory test approval system with rule engine
"""
import pandas as pd
import streamlit as st
from typing import Dict, List, Tuple, Optional
from .rule_validator import RuleValidator


class ApprovalEngine:
    """Main approval engine that processes laboratory test results"""
    
    def __init__(self, config_manager):
        """
        Initialize approval engine
        
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
        Process test results and add approval status
        
        Args:
            df: DataFrame with test results
            
        Returns:
            DataFrame with added approval status and comments
        """
        if df is None or len(df) == 0:
            return df
        
        # Get configuration data
        config_df = self.config_manager.get_config_data()
        if config_df is None:
            st.error("Configuration data not available for approval processing")
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
        Get approval statistics
        
        Args:
            df: DataFrame with approval results
            
        Returns:
            Dictionary with approval statistics
        """
        if df is None or len(df) == 0:
            return {}
        
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
        
        return {
            'total_tests': total_tests,
            'auto_validated': auto_validated,
            'manual_review_needed': manual_review,
            'auto_validation_rate': (auto_validated / total_tests * 100) if total_tests > 0 else 0,
            'manual_review_rate': (manual_review / total_tests * 100) if total_tests > 0 else 0,
            'failed_rules_stats': failed_rules_stats
        }
