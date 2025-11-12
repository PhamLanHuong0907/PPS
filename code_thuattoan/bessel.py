import sympy
import sys
import math

# --- HÀM HỖ TRỢ (PRIVATE) ---
def _xay_dung_bang_sai_phan_tien(Y_sym, n):
    """
    Xây dựng bảng sai phân tiến D.
    D[i][j] = Delta^j (y_i)
    """
    D_table = [[sympy.sympify(0) for _ in range(n + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        D_table[i][0] = Y_sym[i]
    for j in range(1, n + 1):
        for i in range(n - j + 1):
            D_table[i][j] = D_table[i+1][j-1] - D_table[i][j-1]
    return D_table

# --- HÀM CHÍNH (PUBLIC) ---
def xay_dung_da_thuc_bessel(X_input, Y_input, j_s):
    """
    Xây dựng biểu thức đa thức nội suy P(x)
    sử dụng thuật toán BESSEL (theo ảnh).

    :param X_input: Mảng X đã được trích xuất (k mốc, k PHẢI LÀ SỐ CHẴN)
    :param Y_input: Mảng Y đã được trích xuất (k giá trị)
    :param j_s: Chỉ số (index) của mốc x_s trong mảng X_input.
                (x_s là mốc ngay trước khoảng trung tâm).
    
    :return: (P_n, P_n_expanded, D_table, B_coeffs, t)
             hoặc (None, None, None, None, None) nếu lỗi.
    """
    
    # --- Chuyển đổi input (dùng SymPy) ---
    try:
        X = [sympy.sympify(val) for val in X_input]
        Y = [sympy.sympify(val) for val in Y_input]
    except sympy.SympifyError as e:
        print(f"Lỗi: Input không hợp lệ. '{e}'", file=sys.stderr)
        return None, None, None, None, None

    # --- 1. & 2. Xác định và Kiểm tra input ---
    n = len(X) - 1 # n là BẬC (ví dụ: 5, nếu k=6)
    k_points = n + 1
    
    # Yêu cầu quan trọng của Bessel (theo ảnh): n+1 = 2m (số mốc chẵn)
    if k_points % 2 != 0:
        print(f"Lỗi Bessel: Số mốc ({k_points}) phải là số chẵn.", file=sys.stderr)
        return None, None, None, None, None
    if not (0 <= j_s < n): # j_s phải là chỉ số hợp lệ, và j_s+1 cũng phải tồn tại
        print(f"Lỗi: j_s={j_s} không hợp lệ cho mảng n={n}.", file=sys.stderr)
        return None, None, None, None, None
    
    if n > 0:
        h = sympy.simplify(X[1] - X[0])
    else:
        h = 1
    
    # Mốc cơ sở của Bessel
    x_s = X[j_s]
    
    # --- 4. Thực hiện tính toán ---
    
    # Bước 4.1: Lập "Bảng sai phân tiến" D
    D_table = _xay_dung_bang_sai_phan_tien(Y, n)
    
    # Bước 4.2: Lấy mảng hệ số B (Hệ số Bessel)
    B_coeffs = []
    
    for k in range(n + 1): # k chạy từ 0 đến n
        # Khởi tạo giá trị tạm
        B_k = sympy.sympify(0)
        
        try:
            if k == 0:
                B_k = (D_table[j_s][0] + D_table[j_s + 1][0]) / 2
            
            elif k % 2 == 1: # k lẻ (k = 2i - 1)
                i = (k + 1) // 2
                idx_row = j_s - i + 1
                B_k = D_table[idx_row][k]
            
            else: # k chẵn (k = 2i)
                i = k // 2
                idx_row_1 = j_s - i + 1
                idx_row_2 = j_s - i
                B_k = (D_table[idx_row_1][k] + D_table[idx_row_2][k]) / 2
            
            B_coeffs.append(B_k)
            
        except IndexError:
            # Nếu chỉ số (ví dụ j_s - i) bị văng ra ngoài bảng,
            # nghĩa là chúng ta không có đủ sai phân. Dừng lại.
            break
            
    # Bước 4.3: Tính biểu thức t
    x = sympy.symbols('x')
    t = (x - x_s) / h
    
    # --- 5. Xác định output (Xây dựng đa thức P(x) theo Bước 5) ---
    P_n = B_coeffs[0]
    
    # term_t_product_even: Lưu tích chẵn, ví dụ t(t-1)
    # Dùng cho cả k=2, 3, 4, 5, ...
    term_t_product_even = sympy.sympify(1) 
    
    for k in range(1, len(B_coeffs)):
        term_t = sympy.sympify(1)
        
        if k == 1:
            term_t = (t - sympy.Rational(1, 2)) # t - 1/2
        
        elif k == 2:
            term_t = t * (t - 1)
            term_t_product_even = term_t # Lưu lại
        
        elif k % 2 == 1: # k lẻ (3, 5, ...)
            # Lấy tích chẵn k-1 (ví dụ B[2]'s product) và nhân (t - 1/2)
            term_t = term_t_product_even * (t - sympy.Rational(1, 2))
        
        else: # k chẵn (4, 6, ...)
            # Lấy tích chẵn k-2 (ví dụ B[2]'s product)
            # nhân với 2 yếu tố mới (t+i-1) và (t-i)
            i = k // 2
            term_t = term_t_product_even * (t + i - 1) * (t - i)
            term_t_product_even = term_t # Cập nhật
            
        P_n = P_n + (B_coeffs[k] * term_t / sympy.factorial(k))
    
    P_n_expanded = sympy.expand(P_n)

    # Trả về tất cả kết quả trung gian
    return P_n, P_n_expanded, D_table, B_coeffs, t