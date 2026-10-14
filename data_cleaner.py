import pandas as pd 
import numpy as np 
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

# Bộ dữ liệu Kaggle gốc dùng đơn vị USD. Nhóm quy đổi sang VNĐ để phù hợp
# với bối cảnh sinh viên Việt Nam. Tỷ giá có thể chỉnh lại cho khớp thời
# điểm làm báo cáo.
TY_GIA_USD_VND = 25000

# Các cột tiền tệ cần quy đổi (không gồm students_ID, age... vì không phải tiền)
CAC_COT_TIEN_TE = [
    "monthly_income", "financial_aid", "tuition", "housing", "food",
    "transportation", "books_supplies", "entertainment", "personal_care",
    "technology", "health_wellness", "miscellaneous",
]

class DataCleaner:
    def __init__(self, file_path: str):
        # khởi tạo class DataCleaner với đường dẫn tệp dữ liệu
        self.file_path = file_path
        self.data = None

    def load_data(self) -> pd.DataFrame:
        # đọc dữ liệu từ CSV và lưu vào biến self.data
        try:
            # QUAN TRỌNG: đưa con trỏ đọc về đầu file trước khi đọc.
            # Nếu không, khi Streamlit rerun lại script (VD: người dùng
            # chọn bộ lọc), file đã bị đọc hết ở lần trước -> đọc lần 2
            # sẽ ra lỗi "No columns to parse from file".
            if hasattr(self.file_path, "seek"):
                self.file_path.seek(0)
            self.df = pd.read_csv(self.file_path)
            print("Dữ liệu đã được tải thành công từ:", self.file_path)
            return self.df
        except FileNotFoundError:
            print("Không tìm thấy tệp:", self.file_path)
            return None 

    def inspect_data(self):
        # kiểm tra thông tin cơ bản về dữ liệu
        if self.df is None:
            print("Dữ liệu chưa được tải. Vui lòng gọi load_data() trước!")
            return

        print("1. Thông tin dữ liệu:")
        print(self.df.info())
        print(f"\n2. Số lượng cột: {self.df.shape[1]}")
        print(f"\n3. Số lượng hàng: {self.df.shape[0]}")
        print("\n4. Kiểu dữ liệu của các cột: ")
        print(self.df.dtypes)
        print("\n5. Số lượng giá trị thiếu: ")
        print(self.df.isnull().sum())
        print(f"\n6. Số lượng giá trị trùng lặp:")
        print(self.df.duplicated().sum())
        print("\n7. Thống kê mô tả cho các cột số: ")
        print(self.df.describe())
        print("\n8. Xem trước 10 dòng đầu tiên của dữ liệu: ")
        print(self.df.head(10))



    def clean_data(self) -> pd.DataFrame:
        if self.df is None:
            print("Dữ liệu chưa được tải. Vui lòng gọi load_data() trước!")
            return None
        print("Bắt đầu quá trình làm sạch dữ liệu...")

        # đổi tên cột unnamed: 0 thành students_ID
        if 'Unnamed: 0' in self.df.columns:
            self.df.rename(columns = {'Unnamed: 0': 'students_ID'}, inplace=True)
            print("Đã đổi tên cột 'Unnamed: 0' thành 'students_ID'.")
            
        # xóa khoảng trắng thừa trong GIÁ TRỊ của các cột dạng chữ (object/string)
        string_cols = self.df.select_dtypes(include=['object','string']).columns
        for col in string_cols:
            self.df[col] = self.df[col].astype(str).str.strip()
        print("Đã xóa khoảng trắng thừa trong giá trị các cột dạng chữ.")
     

        # loại bỏ các dòng bị trùng lặp hoàn toàn
        so_dong_truoc = len(self.df)
        self.df = self.df.drop_duplicates()
        print(f"Đã loại bỏ {so_dong_truoc - len(self.df)} dòng trùng lặp.")

        # xử lý giá trị thiếu: loại bỏ các dòng thiếu dữ liệu ở cột số quan trọng
        so_dong_truoc = len(self.df)
        self.df = self.df.dropna(subset=[c for c in self.df.columns if c != 'students_ID'])
        print(f"Đã loại bỏ {so_dong_truoc - len(self.df)} dòng có giá trị thiếu.")

        # đảm bảo các cột chi tiêu/ thu nhập không có giá trị âm
        numeric_cols = self.df.select_dtypes(include=['int64','float64']).columns
        for col in numeric_cols:
            if col != 'students_ID':
                self.df[col] = self.df[col].apply(lambda x: max(x, 0))
        print("Đã đảm bảo các cột chi tiêu/ thu nhập không có giá trị âm.")

        # quy đổi các cột tiền tệ từ USD (dữ liệu gốc) sang VNĐ
        cot_can_doi = [c for c in CAC_COT_TIEN_TE if c in self.df.columns]
        for c in cot_can_doi:
            # ép kiểu số trước khi nhân: nếu cột đang ở dạng chữ (object,
            # hoặc kiểu "str" mới của pandas 2.x) - vd "1,000" do dấu phẩy
            # ngăn cách hàng nghìn - phép nhân chuỗi*số trong pandas sẽ
            # LẶP LẠI chuỗi thay vì báo lỗi (vd "1,000"*3 -> "1,0001,000
            # 1,000"). Phải làm sạch dấu phẩy rồi ép kiểu số trước, nếu
            # không quy đổi tiền tệ sẽ tạo ra dữ liệu rác.
            if not pd.api.types.is_numeric_dtype(self.df[c]):
                self.df[c] = self.df[c].astype(str).str.replace(',', '', regex=False)
            self.df[c] = pd.to_numeric(self.df[c], errors='coerce')
        self.df[cot_can_doi] = (self.df[cot_can_doi] * TY_GIA_USD_VND).round(0)
        print(f"Đã quy đổi {len(cot_can_doi)} cột tiền tệ từ USD sang VNĐ (tỷ giá {TY_GIA_USD_VND:,}đ/$).")

        return self.df

    def save_cleaned_data(self, output_path: str = "cleaned_student_spending.csv"):
        """Bước cuối: Xuất dữ liệu đã làm sạch ra file CSV mới"""
        if self.df is not None:
            self.df.to_csv(output_path, index=False)
            print(f"Đã lưu thành công file dữ liệu sạch: '{output_path}'")
        else:
            print("Không có dữ liệu để lưu!")
    
        
if __name__ == "__main__":
    # Khai báo và nạp file
    cleaner = DataCleaner("student_spending (1).csv")
    
    if cleaner.load_data() is not None:
        # Bước 1: Khảo sát
        cleaner.inspect_data()
        
        # Bước 3: Làm sạch
        cleaner.clean_data()
        
        # Bước cuối: Xuất file CSV sạch
        cleaner.save_cleaned_data()

        print("\n XEM THỬ BẢNG DỮ LIỆU MỚI ĐÃ LÀM SẠCH (5 DÒNG ĐẦU):")
        print(cleaner.df.head())