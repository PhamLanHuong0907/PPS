import sympy
import sys

# === HÀM MỚI ĐƯỢC THÊM VÀO ĐỂ IN MA TRẬN ===
def print_matrix(matrix, n, title="Trạng thái ma trận D:"):
    """
    Hàm tiện ích để in ma trận (bảng sai phân) D.
    """
    print(f"\n    {title}")
    col_width = 15 # Độ rộng cột
    header_cols = []
    for j in range(n + 1):
        header_cols.append(f"j={j:<{col_width-2}}")
    print(f"      | {' | '.join(header_cols)}")
    print("-" * (len(header_cols) * (col_width + 2) + 6))
    for i in range(n + 1):
        row_cells = []
        for j in range(n + 1):
            cell_val = matrix[i][j]
            if cell_val == 0: cell_str = "0"
            else: cell_str = str(sympy.simplify(cell_val))
            cell_str = f"{cell_str:<{col_width}}"
            if j > (n - i):
                 cell_str = f"{'.':<{col_width}}"
            row_cells.append(cell_str)
        print(f"i={i:<2}   | {' | '.join(row_cells)}")
    print("") 
# ========================================

# Tận dụng (reuse) logic từ file code trước đó
try:
    # Lấy hàm _build_forward_diff_table từ thư viện Newton
    from newton_tien_moccachdeu import tim_he_so_newton_cach_deu as _newton_forward
    
    # Tạo một hàm riêng chỉ để xây dựng bảng
    # (ĐÃ CẬP NHẬT HÀM NÀY ĐỂ IN CHI TIẾT)
    def _xay_dung_bang_sai_phan_tien(Y_sym, n):
        print(f"  [4.1] Lập \"Bảng sai phân tiến\" (ma trận D kích thước {n+1}x{n+1}).")
        
        D_table = [[sympy.sympify(0) for _ in range(n + 1)] for _ in range(n + 1)]
        # In ma trận ban đầu
        print_matrix(D_table, n, f"Ma trận D ban đầu (khởi tạo 0)")

        # Gán cột 0
        print(f"    Gán cột 0: D[i][0] = Y[i] (cho i từ 0 đến {n})")
        for i in range(n + 1):
            D_table[i][0] = Y_sym[i]
        
        # In ma trận sau khi gán cột 0
        print_matrix(D_table, n, f"Ma trận D sau khi gán cột 0")

        # Lặp j (cột) và i (hàng)
        print(f"\n    Lặp j từ 1 đến {n} (cột) và i từ 0 đến {n}-j (hàng) để tính D[i][j]:")
        print(f"      (Công thức: D[i][j] = D[i+1][j-1] - D[i][j-1])")
        
        for j in range(1, n + 1):
            print(f"      --- Tính Cột j = {j} ---")
            for i in range(n - j + 1):
                val_i_plus_1 = D_table[i+1][j-1]
                val_i = D_table[i][j-1]
                D_table[i][j] = val_i_plus_1 - val_i
                print(f"        i = {i}: Tính D[{i}][{j}] = D[{i+1}][{j-1}] - D[{i}][{j-1}]")
                print(f"          = {val_i_plus_1} - {val_i} = {D_table[i][j]}")

        print("\n    --- Hoàn thành tính toán Bảng D ---")
        # In ma trận sau khi tính toán xong
        print_matrix(D_table, n, f"Ma trận D hoàn chỉnh")
        return D_table

except ImportError:
    print("LỖI: File 'gaussI.py' yêu cầu file 'newton_tien_moccachdeu.py'")
    print("     phải nằm chung thư mục để tận dụng code.")
    sys.exit(1)


