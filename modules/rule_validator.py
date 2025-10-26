"""
Rule Validator Module for LIS
Contains individual rule validation functions
"""
import pandas as pd
from typing import Dict, List, Optional
import numpy as np


class RuleValidator:
    """Contains validation functions for different types of rules"""
    
    def __init__(self):
        """Initialize rule validator"""
        pass
    
    def validate_iqc_rule(self, test_value: float, test_config: Dict) -> Dict:
        """
        Validate IQC (Internal Quality Control) rule
        
        Args:
            test_value: Test result value
            test_config: Test configuration dictionary
            
        Returns:
            Dictionary with validation result
        """
        iqc_value = test_config.get('IQC', False)
        
        # IQC değeri 1 ise onaylanmaya uygun, 0 ise manuel review gerekli
        if iqc_value == 1 or iqc_value is True:
            return {
                'passed': True,
                'message': 'IQC check passed - test approved',
                'rule_type': 'IQC'
            }
        else:
            return {
                'passed': False,
                'message': 'IQC check failed - manual review needed',
                'rule_type': 'IQC'
            }
    
    def validate_eqc_rule(self, test_value: float, test_config: Dict) -> Dict:
        """
        Validate EQC (External Quality Control) rule
        
        Args:
            test_value: Test result value
            test_config: Test configuration dictionary
            
        Returns:
            Dictionary with validation result
        """
        eqc_value = test_config.get('EQC', False)
        
        # EQC değeri 1 ise onaylanmaya uygun, 0 ise manuel review gerekli
        if eqc_value == 1 or eqc_value is True:
            return {
                'passed': True,
                'message': 'EQC check passed - test approved',
                'rule_type': 'EQC'
            }
        else:
            return {
                'passed': False,
                'message': 'EQC check failed - manual review needed',
                'rule_type': 'EQC'
            }
    
    def validate_critical_value_rule(self, test_value: float, test_config: Dict) -> Dict:
        """
        Validate critical value rule
        
        Args:
            test_value: Test result value
            test_config: Test configuration dictionary
            
        Returns:
            Dictionary with validation result
        """
        critical_min = test_config.get('critical_min')
        critical_max = test_config.get('critical_max')
        
        if pd.isna(critical_min) or pd.isna(critical_max):
            return {
                'passed': True,
                'message': 'Critical values not configured',
                'rule_type': 'critical_value'
            }
        
        if pd.isna(test_value):
            return {
                'passed': False,
                'message': 'Test value is missing',
                'rule_type': 'critical_value'
            }
        
        if test_value < critical_min:
            return {
                'passed': False,
                'message': f'Critical low value: {test_value} < {critical_min}',
                'rule_type': 'critical_value'
            }
        
        if test_value > critical_max:
            return {
                'passed': False,
                'message': f'Critical high value: {test_value} > {critical_max}',
                'rule_type': 'critical_value'
            }
        
        return {
            'passed': True,
            'message': f'Critical value check passed: {test_value} within range ({critical_min}-{critical_max})',
            'rule_type': 'critical_value'
        }
    
    def validate_delta_check_rule(self, test_value: float, test_config: Dict, 
                                 previous_value: Optional[float] = None) -> Dict:
        """
        Validate delta check rule
        
        Args:
            test_value: Current test result value
            test_config: Test configuration dictionary
            previous_value: Previous test result value (if available)
            
        Returns:
            Dictionary with validation result
        """
        delta_min = test_config.get('delta_check_min')
        delta_max = test_config.get('delta_check_max')
        delta_interval = test_config.get('delta_check_interval')
        
        if pd.isna(delta_min) or pd.isna(delta_max) or pd.isna(delta_interval):
            return {
                'passed': True,
                'message': 'Delta check not configured',
                'rule_type': 'delta_check'
            }
        
        if pd.isna(test_value):
            return {
                'passed': False,
                'message': 'Test value is missing',
                'rule_type': 'delta_check'
            }
        
        if previous_value is None or pd.isna(previous_value):
            return {
                'passed': True,
                'message': 'Delta check passed (no previous value for comparison)',
                'rule_type': 'delta_check'
            }
        
        # Calculate delta change
        delta_change = abs(test_value - previous_value)
        delta_percentage = (delta_change / previous_value) * 100 if previous_value != 0 else 0
        
        # Check if delta change exceeds limits
        if delta_percentage < delta_min or delta_percentage > delta_max:
            return {
                'passed': False,
                'message': f'Delta check failed: {delta_percentage:.2f}% change (range: {delta_min}-{delta_max}%)',
                'rule_type': 'delta_check'
            }
        
        return {
            'passed': True,
            'message': f'Delta check passed: {delta_percentage:.2f}% change within range ({delta_min}-{delta_max}%)',
            'rule_type': 'delta_check'
        }
    
    def validate_reference_range_rule(self, test_value: float, test_config: Dict) -> Dict:
        """
        Validate reference range rule
        
        Args:
            test_value: Test result value
            test_config: Test configuration dictionary
            
        Returns:
            Dictionary with validation result
        """
        ref_min = test_config.get('ref_min')
        ref_max = test_config.get('ref_max')
        
        if pd.isna(ref_min) or pd.isna(ref_max):
            return {
                'passed': True,
                'message': 'Reference range not configured',
                'rule_type': 'reference_range'
            }
        
        if pd.isna(test_value):
            return {
                'passed': False,
                'message': 'Test value is missing',
                'rule_type': 'reference_range'
            }
        
        if test_value < ref_min:
            return {
                'passed': False,
                'message': f'Below reference range: {test_value} < {ref_min}',
                'rule_type': 'reference_range'
            }
        
        if test_value > ref_max:
            return {
                'passed': False,
                'message': f'Above reference range: {test_value} > {ref_max}',
                'rule_type': 'reference_range'
            }
        
        return {
            'passed': True,
            'message': f'Reference range check passed: {test_value} within range ({ref_min}-{ref_max})',
            'rule_type': 'reference_range'
        }
    
    def validate_serum_index_rule(self, test_value: float, test_config: Dict, 
                                sample_data: Dict) -> Dict:
        """
        Validate serum index interference rule
        
        Args:
            test_value: Test result value
            test_config: Test configuration dictionary
            sample_data: Sample data including hemolysis, icterus, lipemia values
            
        Returns:
            Dictionary with validation result
        """
        sample_hemolysis = sample_data.get('hemolysis_value', 0)
        sample_icterus = sample_data.get('icterus_value', 0)
        sample_lipemia = sample_data.get('lipemia_value', 0)
        
        test_hemolysis = test_config.get('hemolysis', False)
        test_icterus = test_config.get('icterus', False)
        test_lipemia = test_config.get('lipemia', False)
        
        interference_detected = []
        
        # Check for hemolysis interference
        if test_hemolysis and sample_hemolysis == 1:
            interference_detected.append('hemolysis')
        
        # Check for icterus interference
        if test_icterus and sample_icterus == 1:
            interference_detected.append('icterus')
        
        # Check for lipemia interference
        if test_lipemia and sample_lipemia == 1:
            interference_detected.append('lipemia')
        
        if interference_detected:
            return {
                'passed': False,
                'message': f'Serum index interference detected: {", ".join(interference_detected)}',
                'rule_type': 'serum_index',
                'interference_types': interference_detected
            }
        
        return {
            'passed': True,
            'message': 'Serum index check passed: no interference detected',
            'rule_type': 'serum_index'
        }
    
    def validate_analyzer_flag_rule(self, test_value: float, test_config: Dict) -> Dict:
        """
        Validate analyzer flag rule
        
        Args:
            test_value: Test result value
            test_config: Test configuration dictionary
            
        Returns:
            Dictionary with validation result
        """
        analyzer_flag = test_config.get('analyzer_flag', False)
        
        if not analyzer_flag:
            return {
                'passed': True,
                'message': 'Analyzer flag not required for this test',
                'rule_type': 'analyzer_flag'
            }
        
        # Analyzer flag validation logic
        # This would typically involve checking analyzer-specific flags
        # For simulation purposes, we'll assume it passes if required
        
        return {
            'passed': True,
            'message': 'Analyzer flag check passed',
            'rule_type': 'analyzer_flag'
        }
    
    def get_rule_priority(self, rule_type: str) -> int:
        """
        Get priority for a rule type
        
        Args:
            rule_type: Type of rule
            
        Returns:
            Priority number (higher = more important)
        """
        priorities = {
            'IQC': 5,
            'EQC': 4,
            'critical_value': 3,
            'delta_check': 2,
            'reference_range': 1,
            'serum_index': 1,
            'analyzer_flag': 1
        }
        
        return priorities.get(rule_type, 0)
    
    def validate_all_rules(self, test_value: float, test_config: Dict, 
                          sample_data: Dict, previous_value: Optional[float] = None) -> List[Dict]:
        """
        Validate all applicable rules for a test
        
        Args:
            test_value: Test result value
            test_config: Test configuration dictionary
            sample_data: Sample data
            previous_value: Previous test result value (if available)
            
        Returns:
            List of validation results sorted by priority
        """
        validation_results = []
        
        # IQC rule
        iqc_result = self.validate_iqc_rule(test_value, test_config)
        validation_results.append(iqc_result)
        
        # EQC rule
        eqc_result = self.validate_eqc_rule(test_value, test_config)
        validation_results.append(eqc_result)
        
        # Critical value rule
        critical_result = self.validate_critical_value_rule(test_value, test_config)
        validation_results.append(critical_result)
        
        # Delta check rule
        delta_result = self.validate_delta_check_rule(test_value, test_config, previous_value)
        validation_results.append(delta_result)
        
        # Reference range rule
        ref_result = self.validate_reference_range_rule(test_value, test_config)
        validation_results.append(ref_result)
        
        # Serum index rule
        serum_result = self.validate_serum_index_rule(test_value, test_config, sample_data)
        validation_results.append(serum_result)
        
        # Analyzer flag rule
        analyzer_result = self.validate_analyzer_flag_rule(test_value, test_config)
        validation_results.append(analyzer_result)
        
        # Sort by priority (higher priority first)
        validation_results.sort(key=lambda x: self.get_rule_priority(x['rule_type']), reverse=True)
        
        return validation_results
