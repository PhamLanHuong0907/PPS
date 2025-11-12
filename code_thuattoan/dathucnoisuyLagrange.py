import sympy
import sys

def xay_dung_da_thuc_lagrange(X, Y):
    """
    Xây dựng đa thức nội suy Lagrange P(x) từ các mốc X và giá trị Y.
    Hàm này trả về cả biểu thức symbolic P(x) và danh sách các hệ số A
    của đa thức (ví dụ: [a_n, a_{n-1}, ..., a_0]).

    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT CÁC BƯỚC)

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
    print("\n--- Bắt đầu thuật toán xây dựng đa thức Lagrange ---")
    print(f"[Bước 1] Xác định input:")
    n = len(X) - 1 # Bậc của đa thức
    print(f"  X (mốc nội suy) = {X}")
    print(f"  Y (giá trị) = {Y}")
    print(f"  n (bậc đa thức) = len(X) - 1 = {n}")

    # Khởi tạo biến symbolic 'x' (cần cho việc in ấn)
    x = sympy.symbols('x')
    
    # --- 2. Kiểm tra điều kiện của input ---
    print(f"[Bước 2] Kiểm tra điều kiện input:")
    if n < 0:
        print("  Lỗi: Mảng X và Y không được rỗng (n >= 0).")
        return None, None
    print(f"  -> n = {n} >= 0. (Hợp lệ)")
        
    if len(X) != len(Y):
        print(f"  Lỗi: Mảng X ({len(X)}) và Y ({len(Y)}) phải có cùng kích thước.")
        return None, None
    print(f"  -> Kích thước X và Y bằng nhau (n+1 = {n+1}). (Hợp lệ)")
        
    # Kiểm tra các mốc x_i có phân biệt không
    if len(set(X)) != len(X):
        print(f"  Lỗi: Các mốc nội suy X phải phân biệt. Tìm thấy giá trị trùng.")
        return None, None
    print(f"  -> Các mốc X phân biệt. (Hợp lệ)")

    # --- 3. Thiết lập điều kiện dừng ---
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Không cần thiết lập điều kiện dừng (vòng lặp for xác định).")
    
    # --- 4. Thực hiện tính toán ---
    print(f"[Bước 4] Thực hiện tính toán:")
    
    # Bước 4.1: Khởi tạo đa thức tổng P_n(x) = 0
    P_n = sympy.sympify(0)
    print(f"  [4.1] Khởi tạo đa thức tổng: P_n(x) = {P_n}")
    
    # Bước 4.2: Vòng lặp ngoài i chạy từ 0 đến n
    print(f"  [4.2] Bắt đầu vòng lặp ngoài (i = 0 đến {n}) để tính P_n = sum(Y_i * L_i(x))")

    for i in range(n + 1):
        print(f"\n    --- i = {i} (Tính L_{i}(x) và Y_{i}*L_{i}(x)) ---")
        
        # --- Bước 4.3 (Trong vòng lặp i): Xây dựng đa thức cơ sở L_i(x) ---
        print(f"    [4.3] Xây dựng đa thức cơ sở L_{i}(x):")
        
        # 4.3a: Tính tử số N_i(x)
        N_i = sympy.sympify(1) 
        print(f"      [4.3a] Tính tử số N_{i}(x) = Tích(x - x_j) với j != {i}")
        print(f"        Khởi tạo N_{i} = 1")
        
        # 4.3b: Tính mẫu số D_i
        D_i = sympy.sympify(1) 
        print(f"      [4.3b] Tính mẫu số D_{i} = Tích(x_{i} - x_j) với j != {i}")
        print(f"        Khởi tạo D_{i} = 1")

        print(f"        Bắt đầu vòng lặp j = 0 đến {n} (bỏ qua j = {i}):")
        for j in range(n + 1):
            if i != j:
                # Cập nhật N_i
                N_i_old = N_i
                N_i = N_i * (x - X[j])
                print(f"          j = {j}: N_{i} = N_{i}_cu * (x - x_{j}) = {N_i_old} * (x - {X[j]})")
                
                # Cập nhật D_i
                D_i_old = D_i
                term = (X[i] - X[j])
                D_i = D_i * term
                print(f"          j = {j}: D_{i} = D_{i}_cu * (x_{i} - x_{j}) = {D_i_old} * ({X[i]} - {X[j]}) = {D_i}")
            else:
                print(f"          j = {j}: Bỏ qua (vì j == i)")
        
        # Rút gọn tử số N_i (chưa expand)
        N_i = sympy.simplify(N_i)
        print(f"        -> N_{i}(x) (Tử số) = {N_i}")
        print(f"        -> D_{i} (Mẫu số) = {D_i}")
        
        # Bước 4.3c (Tính L_i(x))
        L_i = N_i / D_i
        print(f"      [4.3c] L_{i}(x) = N_{i}(x) / D_{i} = ({N_i}) / ({D_i})")
        # In dạng expand (khai triển) cho dễ đọc
        print(f"             L_{i}(x) (rút gọn) = {sympy.expand(L_i)}") 

        # Bước 4.4 (Trong vòng lặp i): Cộng Y_i * L_i(x) vào đa thức tổng
        P_n_old = P_n
        Y_i = Y[i]
        term_i = Y_i * L_i
        P_n = P_n + term_i
        
        print(f"    [4.4] Cập nhật đa thức tổng P_n(x) = P_n(x) + Y_{i} * L_{i}(x)")
        print(f"          P_n = P_n(cu) + {Y_i} * (L_{i})")
        # In P_n chưa rút gọn để thấy rõ phép cộng
        print(f"          -> P_n hiện tại (chưa rút gọn) = {P_n}")
            
    print("\n    --- Kết thúc vòng lặp i ---")
        
    # Bước 4.5: Sau vòng lặp, P_n là đa thức cần tìm
    print(f"  [4.5] Sau vòng lặp, P_n(x) = {P_n}")
    print(f"        Tiến hành rút gọn (expand) P_n(x)...")
    P_n_expanded = sympy.expand(P_n)
    print(f"        -> P_n(x) (đã rút gọn) = {P_n_expanded}")
    
    # --- 5. Xác định output ---
    print(f"[Bước 5] Xác định output:")
    P_poly = sympy.Poly(P_n_expanded, x)
    A = P_poly.all_coeffs()
    print(f"  -> Đa thức P(x) = {P_n_expanded}")
    
    # Chuyển đổi các hệ số từ kiểu SymPy sang kiểu float/int chuẩn
    try:
        A = [float(coeff) if coeff.is_Float else int(coeff) for coeff in A]
    except TypeError:
        # Giữ nguyên kiểu symbolic nếu không chuyển được (ví dụ: chứa biến)
        A = [coeff for coeff in A]
        
    print(f"  -> Mảng hệ số A (từ bậc cao đến thấp) = {A}")

    print("--- Hoàn thành ---")

    return P_n_expanded, A
