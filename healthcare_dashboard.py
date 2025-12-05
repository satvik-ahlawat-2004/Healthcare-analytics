import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #1f77b4, #0d47a1);
        border-radius: 10px;
        border: 2px solid #0d47a1;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        margin: 0;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #666;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the healthcare dataset"""
    try:
        df = pd.read_csv('healthcare_dataset.csv')
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Convert dates
        df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
        df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
        
        # Calculate length of stay
        df['Length of Stay'] = (df['Discharge Date'] - df['Date of Admission']).dt.days
        
        # Clean numeric columns
        df['Billing Amount'] = pd.to_numeric(df['Billing Amount'], errors='coerce')
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        
        # Create age groups
        df['Age Group'] = pd.cut(df['Age'], 
                               bins=[0, 18, 30, 45, 60, 75, 100], 
                               labels=['0-18', '19-30', '31-45', '46-60', '61-75', '75+'])
        
        # Clean text columns
        text_columns = ['Gender', 'Medical Condition', 'Hospital', 'Insurance Provider', 'Admission Type']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].str.strip().str.title()
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def create_kpi_cards(df):
    """Create KPI cards for key metrics"""
    col1, col2, col3 = st.columns(3)
    
    total_patients = len(df)
    total_billing = df['Billing Amount'].sum()
    avg_length_stay = df['Length of Stay'].mean()
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">{total_patients:,}</p>
            <p class="kpi-label">Total Patients</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">${total_billing:,.0f}</p>
            <p class="kpi-label">Total Billing Amount</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">{avg_length_stay:.1f}</p>
            <p class="kpi-label">Avg Length of Stay (Days)</p>
        </div>
        """, unsafe_allow_html=True)

def create_filters(df):
    """Create sidebar filters"""
    st.sidebar.header("🔍 Filters")
    
    # Gender filter
    gender_options = ['All'] + sorted(df['Gender'].unique().tolist())
    selected_gender = st.sidebar.selectbox("Select Gender", gender_options)
    
    # Age range filter
    age_options = ['All'] + sorted(df['Age Group'].dropna().unique().tolist())
    selected_age = st.sidebar.selectbox("Select Age Range", age_options)
    
    # Insurance provider filter
    insurance_options = ['All'] + sorted(df['Insurance Provider'].unique().tolist())
    selected_insurance = st.sidebar.selectbox("Select Insurance Provider", insurance_options)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    if selected_age != 'All':
        filtered_df = filtered_df[filtered_df['Age Group'] == selected_age]
    
    if selected_insurance != 'All':
        filtered_df = filtered_df[filtered_df['Insurance Provider'] == selected_insurance]
    
    # Display filter summary
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Filter Summary:**")
    st.sidebar.markdown(f"• Gender: {selected_gender}")
    st.sidebar.markdown(f"• Age Range: {selected_age}")
    st.sidebar.markdown(f"• Insurance: {selected_insurance}")
    st.sidebar.markdown(f"• **Records:** {len(filtered_df):,} / {len(df):,}")
    
    return filtered_df

def create_billing_by_condition_chart(df):
    """Create average billing amount per medical condition chart"""
    billing_by_condition = df.groupby('Medical Condition')['Billing Amount'].mean().sort_values(ascending=True)
    
    fig = px.bar(
        x=billing_by_condition.values,
        y=billing_by_condition.index,
        orientation='h',
        title="Average Billing Amount by Medical Condition",
        labels={'x': 'Average Billing Amount ($)', 'y': 'Medical Condition'},
        color=billing_by_condition.values,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_font_size=16,
        title_x=0.5
    )
    
    fig.update_traces(
        texttemplate='$%{x:,.0f}',
        textposition='outside'
    )
    
    return fig

def create_length_stay_chart(df):
    """Create average length of stay by condition chart"""
    stay_by_condition = df.groupby('Medical Condition')['Length of Stay'].mean().sort_values(ascending=False)
    
    fig = px.bar(
        x=stay_by_condition.index,
        y=stay_by_condition.values,
        title="Average Length of Stay by Medical Condition",
        labels={'x': 'Medical Condition', 'y': 'Average Length of Stay (Days)'},
        color=stay_by_condition.values,
        color_continuous_scale='Oranges'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_font_size=16,
        title_x=0.5,
        xaxis_tickangle=-45
    )
    
    fig.update_traces(
        texttemplate='%{y:.1f}',
        textposition='outside'
    )
    
    return fig

def create_top_hospitals_chart(df):
    """Create top 10 hospitals by average billing amount chart"""
    hospital_billing = df.groupby('Hospital')['Billing Amount'].mean().sort_values(ascending=True).tail(10)
    
    fig = px.bar(
        x=hospital_billing.values,
        y=hospital_billing.index,
        orientation='h',
        title="Top 10 Hospitals by Average Billing Amount",
        labels={'x': 'Average Billing Amount ($)', 'y': 'Hospital'},
        color=hospital_billing.values,
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        title_font_size=16,
        title_x=0.5
    )
    
    fig.update_traces(
        texttemplate='$%{x:,.0f}',
        textposition='outside'
    )
    
    return fig

def create_insurance_billing_chart(df):
    """Create total billing by insurance provider pie chart"""
    insurance_billing = df.groupby('Insurance Provider')['Billing Amount'].sum().sort_values(ascending=False)
    
    fig = px.pie(
        values=insurance_billing.values,
        names=insurance_billing.index,
        title="Total Billing Amount by Insurance Provider",
        hole=0.4  # Creates donut chart
    )
    
    fig.update_layout(
        height=400,
        title_font_size=16,
        title_x=0.5
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    return fig

def create_admission_billing_chart(df):
    """Create average billing by admission type chart"""
    admission_billing = df.groupby('Admission Type')['Billing Amount'].mean().sort_values(ascending=False)
    
    fig = px.bar(
        x=admission_billing.index,
        y=admission_billing.values,
        title="Average Billing Amount by Admission Type",
        labels={'x': 'Admission Type', 'y': 'Average Billing Amount ($)'},
        color=admission_billing.values,
        color_continuous_scale='Purples'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_font_size=16,
        title_x=0.5
    )
    
    fig.update_traces(
        texttemplate='$%{y:,.0f}',
        textposition='outside'
    )
    
    return fig

def main():
    """Main dashboard function"""
    # Header
    st.markdown('<h1 class="main-header">🏥 Healthcare Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        st.stop()
    
    # Create filters and get filtered data
    filtered_df = create_filters(df)
    
    # KPI Cards
    st.markdown("## 📊 Key Performance Indicators")
    create_kpi_cards(filtered_df)
    
    # Charts section
    st.markdown("## 📈 Analytics Charts")
    
    # Row 1: Billing by condition and Length of stay
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig1 = create_billing_by_condition_chart(filtered_df)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig2 = create_length_stay_chart(filtered_df)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Top hospitals
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig3 = create_top_hospitals_chart(filtered_df)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Insurance and Admission type
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig4 = create_insurance_billing_chart(filtered_df)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig5 = create_admission_billing_chart(filtered_df)
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data summary
    with st.expander("📋 Data Summary", expanded=False):
        st.markdown("### Dataset Overview")
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.markdown(f"""
            **Dataset Information:**
            - Total Records: {len(df):,}
            - Filtered Records: {len(filtered_df):,}
            - Date Range: {df['Date of Admission'].min().strftime('%Y-%m-%d')} to {df['Date of Admission'].max().strftime('%Y-%m-%d')}
            """)
        
        with col_info2:
            st.markdown(f"""
            **Key Statistics:**
            - Unique Hospitals: {df['Hospital'].nunique()}
            - Medical Conditions: {df['Medical Condition'].nunique()}
            - Insurance Providers: {df['Insurance Provider'].nunique()}
            """)
        
        # Show sample data
        st.markdown("### Sample Data")
        st.dataframe(filtered_df.head(10), use_container_width=True)

if __name__ == "__main__":
    main()
