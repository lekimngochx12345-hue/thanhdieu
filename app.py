"""Ứng dụng phân tích case study quản lý chi tiêu của chị Lan.
Chạy: pip install -r requirements.txt && streamlit run app.py
"""
from pathlib import Path
import io
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).parent))
from data_analysis import tong_hop_thong_ke
from data_visualization import ve_bieu_do_tron, ve_bieu_do_cot

st.set_page_config(page_title="Kiểm soát chi tiêu – Case study chị Lan", page_icon="💳", layout="wide")

THU_NHAP = 18_000_000
THANG = ["Tháng 1", "Tháng 3"]
DATA = [
    {"danh_muc": "Nhà ở", "thang_1": 5_500_000, "thang_3": 5_500_000},
    {"danh_muc": "Ăn uống", "thang_1": 4_800_000, "thang_3": 3_800_000},
    {"danh_muc": "Đi lại", "thang_1": 1_200_000, "thang_3": 1_200_000},
    {"danh_muc": "Mua sắm", "thang_1": 2_800_000, "thang_3": 1_500_000},
    {"danh_muc": "Giải trí, cà phê", "thang_1": 1_500_000, "thang_3": 1_200_000},
    {"danh_muc": "Gói đăng ký", "thang_1": 500_000, "thang_3": 200_000},
    {"danh_muc": "Trả nợ", "thang_1": 1_200_000, "thang_3": 2_000_000},
    {"danh_muc": "Hỗ trợ gia đình", "thang_1": 1_000_000, "thang_3": 1_000_000},
    {"danh_muc": "Tiết kiệm, quỹ khẩn cấp", "thang_1": 0, "thang_3": 1_600_000},
]
df = pd.DataFrame(DATA)

def vnd(value):
    return f"{value:,.0f} đ".replace(",", ".")

def trieu(value):
    return f"{value / 1_000_000:.1f} triệu đ"

def render_plot(func, data):
    plt.close("all")
    func(data)
    fig = plt.gcf()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

