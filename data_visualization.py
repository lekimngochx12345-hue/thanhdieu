"""Các hàm vẽ biểu đồ cho ứng dụng Streamlit."""
import matplotlib.pyplot as plt

def ve_bieu_do_tron(theo_danh_muc):
    labels = list(theo_danh_muc.keys())
    values = list(theo_danh_muc.values())
    # Bỏ hạng mục bằng 0 để biểu đồ tròn không lỗi hoặc tạo nhãn thừa.
    pairs = [(k, v) for k, v in zip(labels, values) if v > 0]
    plt.figure(figsize=(7, 7))
    if pairs:
        plt.pie([v for _, v in pairs], labels=[k for k, _ in pairs], autopct="%1.1f%%", startangle=90)
    else:
        plt.text(0.5, 0.5, "Chưa có dữ liệu", ha="center", va="center")
    plt.title("Tỷ lệ chi tiêu theo danh mục")
    plt.tight_layout()

def ve_bieu_do_cot(theo_danh_muc):
    labels = list(theo_danh_muc.keys())
    values = list(theo_danh_muc.values())
    plt.figure(figsize=(9, 5))
    plt.bar(labels, values)
    plt.title("So sánh chi tiêu theo danh mục")
    plt.xlabel("Danh mục")
    plt.ylabel("Số tiền (VNĐ)")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()

if __name__ == "__main__":
    ve_bieu_do_tron({"Ăn uống": 3800000, "Nhà ở": 5500000, "Mua sắm": 1500000})
    plt.show()
