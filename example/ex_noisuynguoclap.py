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
    
def print_diff_table(X, Y, D_table, precision=7):
    """Hàm hỗ trợ in bảng sai phân đầy đủ cho đẹp."""
    n = len(X) - 1
    header = f"{'i':<3}| {'x_i':<10}| {'y_i':<12}"
    for j in range(1, n + 1):
        header += f"| {'Δ^'+str(j)+'y':<12}"
    print(header)
    print("-" * len(header))
    
    for i in range(n + 1):
        row = f"{i:<3}| {X[i]:<10.4f}| {Y[i]:<{precision+5}.{precision}f}"
        for j in range(1, n - i + 1):
            row += f"| {D_table[i][j]:<{precision+5}.{precision}f}"
        print(row)


# --- HÀM CHÍNH (PUBLIC) ---
def noi_suy_nguoc_lap(X_input, Y_input, k_start_index, y_bar_input, epsilon, N_max, verbose=False):
    """
    Tìm x* tương ứng với y* bằng phương pháp lặp (từ nội suy Newton).
    (Theo thuật toán trong ảnh)
    
    LƯU Ý: Y và y_bar phải là SỐ. X có thể là biểu thức.

    :param k_start_index: Chỉ số k (mốc bắt đầu của khoảng cách ly)
    :param y_bar_input: Giá trị y_bar cần tìm x*
    :param epsilon: Sai số (điều kiện dừng)
    :param N_max: Số vòng lặp tối đa
    :param verbose: Nếu True, sẽ in ra các bước thực hiện
    :return: Giá trị x_bar (dạng symbolic)
    """
    
    # --- 1. & 2. Xác định và Kiểm tra input ---
    try:
        X = [sympy.sympify(val) for val in X_input]
        Y = [sympy.sympify(val) for val in Y_input]
        y_bar = sympy.sympify(y_bar_input)
    except sympy.SympifyError as e:
        print(f"Lỗi: Input không hợp lệ. '{e}'", file=sys.stderr)
        return None

    n = len(X) - 1
    if not (0 <= k_start_index < n):
        print(f"Lỗi: Chỉ số k={k_start_index} không hợp lệ.", file=sys.stderr)
        return None
        
    # Kiểm tra Y và y_bar phải là SỐ
    if not y_bar.is_number or not all(val.is_number for val in Y):
        print(f"Lỗi: Phương pháp lặp yêu cầu Y và y_bar phải là số.", file=sys.stderr)
        return None
        
    # Chuyển Y sang float
    Y_num = [float(val) for val in Y]
    y_bar_num = float(y_bar)
    
    if verbose:
        print("\n--- Bắt đầu thuật toán nội suy ngược (Lặp) ---")
        print(f"Input: k={k_start_index}, y_bar={y_bar_num}, eps={epsilon}, N_max={N_max}")
        print(f"Khoảng X ban đầu: [{X_input[k_start_index]}, {X_input[k_start_index+1]}]")
        print(f"Khoảng Y ban đầu: [{Y_num[k_start_index]}, {Y_num[k_start_index+1]}]")

    # --- 4. Thực hiện tính toán ---
    
    # Bước 4.1: Lập Bảng sai phân tiến
    # (Chúng ta chỉ cần các giá trị bắt đầu từ hàng k)
    D_table = _xay_dung_bang_sai_phan_tien(Y_num, n)
    # Lấy các sai phân cần thiết: [Delta(y_k), Delta^2(y_k), ...]
    diffs_k = []
    for m in range(1, n - k_start_index + 1):
        diffs_k.append(D_table[k_start_index][m])
        
    if verbose:
        # Note: Bảng sai phân đầy đủ sẽ được in ở hàm main
        # Ở đây chỉ in các sai phân liên quan
        print("\nBước 4.1: Các sai phân cần dùng (bắt đầu từ hàng k)")
        print(f"  [Δy_k, Δ²y_k, ...] = {diffs_k}")

    delta_y_k = diffs_k[0] # Delta^1(y_k)
    if delta_y_k == 0:
        print("Lỗi: Delta(y_k) = 0, không thể chia. Dừng.", file=sys.stderr)
        return None
        
    # Bước 4.2: Tính t_0 và gán j = 0
    t_j = (y_bar_num - Y_num[k_start_index]) / delta_y_k
    j = 0
    
    if verbose:
        print(f"\nBước 4.2: Tính giá trị khởi tạo t_0 = (y_bar - y_k) / Δy_k")
        print(f"  t_0 = ({y_bar_num} - {Y_num[k_start_index]}) / {delta_y_k} = {t_j}")
        print(f"\nBước 4.3: Bắt đầu vòng lặp (j=0)...")

    t_final = t_j # Lưu giá trị cuối cùng

    # Bước 4.3: Bắt đầu vòng lặp
    while j < N_max:
        if verbose:
            print(f"\n--- Vòng lặp j = {j} (t_j = {t_j:.8f}) ---")
            
        # Bước 4.4: Tính P_phu
        P_phu = 0
        t_term = t_j * (t_j - 1) # Bắt đầu cho m=2
        
        if verbose: print(f"  Bước 4.4: Tính P_phu = Sum[ (Δ^m * t_term) / m! ]")
        
        # Lặp từ m=2
        for m in range(2, len(diffs_k) + 1):
            delta_m = diffs_k[m-1] # (vì diffs_k[0] là m=1)
            term_val = (delta_m / math.factorial(m)) * t_term
            P_phu = P_phu + term_val
            
            # Cập nhật t_term cho vòng lặp m tiếp theo
            t_term = t_term * (t_j - (m)) 
            
        # Tính t_{j+1}
        t_j_plus_1 = (y_bar_num - Y_num[k_start_index] - P_phu) / delta_y_k
        if verbose:
            print(f"  P_phu (tổng) = {P_phu:.8f}")
            print(f"  t_{j+1} = (y_bar - y_k - P_phu) / Δy_k")
            print(f"  => t_{j+1} = {t_j_plus_1:.8f}")
            
        # Bước 4.5: Kiểm tra hội tụ
        error = abs(t_j_plus_1 - t_j)
        if verbose:
            print(f"  Bước 4.5: Kiểm tra hội tụ |t_{j+1} - t_j| = {error:.8f}")
            
        if error < epsilon:
            if verbose: print(f"    => Lỗi < {epsilon}. Hội tụ. Thoát vòng lặp.")
            t_final = t_j_plus_1
            break
            
        # Bước 4.6: Cập nhật
        t_j = t_j_plus_1
        j = j + 1
        t_final = t_j_plus_1
        if verbose:
            print(f"  Bước 4.6: Cập nhật j = {j}, t_j = {t_j:.8f}")
            
    else: # (else của vòng while)
        if verbose:
            print(f"Cảnh báo: Đạt N_max = {N_max} vòng lặp. Dừng.")

    # Bước 4.7: Tính h
    h = sympy.simplify(X[k_start_index + 1] - X[k_start_index])
    if verbose:
        print(f"\nBước 4.7: Tính h = X[k+1] - X[k] = {h}")
        
    # Bước 4.8: Tính x_bar
    x_bar = X[k_start_index] + t_final * h
    if verbose:
        print(f"Bước 4.8: Tính x_bar = X[k] + t_final * h")
        print(f"  x_bar = {X[k_start_index]} + {t_final:.8f} * {h}")
        print(f"  => x_bar = {x_bar:.8f}")

    # Bước 5: Output
    return sympy.simplify(x_bar)


