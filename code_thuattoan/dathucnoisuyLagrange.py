import sympy
import sys

def xay_dung_da_thuc_lagrange(X, Y):
    """
    Xây dựng đa thức nội suy Lagrange P(x) từ các mốc X và giá trị Y.
    Hàm này trả về cả biểu thức symbolic P(x) và danh sách các hệ số A
    của đa thức (ví dụ: [a_n, a_{n-1}, ..., a_0]).

    (Dựa trên thuật toán trong ảnh bạn cung cấp)

    Tham số:
    X (list): Mảng (danh sách) n + 1 mốc nội suy [x0, x1, ..., xn].
    Y (list): Mảng (danh sách) n + 1 giá trị tương ứng [y0, y1, ..., yn].

    Trả về:
    tuple: (P_n, A)
           P_n (sympy.Expr): Biểu thức đa thức P(x) đã được rút gọn.
           A (list): Danh sách các hệ số của P(x) [a_n, ..., a_0].
           Hoặc (None, None) nếu input không hợp lệ.
    """
    
    # --- 1. Xác định input ---
    n = len(X) - 1 # Bậc của đa thức
    
    # --- 2. Kiểm tra điều kiện của input ---
    if n < 0:
        print("Lỗi: Mảng X và Y không được rỗng.", file=sys.stderr)
        return None, None
        
    if len(X) != len(Y):
        print("Lỗi: Mảng X và Y phải có cùng kích thước.", file=sys.stderr)
        return None, None
        
    # Kiểm tra các mốc x_i có phân biệt không
    if len(set(X)) != len(X):
        print(f"Lỗi: Các mốc nội suy X phải phân biệt. Tìm thấy giá trị trùng.", file=sys.stderr)
        return None, None

    # Khởi tạo biến symbolic 'x'
    x = sympy.symbols('x')

    # --- 4. Thực hiện tính toán ---
    
    # Bước 4.1: Khởi tạo đa thức tổng P_n(x) = 0
    P_n = sympy.sympify(0)
    
    print("--- Bắt đầu xây dựng đa thức ---")

    # Bước 4.2: Vòng lặp ngoài i chạy từ 0 đến n
    for i in range(n + 1):
        # (Tính P_n(x) = sum( Y[i] * L_i(x) ))
        
        # --- Bước 4.3 (Trong vòng lặp i): Xây dựng đa thức cơ sở L_i(x) ---
        N_i = sympy.sympify(1) # 4.3a
        D_i = sympy.sympify(1) # 4.3b
        
        for j in range(n + 1):
            if i != j:
                # 4.3a: Cập nhật N_i(x) = N_i(x) * (x - x_j)
                N_i = N_i * (x - X[j])
                
                # 4.3b: Cập nhật D_i = D_i * (x_i - x_j)
                D_i = D_i * (X[i] - X[j])
        
        # Bước 4.3c (Tính L_i(x))
        L_i = N_i / D_i
        
        # Bước 4.4 (Trong vòng lặp i): Cộng Y_i * L_i(x) vào đa thức tổng
        P_n = P_n + Y[i] * L_i
        
    # Bước 4.5: Sau vòng lặp, P_n là đa thức cần tìm
    P_n_expanded = sympy.expand(P_n)
    
    # --- 5. Xác định output ---
    P_poly = sympy.Poly(P_n_expanded, x)
    A = P_poly.all_coeffs()
    
    print("--- Hoàn thành ---")
    
    # Chuyển đổi các hệ số từ kiểu SymPy sang kiểu float/int chuẩn
    A = [float(coeff) if coeff.is_Float else int(coeff) for coeff in A]

    return P_n_expanded, A