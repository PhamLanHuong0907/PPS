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

def tim_he_so_newton_bat_ky(X_input, Y_input):
    """
    Xác định các hệ số [c0, c1, ..., cn] của đa thức nội suy Newton
    sử dụng thuật toán TỶ SAI PHÂN (Trường hợp 1 trong ảnh).
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT CÁC BƯỚC)

    Trả về:
    list: Mảng C = [c0, c1, ..., cn] (các hệ số Newton).
          Các hệ số này là các đối tượng SymPy.
          Hoặc None nếu input không hợp lệ.
    """
    
    print("\n--- Bắt đầu thuật toán Tỷ Sai Phân (Mốc Bất Kỳ) ---")
    
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
    
    # (Kiểm tra X phân biệt sẽ được thực hiện trong lúc tính)

    # --- 3. Thiết lập điều kiện dừng ---
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Không cần thiết lập (lặp bằng bảng).")
        
    # --- 4. Thực hiện tính toán ---
    print(f"[Bước 4] Thực hiện tính toán (Bước 4.2 - Trường hợp 1):")

    # 4.2 (Trường hợp 1) - Lập Bảng
    D = [[sympy.sympify(0) for _ in range(n + 1)] for _ in range(n + 1)]
    print(f"  Lập \"Bảng tỷ sai phân\" (ma trận D kích thước {n+1}x{n+1}).")
    # Yêu cầu 1: In ma trận ban đầu
    print_matrix(D, n, f"Ma trận D ban đầu (khởi tạo 0)")

    # 4.2 (Trường hợp 1) - Gán cột 0
    print(f"\n  Gán cột 0: D[i][0] = Y[i] (cho i từ 0 đến {n})")
    for i in range(n + 1):
        D[i][0] = Y[i]
        print(f"    Gán D[{i}][0] = Y[{i}] = {Y[i]}")
    
    # Yêu cầu 2: In ma trận sau khi gán cột 0
    print_matrix(D, n, f"Ma trận D sau khi gán cột 0")

    # 4.2 (Trường hợp 1) - Lặp j (cột) và i (hàng)
    print(f"\n  Lặp j từ 1 đến {n} (cột) và i từ 0 đến {n}-j (hàng) để tính D[i][j]:")
    
    # Lặp j từ 1 đến n (cột)
    for j in range(1, n + 1):
        print(f"    --- Tính Cột j = {j} ---")
        # Lặp i từ 0 đến n-j (hàng)
        for i in range(n - j + 1):
            
            print(f"      i = {i}: Tính D[{i}][{j}]")
            
            numerator = D[i+1][j-1] - D[i][j-1]
            denominator = X[i+j] - X[i]
            
            print(f"        Tử số = D[i+1][j-1] - D[i][j-1] = {D[i+1][j-1]} - {D[i][j-1]} = {numerator}")
            print(f"        Mẫu số = X[i+j] - X[i] = X[{i+j}] - X[{i}] = {X[i+j]} - {X[i]} = {denominator}")
            
            if sympy.simplify(denominator) == 0:
                print(f"Lỗi: Các mốc X không phân biệt. {X[i+j]} == {X[i]}", file=sys.stderr)
                return None
            
            D[i][j] = numerator / denominator
            print(f"        => D[{i}][{j}] = {D[i][j]}")

    print("\n  --- Hoàn thành tính toán Bảng D ---")
    # Yêu cầu 3: In ma trận sau khi tính toán xong
    print_matrix(D, n, f"Ma trận D hoàn chỉnh (đã tính xong)")

    # 4.2 (Trường hợp 1) - Lấy hệ số c_k
    print(f"\n  [Bước 4.3 (ảnh)] Lấy hệ số c_k từ đường chéo trên cùng: c_k = D[0][k]")
    C = [D[0][k] for k in range(n + 1)]
    for k in range(n + 1):
        print(f"    c_{k} = D[0][{k}] = {C[k]}")

    # --- 5. Trả về Mảng C ---
    print(f"\n[Bước 5] Xác định output:")
    print(f"  Mảng hệ số C = {C}")
    print("--- Kết thúc thuật toán ---")
    
    return C