# =======================================================================
# HÀM MAIN ĐỂ GIẢI BÀI TOÁN
# =======================================================================
if __name__ == '__main__':

    X_values = [-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0]
    Y_values = [1.0, 1.078125, 0.875, 0.484375, 0.0, -0.484375, -0.875, -1.078125, -1.0]

    y_bar_target = -0.7   
    print("="*50)
    print("BÀI TOÁN: GIẢI PHƯƠNG TRÌNH f(x) = y_bar BẰNG PHƯƠNG PHÁP LẶP")
    print("="*50)
    print(f"Mảng X cho trước: {X_values}")
    print(f"Mảng Y cho trước: {[round(y, 5) for y in Y_values]}")
    print(f"Giá trị cần tìm x cho y_bar = {y_bar_target}\n")

    # --- B1: Tìm khoảng chứa nghiệm (k.c.l no.) ---
    print("--- B1: Tìm khoảng chứa nghiệm ---")
    k_found = -1
    for k in range(len(Y_values) - 1):
        if (Y_values[k] - y_bar_target) * (Y_values[k+1] - y_bar_target) < 0:
            k_found = k
            break
            
    if k_found != -1:
        print(f"Đã tìm thấy khoảng chứa nghiệm (y_k - y_bar) * (y_{k+1} - y_bar) < 0")
        print(f"=> Khoảng nghiệm là: (x_k, x_{k+1}) = ({X_values[k_found]}, {X_values[k_found+1]})")
        print(f"   với chỉ số bắt đầu k = {k_found}")
    else:
        print(f"Lỗi: Không tìm thấy khoảng chứa nghiệm cho y_bar = {y_bar_target}")
        sys.exit()

    # --- B2: Xét bộ đa thức nội suy và tính toán ---
    print("\n--- B2: Xây dựng bảng sai phân và thực hiện lặp ---")
    
    # In bảng sai phân đầy đủ
    print("\nBảng sai phân tiến:")
    full_d_table = _xay_dung_bang_sai_phan_tien(Y_values, len(X_values)-1)
    print_diff_table(X_values, Y_values, full_d_table)

    # Gọi hàm giải chính
    final_x = noi_suy_nguoc_lap(
        X_values, Y_values, k_found, y_bar_target, 
        epsilon=1e-7, N_max=10, verbose=True
    )

    print("\n" + "="*50)
    print("KẾT QUẢ CUỐI CÙNG")
    print("="*50)
    
    if final_x is not None:
        final_result_str = f"{float(final_x):.9f}"
        print("\n+------------------------------+")
        print(f"| x ≈ {final_result_str} |")
        print("+------------------------------+")