"""
Data Visualizer Module
Handles creating visualizations for laboratory data
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


class DataVisualizer:
    """Class for creating visualizations from laboratory data"""
    
    def plot_test_distribution(self, df):
        """
        Plot distribution of test values
        
        Args:
            df: Input DataFrame
        """
        test_name = st.selectbox(
            "Select Test to Plot",
            options=sorted(df['test_name'].unique()),
            key="dist_test"
        )
        
        test_data = df[df['test_name'] == test_name]
        
        # Create histogram
        fig = px.histogram(
            test_data,
            x='test_value',
            nbins=30,
            title=f'Distribution of {test_name} Values',
            labels={'test_value': f'{test_name} Value', 'count': 'Frequency'}
        )
        
        # Add reference range lines
        if len(test_data) > 0:
            ref_min = test_data['reference_min'].iloc[0]
            ref_max = test_data['reference_max'].iloc[0]
            
            fig.add_vline(x=ref_min, line_dash="dash", line_color="green",
                         annotation_text=f"Min: {ref_min}")
            fig.add_vline(x=ref_max, line_dash="dash", line_color="red",
                         annotation_text=f"Max: {ref_max}")
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_patient_trend(self, df, patient_id):
        """
        Plot test trends for a specific patient
        
        Args:
            df: Input DataFrame
            patient_id: Patient ID
        """
        patient_data = df[df['patient_id'] == patient_id].copy()
        
        if len(patient_data) == 0:
            st.warning("No data available for this patient")
            return
        
        test_name = st.selectbox(
            "Select Test to Plot",
            options=sorted(patient_data['test_name'].unique()),
            key="trend_test"
        )
        
        test_data = patient_data[patient_data['test_name'] == test_name].copy()
        
        if 'sample_lab_admission_time' in test_data.columns:
            # Sort by date
            test_data = test_data.sort_values('sample_lab_admission_time')
            
            fig = go.Figure()
            
            # Plot test values over time
            fig.add_trace(go.Scatter(
                x=test_data['sample_lab_admission_time'],
                y=test_data['test_value'],
                mode='lines+markers',
                name='Test Value',
                marker=dict(color='blue', size=10)
            ))
            
            # Add reference range
            if len(test_data) > 0:
                ref_min = test_data['reference_min'].iloc[0]
                ref_max = test_data['reference_max'].iloc[0]
                
                fig.add_hline(y=ref_min, line_dash="dash", line_color="green",
                             annotation_text=f"Min: {ref_min}")
                fig.add_hline(y=ref_max, line_dash="dash", line_color="red",
                             annotation_text=f"Max: {ref_max}")
            
            fig.update_layout(
                title=f'{test_name} Trend for {patient_id}',
                xaxis_title='Date',
                yaxis_title='Value',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def plot_flag_analysis(self, df):
        """
        Plot analysis of test flags (Normal/High/Low)
        
        Args:
            df: Input DataFrame
        """
        # Create count of flags
        flag_counts = df['test_flag'].value_counts()
        
        # Create pie chart
        fig = px.pie(
            values=flag_counts.values,
            names=flag_counts.index,
            title='Distribution of Test Flags',
            color_discrete_map={'N': 'green', 'H': 'red', 'L': 'yellow'}
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed breakdown by test
        st.subheader("Flag Distribution by Test")
        
        flag_by_test = df.groupby(['test_name', 'test_flag']).size().reset_index(name='count')
        
        fig = px.bar(
            flag_by_test,
            x='test_name',
            y='count',
            color='test_flag',
            title='Flag Distribution by Test Type',
            color_discrete_map={'N': 'green', 'H': 'red', 'L': 'orange'}
        )
        
        fig.update_layout(height=500)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_time_series(self, df, test_name):
        """
        Plot time series for a specific test
        
        Args:
            df: Input DataFrame
            test_name: Test name
        """
        test_data = df[df['test_name'] == test_name].copy()
        
        if 'sample_lab_admission_time' not in test_data.columns:
            st.warning("No time data available")
            return
        
        test_data = test_data.sort_values('sample_lab_admission_time')
        test_data['sample_lab_admission_time'] = pd.to_datetime(test_data['sample_lab_admission_time'])
        
        # Group by date and calculate average
        daily_avg = test_data.groupby(test_data['sample_lab_admission_time'].dt.date)['test_value'].mean()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_avg.index,
            y=daily_avg.values,
            mode='lines+markers',
            name='Average Value',
            line=dict(color='blue', width=2)
        ))
        
        # Add reference range
        if len(test_data) > 0:
            ref_min = test_data['reference_min'].iloc[0]
            ref_max = test_data['reference_max'].iloc[0]
            
            fig.add_hline(y=ref_min, line_dash="dash", line_color="green",
                         annotation_text=f"Min: {ref_min}")
            fig.add_hline(y=ref_max, line_dash="dash", line_color="red",
                         annotation_text=f"Max: {ref_max}")
        
        fig.update_layout(
            title=f'{test_name} Time Series',
            xaxis_title='Date',
            yaxis_title='Average Value',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_correlation_matrix(self, df):
        """
        Plot correlation matrix for selected tests
        
        Args:
            df: Input DataFrame
        """
        st.subheader("Test Value Correlation Analysis")
        
        # Select tests for correlation
        selected_tests = st.multiselect(
            "Select Tests for Correlation",
            options=sorted(df['test_name'].unique()),
            default=sorted(df['test_name'].unique())[:5]
        )
        
        if len(selected_tests) < 2:
            st.warning("Please select at least 2 tests for correlation analysis")
            return
        
        # Pivot table
        pivot_data = df[df['test_name'].isin(selected_tests)].pivot_table(
            index=['patient_id', 'sample_id'],
            columns='test_name',
            values='test_value'
        )
        
        # Calculate correlation
        corr_matrix = pivot_data.corr()
        
        # Create heatmap
        fig = px.imshow(
            corr_matrix,
            labels=dict(color="Correlation"),
            title="Test Correlation Matrix",
            color_continuous_scale='RdBu',
            aspect="auto"
        )
        
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

