# 💰 Financial Anomaly Detection & Analysis

Dự án phân tích dữ liệu bất thường tài chính sử dụng Isolation Forest algorithm và dashboard web tương tác.

## 📋 Nội dung Dự án

### 📊 Notebook Phân tích (`financial_anomaly_analysis.ipynb`)
- **Khám phá dữ liệu**: Phân tích cấu trúc, kiểu dữ liệu, thiếu dữ liệu
- **Tiền xử lý**: Làm sạch dữ liệu, encoding features, scaling
- **EDA**: Visualize phân bố, correlation, anomalies
- **Feature Engineering**: Trích xuất features thời gian, tính toán thống kê
- **Mô hình**: Sử dụng Isolation Forest để phát hiện bất thường
- **Đánh giá**: Phân tích kết quả, visualize anomalies

### 🌐 Web Dashboard
- **Flask App** (`flask_app.py`): Backend API cho dữ liệu
- **Streamlit App** (`app.py`): Dashboard tương tác thay thế
- **Frontend**: HTML/CSS/JavaScript responsive dashboard

## 🚀 Cách Sử Dụng

### 1. Thiết lập Môi trường

```bash
# Tạo môi trường Anaconda
conda env create -f environment.yml
conda activate financial_anomaly_env
```

### 2. Chạy Notebook để xử lý dữ liệu

```bash
# Khởi động Jupyter
jupyter notebook
# Mở financial_anomaly_analysis.ipynb và chạy tất cả cell
```

### 3. Chạy Web Dashboard

**Option A - Flask (Khuyến nghị):**
```bash
pip install flask
python flask_app.py
# Truy cập: http://localhost:5000
```

**Option B - Streamlit:**
```bash
pip install streamlit plotly
streamlit run app.py
```

## 📁 Cấu trúc Thư mục

```
c:\Users\Quan\vscode\
├── financial_anomaly_analysis.ipynb     # Notebook chính
├── financial_anomaly_data.csv           # Dữ liệu gốc
├── flask_app.py                         # Flask backend
├── app.py                               # Streamlit app
├── requirements.txt                     # Python dependencies
├── environment.yml                      # Conda environment
├── DASHBOARD_USAGE.md                   # Hướng dẫn chi tiết
├── templates/
│   └── index.html                       # HTML dashboard
└── static/
    ├── style.css                        # Styling
    └── script.js                        # Interactivity
```

## 🔧 Tính Năng Dashboard

- 📈 Metrics: Tổng giao dịch, bất thường phát hiện, tỉ lệ, mức trung bình
- 📊 Charts: Phân bố điểm bất thường, số tiền, anomalies theo loại
- 🎯 Filters: Lọc theo loại giao dịch, phạm vi số tiền
- 📋 Tables: Top anomalies với thông tin chi tiết
- 📱 Responsive: Tương thích với desktop, tablet, mobile

## 🧬 Mô hình Isolation Forest

- **Thuật toán**: Isolation Forest
- **Tham số contamination**: 5%
- **Features**: Amount, Merchant, TransactionType, Location, temporal features
- **Output**: Anomaly score và binary classification

## 📊 Thống kê Dữ liệu

Các file được tạo sau khi chạy notebook:
- `financial_anomaly_results.csv`: Dữ liệu đầy đủ + anomaly scores
- `isolation_forest_model.pkl`: Mô hình đã train
- `scaler.pkl`: StandardScaler cho features
- `summary_statistics.json`: Thống kê tóm tắt

## 💡 Ghi Chú

- Luôn chạy notebook trước khi khởi động dashboard
- Dashboard tự động load dữ liệu từ CSV
- Có thể tùy chỉnh contamination rate trong notebook
