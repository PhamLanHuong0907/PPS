# ... (Giữ nguyên tất cả code đã có:
# _xay_dung_bang_sai_phan_tien,
# xay_dung_da_thuc_gauss_1,
# tinh_gia_tri_gauss_1) ...

# --------------------------------------------------------------------
# BỔ SUNG HÀM MỚI CHO GAUSS II
# --------------------------------------------------------------------
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

def xay_dung_da_thuc_gauss_2(X_input, Y_input, j0):
    """
    Xây dựng biểu thức đa thức nội suy P(x)
    sử dụng thuật toán GAUSS II (Gauss Backward).

    LƯU Ý: Bước 4.2 trong ảnh của bạn bị sai. Code này
    triển khai logic ĐÚNG để khớp với công thức ở Bước 5.

    :param X_input: Mảng X đã được trích xuất (k mốc)
    :param Y_input: Mảng Y đã được trích xuất (k giá trị)
    :param j0: Chỉ số (index) của mốc trung tâm x0 trong mảng X
    :return: (P_n, P_n_expanded)
             P_n: Đa thức dạng Gauss II (chưa rút gọn)
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
    
    # Bước 4.1: Lập "Bảng sai phân tiến" D (Tận dụng code)
    D_table = _xay_dung_bang_sai_phan_tien(Y, n)
    
    # Bước 4.2: Lấy mảng hệ số D_coeff (LOGIC ĐÚNG CỦA GAUSS II)
    # Đường chéo: y0, Delta(y_{-1}), Delta^2(y_{-1}), Delta^3(y_{-2}), ...
    # Chỉ số: D[j0][0], D[j0-1][1], D[j0-1][2], D[j0-2][3], D[j0-2][4], ...
    # Chỉ số hàng là: j0 - ceil(k/2)
    D_coeffs = [] 
    for k in range(n + 1):
        # i = ceil(k/2)
        # (k + 1) // 2 trong Python là phép toán ceil(k/2) cho số nguyên
        i_term = (k + 1) // 2 
        idx_row = j0 - i_term
            
        if 0 <= idx_row <= n:
            D_coeffs.append(D_table[idx_row][k])
        else:
            # Không đủ sai phân, dừng lại
            break
            
    # Bước 4.3: Tính biểu thức t
    x = sympy.symbols('x')
    t = (x - x0) / h
    
    # --- 5. Xác định output (Xây dựng đa thức P(x) theo Bước 5) ---
    
    P_n = D_coeffs[0] # Đa thức P(x)
    term_t = sympy.sympify(1) # Tích các (t+i)
    
    for k in range(1, len(D_coeffs)):
        # Cập nhật tích term_t theo công thức Bước 5
        if k == 1:
            term_t = t
        else:
            i_term = k // 2
            if k % 2 == 0: # k chẵn (2, 4, ...): nhân (t+i)
                # k=2 -> i=1 -> (t+1)
                # k=4 -> i=2 -> (t+2)
                term_t = term_t * (t + i_term)
            else: # k lẻ (3, 5, ...): nhân (t-i)
                # k=3 -> i=1 -> (t-1)
                # k=5 -> i=2 -> (t-2)
                term_t = term_t * (t - i_term)
            
        P_n = P_n + (D_coeffs[k] * term_t / sympy.factorial(k))
    
    P_n_expanded = sympy.expand(P_n)

    return P_n, P_n_expanded