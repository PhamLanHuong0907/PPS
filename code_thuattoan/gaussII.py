# --- (File: gaussII.py) ---
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
        """Hàm nội bộ để xây dựng và IN bảng sai phân."""
        
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
    print("LỖI: File 'gaussII.py' yêu cầu file 'newton_tien_moccachdeu.py'")
    print("     phải nằm chung thư mục để tận dụng code.")
    sys.exit(1)

def xay_dung_da_thuc_gauss_2(X_input, Y_input, j0):
    """
    Xây dựng biểu thức đa thức nội suy P(x)
    sử dụng thuật toán GAUSS II (Gauss Backward).
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT CÁC BƯỚC)

    :param X_input: Mảng X đã được trích xuất (k mốc)
    :param Y_input: Mảng Y đã được trích xuất (k giá trị)
    :param j0: Chỉ số (index) của mốc trung tâm x0 trong mảng X
    :return: (P_n, P_n_expanded)
    """
    
    print("\n--- Bắt đầu thuật toán xây dựng Đa thức Gauss II ---")

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
    else:
        h = 1
    print(f"  -> h = {h}")
    
    x0 = X[j0]
    
    # --- 3. Thiết lập điều kiện dừng ---
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Không cần thiết lập (lặp bằng bảng).")
    
    # --- 4. Thực hiện tính toán ---
    print(f"[Bước 4] Thực hiện tính toán:")
    
    # Bước 4.1: Lập "Bảng sai phân tiến" D (Tận dụng code)
    # (Hàm _xay_dung_bang_sai_phan_tien sẽ tự in các bước con)
    D_table = _xay_dung_bang_sai_phan_tien(Y, n)
    
    # Bước 4.2: Lấy mảng hệ số D_coeff (LOGIC ĐÚNG CỦA GAUSS II)
    # Đường chéo: y0, Delta(y_{-1}), Delta^2(y_{-1}), Delta^3(y_{-2}), ...
    # Chỉ số: D[j0][0], D[j0-1][1], D[j0-1][2], D[j0-2][3], D[j0-2][4], ...
    # Chỉ số hàng là: j0 - ceil(k/2)
    print(f"\n  [4.2] Lấy mảng hệ số D_coeff (lấy zigzag từ D_table):")
    print(f"    (Công thức chỉ số hàng: idx_row = j0 - ceil(k/2))")
    
    D_coeffs = [] 
    for k in range(n + 1):
        # i = ceil(k/2)
        # (k + 1) // 2 trong Python là phép toán ceil(k/2) cho số nguyên
        i_term = (k + 1) // 2 
        idx_row = j0 - i_term
        
        print(f"    k = {k}: i=ceil(k/2) = {i_term}. D_coeff[{k}] = D[j0-i][k] = D[{idx_row}][{k}]")
            
        if 0 <= idx_row <= n:
            D_coeffs.append(D_table[idx_row][k])
            print(f"      -> Lấy D[{idx_row}][{k}] = {D_table[idx_row][k]}")
        else:
            # Không đủ sai phân, dừng lại
            print(f"    -> Dừng vì idx_row = {idx_row} nằm ngoài [0, {n}]")
            break
    print(f"    -> Hệ số D_coeffs = {D_coeffs}")
            
    # Bước 4.3: Tính biểu thức t
    x = sympy.symbols('x')
    t = (x - x0) / h
    print(f"\n  [4.3] Tính t = (x - x0) / h")
    print(f"    t = (x - {x0}) / {h} = {t}")
    
    # --- 5. Xác định output (Xây dựng đa thức P(x) theo Bước 5) ---
    print(f"\n[Bước 5] Xác định output (Xây dựng P(x) từ D_coeffs và t):")
    
    P_n = D_coeffs[0] # Đa thức P(x)
    term_t = sympy.sympify(1) # Tích các (t+i)
    
    print(f"  Khởi tạo: P(x) = D_coeffs[0] = {P_n}")
    
    for k in range(1, len(D_coeffs)):
        print(f"    --- k = {k} ---")
        
        # Cập nhật tích term_t theo công thức Bước 5
        if k == 1:
            term_t = t
            print(f"      Tích t_term = t = {term_t}")
        else:
            i_term = k // 2
            if k % 2 == 0: # k chẵn (2, 4, ...): nhân (t+i)
                # k=2 -> i=1 -> (t+1)
                new_factor = (t + i_term)
                term_t = term_t * new_factor
                print(f"      k chẵn. Tích t_term = t_term * (t + {i_term}) = {term_t}")
            else: # k lẻ (3, 5, ...): nhân (t-i)
                # k=3 -> i=1 -> (t-1)
                new_factor = (t - i_term)
                term_t = term_t * new_factor
                print(f"      k lẻ. Tích t_term = t_term * (t - {i_term}) = {term_t}")
        
        # Cập nhật P_n
        k_factorial = sympy.factorial(k)
        P_n_old = P_n
        P_n = P_n + (D_coeffs[k] * term_t / k_factorial)
        
        print(f"      P(x) = P(x) + (D_coeffs[{k}] * t_term / {k}!)")
        print(f"      P(x) = {P_n_old} + ({D_coeffs[k]} * {term_t} / {k_factorial})")
        print(f"      -> P(x) (chưa rút gọn) = {P_n}")
    
    print("\n  Rút gọn P(x)...")
    P_n_expanded = sympy.expand(P_n)

    print(f"\n  Đa thức P(x) (dạng Gauss II) = {P_n}")
    print(f"  Đa thức P(x) (dạng rút gọn) = {P_n_expanded}")
    print("--- Kết thúc thuật toán ---")

    return P_n, P_n_expanded