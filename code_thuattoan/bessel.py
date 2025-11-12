import sympy
import sys
import math

# === HÀM MỚI ĐƯỢC THÊM VÀO ĐỂ IN MA TRẬN ===
def print_matrix(matrix, n, title="Trạng thái ma trận D:"):
    """
    Hàm tiện ích để in ma trận (bảng sai phân) D.
    """
    print(f"\n    {title}")
    
    # Tạo tiêu đề cột (j = 0...n)
    col_width = 15 # Độ rộng cột
    header_cols = []
    for j in range(n + 1):
        header_cols.append(f"j={j:<{col_width-2}}")
    print(f"      | {' | '.join(header_cols)}")
    print("-" * (len(header_cols) * (col_width + 2) + 6))

    # In từng hàng (i = 0...n)
    for i in range(n + 1):
        row_cells = []
        for j in range(n + 1):
            cell_val = matrix[i][j]
            
            # Rút gọn và chuyển sang chuỗi
            if cell_val == 0:
                 cell_str = "0"
            else:
                 cell_str = str(sympy.simplify(cell_val))
                 
            # Căn trái và giới hạn độ rộng
            cell_str = f"{cell_str:<{col_width}}"
            
            # Đánh dấu các ô chưa được tính
            if j > (n - i):
                 cell_str = f"{'.':<{col_width}}" # Dấu chấm cho ô ngoài phạm vi
                 
            row_cells.append(cell_str)
        
        print(f"i={i:<2}   | {' | '.join(row_cells)}")
    print("") # Thêm một dòng trống
# ========================================

# --- HÀM HỖ TRỢ (PRIVATE) ---
def _xay_dung_bang_sai_phan_tien(Y_sym, n):
    """
    Xây dựng bảng sai phân tiến D.
    D[i][j] = Delta^j (y_i)
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT)
    """
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
    print(f"\n    Lặp j từ 1 đến {n} (cột) và i từ 0 đến {n}-j (hàng):")
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

