# 🌐 Web Dashboard - Hướng Dẫn Sử Dụng

## Bước 1: Chạy Notebook để tạo dữ liệu

Trước tiên, bạn cần chạy notebook `financial_anomaly_analysis.ipynb` để xử lý dữ liệu và tạo các file kết quả:

```bash
# Kích hoạt environment
conda activate financial_anomaly_env

# Hoặc nếu đang sử dụng PowerShell
D:\anaconda\condabin\conda.bat run -n financial_anomaly_env jupyter notebook
```

Chạy tất cả các cell trong notebook. Lần cuối cùng sẽ lưu các file:
- `financial_anomaly_results.csv`
- `isolation_forest_model.pkl`
- `scaler.pkl`
- `summary_statistics.json`

## Bước 2: Chạy Ứng dụng Flask

### Tùy chọn A: Chạy Flask App (Khuyến nghị)

```bash
# Kích hoạt environment
conda activate financial_anomaly_env

# Cài đặt Flask nếu chưa có
pip install flask

# Chạy ứng dụng
python flask_app.py
```

Sau đó, mở browser và truy cập: **http://localhost:5000**

### Tùy chọn B: Chạy Streamlit App

Nếu Streamlit cài đặt thành công, bạn có thể chạy:

```bash
streamlit run app.py
```

## Tính Năng Dashboard

### 📊 Hiển thị
- **Metrics**: Tổng giao dịch, số bất thường phát hiện, tỉ lệ, mức trung bình
- **Biểu đồ**: Phân bố điểm bất thường, phân bố số tiền, bất thường theo loại giao dịch
- **Bảng dữ liệu**: Top 10 giao dịch có điểm bất thường cao nhất
- **Thống kê**: So sánh giữa giao dịch bình thường và bất thường

### 🔍 Lọc dữ liệu
- **Loại hiển thị**: Tất cả / Chỉ bất thường / Chỉ bình thường
- **Loại giao dịch**: Lọc theo loại giao dịch
- **Phạm vi số tiền**: Chọn khoảng số tiền cần phân tích

## Cấu trúc Thư mục

```
c:\Users\Quan\vscode\
├── financial_anomaly_analysis.ipynb    # Notebook phân tích
├── financial_anomaly_data.csv          # Dữ liệu gốc
├── financial_anomaly_results.csv       # Kết quả (sau khi chạy notebook)
├── isolation_forest_model.pkl          # Model (sau khi chạy notebook)
├── scaler.pkl                          # Scaler (sau khi chạy notebook)
├── summary_statistics.json             # Thống kê (sau khi chạy notebook)
├── app.py                              # Streamlit app
├── flask_app.py                        # Flask app
├── requirements.txt                    # Dependencies
├── environment.yml                     # Conda environment
├── templates/
│   └── index.html                      # HTML dashboard
└── static/
    ├── style.css                       # CSS styling
    └── script.js                       # JavaScript
```

## Yêu cầu

- Python 3.9+
- Anaconda/Conda
- Các thư viện: pandas, numpy, scikit-learn, matplotlib, seaborn
- Cho Flask: flask
- Cho Streamlit: streamlit, plotly

## Khắc Phục Sự Cố

### "Data files not found"
→ Chạy notebook `financial_anomaly_analysis.ipynb` để tạo dữ liệu trước

### Lỗi kết nối
→ Đảm bảo đã kích hoạt environment: `conda activate financial_anomaly_env`

### Port 5000 đang sử dụng
→ Sửa port trong `flask_app.py`: thay `app.run(debug=True, port=5000)` bằng port khác

## Liên Hệ

Nếu gặp bất kỳ vấn đề nào, kiểm tra logs và đảm bảo tất cả các file được tạo sau khi chạy notebook.
