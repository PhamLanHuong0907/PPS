import sympy # type: ignore
import math

def fixed_point_iteration(g_expr, x0_val, tolerance, max_iter, params={}):
    """
    Tìm nghiệm của x = g(x) bằng phương pháp lặp đơn.
    
    :param g_expr: Biểu thức g(x) dưới dạng chuỗi (ví dụ: "cos(x)")
    :param x0_val: Giá trị lặp ban đầu (số)
    :param tolerance: Sai số cho phép (ví dụ: 1e-6)
    :param max_iter: Số lần lặp tối đa
    :param params: Dict chứa các tham số symbolic và giá trị của chúng (ví dụ: {'a': 1.5})
    :return: Nghiệm x (hoặc None nếu không hội tụ)
    """
    
    print("--- Bắt đầu phương pháp lặp đơn x = g(x) ---")
    
    # --- Bước 1: Thiết lập hàm symbolic ---
    x = sympy.symbols('x')
    
    # Xác định các tham số có trong biểu thức
    all_symbols = [str(s) for s in sympy.sympify(g_expr).atoms(sympy.Symbol)]
    
    # Tạo symbol cho các tham số (ví dụ: 'a', 'b')
    param_symbols = []
    if 'x' in all_symbols:
        all_symbols.remove('x')
    
    param_sym_dict = {s: sympy.symbols(s) for s in all_symbols}

    # Chuyển chuỗi g_expr thành biểu thức SymPy
    try:
        g = sympy.sympify(g_expr, locals=param_sym_dict)
    except sympy.SympifyError as e:
        print(f"Lỗi: Biểu thức g(x) không hợp lệ: {e}")
        return None
        
    print(f"Phương trình lặp: x = g(x) = {g}")
    print(f"Tham số đầu vào: {params}")

    # --- Bước 2: Thay thế các tham số (ví dụ: 'a') bằng giá trị số ---
    g_with_params = g.subs(params)
    print(f"Biểu thức g(x) sau khi thay tham số: {g_with_params}")

    # Kiểm tra xem g_with_params còn biến symbolic nào khác x không
    if g_with_params.atoms(sympy.Symbol) - {x}:
         print(f"Lỗi: Vẫn còn tham số chưa được gán giá trị: {g_with_params.atoms(sympy.Symbol) - {x}}")
         return None

    # --- Bước 3: Chuyển hàm symbolic thành hàm số (numerical) để lặp ---
    # Đây là bước quan trọng để tăng tốc độ
    try:
        g_numeric = sympy.lambdify(x, g_with_params, 'math')
    except Exception as e:
        print(f"Lỗi khi chuyển g(x) sang hàm số: {e}")
        print("Hãy đảm bảo g(x) sử dụng các hàm trong thư viện 'math' (ví dụ: 'cos', 'sin', 'exp')")
        return None

    print(f"\nBước lặp bắt đầu với x0 = {x0_val}, Sai số = {tolerance}")
    print("-" * 50)
    print("Iter |     x_k     |    g(x_k)   |   |x_{k+1} - x_k| ")
    print("-" * 50)
    
    x_k = x0_val
    for i in range(max_iter):
        try:
            x_k_plus_1 = g_numeric(x_k)
        except (ValueError, TypeError, OverflowError) as e:
            print(f"Lỗi tính toán tại x_k = {x_k}: {e}")
            return None
            
        error = abs(x_k_plus_1 - x_k)
        
        print(f"{i:4d} | {x_k:11.7f} | {x_k_plus_1:11.7f} | {error:15.7e}")
        
        if error < tolerance:
            print("-" * 50)
            print(f"\nThuật toán hội tụ sau {i+1} bước.")
            print(f"Nghiệm x ≈ {x_k_plus_1}")
            print("--- Kết thúc ---")
            return x_k_plus_1
            
        x_k = x_k_plus_1

    print("-" * 50)
    print(f"\nLỗi: Thuật toán không hội tụ sau {max_iter} bước.")
    print("--- Kết thúc ---")
    return None