def main():
    st.title("💳 Từ ‘hết tiền cuối tháng’ đến kiểm soát chi tiêu")
    st.caption("Case study: Chị Lan – nhân viên marketing, 29 tuổi, sống tại TP.HCM")

    with st.sidebar:
        st.header("Thông tin tình huống")
        st.metric("Thu nhập cố định/tháng", "18.000.000 đ")
        st.metric("Dư nợ ban đầu", "Khoảng 6.000.000 đ")
        st.write("**Mục tiêu hệ thống**")
        st.write("Ghi chép giao dịch → phân loại → lập ngân sách → ưu tiên trả nợ và tiết kiệm → rà soát định kỳ.")
        st.divider()
        st.caption("Dữ liệu được nhập sẵn theo case study, đơn vị gốc là VNĐ.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📌 Tổng quan", "📊 So sánh chi tiêu", "📈 Biểu đồ", "⚙️ Quy trình", "💬 Thảo luận"
    ])

    total1 = int(df["thang_1"].sum())
    total3 = int(df["thang_3"].sum())
    with tab1:
        st.subheader("Kết quả chính sau 3 tháng")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Thu nhập/tháng", trieu(THU_NHAP))
        c2.metric("Tổng chi tháng 1", trieu(total1), delta="-0,5 triệu so với thu nhập", delta_color="inverse")
        c3.metric("Tổng chi tháng 3", trieu(total3), delta="Cân đối thu – chi")
        c4.metric("Dư nợ còn lại", "~0,5 triệu đ", delta="Giảm ~5,5 triệu đ")
        st.success("Sau điều chỉnh: không còn thâm hụt hàng tháng, không phát sinh nợ mới và quỹ khẩn cấp bắt đầu hình thành.")
        st.markdown("#### Bức tranh trước và sau")
        summary = pd.DataFrame({
            "Chỉ số": ["Tổng chi", "Cân đối thu – chi", "Trả nợ", "Quỹ khẩn cấp"],
            "Tháng 1": [total1, total1-THU_NHAP, 1_200_000, 0],
            "Tháng 3": [total3, total3-THU_NHAP, 2_000_000, 1_600_000],
        })
        st.dataframe(summary.style.format({"Tháng 1": lambda x: vnd(x), "Tháng 3": lambda x: vnd(x)}), use_container_width=True, hide_index=True)
        st.info("Lưu ý: Tháng 1 ghi nhận tổng chi 18,5 triệu đồng, cao hơn mức 14 triệu đồng chị Lan tự ước tính. Khoản chênh lệch chủ yếu được phát hiện nhờ ghi lại các giao dịch nhỏ lẻ.")

    with tab2:
        st.subheader("Bảng so sánh theo danh mục")
        long_month1 = df[["danh_muc", "thang_1"]].rename(columns={"thang_1": "so_tien"})
        stats_month1 = tong_hop_thong_ke(long_month1)
        m1, m2 = st.columns(2)
        m1.metric("Tổng chi tháng 1 (từ module phân tích)", vnd(stats_month1["tong_tien"]))
        m2.metric("Chi trung bình mỗi danh mục tháng 1", vnd(stats_month1["trung_binh_chi_tieu"]))
        view = df.copy()
        view["thay_doi"] = view["thang_3"] - view["thang_1"]
        view = view.rename(columns={"danh_muc":"Hạng mục", "thang_1":"Tháng 1 (VNĐ)", "thang_3":"Tháng 3 (VNĐ)", "thay_doi":"Thay đổi (VNĐ)"})
        st.dataframe(view.style.format({"Tháng 1 (VNĐ)": lambda x: vnd(x), "Tháng 3 (VNĐ)": lambda x: vnd(x), "Thay đổi (VNĐ)": lambda x: vnd(x)}), use_container_width=True, hide_index=True)
        st.caption("Số âm ở cột thay đổi thể hiện mức chi đã giảm; số dương thể hiện tăng chi cho trả nợ hoặc tiết kiệm.")
        st.download_button("⬇️ Tải bảng dữ liệu CSV", data=view.to_csv(index=False).encode("utf-8-sig"), file_name="case_study_chi_tieu_chi_Lan.csv", mime="text/csv")

    with tab3:
        st.subheader("Trực quan hóa dữ liệu")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Cơ cấu chi tháng 1**")
            render_plot(ve_bieu_do_tron, dict(zip(df["danh_muc"], df["thang_1"])))
        with c2:
            st.markdown("**So sánh từng hạng mục: tháng 1 và tháng 3**")
            fig, ax = plt.subplots(figsize=(10, 5))
            x = range(len(df))
            width = 0.38
            ax.bar([i-width/2 for i in x], df["thang_1"] / 1_000_000, width, label="Tháng 1")
            ax.bar([i+width/2 for i in x], df["thang_3"] / 1_000_000, width, label="Tháng 3")
            ax.set_ylabel("Triệu đồng")
            ax.set_xticks(list(x), df["danh_muc"], rotation=35, ha="right")
            ax.legend()
            ax.set_title("Chi tiêu theo danh mục")
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        st.markdown("**Điểm cần chú ý**")
        st.write("- Ăn uống giảm 1 triệu đồng; mua sắm giảm 1,3 triệu đồng; gói đăng ký giảm 300 nghìn đồng.")
        st.write("- Trả nợ tăng 800 nghìn đồng và quỹ khẩn cấp tăng từ 0 lên 1,6 triệu đồng.")

    with tab4:
        st.subheader("Quy trình quản lý chi tiêu được áp dụng")
        steps = [
            ("1. Ghi nhận", "Ghi từng giao dịch vào ứng dụng ngay sau khi chi, chậm nhất trong ngày."),
            ("2. Phân loại", "Nhà ở, ăn uống, đi lại, mua sắm, giải trí, đăng ký dịch vụ, trả nợ, gia đình, tiết kiệm."),
            ("3. Lập ngân sách", "Dùng dữ liệu tháng đầu để đặt hạn mức thực tế; điều chỉnh khung 50/30/20 vì đang có nợ."),
            ("4. Ưu tiên tiền", "Ngày nhận lương, chuyển tiền trả nợ và tiết kiệm sang tài khoản riêng."),
            ("5. Rà soát", "10 phút mỗi Chủ nhật và 30 phút cuối tháng để so sánh thực tế với ngân sách."),
        ]
        for title, desc in steps:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(desc)
        st.markdown("#### Khó khăn và cách xử lý")
        st.write("- Quên ghi chép: đặt nhắc nhở lúc 21:00 hằng ngày.")
        st.write("- Cắt giảm quá gắt: giữ một khoản giải trí cố định để dễ duy trì.")
        st.write("- Chi phí bất thường: dùng quỹ khẩn cấp, sau đó bổ sung lại theo kế hoạch.")

    with tab5:
        st.subheader("Câu hỏi thảo luận trên lớp")
        questions = [
            "Vì sao chị Lan đánh giá thấp chi tiêu tháng 1? Yếu tố hành vi nào gây ra điều đó?",
            "Nếu là cố vấn, bạn ưu tiên trả nợ trước hay lập quỹ khẩn cấp trước? Vì sao?",
            "Nên thiết kế ngân sách thế nào cho những tháng có thu nhập không cố định?",
            "Ngoài tổng chi, cần theo dõi chỉ số nào để đánh giá hệ thống có hiệu quả?",
            "Hệ thống cần thay đổi gì nếu áp dụng cho hộ gia đình hai người có thu nhập?",
        ]
        for i, q in enumerate(questions, 1):
            st.markdown(f"**{i}. {q}**")
            st.text_area("Ghi chú trả lời", key=f"answer_{i}", height=75, label_visibility="collapsed", placeholder="Nhập ý chính để thảo luận...")
        st.download_button("⬇️ Xuất dữ liệu phân tích tổng hợp", data=df.to_csv(index=False).encode("utf-8-sig"), file_name="du_lieu_chi_tieu_Lan.csv", mime="text/csv")

if __name__ == "__main__":
    main()
