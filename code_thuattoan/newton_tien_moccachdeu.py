import sympy
import sys

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

def tim_he_so_newton_cach_deu(X_input, Y_input):
    """
    Xác định các hệ số [c0, c1, ..., cn] của đa thức nội suy Newton
    sử dụng thuật toán SAI PHÂN TIẾN (Trường hợp 2 trong ảnh).
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT CÁC BƯỚC)

    Trả về:
    list: Mảng C = [c0, c1, ..., cn] (các hệ số Newton).
          Các hệ số này là các đối tượng SymPy.
          Hoặc None nếu input không hợp lệ.
    """
    
    print("\n--- Bắt đầu thuật toán Sai Phân Tiến (Mốc Cách Đều) ---")

    # --- 1. Xác định input ---
    print(f"[Bước 1] Xác định input:")
    try:
        X = [sympy.sympify(val) for val in X_input]
        Y = [sympy.sympify(val) for val in Y_input]
    except sympy.SympifyError as e:
        print(f"Lỗi: Input không hợp lệ, không thể chuyển đổi. '{e}'", file=sys.stderr)
        return None

    n = len(X) - 1
    print(f"  X (mốc nội suy) = {X}")
    print(f"  Y (giá trị) = {Y}")
    print(f"  n (bậc đa thức) = len(X) - 1 = {n}")

    # --- 2. Kiểm tra điều kiện của input ---
    print(f"[Bước 2] Kiểm tra điều kiện input:")
    if n < 0:
        print("  Lỗi: Mảng X và Y không được rỗng (n >= 0).")
        return None
    print(f"  -> n = {n} >= 0. (Hợp lệ)")
    
    if len(X) != len(Y):
        print(f"  Lỗi: Mảng X ({len(X)}) và Y ({len(Y)}) phải có cùng kích thước.")
        return None
    print(f"  -> Kích thước X và Y bằng nhau (n+1 = {n+1}). (Hợp lệ)")
        
    # --- Kiểm tra điều kiện mốc cách đều (Bước 4.2 trong ảnh) ---
    print(f"  Kiểm tra mốc cách đều (tính h):")
    if n >= 1:
        h = sympy.simplify(X[1] - X[0])
        print(f"    Tính h = X[1] - X[0] = {X[1]} - {X[0]} = {h}")
        if h == 0:
             print(f"    Lỗi: Các mốc X không phân biệt. h=0", file=sys.stderr)
             return None
        for i in range(2, n + 1):
            h_i = sympy.simplify(X[i] - X[i-1])
            print(f"    Kiểm tra: h_{i} = X[{i}] - X[{i-1}] = {X[i]} - {X[i-1]} = {h_i}")
            if h_i != h:
                print(f"    Lỗi: Mốc không cách đều. Khoảng h_{i} ({h_i}) != h ({h})", file=sys.stderr)
                return None
    elif n == 0:
        h = 1 # h không quan trọng nếu chỉ có 1 điểm
        print(f"    n=0, không cần kiểm tra h (mặc định h=1).")
    print(f"  -> Mốc cách đều với h = {h}. (Hợp lệ)")
    
    # --- 3. Thiết lập điều kiện dừng ---
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Không cần thiết lập (lặp bằng bảng).")

    # --- 4. Thực hiện tính toán (Trường hợp 2: Sai phân tiến) ---
    print(f"[Bước 4] Thực hiện tính toán (Bước 4.2 - Trường hợp 2):")
    
    # Lập "Bảng sai phân tiến" (ma trận D)
    D = [[sympy.sympify(0) for _ in range(n + 1)] for _ in range(n + 1)]
    print(f"  Lập \"Bảng sai phân tiến\" (ma trận D kích thước {n+1}x{n+1}).")
    # Yêu cầu 1: In ma trận ban đầu
    print_matrix(D, n, f"Ma trận D ban đầu (khởi tạo 0)")

    # Gán cột 0: D[i][0] = Y[i]
    print(f"\n  Gán cột 0: D[i][0] = Y[i] (cho i từ 0 đến {n})")
    for i in range(n + 1):
        D[i][0] = Y[i]
        print(f"    Gán D[{i}][0] = Y[{i}] = {Y[i]}")
    
    # Yêu cầu 2: In ma trận sau khi gán cột 0
    print_matrix(D, n, f"Ma trận D sau khi gán cột 0")
        
    # Lặp j từ 1 đến n (cột - cấp sai phân)
    print(f"\n  Lặp j từ 1 đến {n} (cột) và i từ 0 đến {n}-j (hàng) để tính D[i][j]:")
    print(f"    (Công thức: D[i][j] = D[i+1][j-1] - D[i][j-1])")
    
    for j in range(1, n + 1):
        print(f"    --- Tính Cột j = {j} ---")
        # Lặp i từ 0 đến n-j (hàng)
        for i in range(n - j + 1):
            # Công thức sai phân tiến:
            # D[i][j] = D[i+1][j-1] - D[i][j-1]
            val_i_plus_1 = D[i+1][j-1]
            val_i = D[i][j-1]
            D[i][j] = val_i_plus_1 - val_i
            print(f"      i = {i}: Tính D[{i}][{j}] = D[{i+1}][{j-1}] - D[{i}][{j-1}]")
            print(f"        = {val_i_plus_1} - {val_i} = {D[i][j]}")

    print("\n  --- Hoàn thành tính toán Bảng D ---")
    # Yêu cầu 3: In ma trận sau khi tính toán xong
    print_matrix(D, n, f"Ma trận D hoàn chỉnh (đã tính xong)")

    # Lấy hệ số c_k (theo ảnh image_54e93b.png)
    print(f"\n  [Bước 4.2/4.3] Lấy hệ số c_k = D[0][k] / (k! * h^k)")
    
    C = []
    for k in range(n + 1):
        numerator = D[0][k]
        k_factorial = sympy.factorial(k)
        h_power_k = (h**k)
        denominator = k_factorial * h_power_k
        
        c_k = numerator / denominator
        C.append(c_k)
        print(f"    c_{k}:")
        print(f"      Tử số: D[0][{k}] = {numerator}")
        print(f"      Mẫu số: {k}! * h^{k} = {k_factorial} * {h}^{k} = {denominator}")
        print(f"      => c_{k} = {c_k}")

    # --- 5. Trả về Mảng C ---
    print(f"\n[Bước 5] Xác định output:")
    print(f"  Mảng hệ số C = {C}")
    print("--- Kết thúc thuật toán ---")
    
    return C