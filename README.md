# Hệ thống quản lý chi tiêu – Case study chị Lan

## Yêu cầu
- Python 3.9 trở lên
- Kết nối Internet lần đầu để cài thư viện

## Cách chạy
Mở Terminal/CMD tại thư mục chứa `app.py`, chạy:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Sau đó mở địa chỉ Local URL mà Streamlit hiển thị (thường là `http://localhost:8501`).

## Nội dung
- `app.py`: giao diện Streamlit và dữ liệu case study.
- `data_analysis.py`: các hàm thống kê tổng chi, trung bình và gom nhóm danh mục.
- `data_visualization.py`: hàm vẽ biểu đồ tròn và cột.
- `requirements.txt`: thư viện cần cài.

## Ghi chú dữ liệu
Số liệu được nhập theo case study được cung cấp. Đơn vị là VNĐ; bảng trong đề có thể trình bày theo nghìn đồng. Tổng tháng 1 là 18,5 triệu đồng và tháng 3 là 18 triệu đồng.
