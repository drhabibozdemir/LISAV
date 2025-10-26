"""
Data Loader Module
Handles loading CSV files and sample data
"""
import pandas as pd
import os
import streamlit as st
from pathlib import Path


class DataLoader:
    """Class for loading laboratory data from CSV files"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
    
    def load_csv(self, file_path):
        """
        Load data from CSV file with enhanced error handling
        
        Args:
            file_path: Path to CSV file or file-like object
            
        Returns:
            DataFrame: Loaded data as pandas DataFrame
            
        Raises:
            ValueError: If file format is invalid or data is malformed
            FileNotFoundError: If file path is invalid
        """
        try:
            # If file_path is a file-like object (uploaded file)
            if hasattr(file_path, 'read'):
                df = pd.read_csv(file_path)
            else:
                # If it's a string path
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")
                df = pd.read_csv(file_path)
            
            # Validate data structure
            self.validate_data(df)
            
            # Parse datetime with error handling
            if 'sample_lab_admission_time' in df.columns:
                try:
                    df['sample_lab_admission_time'] = pd.to_datetime(df['sample_lab_admission_time'])
                except Exception as e:
                    st.warning(f"Warning: Could not parse datetime column: {e}")
            
            return df
            
        except pd.errors.EmptyDataError:
            raise ValueError("The uploaded file is empty")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing CSV file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading file: {e}")
    
    def load_sample_data(self):
        """
        Load sample data from the project directory with enhanced error handling
        
        Returns:
            DataFrame: Sample data as pandas DataFrame
            
        Raises:
            FileNotFoundError: If sample data file is not found
            ValueError: If sample data is malformed
        """
        # Try multiple possible paths (deployment-friendly)
        possible_paths = [
            Path(__file__).parent.parent / 'data' / "v1.1.0" / 'synthetic_patient_data_v1.1.0.csv',
            self.base_path / 'data' / "v1.1.0" / 'synthetic_patient_data_v1.1.0.csv',
            Path('data') / "v1.1.0" / 'synthetic_patient_data_v1.1.0.csv',
            self.base_path.parent / 'data' / "v1.1.0" / 'synthetic_patient_data_v1.1.0.csv',
            self.base_path.parent.parent / 'data' / "v1.1.0" / 'synthetic_patient_data_v1.1.0.csv',
        ]
        
        sample_path = None
        for path in possible_paths:
            if path.exists():
                sample_path = path
                break
        
        if sample_path is None:
            # If no file found, raise informative error
            raise FileNotFoundError(
                f"Sample data file not found. Tried paths: {[str(p) for p in possible_paths]}"
            )
        
        try:
            df = pd.read_csv(sample_path)
            
            # Validate data structure
            self.validate_data(df)
            
            # Parse datetime with error handling
            if 'sample_lab_admission_time' in df.columns:
                try:
                    df['sample_lab_admission_time'] = pd.to_datetime(df['sample_lab_admission_time'])
                except Exception as e:
                    st.warning(f"Warning: Could not parse datetime column: {e}")
            
            return df
            
        except pd.errors.EmptyDataError:
            raise ValueError("Sample data file is empty")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing sample data file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading sample data: {e}")
    
    def validate_data(self, df):
        """
        Validate that the loaded data has required columns
        
        Args:
            df: DataFrame to validate
            
        Returns:
            bool: True if data is valid
        """
        required_columns = [
            'patient_id',
            'sample_id',
            'test_name',
            'test_value',
            'test_flag',
            'reference_min',
            'reference_max'
        ]
        
        missing_columns = set(required_columns) - set(df.columns)
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        return True

