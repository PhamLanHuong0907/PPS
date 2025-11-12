import os
import sys
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    # Đảm bảo bạn đang import file "newton_lui_mocbatky.py" đã được chỉnh sửa
    from newton_lui_mocbatky import tim_he_so_newton_lui_bat_ky
except ImportError:
    print("Lỗi: Không tìm thấy file 'newton_lui_mocbatky.py'.")
    exit()
except ModuleNotFoundError:
    print("Lỗi: Chưa cài thư viện 'sympy'. Chạy 'pip install sympy'.")
    exit()

import sympy

def hien_thi_da_thuc_lui(D_coeffs, X_input):
    """
    Hàm tiện ích để in đa thức Newton LÙI từ hệ số D và mốc X.
    P(x) = d0 + d1(x-xn) + d2(x-xn)(x-x_{n-1}) + ...
    """
    x = sympy.symbols('x')
    X = [sympy.sympify(val) for val in X_input]
    n = len(X) - 1
    P_n = sympy.sympify(0)
    
    for k in range(len(D_coeffs)):
        term = D_coeffs[k]
        # Nhân với tích (x - x_n) * (x - x_{n-1}) * ...
        for i in range(k):
            term = term * (x - X[n - i])
        P_n = P_n + term
        
    print("\n  Hiển thị đa thức (dạng Newton Lùi):")
    print(f"    P(x) = {P_n}")
    print(f"  Dạng rút gọn (expand):")
    print(f"    P(x) = {sympy.expand(P_n)}")

def chay_vi_du_lui_bat_ky():
    print("\n" + "="*50)
    print("  CHẠY VÍ DỤ NEWTON LÙI (MỐC BẤT KỲ)")
    print("="*50)

    # --- Ví dụ 1: Input là SỐ ---
    print("\n--- Ví dụ 1: Input là SỐ (mốc không cách đều) ---")
    X1 = [0, 1, 3] # n=2
    Y1 = [1, 3, 13]
    print(f"X = {X1}, Y = {Y1}")
    
    # Hàm thuật toán sẽ tự in các bước và hệ số D
    D1 = tim_he_so_newton_lui_bat_ky(X1, Y1)
    
    if D1:
        # Bảng D: [ [1, 2, 1], [3, 5, 0], [13, 0, 0] ]
        # d0 = D[2][0] = 13
        # d1 = D[1][1] = 5
        # d2 = D[0][2] = 1
        
        # print(f"Hệ số Newton Lùi D = {D1}") # Đã được in trong hàm
        print("(Kiểm tra: Kết quả mong đợi: D = [13, 5, 1])")
        hien_thi_da_thuc_lui(D1, X1)

    # --- Ví dụ 2: Input là SỐ và CHỮ CÁI (biến) ---
    print("\n--- Ví dụ 2: Input là SỐ và CHỮ CÁI (biến) ---")
    X2 = [0, 1] # n=1
    Y2 = ["y0", "y1"]
    print(f"X = {X2}, Y = {Y2}")
    
    # Hàm thuật toán sẽ tự in các bước và hệ số D
    D2 = tim_he_so_newton_lui_bat_ky(X2, Y2)
    
    if D2:
        # d0 = D[1][0] = y1
        # d1 = D[0][1] = y1 - y0
        
        # print(f"Hệ số Newton Lùi D = {D2}") # Đã được in trong hàm
        print("(Kiểm tra: Kết quả mong đợi: D = [y1, -y0 + y1])")
        hien_thi_da_thuc_lui(D2, X2)

if __name__ == "__main__":
    chay_vi_du_lui_bat_ky()