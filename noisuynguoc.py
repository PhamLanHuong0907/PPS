import sympy

def inverse_lagrange_polynomial(y_data, x_data, y_star):
    """
    Tìm x* tương ứng với y* bằng nội suy ngược (dùng Lagrange).
    Xây dựng đa thức P(y) đi qua các điểm (y_i, x_i).
    Tính x* = P(y*)
    
    :param y_data: List các giá trị y (số hoặc symbolic)
    :param x_data: List các giá trị x (số hoặc symbolic)
    :param y_star: Giá trị y* cần tìm x* tương ứng (số hoặc symbolic)
    :return: (Đa thức P(y), Giá trị nội suy x*)
    """
    
    print("--- Bắt đầu thuật toán nội suy ngược (Lagrange) ---")
    
    n = len(y_data)
    if n != len(x_data):
        print("Lỗi: Số lượng x và y không khớp.")
        return None, None

    # Chuyển đổi tất cả sang symbolic
    y_sym = [sympy.sympify(val) for val in y_data]
    x_sym = [sympy.sympify(val) for val in x_data]
    y_star_sym = sympy.sympify(y_star)
    
    y = sympy.symbols('y') # Biến của đa thức nội suy là 'y'
    
    print(f"Xây dựng P(y) đi qua các điểm (y_i, x_i):")
    for i in range(n):
        print(f"  ({y_sym[i]}, {x_sym[i]})")
        
    P = sympy.sympify(0) # Đa thức P(y)
    
    print("\nBước 1: Xây dựng các đa thức cơ sở L_i(y)")
    for i in range(n):
        L_i = sympy.sympify(1)
        print(f"  Tính L_{i}(y):")
        for j in range(n):
            if i == j:
                continue
            
            term = (y - y_sym[j]) / (y_sym[i] - y_sym[j])
            print(f"    * (y - y_{j}) / (y_{i} - y_{j}) = (y - {y_sym[j]}) / ({y_sym[i]} - {y_sym[j]})")
            L_i = L_i * term
            
        L_i = sympy.simplify(L_i)
        print(f"  => L_{i}(y) = {L_i}")
        
        P_term = x_sym[i] * L_i
        print(f"  Thêm vào P(y): x_{i} * L_{i}(y) = {x_sym[i]} * ({L_i})")
        P = P + P_term
        print("-" * 20)

    print("\nBước 2: Rút gọn đa thức P(y)")
    P_simplified = sympy.expand(P)
    print(f"P(y) = {P_simplified}")

    print("\nBước 3: Tính x* = P(y*)")
    x_star = P.subs(y, y_star_sym)
    x_star = sympy.simplify(x_star)
    print(f"x* = P({y_star_sym}) = {x_star}")
    
    print("--- Kết thúc ---")
    return P_simplified, x_star