#!/usr/bin/env python
"""
Script để chạy phân tích Financial Anomaly và lưu kết quả
Có thể chạy standalone để sinh dữ liệu cho dashboard
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle
import json
from pathlib import Path

print("=" * 70)
print("Financial Anomaly Detection - Data Processing")
print("=" * 70)

# ==================== LOAD AND EXPLORE ====================
print("\n[1/6] Loading and exploring dataset...")
df = pd.read_csv('financial_anomaly_data.csv')
print(f"✓ Dataset Shape: {df.shape}")
print(f"✓ Columns: {df.columns.tolist()}")

# ==================== PREPROCESSING ====================
print("\n[2/6] Data preprocessing and cleaning...")

# Check missing values
missing = df.isnull().sum()
if missing.sum() > 0:
    print(f"  - Missing values found: {missing.sum()} total")
    df = df.dropna()
else:
    print("  - No missing values")

# Remove duplicates
before_dup = len(df)
df = df.drop_duplicates()
print(f"✓ Removed duplicates: {before_dup - len(df)} rows")

# Convert Timestamp to datetime - handle DD-MM-YYYY format
try:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y %H:%M')
except:
    try:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)
    except:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Encode categorical variables
le_merchant = LabelEncoder()
le_transaction_type = LabelEncoder()
le_location = LabelEncoder()

df['Merchant_encoded'] = le_merchant.fit_transform(df['Merchant'])
df['TransactionType_encoded'] = le_transaction_type.fit_transform(df['TransactionType'])
df['Location_encoded'] = le_location.fit_transform(df['Location'])
print("✓ Categorical variables encoded")

# Select numerical features for anomaly detection
numerical_features = ['Amount', 'Merchant_encoded', 'TransactionType_encoded', 'Location_encoded']
df_numerical = df[numerical_features]

# Scale the data
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_numerical), columns=numerical_features)
print(f"✓ Data scaled, shape: {df_scaled.shape}")

# ==================== FEATURE ENGINEERING ====================
print("\n[3/6] Feature engineering...")

# Extract time-based features
df['Hour'] = df['Timestamp'].dt.hour
df['DayOfWeek'] = df['Timestamp'].dt.dayofweek
df['Month'] = df['Timestamp'].dt.month

# Group by AccountID and calculate statistics
account_stats = df.groupby('AccountID')['Amount'].agg(['mean', 'std', 'count']).reset_index()
account_stats.columns = ['AccountID', 'Account_Mean_Amount', 'Account_Std_Amount', 'Account_Transaction_Count']
df = df.merge(account_stats, on='AccountID', how='left')

# Calculate deviation from account mean
df['Amount_Deviation_From_Mean'] = df['Amount'] - df['Account_Mean_Amount']

# Fill NaN for std (if count=1)
df['Account_Std_Amount'] = df['Account_Std_Amount'].fillna(0)

# Update numerical features
numerical_features.extend(['Hour', 'DayOfWeek', 'Month', 'Account_Mean_Amount', 'Account_Std_Amount', 'Account_Transaction_Count', 'Amount_Deviation_From_Mean'])

# Update scaled data
df_numerical = df[numerical_features]
df_scaled = pd.DataFrame(scaler.fit_transform(df_numerical), columns=numerical_features)
print(f"✓ Features engineered, total: {len(numerical_features)}")

# ==================== ANOMALY DETECTION ====================
print("\n[4/6] Training Isolation Forest model...")

contamination_rate = 0.05
iso_forest = IsolationForest(n_estimators=100, contamination=contamination_rate, random_state=42)
iso_forest.fit(df_scaled)

# Predict anomalies
df['Anomaly_Score'] = iso_forest.decision_function(df_scaled)
df['Anomaly'] = iso_forest.predict(df_scaled)

# Convert predictions: -1 for anomaly, 1 for normal
df['Anomaly'] = df['Anomaly'].map({1: 0, -1: 1})

anomaly_count = df['Anomaly'].sum()
anomaly_pct = (anomaly_count / len(df)) * 100

print(f"✓ Model trained with contamination rate: {contamination_rate}")
print(f"✓ Anomalies detected: {int(anomaly_count)} ({anomaly_pct:.2f}%)")

# ==================== SAVE RESULTS ====================
print("\n[5/6] Saving results...")

# Save the DataFrame with results
df.to_csv('financial_anomaly_results.csv', index=False)
print("✓ Saved: financial_anomaly_results.csv")

# Save the model and scaler
with open('isolation_forest_model.pkl', 'wb') as f:
    pickle.dump(iso_forest, f)
print("✓ Saved: isolation_forest_model.pkl")

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("✓ Saved: scaler.pkl")

# Create summary statistics
anomalies_df = df[df['Anomaly'] == 1]
normal_df = df[df['Anomaly'] == 0]

summary = {
    'total_transactions': len(df),
    'anomalies_detected': int(anomaly_count),
    'anomaly_percentage': float(anomaly_pct),
    'avg_amount': float(df['Amount'].mean()),
    'avg_anomaly_amount': float(anomalies_df['Amount'].mean()) if len(anomalies_df) > 0 else 0,
    'avg_normal_amount': float(normal_df['Amount'].mean()) if len(normal_df) > 0 else 0,
}

with open('summary_statistics.json', 'w') as f:
    json.dump(summary, f, indent=2)
print("✓ Saved: summary_statistics.json")

# ==================== STATISTICS ====================
print("\n[6/6] Analysis Summary:")
print(f"  - Total Transactions: {summary['total_transactions']:,}")
print(f"  - Anomalies Detected: {summary['anomalies_detected']:,}")
print(f"  - Anomaly Rate: {summary['anomaly_percentage']:.2f}%")
print(f"  - Avg Transaction Amount: ${summary['avg_amount']:,.2f}")
print(f"  - Avg Anomaly Amount: ${summary['avg_anomaly_amount']:,.2f}")
print(f"  - Avg Normal Amount: ${summary['avg_normal_amount']:,.2f}")

print("\n" + "=" * 70)
print("✓ All data processing completed successfully!")
print("✓ Dashboard is ready to run: python flask_app.py")
print("=" * 70)
