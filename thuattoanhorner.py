import sympy # type: ignore

def horner_k_derivative(coeffs, x0, k):
    """
    Tính đạo hàm cấp 1 đến k của đa thức P tại điểm x0 bằng sơ đồ Horner.
    
    :param coeffs: List các hệ số của P, bắt đầu từ bậc cao nhất (ví dụ: [a_n, a_n-1, ..., a_0])
    :param x0: Điểm cần tính đạo hàm (có thể là số hoặc biến symbolic)
    :param k: Bậc đạo hàm cao nhất cần tính (ví dụ: k=2 nghĩa là tính P', P'')
    :return: Dict chứa các giá trị P(x0), P'(x0), P''(x0), ...
    """
    
    print(f"--- Bắt đầu thuật toán Horner cho đạo hàm cấp {k} tại x0 = {x0} ---")
    
    P_coeffs = [sympy.sympify(c) for c in coeffs]
    n = len(P_coeffs) - 1
    
    if k > n:
        print(f"Lỗi: Đa thức chỉ có bậc {n}, không thể tính đạo hàm cấp {k}.")
        return {}

    # Chúng ta cần k+1 lần lặp (i=1 đến k+1) để tính P(x0) đến P^k(x0)
    # Bảng 'a' cần k+2 hàng (từ 0 đến k+1)
    a = [[sympy.sympify(0) for _ in range(n + 1)] for _ in range(k + 2)]
    a[0] = P_coeffs.copy()
    
    results = {}
    
    print("Đa thức gốc P(x):")
    print_polynomial(a[0])
    print("-" * 20)

    # Phải lặp k+1 lần (i=1...k+1) để lấy k+1 phần dư (R1 đến R(k+1))
    for i in range(1, k + 2):
        # Mức đạo hàm (i=1 -> P^0, i=2 -> P^1, ...)
        deriv_level = i - 1
        print(f"Bước {i}: Tính hàng a[{i}] (cho đạo hàm cấp {deriv_level})")
        
        # Bắt đầu lặp Horner cho hàng mới
        # Hệ số đầu tiên luôn bằng hệ số đầu của hàng trước
        a[i][0] = a[i-1][0]
        print(f"  a[{i}][0] = a[{i-1}][0] = {a[i][0]}")

        # Vòng lặp Horner
        # Số hệ số giảm dần, dừng ở j = n-i+1
        for j in range(1, n - i + 2):
            a[i][j] = a[i-1][j] + a[i][j-1] * x0
            print(f"  a[{i}][{j}] = a[{i-1}][{j}] + a[{i}][{j-1}] * x0")
            print(f"         = {a[i-1][j]} + {a[i][j-1]} * {x0} = {a[i][j]}")

        # === Phần logic quan trọng đã được sửa ===
        
        # Phần dư là phần tử cuối cùng được tính: a[i][n-i+1]
        # i=1: R1 = a[1][n]
        # i=2: R2 = a[2][n-1]
        # i=3: R3 = a[3][n-2]
        remainder = a[i][n - i + 1]
        
        # Công thức: P^(m)(x0) = R_{m+1} * m!
        # (với m là bậc đạo hàm)
        
        # deriv_level = i - 1
        # P^(deriv_level)(x0) = remainder * (deriv_level)!
        
        result_val = sympy.simplify(remainder * sympy.factorial(deriv_level))
        
        if deriv_level == 0:
            key_name = "P(x0)"
            results[key_name] = result_val
            print(f"\n=> Hàng {i} hoàn tất. Phần dư R{i} = a[{i}][{n-i+1}] = {remainder}")
            print(f"   Kết quả P(x0) = R{i} * 0! = {result_val}\n")
        else:
            key_name = f"P_k{deriv_level}(x0)"
            results[key_name] = result_val
            print(f"\n=> Hàng {i} hoàn tất. Phần dư R{i} = a[{i}][{n-i+1}] = {remainder}")
            print(f"   Kết quả P^({deriv_level})(x0) = R{i} * {deriv_level}! = {remainder} * {sympy.factorial(deriv_level)} = {result_val}\n")
            
        print("-" * 20)

    print("--- Kết thúc ---")
    return results

def print_polynomial(coeffs):
    """Hàm tiện ích để in đa thức từ hệ số symbolic."""
    x = sympy.symbols('x')
    n = len(coeffs) - 1
    P = sum(coeffs[i] * x**(n - i) for i in range(n + 1))
    print(sympy.expand(P))