# HÀM MỚI (Theo yêu cầu của bạn)
def xay_dung_da_thuc_gauss_1(X_input, Y_input, j0):
    """
    Xây dựng biểu thức đa thức nội suy P(x)
    sử dụng thuật toán GAUSS I (Gauss Forward).
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT CÁC BƯỚC)

    :param X_input: Mảng X đã được trích xuất (k mốc)
    :param Y_input: Mảng Y đã được trích xuất (k giá trị)
    :param j0: Chỉ số (index) của mốc trung tâm x0 trong mảng X
    :return: (P_n, P_n_expanded)
    """
    
    print("\n--- Bắt đầu thuật toán xây dựng Đa thức Gauss I ---")
    
    # --- Chuyển đổi input (dùng SymPy) ---
    try:
        X = [sympy.sympify(val) for val in X_input]
        Y = [sympy.sympify(val) for val in Y_input]
    except sympy.SympifyError as e:
        print(f"Lỗi: Input không hợp lệ. '{e}'", file=sys.stderr)
        return None, None

    # --- 1. Xác định input ---
    print(f"[Bước 1] Xác định input:")
    n = len(X) - 1 
    print(f"  X (Mảng) = {X_input}")
    print(f"  Y (Mảng) = {Y_input}")
    print(f"  n (Bậc) = {n} (có {n+1} điểm)")
    print(f"  j0 (Chỉ số mốc trung tâm) = {j0} (tương ứng X[j0] = {X_input[j0]})")

    # --- 2. Kiểm tra input ---
    print(f"[Bước 2] Kiểm tra điều kiện input:")
    if n < 0 or not (0 <= j0 <= n):
        print("  Lỗi: Dữ liệu rỗng hoặc j0 nằm ngoài [0, n].", file=sys.stderr)
        return None, None
    print(f"  -> n = {n} >= 0. (Hợp lệ)")
    print(f"  -> j0 = {j0} trong [0, {n}]. (Hợp lệ)")
    
    print(f"  Kiểm tra mốc cách đều (tính h):")
    if n > 0:
        h = sympy.simplify(X[1] - X[0])
        # (Giả định mốc đã cách đều sau khi trích xuất)
    else:
        h = 1
    print(f"  -> h = {h}")
    
    x0 = X[j0]
    
    # --- 3. Thiết lập điều kiện dừng ---
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Không cần thiết lập (lặp bằng bảng).")
    
    # --- 4. Thực hiện tính toán ---
    print(f"[Bước 4] Thực hiện tính toán:")
    
    # Bước 4.1: Lập "Bảng sai phân tiến" D
    # (Hàm _xay_dung_bang_sai_phan_tien sẽ tự in các bước con)
    D_table = _xay_dung_bang_sai_phan_tien(Y, n)
    
    # Bước 4.2: Lấy mảng hệ số C
    print(f"\n  [4.2] Lấy mảng hệ số C (lấy zigzag từ D_table):")
    C = [] 
    for k in range(n + 1):
        idx_row = -1
        if k == 0:
            idx_row = j0 
            print(f"    k = {k} (k=0): C[0] = D[j0][0] = D[{idx_row}][0] = {D_table[idx_row][k]}")
        
        elif k % 2 == 1: # k lẻ
            i_term = (k + 1) // 2
            idx_row = j0 - (i_term - 1)
            print(f"    k = {k} (lẻ): i=(k+1)/2 = {i_term}. C[{k}] = D[j0-(i-1)][k] = D[{idx_row}][{k}] = {D_table[idx_row][k]}")
        
        elif k % 2 == 0: # k chẵn
            i_term = k // 2
            idx_row = j0 - i_term
            print(f"    k = {k} (chẵn): i=k/2 = {i_term}. C[{k}] = D[j0-i][k] = D[{idx_row}][{k}] = {D_table[idx_row][k]}")
        
        # (Thuật toán trong code có kiểm tra biên, ta giữ nguyên)
        if 0 <= idx_row <= n:
            C.append(D_table[idx_row][k])
        else:
            print(f"    -> Dừng vì idx_row = {idx_row} nằm ngoài [0, {n}]")
            break
    print(f"    -> Hệ số C = {C}")
            
    # Bước 4.3: Tính biểu thức t
    x = sympy.symbols('x') 
    t = (x - x0) / h
    print(f"\n  [4.3] Tính t = (x - x0) / h")
    print(f"    t = (x - {x0}) / {h} = {t}")
    
    # --- 5. Xác định output (Xây dựng đa thức P(x)) ---
    print(f"\n[Bước 5] Xác định output (Xây dựng P(x) từ C và t):")
    
    P_n = C[0] 
    term_t = sympy.sympify(1) 
    
    print(f"  Khởi tạo: P(x) = C[0] = {P_n}")
    
    for k in range(1, len(C)):
        print(f"    --- k = {k} ---")
        
        # Cập nhật tích term_t (tích các (t-i))
        if k == 1:
            term_t = t
            print(f"      Tích t_term = t = {term_t}")
        elif k % 2 == 0: # k chẵn (2, 4, 6...)
            i_term = (k // 2) - 1
            new_factor = (t - (i_term + 1)) # (t-1), (t-2), ...
            term_t = term_t * new_factor
            print(f"      k chẵn. Tích t_term = t_term * (t - {i_term+1}) = {term_t}")
        else: # k lẻ (3, 5, 7...)
            i_term = (k - 1) // 2
            new_factor = (t + i_term) # (t+1), (t+2), ...
            term_t = term_t * new_factor
            print(f"      k lẻ. Tích t_term = t_term * (t + {i_term}) = {term_t}")
        
        # Cập nhật đa thức P_n
        k_factorial = sympy.factorial(k)
        P_n_old = P_n
        P_n = P_n + (C[k] * term_t / k_factorial)
        
        print(f"      P(x) = P(x) + (C[{k}] * t_term / {k}!)")
        print(f"      P(x) = {P_n_old} + ({C[k]} * {term_t} / {k_factorial})")
        print(f"      -> P(x) (chưa rút gọn) = {P_n}")
    
    print("\n  Rút gọn P(x)...")
    P_n_expanded = sympy.expand(P_n)

    print(f"\n  Đa thức P(x) (dạng Gauss) = {P_n}")
    print(f"  Đa thức P(x) (dạng rút gọn) = {P_n_expanded}")
    print("--- Kết thúc thuật toán ---")

    return P_n, P_n_expanded


# HÀM CŨ (Dùng để tính giá trị, vẫn giữ lại)
# (Hàm này giờ sẽ tự động in chi tiết vì nó gọi hàm xay_dung... ở trên)
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