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
    (Đã BỔ SUNG Bước 2: Kiểm tra điều kiện)

    :param verbose: Nếu True, sẽ in ra TẤT CẢ các bước
    :return: (Đa thức P(y), Giá trị nội suy x*)
    """
    
    if verbose:
        print("\n--- Bắt đầu thuật toán nội suy ngược (Lagrange) ---")
    
    n = len(y_data)
    if n != len(x_data):
        print("Lỗi: Số lượng x và y không khớp.")
        return None, None
    if n < 2:
        print("Lỗi: Cần ít nhất 2 điểm (n+1 >= 2) để nội suy.")
        return None, None

    # --- Chuyển đổi sang Symbolic ---
    try:
        y_sym = [sympy.sympify(val) for val in y_data]
        x_sym = [sympy.sympify(val) for val in x_data]
        y_star_sym = sympy.sympify(y_star)
    except sympy.SympifyError as e:
        print(f"Lỗi: Input không hợp lệ. '{e}'")
        return None, None
        
    y = sympy.symbols('y')

    # --- BƯỚC 2: KIỂM TRA ĐIỀU KIỆN INPUT ---
    
    # 2a. Kiểm tra tính đơn điệu (chỉ áp dụng nếu Y là số)
    all_y_are_numbers = all(val.is_number for val in y_sym)
    
    if all_y_are_numbers:
        if verbose:
            print("\nBước 2a: Kiểm tra tính đơn điệu của Y (vì Y là số)...")
        
        diff_0 = y_sym[1] - y_sym[0]
        sign_0 = _sign(diff_0)
        
        if sign_0 == 0:
             if verbose:
                print(f"  (Y[1] - Y[0]) = 0. Bỏ qua kiểm tra đơn điệu.")
        else:
            is_monotonic = True
            for i in range(1, n - 1):
                diff_i = y_sym[i+1] - y_sym[i]
                sign_i = _sign(diff_i)
                if verbose:
                    print(f"  Kiểm tra: (Y[{i+1}]-Y[{i}]) = {diff_i}. Dấu = {sign_i}")
                if sign_i != 0 and sign_i != sign_0:
                    is_monotonic = False
                    break
            
            if not is_monotonic:
                if verbose:
                    print("  => Kết quả: Lỗi. Dữ liệu Y không đơn điệu (lên rồi xuống, hoặc ngược lại).")
                return None, None
            else:
                if verbose:
                    print("  => Kết quả: Dữ liệu Y đơn điệu.")
    else:
        if verbose:
            print("\nBước 2a: Bỏ qua kiểm tra đơn điệu (vì Y là biểu thức symbolic).")

    # 2b. Kiểm tra tính phân biệt của Y
    if verbose:
        print("\nBước 2b: Kiểm tra tính phân biệt của Y...")
    
    y_set = set([sympy.simplify(val) for val in y_sym])
    
    if len(y_set) != len(y_sym):
        if verbose:
            print(f"  Phát hiện {len(y_sym)} giá trị Y nhưng chỉ có {len(y_set)} giá trị duy nhất.")
            print("  => Kết quả: Lỗi. Các giá trị Y (mốc nội suy) không phân biệt.")
        return None, None
    else:
        if verbose:
            print("  => Kết quả: Các giá trị Y phân biệt.")

    # --- BƯỚC 4.1: Hoán đổi vai trò ---
    if verbose:
        print(f"\nBước 4.1: Hoán đổi vai trò. Xây dựng P(y) đi qua các điểm (y_i, x_i):")
        for i in range(n):
            print(f"  ({y_sym[i]}, {x_sym[i]})")
        
    P = sympy.sympify(0) # Đa thức P(y)
    
    # --- BƯỚC 4.2: Xây dựng P(y) ---
    if verbose:
        print("\nBước 4.2: Xây dựng P(y) bằng công thức Lagrange")
        print("  P(y) = Sum[ x_i * L_i(y) ]")
    
    for i in range(n):
        L_i = sympy.sympify(1)
        if verbose: print(f"  Tính L_{i}(y):")
        
        for j in range(n):
            if i == j:
                continue
            
            denominator = y_sym[i] - y_sym[j]
            term = (y - y_sym[j]) / denominator
            
            if verbose:
                print(f"    * (y - y_{j}) / (y_{i} - y_{j}) = (y - {y_sym[j]}) / ({denominator})")
            L_i = L_i * term
            
        L_i = sympy.simplify(L_i)
        if verbose: print(f"  => L_{i}(y) = {L_i}")
        
        P_term = x_sym[i] * L_i
        if verbose:
            print(f"  Thêm vào P(y): x_{i} * L_{i}(y) = {x_sym[i]} * ({L_i})")
        P = P + P_term
        if verbose: print("-" * 20)

    if verbose: print("\nBước 4.2 (Tiếp): Rút gọn đa thức P(y)")
    P_simplified = sympy.expand(P)
    if verbose: print(f"P(y) = {P_simplified}")

    # --- BƯỚC 4.3: Tính giá trị x* ---
    if verbose:
        print(f"\nBước 4.3: Tính x_bar = P(y_bar) với y_bar = {y_star_sym}")
    x_star = P.subs(y, y_star_sym)
    x_star = sympy.simplify(x_star)
    if verbose: print(f"x_bar = P({y_star_sym}) = {x_star}")
    
    if verbose: print("\n--- Kết thúc thuật toán ---")
    
    # --- BƯỚC 5: Xác định output ---
    return P_simplified, x_star