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
        print(f"Khoảng X: [{X_input[k_start_index]}, {X_input[k_start_index+1]}]")
        print(f"Khoảng Y: [{Y_num[k_start_index]}, {Y_num[k_start_index+1]}]")

    # --- 4. Thực hiện tính toán ---
    
    # Bước 4.1: Lập Bảng sai phân tiến
    # (Chúng ta chỉ cần các giá trị bắt đầu từ hàng k)
    D_table = _xay_dung_bang_sai_phan_tien(Y_num, n)
    # Lấy các sai phân cần thiết: [Delta(y_k), Delta^2(y_k), ...]
    diffs_k = []
    for m in range(1, n - k_start_index + 1):
        diffs_k.append(D_table[k_start_index][m])
        
    if verbose:
        print("\nBước 4.1: Lập bảng sai phân (từ hàng k)")
        print(f"  Các sai phân: Delta^m(y_k) = {diffs_k}")

    delta_y_k = diffs_k[0] # Delta^1(y_k)
    if delta_y_k == 0:
        print("Lỗi: Delta(y_k) = 0, không thể chia. Dừng.", file=sys.stderr)
        return None
        
    # Bước 4.2: Tính t_0 và gán j = 0
    t_j = (y_bar_num - Y_num[k_start_index]) / delta_y_k
    j = 0
    
    if verbose:
        print(f"\nBước 4.2: Tính t_0 = (y_bar - y_k) / Delta(y_k)")
        print(f"  t_0 = ({y_bar_num} - {Y_num[k_start_index]}) / {delta_y_k} = {t_j}")
        print(f"\nBước 4.3: Bắt đầu vòng lặp (j=0)...")

    t_final = t_j # Lưu giá trị cuối cùng

    # Bước 4.3: Bắt đầu vòng lặp
    while j < N_max:
        if verbose:
            print(f"\n--- Vòng lặp j = {j} (t_j = {t_j}) ---")
            
        # Bước 4.4: Tính P_phu
        P_phu = 0
        t_term = t_j * (t_j - 1) # Bắt đầu cho m=2
        
        if verbose: print(f"  Bước 4.4: Tính P_phu = Sum[ (Delta^m * t_term) / m! ]")
        
        # Lặp từ m=2
        for m in range(2, len(diffs_k) + 1):
            delta_m = diffs_k[m-1] # (vì diffs_k[0] là m=1)
            term_val = (delta_m / math.factorial(m)) * t_term
            P_phu = P_phu + term_val
            
            if verbose:
                print(f"    m={m}: Delta^{m}={delta_m}, t_term={t_term}")
                print(f"    => P_phu += {term_val}")
            
            # Cập nhật t_term cho vòng lặp m tiếp theo
            t_term = t_term * (t_j - (m - 1)) # (t-2), (t-3), ...
            
        # Tính t_{j+1}
        t_j_plus_1 = (y_bar_num - Y_num[k_start_index] - P_phu) / delta_y_k
        if verbose:
            print(f"  P_phu (tổng) = {P_phu}")
            print(f"  t_{j+1} = (y_bar - y_k - P_phu) / Delta(y_k)")
            print(f"  t_{j+1} = ({y_bar_num} - {Y_num[k_start_index]} - {P_phu}) / {delta_y_k}")
            print(f"  => t_{j+1} = {t_j_plus_1}")
            
        # Bước 4.5: Kiểm tra hội tụ
        error = abs(t_j_plus_1 - t_j)
        if verbose:
            print(f"  Bước 4.5: Kiểm tra hội tụ |t_{j+1} - t_j| = {error}")
            
        if error < epsilon:
            if verbose: print(f"    => {error} < {epsilon}. Hội tụ. Thoát vòng lặp.")
            t_final = t_j_plus_1
            break
            
        # Bước 4.6: Cập nhật
        t_j = t_j_plus_1
        j = j + 1
        t_final = t_j_plus_1
        if verbose:
            print(f"  Bước 4.6: Cập nhật j = {j}, t_j = {t_j}")
            
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
        print(f"  x_bar = {X[k_start_index]} + {t_final} * {h}")
        print(f"  => x_bar = {x_bar}")

    # Bước 5: Output
    return sympy.simplify(x_bar)