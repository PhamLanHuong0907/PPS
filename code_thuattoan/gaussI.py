import sympy
import sys

# Tận dụng (reuse) logic từ file code trước đó
try:
    # Lấy hàm _build_forward_diff_table từ thư viện Newton
    from newton_tien_moccachdeu import tim_he_so_newton_cach_deu as _newton_forward
    
    # Tạo một hàm riêng chỉ để xây dựng bảng
    def _xay_dung_bang_sai_phan_tien(Y_sym, n):
        D_table = [[sympy.sympify(0) for _ in range(n + 1)] for _ in range(n + 1)]
        for i in range(n + 1):
            D_table[i][0] = Y_sym[i]
        for j in range(1, n + 1):
            for i in range(n - j + 1):
                D_table[i][j] = D_table[i+1][j-1] - D_table[i][j-1]
        return D_table

except ImportError:
    print("LỖI: File 'thu_vien_gauss.py' yêu cầu file 'thu_vien_newton_cach_deu.py'")
    print("     phải nằm chung thư mục để tận dụng code.")
    sys.exit(1)


# HÀM MỚI (Theo yêu cầu của bạn)
def xay_dung_da_thuc_gauss_1(X_input, Y_input, j0):
    """
    Xây dựng biểu thức đa thức nội suy P(x)
    sử dụng thuật toán GAUSS I (Gauss Forward).

    :param X_input: Mảng X đã được trích xuất (k mốc)
    :param Y_input: Mảng Y đã được trích xuất (k giá trị)
    :param j0: Chỉ số (index) của mốc trung tâm x0 trong mảng X
    :return: (P_n, P_n_expanded)
             P_n: Đa thức dạng Gauss (chưa rút gọn)
             P_n_expanded: Đa thức dạng a_n*x^n + ... (đã rút gọn)
    """
    
    # --- Chuyển đổi input (dùng SymPy) ---
    try:
        X = [sympy.sympify(val) for val in X_input]
        Y = [sympy.sympify(val) for val in Y_input]
    except sympy.SympifyError as e:
        print(f"Lỗi: Input không hợp lệ. '{e}'", file=sys.stderr)
        return None, None

    # --- 1. & 2. Xác định và Kiểm tra input ---
    n = len(X) - 1 
    if n < 0 or not (0 <= j0 <= n):
        print("Lỗi: Dữ liệu rỗng hoặc j0 nằm ngoài [0, n].", file=sys.stderr)
        return None, None
    
    if n > 0:
        h = sympy.simplify(X[1] - X[0])
    else:
        h = 1
    
    x0 = X[j0]
    
    # --- 4. Thực hiện tính toán ---
    
    # Bước 4.1: Lập "Bảng sai phân tiến" D
    D_table = _xay_dung_bang_sai_phan_tien(Y, n)
    
    # Bước 4.2: Lấy mảng hệ số C
    C = [] 
    for k in range(n + 1):
        idx_row = -1
        if k == 0:
            idx_row = j0 
        elif k % 2 == 1: 
            i_term = (k + 1) // 2
            idx_row = j0 - (i_term - 1)
        elif k % 2 == 0:
            i_term = k // 2
            idx_row = j0 - i_term
        if 0 <= idx_row <= n:
            C.append(D_table[idx_row][k])
        else:
            break
            
    # Bước 4.3: Tính biểu thức t
    x = sympy.symbols('x') # Đây là thay đổi quan trọng
    t = (x - x0) / h
    
    # --- 5. Xác định output (Xây dựng đa thức P(x)) ---
    
    P_n = C[0] # Đa thức P(x)
    term_t = sympy.sympify(1) 
    
    for k in range(1, len(C)):
        # Cập nhật tích term_t
        if k == 1:
            term_t = t
        elif k % 2 == 0: # k chẵn (2, 4, 6...)
            i_term = (k // 2) - 1
            term_t = term_t * (t - (i_term + 1)) # (t-1), (t-2), ...
        else: # k lẻ (3, 5, 7...)
            i_term = (k - 1) // 2
            term_t = term_t * (t + i_term) # (t+1), (t+2), ...
            
        P_n = P_n + (C[k] * term_t / sympy.factorial(k))
    
    P_n_expanded = sympy.expand(P_n)

    return P_n, P_n_expanded


# HÀM CŨ (Dùng để tính giá trị, vẫn giữ lại)
def tinh_gia_tri_gauss_1(X_input, Y_input, j0, x_target_input):
    """
    Tính giá trị nội suy P(x) tại x_target sử dụng
    thuật toán GAUSS I (Gauss Forward).
    """
    
    # Bước A: Xây dựng đa thức
    P_n, _ = xay_dung_da_thuc_gauss_1(X_input, Y_input, j0)
    
    if P_n is None:
        return None
        
    # Bước B: Thay giá trị vào đa thức
    try:
        x = sympy.symbols('x')
        x_target = sympy.sympify(x_target_input)
        P_val = P_n.subs(x, x_target)
        return sympy.simplify(P_val)
    except Exception as e:
        print(f"Lỗi khi thay giá trị: {e}", file=sys.stderr)
        return None