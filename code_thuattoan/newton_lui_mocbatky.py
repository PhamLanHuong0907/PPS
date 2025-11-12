import sympy
import sys

# === HÀM MỚI ĐƯỢC THÊM VÀO ĐỂ IN MA TRẬN ===
def print_matrix(matrix, n, title="Trạng thái ma trận D:"):
    """
    Hàm tiện ích để in ma trận (bảng tỷ sai phân) D.
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

def tim_he_so_newton_lui_bat_ky(X_input, Y_input):
    """
    Xác định các hệ số [d0, d1, ..., dn] của đa thức nội suy Newton LÙI
    sử dụng thuật toán TỶ SAI PHÂN (Trường hợp 1 trong ảnh).
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT CÁC BƯỚC)

    Trả về:
    list: Mảng D_coeffs = [d0, d1, ..., dn] (các hệ số Newton Lùi).
          Hoặc None nếu input không hợp lệ.
    """
    
    print("\n--- Bắt đầu thuật toán Newton LÙI (Tỷ Sai Phân - Mốc Bất Kỳ) ---")

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

    # --- 2. Kiểm tra điều kiện input ---
    print(f"[Bước 2] Kiểm tra điều kiện input:")
    if n < 0:
        print("  Lỗi: Mảng X và Y không được rỗng (n >= 0).")
        return None
    print(f"  -> n = {n} >= 0. (Hợp lệ)")
    
    if len(X) != len(Y):
        print(f"  Lỗi: Mảng X ({len(X)}) và Y ({len(Y)}) phải có cùng kích thước.")
        return None
    print(f"  -> Kích thước X và Y bằng nhau (n+1 = {n+1}). (Hợp lệ)")

    # --- 3. Thiết lập điều kiện dừng ---
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Không cần thiết lập (lặp bằng bảng).")
        
    # --- 4. Thực hiện tính toán ---
    # Bước 4.1: Khởi tạo mảng D (trong code là D_table)
    # Bước 4.2 (Trường hợp 1) - Lập Bảng
    print(f"[Bước 4.1 & 4.2] Thực hiện tính toán (Lập Bảng tỷ sai phân):")
    
    # Lập "Bảng tỷ sai phân" (ma trận D_table)
    D_table = [[sympy.sympify(0) for _ in range(n + 1)] for _ in range(n + 1)]
    print(f"  Lập \"Bảng tỷ sai phân\" (ma trận D_table kích thước {n+1}x{n+1}).")
    # Yêu cầu 1: In ma trận ban đầu
    print_matrix(D_table, n, f"Ma trận D_table ban đầu (khởi tạo 0)")

    # Gán cột 0: D_table[i][0] = Y[i]
    print(f"\n  Gán cột 0: D_table[i][0] = Y[i] (cho i từ 0 đến {n})")
    for i in range(n + 1):
        D_table[i][0] = Y[i]
        print(f"    Gán D_table[{i}][0] = Y[{i}] = {Y[i]}")
    
    # Yêu cầu 2: In ma trận sau khi gán cột 0
    print_matrix(D_table, n, f"Ma trận D_table sau khi gán cột 0")

    # Lặp j (cột) và i (hàng)
    print(f"\n  Lặp j từ 1 đến {n} (cột) và i từ 0 đến {n}-j (hàng) để tính D_table[i][j]:")
    
    for j in range(1, n + 1):
        print(f"    --- Tính Cột j = {j} ---")
        for i in range(n - j + 1):
            
            print(f"      i = {i}: Tính D_table[{i}][{j}]")
            
            numerator = D_table[i+1][j-1] - D_table[i][j-1]
            denominator = X[i+j] - X[i]
            
            print(f"        Tử số = D_table[i+1][j-1] - D_table[i][j-1] = {D_table[i+1][j-1]} - {D_table[i][j-1]} = {numerator}")
            print(f"        Mẫu số = X[i+j] - X[i] = X[{i+j}] - X[{i}] = {X[i+j]} - {X[i]} = {denominator}")
            
            if sympy.simplify(denominator) == 0:
                print(f"Lỗi: Các mốc X không phân biệt. {X[i+j]} == {X[i]}", file=sys.stderr)
                return None
            
            D_table[i][j] = numerator / denominator
            print(f"        => D_table[{i}][{j}] = {D_table[i][j]}")

    print("\n  --- Hoàn thành tính toán Bảng D_table ---")
    # Yêu cầu 3: In ma trận sau khi tính toán xong
    print_matrix(D_table, n, f"Ma trận D_table hoàn chỉnh")

    # Lấy hệ số d_k từ ĐƯỜNG CHÉO DƯỚI CÙNG
    # Công thức: d_k = D_table[n-k][k]
    print(f"\n  [Bước 4.3 (ảnh)] Lấy hệ số d_k từ ĐƯỜNG CHÉO DƯỚI CÙNG: d_k = D_table[n-k][k]")
    D_coeffs = []
    for k in range(n + 1):
        d_k = D_table[n-k][k]
        D_coeffs.append(d_k)
        print(f"    d_{k} = D_table[{n-k}][{k}] = {d_k}")

    # --- 5. Trả về Mảng D_coeffs ---
    print(f"\n[Bước 5] Xác định output:")
    print(f"  Mảng hệ số D (Lùi) = {D_coeffs}")
    print("--- Kết thúc thuật toán ---")
    
    return D_coeffs
