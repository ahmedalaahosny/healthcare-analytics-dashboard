import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(page_title="Healthcare Analytics", layout="wide", initial_sidebar_state="expanded")

# Title and Description
st.title("🏥 Healthcare Analytics Dashboard")
st.markdown("Interactive healthcare data analytics platform for medical insights and patient management")

# Sidebar Navigation
with st.sidebar:
    st.header("Dashboard Options")
    page = st.radio("Select a page:", ["Patient Analytics", "Medical Trends", "Operational Metrics"])

# Generate Sample Data
@st.cache_data
def load_patient_data():
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    np.random.seed(42)
    df = pd.DataFrame({
        'date': dates,
        'patient_id': np.random.randint(1000, 9999, len(dates)),
        'age': np.random.randint(18, 85, len(dates)),
        'diagnosis': np.random.choice(['Diabetes', 'Hypertension', 'Heart Disease', 'Asthma', 'Arthritis'], len(dates)),
        'treatment_days': np.random.randint(1, 30, len(dates)),
        'cost': np.random.randint(500, 10000, len(dates))
    })
    return df

df = load_patient_data()

if page == "Patient Analytics":
    st.header("Patient Demographics & Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Patients", "2,547", "+12%")
    col2.metric("Avg Age", "52.3 years", "-2.1%")
    col3.metric("Recovery Rate", "94.2%", "+3.5%")
    
    fig = px.histogram(df, x='age', title='Patient Age Distribution', nbins=20)
    st.plotly_chart(fig, use_container_width=True)
    
    fig2 = px.pie(df, names='diagnosis', title='Top Diagnoses')
    st.plotly_chart(fig2, use_container_width=True)

elif page == "Medical Trends":
    st.header("Medical Trends Analysis")
    trend_data = df.groupby('date').size()
    fig = px.line(x=trend_data.index, y=trend_data.values, title='Daily Patient Admissions', labels={'x': 'Date', 'y': 'Number of Patients'})
    st.plotly_chart(fig, use_container_width=True)
    
    diag_trends = df.groupby(['date', 'diagnosis']).size().reset_index(name='count')
    fig2 = px.area(diag_trends, x='date', y='count', color='diagnosis', title='Diagnosis Trends Over Time')
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.header("Operational Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        avg_cost = df['cost'].mean()
        st.metric("Average Treatment Cost", f"${avg_cost:,.0f}", "+5.2%")
        
    with col2:
        avg_days = df['treatment_days'].mean()
        st.metric("Average Treatment Days", f"{avg_days:.1f}", "-1.3%")
    
    fig = px.box(df, x='diagnosis', y='cost', title='Cost Distribution by Diagnosis')
    st.plotly_chart(fig, use_container_width=True)
