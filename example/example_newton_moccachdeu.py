import os
import sys
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    # Đảm bảo bạn đang import file "newton_tien_moccachdeu.py" đã được chỉnh sửa
    from newton_tien_moccachdeu import tim_he_so_newton_cach_deu
except ImportError:
    print("Lỗi: Không tìm thấy file 'newton_tien_moccachdeu.py'.")
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

def chay_vi_du_cach_deu():
    print("\n" + "="*50)
    print("  CHẠY VÍ DỤ CHO MỐC CÁCH ĐỀU (SAI PHÂN TIẾN)")
    print("="*50)

    # --- Ví dụ 1: Input là SỐ ---
    print("\n--- Ví dụ 1: Input là SỐ (mốc cách đều) ---")
    # P(x) = x^2 + x + 1. Đi qua (0,1), (1,3), (2,7)
    X1 = [0, 1, 2]
    Y1 = [1, 3, 7]
    print(f"X = {X1}, Y = {Y1}")
    
    # Hàm thuật toán sẽ tự in các bước và hệ số C
    C1 = tim_he_so_newton_cach_deu(X1, Y1)
    
    if C1:
        # print(f"Hệ số Newton C = {C1}") # Đã được in trong hàm
        hien_thi_da_thuc(C1, X1)

    # --- Ví dụ 2: Input là SỐ KẾT HỢP BIỂU THỨC ---
    print("\n--- Ví dụ 2: Input là SỐ KẾT HỢP BIỂU THỨC ---")
    # Mốc cách đều h = 2
    X2 = ["a+1", "a+3", "a+5"]
    Y2 = [5, "a", "b"]
    print(f"X = {X2}, Y = {Y2}")
    
    # Hàm thuật toán sẽ tự in các bước và hệ số C
    C2 = tim_he_so_newton_cach_deu(X2, Y2)
    
    if C2:
        # print(f"Hệ số Newton C = {C2}") # Đã được in trong hàm
        hien_thi_da_thuc(C2, X2)

    # --- Ví dụ 3: Thử trường hợp mốc không cách đều ---
    print("\n--- Ví dụ 3: Thử mốc KHÔNG cách đều ---")
    X3 = [0, 1, 3] # h=1, h=2 -> Lỗi
    Y3 = [1, 3, 13]
    print(f"X = {X3}, Y = {Y3}")
    
    # Hàm sẽ tự in lỗi ở Bước 2
    C3 = tim_he_so_newton_cach_deu(X3, Y3)


if __name__ == "__main__":
    chay_vi_du_cach_deu()