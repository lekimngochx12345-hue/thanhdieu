"""Các hàm thống kê dùng chung cho hệ thống quản lý chi tiêu."""
import pandas as pd

def load_data(filepath_or_records):
    if isinstance(filepath_or_records, (str, bytes)):
        return pd.read_csv(filepath_or_records)
    return pd.DataFrame(filepath_or_records)

def tinh_tong_tien(df, cot_so_tien="so_tien"):
    return float(df[cot_so_tien].sum()) if cot_so_tien in df.columns else 0.0

def tinh_trung_binh_chi_tieu(df, cot_so_tien="so_tien"):
    if df.empty or cot_so_tien not in df.columns:
        return 0.0
    return float(df[cot_so_tien].mean())

def gom_nhom_theo_danh_muc(df, cot_danh_muc="danh_muc", cot_so_tien="so_tien"):
    if df.empty or cot_danh_muc not in df.columns or cot_so_tien not in df.columns:
        return pd.DataFrame(columns=[cot_danh_muc, "tong_tien", "trung_binh", "so_giao_dich"])
    return df.groupby(cot_danh_muc, dropna=False)[cot_so_tien].agg(
        tong_tien="sum", trung_binh="mean", so_giao_dich="count"
    ).reset_index()

def tong_hop_thong_ke(df, cot_danh_muc="danh_muc", cot_so_tien="so_tien"):
    return {"tong_tien": tinh_tong_tien(df, cot_so_tien),
            "trung_binh_chi_tieu": tinh_trung_binh_chi_tieu(df, cot_so_tien),
            "theo_danh_muc": gom_nhom_theo_danh_muc(df, cot_danh_muc, cot_so_tien)}

if __name__ == "__main__":
    sample = pd.DataFrame([{"danh_muc":"Ăn uống", "so_tien":50000}, {"danh_muc":"Nhà ở", "so_tien":500000}])
    print(tong_hop_thong_ke(sample))
