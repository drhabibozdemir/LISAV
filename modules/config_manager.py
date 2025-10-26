"""
Configuration Manager Module for LIS
Handles dictionary configuration management
"""
import pandas as pd
import streamlit as st
import os
from typing import Dict, List, Any, Optional

class ConfigManager:
    """Manages laboratory test configuration dictionary"""
    
    def __init__(self):
        # Try different possible paths for the dictionary file (prioritize Excel)
        possible_paths = [
            "data/dictionary/dictionary_v14.0.0.xlsx",
            "data/dictionary/dictionary_v14.0.0.csv",
            "../../data/dictionary/dictionary_v14.0.0.xlsx",
            "../../data/dictionary/dictionary_v14.0.0.csv",
            "../data/dictionary/dictionary_v14.0.0.xlsx",
            "../data/dictionary/dictionary_v14.0.0.csv",
            "../../../data/dictionary/dictionary_v14.0.0.xlsx",
            "../../../data/dictionary/dictionary_v14.0.0.csv"
        ]
        
        self.dictionary_path = None
        for path in possible_paths:
            if os.path.exists(path):
                self.dictionary_path = path
                break
        
        if self.dictionary_path is None:
            self.dictionary_path = possible_paths[0]  # Default fallback
        
        self.config_data = None
        self.boolean_columns = ['hemolysis', 'icterus', 'lipemia', 'IQC', 'EQC', 'analyzer_flag']
        self.numeric_columns = ['ref_min', 'ref_max', 'delta_check_min', 'delta_check_max', 
                               'critical_min', 'critical_max', 'delta_check_interval']
    
    def _load_file(self, file_path: str) -> pd.DataFrame:
        """Load file based on extension (Excel or CSV)"""
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        else:
            return pd.read_csv(file_path, sep=';')
        
    def load_dictionary(self) -> pd.DataFrame:
        """Load dictionary from Excel or CSV file with enhanced error handling"""
        try:
            # Try to load from the specified path
            if os.path.exists(self.dictionary_path):
                df = self._load_file(self.dictionary_path)
            else:
                # Try alternative paths
                alternative_paths = [
                    "../../data/dictionary/dictionary_v14.0.0.xlsx",
                    "../../data/dictionary/dictionary_v14.0.0.csv",
                    "../data/dictionary/dictionary_v14.0.0.xlsx",
                    "../data/dictionary/dictionary_v14.0.0.csv",
                    "../../../data/dictionary/dictionary_v14.0.0.xlsx",
                    "../../../data/dictionary/dictionary_v14.0.0.csv"
                ]
                
                df = None
                for alt_path in alternative_paths:
                    if os.path.exists(alt_path):
                        df = self._load_file(alt_path)
                        self.dictionary_path = alt_path
                        break
                
                if df is None:
                    st.error(f"Dictionary file not found. Tried paths: {self.dictionary_path} and alternatives")
                    return None
            
            # Clean the data
            df = df.dropna(how='all')  # Remove empty rows
            
            # Validate that we have data
            if len(df) == 0:
                st.error("Dictionary file is empty")
                return None
            
            # Convert boolean columns to proper format
            for col in self.boolean_columns:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
                    df[col] = df[col].replace({'1': True, '0': False, 'True': True, 'False': False}).infer_objects(copy=False)
            
            # Convert numeric columns
            for col in self.numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            self.config_data = df
            return df
            
        except FileNotFoundError as e:
            st.error(f"Dictionary file not found: {e}")
            return None
        except pd.errors.EmptyDataError:
            st.error("Dictionary file is empty")
            return None
        except pd.errors.ParserError as e:
            st.error(f"Error parsing dictionary file: {e}")
            return None
        except Exception as e:
            st.error(f"Unexpected error loading dictionary: {str(e)}")
            return None
    
    def get_config_data(self) -> pd.DataFrame:
        """Get current configuration data"""
        if self.config_data is None:
            return self.load_dictionary()
        return self.config_data
    
    def save_config_data(self, df: pd.DataFrame) -> bool:
        """Save configuration data to Excel or CSV file"""
        try:
            # Convert boolean values back to 0/1 for saving
            df_to_save = df.copy()
            for col in self.boolean_columns:
                if col in df_to_save.columns:
                    df_to_save[col] = df_to_save[col].astype(int)
            
            # Save to file based on extension
            if self.dictionary_path.endswith('.xlsx') or self.dictionary_path.endswith('.xls'):
                df_to_save.to_excel(self.dictionary_path, index=False)
            else:
                df_to_save.to_csv(self.dictionary_path, sep=';', index=False)
            
            self.config_data = df
            return True
        except Exception as e:
            st.error(f"Error saving configuration: {str(e)}")
            return False
    
    def export_excel(self, df: pd.DataFrame) -> bytes:
        """Export configuration to Excel bytes"""
        try:
            df_to_export = df.copy()
            for col in self.boolean_columns:
                if col in df_to_export.columns:
                    df_to_export[col] = df_to_export[col].astype(int)
            
            # Create Excel file in memory
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_to_export.to_excel(writer, index=False, sheet_name='Dictionary')
            output.seek(0)
            return output.getvalue()
        except Exception as e:
            st.error(f"Error exporting to Excel: {str(e)}")
            return b""
    
    def export_config(self, df: pd.DataFrame, filename: str = "dictionary_config.csv") -> str:
        """Export configuration to CSV string"""
        try:
            df_to_export = df.copy()
            for col in self.boolean_columns:
                if col in df_to_export.columns:
                    df_to_export[col] = df_to_export[col].astype(int)
            
            return df_to_export.to_csv(index=False, sep=';')
        except Exception as e:
            st.error(f"Error exporting configuration: {str(e)}")
            return ""
    
    def import_config(self, uploaded_file) -> pd.DataFrame:
        """Import configuration from uploaded Excel or CSV file"""
        try:
            # Determine file type and load accordingly
            if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file, sep=';')
            
            # Clean the data
            df = df.dropna(how='all')
            
            # Convert boolean columns
            for col in self.boolean_columns:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
                    df[col] = df[col].replace({'1': True, '0': False, 'True': True, 'False': False}).infer_objects(copy=False)
            
            # Convert numeric columns
            for col in self.numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            self.config_data = df
            return df
            
        except Exception as e:
            st.error(f"Error importing configuration: {str(e)}")
            return None
    
    def get_column_info(self) -> Dict[str, Dict[str, Any]]:
        """Get column information for UI rendering"""
        return {
            'test': {'type': 'text', 'editable': True, 'description': 'Test Name'},
            'age': {'type': 'text', 'editable': True, 'description': 'Age Group'},
            'hemolysis': {'type': 'checkbox', 'editable': True, 'description': 'Hemolysis Flag'},
            'icterus': {'type': 'checkbox', 'editable': True, 'description': 'Icterus Flag'},
            'lipemia': {'type': 'checkbox', 'editable': True, 'description': 'Lipemia Flag'},
            'IQC': {'type': 'checkbox', 'editable': True, 'description': 'Internal Quality Control'},
            'EQC': {'type': 'checkbox', 'editable': True, 'description': 'External Quality Control'},
            'ref_min': {'type': 'number', 'editable': True, 'description': 'Reference Minimum'},
            'ref_max': {'type': 'number', 'editable': True, 'description': 'Reference Maximum'},
            'delta_check_min': {'type': 'number', 'editable': True, 'description': 'Delta Check Minimum'},
            'delta_check_max': {'type': 'number', 'editable': True, 'description': 'Delta Check Maximum'},
            'analyzer_flag': {'type': 'checkbox', 'editable': True, 'description': 'Analyzer Flag'},
            'units': {'type': 'text', 'editable': True, 'description': 'Units'},
            'critical_min': {'type': 'number', 'editable': True, 'description': 'Critical Minimum'},
            'critical_max': {'type': 'number', 'editable': True, 'description': 'Critical Maximum'},
            'delta_check_interval': {'type': 'number', 'editable': True, 'description': 'Delta Check Interval'}
        }
