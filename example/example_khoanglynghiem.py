import sys
import math
import sympy 
import os
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    # Đảm bảo bạn đang import file "khoanglynghiem.py" đã được chỉnh sửa
    from khoanglynghiem import tim_khoang_cach_ly
except ImportError:
    print("LỖI: Không tìm thấy file 'khoanglynghiem.py'.")
    print("     Hãy đảm bảo 2 file nằm chung thư mục.")
    sys.exit(1)
except ModuleNotFoundError:
    print("LỖI: Bạn cần cài đặt thư viện 'sympy'.")
    print("     Hãy chạy lệnh: pip install sympy")
    sys.exit(1)

def chay_vi_du_cach_ly():
    print("=" * 60)
    print("  CHẠY VÍ DỤ TÌM KHOẢNG CÁCH LY NGHIỆM")
    print("=" * 60)

    # --- Trường hợp 1: Mảng SỐ ---
    print("\n--- TRƯỜNG HỢP 1: Mảng SỐ ---")
    X_num = [0, 1, 2, 3, 4, 5]
    Y_num = [-5, 2, 8, -1, 0, 3] # y = f(x)
    y_bar_num = 0 # Tìm f(x) = 0
    
    print("Input:")
    print(f"  X = {X_num}")
    print(f"  Y = {Y_num}")
    print(f"  y_bar = {y_bar_num}")
    
    # Gọi hàm với verbose=True để in các bước (hàm sẽ tự in kết quả ở Bước 5)
    ket_qua_1 = tim_khoang_cach_ly(X_num, Y_num, y_bar_num, verbose=True)
    
    print("\nKết quả cuối cùng (Trường hợp 1):")
    
    print("\n" + "=" * 60)

    # --- Trường hợp 2: Mảng BIỂU THỨC (X biểu thức, Y là số) ---
    print("\n--- TRƯỜNG HỢP 2: Mảng BIỂU THỨC (X là biểu thức) ---")
    X_sym = ["a", "a+h", "a+2*h", "a+3*h"]
    Y_sym = [10, -2, 5, 1] # Y vẫn phải là số
    y_bar_sym = 0
    
    print("Input:")
    print(f"  X = {X_sym}")
    print(f"  Y = {Y_sym}")
    print(f"  y_bar = {y_bar_sym}")
    
    # Gọi hàm với verbose=True để in các bước
    ket_qua_2 = tim_khoang_cach_ly(X_sym, Y_sym, y_bar_sym, verbose=True)
    
    print("\nKết quả cuối cùng (Trường hợp 2):")
    # print(f"Các khoảng cách ly nghiệm: {ket_qua_2}") # Đã được in ở Bước 5
    print("(Mong đợi: [['a', 'a+h'], ['a+h', 'a+2h']])")

    print("\n" + "=" * 60)
    
    # --- Trường hợp 3: Thử nghiệm thất bại (Y là biểu thức) ---
    print("\n--- TRƯỜNG HỢP 3: Thử nghiệm thất bại (Y là biểu thức) ---")
    X_fail = [0, 1]
    Y_fail = ["y0", "y1"]
    y_bar_fail = 0
    
    print("Input:")
    print(f"  X = {X_fail}")
    print(f"  Y = {Y_fail}")
    print(f"  y_bar = {y_bar_fail}")
    
    # Hàm sẽ tự in lỗi ở Bước 2
    ket_qua_3 = tim_khoang_cach_ly(X_fail, Y_fail, y_bar_fail, verbose=True)
    print(f"Kết quả cuối cùng (Trường hợp 3): {ket_qua_3}")


if __name__ == "__main__":
    chay_vi_du_cach_ly()