import sympy # type: ignore
import math
import sys    # Dùng để in lỗi

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


def stirling_polynomial(x_data, y_data):
    """
    Xây dựng đa thức nội suy Stirling.
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT CÁC BƯỚC)
    
    :param x_data: List các mốc x (số)
    :param y_data: List các giá trị y (có thể là số hoặc symbolic)
    :return: Đa thức nội suy P(x) (biểu thức SymPy)
    """
    print("\n--- Bắt đầu thuật toán nội suy Stirling ---")
    
    # --- 1. Xác định input ---
    print(f"[Bước 1] Xác định input:")
    n = len(x_data) - 1 # n là bậc, n+1 là số điểm
    print(f"  X (Mảng) = {x_data} (n+1 = {n+1} điểm)")
    print(f"  Y (Mảng) = {y_data}")
    
    # Chuyển Y sang symbolic
    try:
        Y_sym = [sympy.sympify(val) for val in y_data]
    except sympy.SympifyError as e:
        print(f"Lỗi: Input Y không hợp lệ. '{e}'", file=sys.stderr)
        return None
        
    # --- 2. Kiểm tra điều kiện input ---
    print(f"[Bước 2] Kiểm tra điều kiện input:")
    if n < 0:
        print("  Lỗi: Dữ liệu rỗng.")
        return None
    if (n + 1) != len(y_data):
        print("  Lỗi: Số lượng x và y không khớp.")
        return None

    # Kiểm tra h
    print("  Kiểm tra mốc cách đều (h):")
    h = x_data[1] - x_data[0]
    for i in range(1, n): # Lặp đến n-1 (kiểm tra đến X[n])
        if not math.isclose(x_data[i+1] - x_data[i], h):
            print("  Lỗi: Các mốc x không cách đều. Không thể dùng Stirling.")
            return None
    print(f"  -> Mốc cách đều h = {h}. (Hợp lệ)")

    # Kiểm tra n+1 là số lẻ (theo ảnh)
    print("  Kiểm tra n+1 là số lẻ (theo thuật toán):")
    if (n + 1) % 2 == 0:
        print(f"  -> Cảnh báo: Thuật toán Stirling (ảnh) ưu tiên n+1 lẻ. {n+1} là chẵn.")
        print(f"     (Code sẽ chọn mốc trung tâm lệch về bên trái)")
    else:
        print(f"  -> n+1 = {n+1} là số lẻ. (Hợp lệ)")
    
    # --- 3. Thiết lập điều kiện dừng ---
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Không cần thiết lập (lặp bằng bảng).")

    # --- 4. Thực hiện tính toán ---
    print(f"[Bước 4] Thực hiện tính toán:")

    # Bước 4.1: Lập "Bảng sai phân tiến" D
    print(f"  [4.1] Lập \"Bảng sai phân tiến\" (ma trận D kích thước {n+1}x{n+1}).")
    D_table = [[sympy.sympify(0) for _ in range(n + 1)] for _ in range(n + 1)]
    print_matrix(D_table, n, "Ma trận D ban đầu (khởi tạo 0)")

    print(f"    Gán cột 0: D[i][0] = Y[i] (cho i từ 0 đến {n})")
    for i in range(n + 1):
        D_table[i][0] = Y_sym[i]
    print_matrix(D_table, n, "Ma trận D sau khi gán cột 0")

    print(f"\n    Lặp j từ 1 đến {n} (cột) và i từ 0 đến {n}-j (hàng):")
    for j in range(1, n + 1):
        print(f"      --- Tính Cột j = {j} ---")
        for i in range(n - j + 1):
            val_i_plus_1 = D_table[i+1][j-1]
            val_i = D_table[i][j-1]
            D_table[i][j] = val_i_plus_1 - val_i
            print(f"        i = {i}: Tính D[{i}][{j}] = D[{i+1}][{j-1}] - D[{i}][{j-1}] = {val_i_plus_1} - {val_i} = {D_table[i][j]}")
    
    print("\n    --- Hoàn thành tính toán Bảng D ---")
    print_matrix(D_table, n, f"Ma trận D hoàn chỉnh")

    # Bước 4.2: Khởi tạo mảng hệ số S
    # Tìm j0 (mid_index)
    # Nếu n=4 (5 pts, 0..4), j0=2.
    # Nếu n=3 (4 pts, 0..3), j0=1.
    j0 = (n) // 2 
    x0 = x_data[j0]
    print(f"\n  [4.2] Lấy mảng hệ số S (Stirling) (chọn j0 = {j0}, x0 = {x0}):")
    
    S = [] # Đây là mảng S[k]
    
    for k in range(n + 1):
        if k == 0:
            # S[0] = D[j0][0]
            s_k = D_table[j0][0]
            S.append(s_k)
            print(f"    k = {k}: S[0] = D[j0][0] = D[{j0}][0] = {s_k}")
        
        elif k % 2 == 1: # k lẻ (1, 3, 5...)
            # k = 2i - 1 -> i = (k+1)/2
            i_term = (k + 1) // 2
            idx_row_1 = j0 - (i_term - 1)
            idx_row_2 = j0 - i_term
            
            if (idx_row_2 < 0) or (idx_row_1 > n) or (k > n-idx_row_2):
                print(f"    k = {k}: Không thể tính (ra ngoài bảng). Dừng.")
                break
            
            val1 = D_table[idx_row_1][k]
            val2 = D_table[idx_row_2][k]
            s_k = (val1 + val2) / 2
            S.append(s_k)
            print(f"    k = {k} (lẻ): i=(k+1)/2 = {i_term}. S[{k}] = (D[j0-(i-1)][k] + D[j0-i][k]) / 2")
            print(f"           = (D[{idx_row_1}][{k}] + D[{idx_row_2}][{k}]) / 2 = ({val1} + {val2}) / 2 = {s_k}")
        
        else: # k chẵn (2, 4, 6...)
            # k = 2i -> i = k/2
            i_term = k // 2
            idx_row = j0 - i_term
            
            if (idx_row < 0) or (idx_row > n) or (k > n-idx_row):
                print(f"    k = {k}: Không thể tính (ra ngoài bảng). Dừng.")
                break

            s_k = D_table[idx_row][k]
            S.append(s_k)
            print(f"    k = {k} (chẵn): i=k/2 = {i_term}. S[{k}] = D[j0-i][k] = D[{idx_row}][{k}] = {s_k}")

    print(f"    -> Mảng hệ số S = {S}")

    # Bước 4.3: Tính t
    x = sympy.symbols('x')
    t = (x - x0) / h
    print(f"\n  [4.3] Tính t = (x - x0) / h")
    print(f"    t = (x - {x0}) / {h}")

    # --- 5. Xác định output ---
    print(f"\n[Bước 5] Xác định output (Xây dựng P(x) từ S và t):")
    
    P = S[0]
    print(f"  Khởi tạo: P(x) = S[0] = {P}")
    
    # Logic xây dựng tích t_term
    t_term_odd = sympy.sympify(1)
    t_term_even = sympy.sympify(1)
    
    for k in range(1, len(S)):
        print(f"    --- k = {k} ---")
        
        if k % 2 == 1: # k lẻ (1, 3, 5...)
            i_term = (k-1)//2 # k=1 -> i=0. k=3 -> i=1
            if k == 1:
                t_term_odd = t
            else:
                t_term_odd = t_term_odd * (t**2 - i_term**2)
            
            term = (S[k] / sympy.factorial(k)) * t_term_odd
            print(f"      k lẻ. Tích t_term = {t_term_odd}")
            print(f"      P(x) = P(x) + (S[{k}] * t_term / {k}!)")
            print(f"           = P(x) + ({S[k]} * {t_term_odd} / {sympy.factorial(k)})")

        else: # k chẵn (2, 4, 6...)
            i_term = k//2 # k=2 -> i=1. k=4 -> i=2
            if k == 2:
                t_term_even = t**2
            else:
                t_term_even = t_term_even * (t**2 - (i_term-1)**2)
            
            term = (S[k] / sympy.factorial(k)) * t_term_even
            print(f"      k chẵn. Tích t_term = {t_term_even}")
            print(f"      P(x) = P(x) + (S[{k}] * t_term / {k}!)")
            print(f"           = P(x) + ({S[k]} * {t_term_even} / {sympy.factorial(k)})")
        
        P = P + term
        print(f"      -> P(x) (chưa rút gọn) = {P}")

    print("\n  Rút gọn P(x)...")
    P_simplified = sympy.expand(P)
    
    print(f"\n  Đa thức P(x) (dạng Stirling) = {P}")
    print(f"  Đa thức P(x) (dạng rút gọn) = {P_simplified}")
    print("--- Kết thúc thuật toán ---")
    
    return P_simplified