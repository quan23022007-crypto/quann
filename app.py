import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle
import json
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Financial Anomaly Analysis",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("💰 Financial Anomaly Detection Dashboard")
st.markdown("---")

# Load data and models
@st.cache_resource
def load_data():
    """Load results CSV"""
    df = pd.read_csv('financial_anomaly_results.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

@st.cache_resource
def load_summary():
    """Load summary statistics"""
    with open('summary_statistics.json', 'r') as f:
        return json.load(f)

# Load data
try:
    df = load_data()
    summary = load_summary()
except FileNotFoundError:
    st.error("❌ Data files not found. Please run the notebook first to generate the data.")
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Filter by anomaly
show_anomalies = st.sidebar.checkbox("Show only anomalies", value=False)
transaction_type_filter = st.sidebar.multiselect(
    "Filter by Transaction Type",
    df['TransactionType'].unique(),
    default=df['TransactionType'].unique()
)

# Filter amount range
amount_range = st.sidebar.slider(
    "Amount Range",
    float(df['Amount'].min()),
    float(df['Amount'].max()),
    (float(df['Amount'].min()), float(df['Amount'].max()))
)

# Apply filters
filtered_df = df[
    (df['TransactionType'].isin(transaction_type_filter)) &
    (df['Amount'] >= amount_range[0]) &
    (df['Amount'] <= amount_range[1])
]

if show_anomalies:
    filtered_df = filtered_df[filtered_df['Anomaly'] == 1]

# Display key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Total Transactions",
        value=f"{len(filtered_df):,}",
        delta=f"({len(filtered_df)/len(df)*100:.1f}% of total)"
    )

with col2:
    anomaly_count = filtered_df['Anomaly'].sum()
    st.metric(
        label="⚠️ Anomalies Detected",
        value=f"{int(anomaly_count):,}",
        delta=f"{anomaly_count/len(filtered_df)*100:.2f}% anomaly rate" if len(filtered_df) > 0 else "N/A"
    )

with col3:
    avg_amount = filtered_df['Amount'].mean()
    st.metric(
        label="💵 Average Amount",
        value=f"${avg_amount:,.2f}",
        delta=f"vs ${summary['avg_amount']:,.2f} overall"
    )

with col4:
    st.metric(
        label="📈 Dataset Size",
        value=f"{summary['total_transactions']:,}",
        delta=f"{summary['anomaly_percentage']:.2f}% anomalies"
    )

st.markdown("---")

# Row 1: Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Distribution of Anomaly Scores")
    fig = px.histogram(
        filtered_df,
        x='Anomaly_Score',
        nbins=50,
        title="Anomaly Score Distribution",
        labels={'Anomaly_Score': 'Anomaly Score', 'count': 'Frequency'},
        color_discrete_sequence=['#3498db']
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 Anomaly vs Normal Transactions")
    anomaly_counts = filtered_df['Anomaly'].value_counts().reset_index()
    anomaly_counts.columns = ['Anomaly', 'Count']
    anomaly_counts['Label'] = anomaly_counts['Anomaly'].map({0: 'Normal', 1: 'Anomaly'})
    
    fig = px.pie(
        anomaly_counts,
        values='Count',
        names='Label',
        title="Transaction Classification",
        color_discrete_map={'Normal': '#2ecc71', 'Anomaly': '#e74c3c'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 2: Amount Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Amount vs Anomaly Score")
    fig = px.scatter(
        filtered_df,
        x='Amount',
        y='Anomaly_Score',
        color='Anomaly',
        color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
        title="Transaction Amount vs Anomaly Score",
        labels={'Amount': 'Amount ($)', 'Anomaly_Score': 'Anomaly Score', 'Anomaly': 'Type'},
        hover_data=['TransactionType', 'Merchant']
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📦 Amount Distribution by Type")
    fig = px.box(
        filtered_df,
        x='TransactionType',
        y='Amount',
        color='Anomaly',
        color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
        title="Amount Distribution by Transaction Type",
        labels={'Amount': 'Amount ($)', 'TransactionType': 'Transaction Type', 'Anomaly': 'Type'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 3: Time Series
st.subheader("📈 Time Series: Transactions with Anomalies")
df_sorted = filtered_df.sort_values('Timestamp')

fig = go.Figure()

# Add normal transactions
normal_data = df_sorted[df_sorted['Anomaly'] == 0]
fig.add_trace(go.Scatter(
    x=normal_data['Timestamp'],
    y=normal_data['Amount'],
    mode='lines',
    name='Normal',
    line=dict(color='#2ecc71', width=1),
    opacity=0.5
))

# Add anomalies
anomaly_data = df_sorted[df_sorted['Anomaly'] == 1]
fig.add_trace(go.Scatter(
    x=anomaly_data['Timestamp'],
    y=anomaly_data['Amount'],
    mode='markers',
    name='Anomaly',
    marker=dict(color='#e74c3c', size=8),
    hovertemplate='<b>Anomaly</b><br>Time: %{x}<br>Amount: $%{y:,.2f}<extra></extra>'
))

fig.update_layout(
    title="Time Series of Transactions",
    xaxis_title="Timestamp",
    yaxis_title="Amount ($)",
    hovermode='x unified',
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 4: Transaction Type Analysis
st.subheader("🔍 Anomalies by Transaction Type")

transaction_anomalies = filtered_df[filtered_df['Anomaly'] == 1]['TransactionType'].value_counts().reset_index()
transaction_anomalies.columns = ['TransactionType', 'Count']

fig = px.bar(
    transaction_anomalies,
    x='TransactionType',
    y='Count',
    title="Anomaly Count by Transaction Type",
    labels={'TransactionType': 'Transaction Type', 'Count': 'Number of Anomalies'},
    color_discrete_sequence=['#e74c3c']
)
fig.update_layout(height=400)

col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("### Statistics")
    st.write(f"Total Anomalies: **{len(filtered_df[filtered_df['Anomaly'] == 1])}**")
    st.write(f"Avg Anomaly Amount: **${filtered_df[filtered_df['Anomaly'] == 1]['Amount'].mean():,.2f}**")
    st.write(f"Max Anomaly Amount: **${filtered_df[filtered_df['Anomaly'] == 1]['Amount'].max():,.2f}**")
    st.write(f"Min Anomaly Amount: **${filtered_df[filtered_df['Anomaly'] == 1]['Amount'].min():,.2f}**")

st.markdown("---")

# Row 5: Top Anomalies
st.subheader("🚨 Top 10 Highest Anomaly Scores")

top_anomalies = filtered_df.nlargest(10, 'Anomaly_Score')[
    ['Timestamp', 'Amount', 'TransactionType', 'Merchant', 'Location', 'Anomaly_Score']
]
top_anomalies['Amount'] = top_anomalies['Amount'].apply(lambda x: f"${x:,.2f}")
top_anomalies['Anomaly_Score'] = top_anomalies['Anomaly_Score'].apply(lambda x: f"{x:.4f}")

st.dataframe(top_anomalies, use_container_width=True, hide_index=True)

st.markdown("---")

# Footer
st.info(
    """
    💡 **About This Dashboard**
    - Uses Isolation Forest algorithm for anomaly detection
    - Contamination rate: 5%
    - Features include temporal patterns, merchant data, and transaction amounts
    """
)
