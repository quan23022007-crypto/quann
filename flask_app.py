from flask import Flask, render_template, jsonify, request
import pandas as pd
import json
import os
from pathlib import Path

app = Flask(__name__)

# Load data
def load_data():
    try:
        df = pd.read_csv('financial_anomaly_results.csv')
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except FileNotFoundError:
        return None

def load_summary():
    try:
        with open('summary_statistics.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@app.route('/')
def index():
    df = load_data()
    summary = load_summary()
    
    if df is None or summary is None:
        return render_template('error.html', message="Data files not found. Please run the notebook first.")
    
    return render_template('index.html', summary=summary)

@app.route('/api/data')
def get_data():
    df = load_data()
    
    if df is None:
        return jsonify({'error': 'Data not found'}), 404
    
    # Get filter parameters
    anomaly_filter = request.args.get('anomaly', 'all')
    transaction_type = request.args.getlist('type')
    amount_min = float(request.args.get('min_amount', df['Amount'].min()))
    amount_max = float(request.args.get('max_amount', df['Amount'].max()))
    
    # Apply filters
    filtered_df = df[
        (df['Amount'] >= amount_min) &
        (df['Amount'] <= amount_max)
    ]
    
    if transaction_type:
        filtered_df = filtered_df[filtered_df['TransactionType'].isin(transaction_type)]
    
    if anomaly_filter == 'anomalies':
        filtered_df = filtered_df[filtered_df['Anomaly'] == 1]
    elif anomaly_filter == 'normal':
        filtered_df = filtered_df[filtered_df['Anomaly'] == 0]
    
    return jsonify({
        'count': len(filtered_df),
        'anomalies': int(filtered_df['Anomaly'].sum()),
        'avg_amount': float(filtered_df['Amount'].mean()),
        'transactions': filtered_df.to_dict('records')
    })

@app.route('/api/charts/anomaly-distribution')
def anomaly_distribution():
    df = load_data()
    anomaly_counts = df['Anomaly'].value_counts().to_dict()
    return jsonify({
        'normal': int(anomaly_counts.get(0, 0)),
        'anomalies': int(anomaly_counts.get(1, 0))
    })

@app.route('/api/charts/amount-distribution')
def amount_distribution():
    df = load_data()
    bins = pd.cut(df['Amount'], bins=20)
    counts = bins.value_counts().sort_index()
    return jsonify({
        'labels': [f"{i.left:.2f}-{i.right:.2f}" for i in counts.index],
        'data': counts.values.tolist()
    })

@app.route('/api/charts/by-type')
def by_type():
    df = load_data()
    type_anomalies = df[df['Anomaly'] == 1]['TransactionType'].value_counts()
    return jsonify({
        'labels': type_anomalies.index.tolist(),
        'data': type_anomalies.values.tolist()
    })

@app.route('/api/top-anomalies')
def top_anomalies():
    df = load_data()
    top_10 = df.nlargest(10, 'Anomaly_Score')[
        ['Timestamp', 'Amount', 'TransactionType', 'Merchant', 'Location', 'Anomaly_Score']
    ]
    return jsonify(top_10.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
