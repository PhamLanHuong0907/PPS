import os
import sys
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    # Đảm bảo bạn đang import file "newton_tien_mocbatky.py" đã được chỉnh sửa
    from newton_tien_mocbatky import tim_he_so_newton_bat_ky
except ImportError:
    print("Lỗi: Không tìm thấy file 'newton_tien_mocbatky.py'.")
    exit()
except ModuleNotFoundError:
    print("Lỗi: Chưa cài thư viện 'sympy'. Chạy 'pip install sympy'.")
    exit()

import sympy

def hien_thi_da_thuc(C, X_input):
    """Hàm tiện ích để in đa thức Newton từ hệ số C và mốc X."""
    x = sympy.symbols('x')
    X = [sympy.sympify(val) for val in X_input]
    P_n = sympy.sympify(0)
    
    for k in range(len(C)):
        term = C[k]
        for i in range(k):
            term = term * (x - X[i])
        P_n = P_n + term
    
    print("\n  Hiển thị đa thức (dạng Newton):")
    print(f"    P(x) = {P_n}")
    print(f"  Dạng rút gọn (expand):")
    print(f"    P(x) = {sympy.expand(P_n)}")

def chay_vi_du_bat_ky():
    print("\n" + "="*50)
    print("  CHẠY VÍ DỤ CHO MỐC BẤT KỲ (TỶ SAI PHÂN)")
    print("="*50)

    # --- Ví dụ 1: Input là SỐ ---
    print("\n--- Ví dụ 1: Input là SỐ (mốc không cách đều) ---")
    X1 = [0, 1, 3]
    Y1 = [1, 3, 13]
    print(f"X = {X1}, Y = {Y1}")
    
    # Hàm thuật toán sẽ tự in các bước và hệ số C
    C1 = tim_he_so_newton_bat_ky(X1, Y1)
    
    if C1:
        # Chỉ cần gọi hàm hiển thị đa thức
        hien_thi_da_thuc(C1, X1)

    # --- Ví dụ 2: Input là SỐ và CHỮ CÁI (biến) ---
    print("\n--- Ví dụ 2: Input là SỐ và CHỮ CÁI (biến) ---")
    X2 = [0, 1, 2]
    Y2 = ["y0", "y1", "y2"]
    print(f"X = {X2}, Y = {Y2}")
    
    # Hàm thuật toán sẽ tự in các bước và hệ số C
    C2 = tim_he_so_newton_bat_ky(X2, Y2)
    
    if C2:
        hien_thi_da_thuc(C2, X2)

    # --- Ví dụ 3: Input là SỐ KẾT HỢP BIỂU THỨC ---
    print("\n--- Ví dụ 3: Input là SỐ KẾT HỢP BIỂU THỨC ---")
    X3 = [1, "a"] # Mốc X cũng có thể là biểu thức
    Y3 = [3, "b"]
    print(f"X = {X3}, Y = {Y3}")
    
    # Hàm thuật toán sẽ tự in các bước và hệ số C
    C3 = tim_he_so_newton_bat_ky(X3, Y3)
    
    if C3:
        hien_thi_da_thuc(C3, X3)

if __name__ == "__main__":
    chay_vi_du_bat_ky()