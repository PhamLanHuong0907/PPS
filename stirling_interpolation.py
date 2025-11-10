import sympy # type: ignore
import math

def stirling_polynomial(x_data, y_data):
    """
    Xây dựng đa thức nội suy Stirling.
    Yêu cầu: x_data phải cách đều.
    
    :param x_data: List các mốc x (số)
    :param y_data: List các giá trị y (có thể là số hoặc symbolic)
    :return: Đa thức nội suy P(x) (biểu thức SymPy)
    """
    print("--- Bắt đầu thuật toán nội suy Stirling ---")
    
    n = len(x_data)
    if n != len(y_data):
        print("Lỗi: Số lượng x và y không khớp.")
        return None
        
    h = x_data[1] - x_data[0]
    for i in range(1, n - 1):
        if not math.isclose(x_data[i+1] - x_data[i], h):
            print("Lỗi: Các mốc x không cách đều. Không thể dùng Stirling.")
            return None
    
    print(f"Các mốc x: {x_data}")
    print(f"Các giá trị y: {y_data}")
    print(f"Bước h = {h}")

    y = [[sympy.sympify(val) for val in y_data]]
    
    print("\nBước 1: Xây dựng bảng sai phân:")
    for k in range(1, n):
        row_k = []
        for i in range(n - k):
            diff = y[k-1][i+1] - y[k-1][i]
            row_k.append(diff)
            print(f"  Delta^{k}_y{i} = Delta^{k-1}_y{i+1} - Delta^{k-1}_y{i} = {y[k-1][i+1]} - {y[k-1][i]} = {diff}")
        y.append(row_k)
        
    print("\nBảng sai phân (theo hàng, chỉ lưu giá trị):")
    for k in range(n):
        print(f"  Cấp {k}: {y[k]}")

    mid_index = n // 2
    if n % 2 == 0:
        mid_index -= 1
        
    x0 = x_data[mid_index]
    y0 = y[0][mid_index]
    print(f"\nBước 2: Chọn mốc trung tâm x0 = x_{mid_index} = {x0}, y0 = {y0}")

    x = sympy.symbols('x')
    t = (x - x0) / h
    print(f"Đặt t = (x - x0) / h = (x - {x0}) / {h}")
    
    P = y0
    print(f"\nBước 3: Xây dựng đa thức P(x)")
    print(f"P = y0 = {y0}")

    # --- SỬA LỖI LOGIC ---
    # Phải dùng 2 biến t_term riêng biệt
    t_term_odd = sympy.sympify(1)  # Sẽ trở thành t, t(t^2-1), ...
    t_term_even = sympy.sympify(1) # Sẽ trở thành t^2, t^2(t^2-1), ...
    
    for i in range(1, n):
        idx = mid_index - (i // 2)
        
        if i % 2 == 1: # Cấp lẻ (1, 3, 5, ...)
            if idx < 0 or (idx - 1) < 0 or i >= len(y) or (idx) >= len(y[i]):
                print(f"  (i={i}): Đã ra khỏi bảng, dừng.")
                break
                
            term1_val = y[i][idx]
            term2_val = y[i][idx-1]
            avg_diff = (term1_val + term2_val) / 2
            
            # Cập nhật t_term_odd
            k = (i-1)//2 # k = 0, 1, 2, ...
            if i == 1:
                t_term_odd = t
            else:
                t_term_odd = t_term_odd * (t - k) * (t + k)
            
            term = (avg_diff / sympy.factorial(i)) * t_term_odd
            print(f"  (i={i}, lẻ): Thêm ( (D^{i}y{idx} + D^{i}y{idx-1}) / 2 ) * (term_t / {i}!)")
            print(f"            = ( ({term1_val} + {term2_val}) / 2 ) * ({t_term_odd} / {sympy.factorial(i)})")
            
        else: # Cấp chẵn (2, 4, 6, ...)
            if idx < 0 or i >= len(y) or (idx) >= len(y[i]):
                print(f"  (i={i}): Đã ra khỏi bảng, dừng.")
                break
                
            diff_val = y[i][idx]
            
            # Cập nhật t_term_even
            k = i//2 # k = 1, 2, 3, ...
            if i == 2:
                t_term_even = t**2
            else:
                t_term_even = t_term_even * (t - (k-1)) * (t + (k-1))

            term = (diff_val / sympy.factorial(i)) * t_term_even
            print(f"  (i={i}, chẵn): Thêm ( D^{i}y{idx} ) * (term_t / {i}!)")
            print(f"            = ( {diff_val} ) * ({t_term_even} / {sympy.factorial(i)})")

        P = P + term
        print(f"  => P hiện tại = {sympy.simplify(P)}")

    P_simplified = sympy.expand(P)
    print("\n--- Đa thức Stirling cuối cùng (trước khi rút gọn) ---")
    print(P)
    print("\n--- Đa thức Stirling cuối cùng (sau khi rút gọn) ---")
    print(P_simplified)
    print("--- Kết thúc ---")
    
    return P_simplified