# --- HÀM CHÍNH (PUBLIC) ---
def xay_dung_da_thuc_bessel(X_input, Y_input, j_s):
    """
    Xây dựng biểu thức đa thức nội suy P(x)
    sử dụng thuật toán BESSEL (theo ảnh).
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT CÁC BƯỚC)

    :param X_input: Mảng X đã được trích xuất (k mốc, k PHẢI LÀ SỐ CHẴN)
    :param Y_input: Mảng Y đã được trích xuất (k giá trị)
    :param j_s: Chỉ số (index) của mốc x_s trong mảng X_input.
    
    :return: (P_n, P_n_expanded)
             hoặc (None, None) nếu lỗi.
    """
    
    print("\n--- Bắt đầu thuật toán xây dựng Đa thức Bessel ---")

    # --- Chuyển đổi input (dùng SymPy) ---
    try:
        X = [sympy.sympify(val) for val in X_input]
        Y = [sympy.sympify(val) for val in Y_input]
    except sympy.SympifyError as e:
        print(f"Lỗi: Input không hợp lệ. '{e}'", file=sys.stderr)
        return None, None

    # --- 1. Xác định input ---
    print(f"[Bước 1] Xác định input:")
    n = len(X) - 1 # n là BẬC (ví dụ: 5, nếu k=6)
    k_points = n + 1
    print(f"  X (Mảng) = {X_input}")
    print(f"  Y (Mảng) = {Y_input}")
    print(f"  n (Bậc) = {n} (có {k_points} điểm)")
    print(f"  j_s (Chỉ số mốc cơ sở) = {j_s} (tương ứng X[j_s] = {X_input[j_s]})")
    
    # --- 2. Kiểm tra input ---
    print(f"[Bước 2] Kiểm tra điều kiện input:")
    
    # Yêu cầu quan trọng của Bessel (theo ảnh): n+1 = 2m (số mốc chẵn)
    if k_points % 2 != 0:
        print(f"  Lỗi Bessel: Số mốc ({k_points}) phải là số chẵn.", file=sys.stderr)
        return None, None
    print(f"  -> Số mốc {k_points} là chẵn. (Hợp lệ)")
    
    if not (0 <= j_s < n): # j_s phải là chỉ số hợp lệ, và j_s+1 cũng phải tồn tại
        print(f"  Lỗi: j_s={j_s} không hợp lệ cho mảng n={n}.", file=sys.stderr)
        return None, None
    print(f"  -> j_s = {j_s} hợp lệ.")
    
    print(f"  Kiểm tra mốc cách đều (tính h):")
    if n > 0:
        h = sympy.simplify(X[1] - X[0])
    else:
        h = 1
    print(f"  -> h = {h}")
    
    # Mốc cơ sở của Bessel
    x_s = X[j_s]
    
    # --- 3. Thiết lập điều kiện dừng ---
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Không cần thiết lập (lặp bằng bảng).")
    
    # --- 4. Thực hiện tính toán ---
    print(f"[Bước 4] Thực hiện tính toán:")
    
    # Bước 4.1: Lập "Bảng sai phân tiến" D
    # (Hàm _xay_dung_bang_sai_phan_tien sẽ tự in các bước con)
    D_table = _xay_dung_bang_sai_phan_tien(Y, n)
    
    # Bước 4.2: Lấy mảng hệ số B (Hệ số Bessel)
    print(f"\n  [4.2] Lấy mảng hệ số B (Bessel) (với j_s = {j_s}):")
    B_coeffs = []
    
    for k in range(n + 1): # k chạy từ 0 đến n
        B_k = sympy.sympify(0)
        print(f"    --- k = {k} ---")
        
        try:
            if k == 0:
                val1 = D_table[j_s][0]
                val2 = D_table[j_s + 1][0]
                B_k = (val1 + val2) / 2
                print(f"      k=0: B[0] = (D[j_s][0] + D[j_s+1][0]) / 2")
                print(f"           = ({val1} + {val2}) / 2 = {B_k}")
            
            elif k % 2 == 1: # k lẻ (k = 2i - 1)
                i = (k + 1) // 2
                idx_row = j_s - i + 1
                B_k = D_table[idx_row][k]
                print(f"      k lẻ (i={i}): B[{k}] = D[j_s-i+1][k]")
                print(f"           = D[{idx_row}][{k}] = {B_k}")
            
            else: # k chẵn (k = 2i)
                i = k // 2
                idx_row_1 = j_s - i + 1
                idx_row_2 = j_s - i
                val1 = D_table[idx_row_1][k]
                val2 = D_table[idx_row_2][k]
                B_k = (val1 + val2) / 2
                print(f"      k chẵn (i={i}): B[{k}] = (D[j_s-i+1][k] + D[j_s-i][k]) / 2")
                print(f"           = (D[{idx_row_1}][{k}] + D[{idx_row_2}][{k}]) / 2")
                print(f"           = ({val1} + {val2}) / 2 = {B_k}")
            
            B_coeffs.append(B_k)
            
        except IndexError:
            print(f"      Lỗi: Chỉ số (ví dụ {idx_row}) nằm ngoài bảng. Dừng lấy hệ số.")
            break
            
    print(f"    -> Mảng hệ số B = {B_coeffs}")
            
    # Bước 4.3: Tính biểu thức t
    x = sympy.symbols('x')
    t = (x - x_s) / h
    print(f"\n  [4.3] Tính t = (x - x_s) / h")
    print(f"    t = (x - {x_s}) / {h}")
    
    # --- 5. Xác định output (Xây dựng đa thức P(x) theo Bước 5) ---
    print(f"\n[Bước 5] Xác định output (Xây dựng P(x) từ B và t):")
    P_n = B_coeffs[0]
    print(f"  Khởi tạo: P(x) = B[0] = {P_n}")
    
    term_t_product_even = sympy.sympify(1) 
    
    for k in range(1, len(B_coeffs)):
        print(f"    --- k = {k} ---")
        term_t = sympy.sympify(1)
        
        if k == 1:
            term_t = (t - sympy.Rational(1, 2)) # t - 1/2
            print(f"      k lẻ. Tích t_term = (t - 1/2) = {term_t}")
        
        elif k == 2:
            term_t = t * (t - 1)
            term_t_product_even = term_t # Lưu lại
            print(f"      k chẵn. Tích t_term = t*(t - 1) = {term_t}")
        
        elif k % 2 == 1: # k lẻ (3, 5, ...)
            term_t = term_t_product_even * (t - sympy.Rational(1, 2))
            print(f"      k lẻ. Tích t_term = (Tích chẵn k-1) * (t - 1/2)")
            print(f"           = {term_t_product_even} * (t - 1/2) = {term_t}")
        
        else: # k chẵn (4, 6, ...)
            i = k // 2
            term_t = term_t_product_even * (t + i - 1) * (t - i)
            term_t_product_even = term_t # Cập nhật
            print(f"      k chẵn (i={i}). Tích t_term = (Tích chẵn k-2) * (t + {i-1}) * (t - {i})")
            print(f"           = {term_t}")
            
        P_n = P_n + (B_coeffs[k] * term_t / sympy.factorial(k))
        print(f"      P(x) = P(x) + (B[{k}] * t_term / {k}!)")
        print(f"      -> P(x) (chưa rút gọn) = {P_n}")
    
    print("\n  Rút gọn P(x)...")
    P_n_expanded = sympy.expand(P_n)

    print(f"\n  Đa thức P(x) (dạng Bessel) = {P_n}")
    print(f"  Đa thức P(x) (dạng rút gọn) = {P_n_expanded}")
    print("--- Kết thúc thuật toán ---")

    # Trả về kết quả cuối cùng
    return P_n, P_n_expanded