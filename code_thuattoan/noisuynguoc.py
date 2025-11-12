import sympy
import sys

def _sign(x):
    """Hàm hỗ trợ (private) để lấy dấu của một số."""
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def inverse_lagrange_polynomial(y_data, x_data, y_star, verbose=False):
    """
    Tìm x* tương ứng với y* bằng nội suy ngược (dùng Lagrange).
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT 5 BƯỚC VÀ SỬA LỖI VÒNG LẶP)

    :param y_data: Mảng Y (dùng làm mốc)
    :param x_data: Mảng X (dùng làm giá trị)
    :param y_star: Giá trị y* (y_bar)
    :param verbose: Nếu True, sẽ in ra TẤT CẢ các bước
    :return: (Đa thức P(y), Giá trị nội suy x*)
    """
    
    if verbose:
        print("\n--- Bắt đầu thuật toán nội suy ngược (Lagrange) ---")
    
    # --- 1. Xác định input ---
    try:
        y_sym = [sympy.sympify(val) for val in y_data]
        x_sym = [sympy.sympify(val) for val in x_data]
        y_star_sym = sympy.sympify(y_star)
    except sympy.SympifyError as e:
        err_msg = f"Lỗi: Input không hợp lệ. '{e}'"
        if verbose: print(f"[Bước 1] {err_msg}", file=sys.stderr)
        else: print(err_msg, file=sys.stderr)
        return None, None
        
    n = len(y_sym) - 1 # n là BẬC (n+1 điểm)
    
    if verbose:
        print(f"[Bước 1] Xác định input:")
        print(f"  Y (Mảng mốc) = {y_data} (n+1 = {n+1} điểm)")
        print(f"  X (Mảng giá trị) = {x_data}")
        print(f"  n (Bậc) = {n}")
        print(f"  y_bar (Giá trị y*) = {y_star}")

    # --- 2. Kiểm tra điều kiện input ---
    if verbose: print(f"\n[Bước 2] Kiểm tra điều kiện input:")
    
    if n < 1: # Cần ít nhất 2 điểm
        msg = f"Lỗi: Cần ít nhất 2 điểm (n >= 1). Nhận được n = {n}."
        if verbose: print(f"  {msg}", file=sys.stderr)
        else: print(msg, file=sys.stderr)
        return None, None
    if verbose: print(f"  -> n = {n} >= 1. (Hợp lệ)")

    # 2a. Kiểm tra tính đơn điệu (chỉ áp dụng nếu Y là số)
    all_y_are_numbers = all(val.is_number for val in y_sym)
    
    if all_y_are_numbers:
        if verbose:
            print(f"  Kiểm tra tính đơn điệu của Y (vì Y là số)...")
        
        diff_0 = y_sym[1] - y_sym[0]
        sign_0 = _sign(diff_0)
        
        if sign_0 == 0:
             if verbose:
                print(f"    (Y[1] - Y[0]) = 0. Bỏ qua kiểm tra đơn điệu (nhưng sẽ thất bại ở Bước 2b).")
        else:
            is_monotonic = True
            # Lặp từ 1 đến n-1 (kiểm tra đến cuối)
            for i in range(1, n): 
                diff_i = y_sym[i+1] - y_sym[i]
                sign_i = _sign(diff_i)
                if verbose:
                    print(f"    Kiểm tra: (Y[{i+1}]-Y[{i}]) = {diff_i}. Dấu = {sign_i}")
                if sign_i != 0 and sign_i != sign_0:
                    is_monotonic = False
                    break
            
            if not is_monotonic:
                if verbose:
                    print("    => Lỗi. Dữ liệu Y không đơn điệu (lên rồi xuống, hoặc ngược lại).")
                return None, None
            else:
                if verbose:
                    print("    => Dữ liệu Y đơn điệu.")
    else:
        if verbose:
            print("  Bỏ qua kiểm tra đơn điệu (vì Y là biểu thức symbolic).")

    # 2b. Kiểm tra tính phân biệt của Y
    if verbose:
        print(f"  Kiểm tra tính phân biệt của Y (mốc nội suy)...")
    
    y_set = set([sympy.simplify(val) for val in y_sym])
    
    if len(y_set) != len(y_sym):
        if verbose:
            print(f"    Phát hiện {len(y_sym)} giá trị Y nhưng chỉ có {len(y_set)} giá trị duy nhất.")
            print("    => Lỗi. Các giá trị Y (mốc nội suy) không phân biệt.")
        return None, None
    else:
        if verbose:
            print("    => Các giá trị Y phân biệt.")
            
    # --- 3. Thiết lập điều kiện dừng ---
    if verbose:
        print(f"\n[Bước 3] Thiết lập điều kiện dừng:")
        print(f"  Không cần thiết lập (tính toán trực tiếp 1 lần).")

    # --- 4. Thực hiện tính toán ---
    if verbose: print(f"\n[Bước 4] Thực hiện tính toán:")
    
    # Bước 4.1: Hoán đổi vai trò
    if verbose:
        print(f"  [4.1] Hoán đổi vai trò. Xây dựng P(y) đi qua các điểm (y_i, x_i):")
        # Sửa: Lặp đến n (tức là n+1 điểm)
        for i in range(n + 1): 
            print(f"    ({y_sym[i]}, {x_sym[i]})")
        
    P = sympy.sympify(0) # Đa thức P(y)
    y = sympy.symbols('y')
    
    # --- BƯỚC 4.2: Xây dựng P(y) ---
    if verbose:
        print("\n  [4.2] Xây dựng P(y) bằng công thức Lagrange")
        print("    P(y) = Sum[ x_i * L_i(y) ]")
    
    # Sửa: Lặp đến n (tức là n+1 điểm)
    for i in range(n + 1):
        L_i = sympy.sympify(1)
        if verbose: print(f"    --- i = {i} (Tính L_{i}(y)) ---")
        
        # Sửa: Lặp đến n (tức là n+1 điểm)
        for j in range(n + 1):
            if i == j:
                continue
            
            denominator = y_sym[i] - y_sym[j]
            term = (y - y_sym[j]) / denominator
            
            if verbose:
                print(f"      * (y - y_{j}) / (y_{i} - y_{j}) = (y - {y_sym[j]}) / ({denominator})")
            L_i = L_i * term
            
        L_i = sympy.simplify(L_i)
        if verbose: print(f"    => L_{i}(y) = {L_i}")
        
        P_term = x_sym[i] * L_i
        if verbose:
            print(f"    Thêm vào P(y): x_{i} * L_{i}(y) = {x_sym[i]} * ({L_i})")
        P = P + P_term
        if verbose: print(f"    -> P(y) (hiện tại) = {P}")

    if verbose: print("\n    Rút gọn đa thức P(y)...")
    P_simplified = sympy.expand(P)
    if verbose: print(f"    P(y) (đã rút gọn) = {P_simplified}")

    # --- BƯỚC 4.3: Tính giá trị x* ---
    if verbose:
        print(f"\n  [4.3] Tính x_bar = P(y_bar) với y_bar = {y_star_sym}")
    x_star = P.subs(y, y_star_sym)
    x_star = sympy.simplify(x_star)
    if verbose: print(f"    -> x_bar = P({y_star_sym}) = {x_star}")
    
    # --- BƯỚC 5: Xác định output ---
    if verbose:
        print(f"\n[Bước 5] Xác định output:")
        print(f"  Đa thức P(y) = {P_simplified}")
        print(f"  Giá trị x* = {x_star}")
        print("--- Kết thúc thuật toán ---")
    
    return P_simplified, x_star