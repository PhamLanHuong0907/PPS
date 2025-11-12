import sympy
import sys

def tim_he_so_newton_cach_deu(X_input, Y_input):
    """
    Xác định các hệ số [c0, c1, ..., cn] của đa thức nội suy Newton
    sử dụng thuật toán SAI PHÂN TIẾN (Trường hợp 2 trong ảnh).

    Hàm này yêu cầu các mốc X phải cách đều.
    Hoạt động với input là số hoặc biểu thức.

    Trả về:
    list: Mảng C = [c0, c1, ..., cn] (các hệ số Newton).
          Các hệ số này là các đối tượng SymPy.
          Hoặc None nếu input không hợp lệ.
    """
    
    # --- Chuyển đổi mọi input thành dạng symbolic ---
    try:
        X = [sympy.sympify(val) for val in X_input]
        Y = [sympy.sympify(val) for val in Y_input]
    except sympy.SympifyError as e:
        print(f"Lỗi: Input không hợp lệ, không thể chuyển đổi. '{e}'", file=sys.stderr)
        return None

    # --- 1. & 2. Xác định và Kiểm tra input ---
    n = len(X) - 1
    if n < 0:
        print("Lỗi: Mảng X và Y không được rỗng.", file=sys.stderr)
        return None
    if len(X) != len(Y):
        print("Lỗi: Mảng X và Y phải có cùng kích thước.", file=sys.stderr)
        return None
        
    # --- Kiểm tra điều kiện mốc cách đều ---
    if n >= 1:
        h = sympy.simplify(X[1] - X[0])
        if h == 0:
             print(f"Lỗi: Các mốc X không phân biệt. h=0", file=sys.stderr)
             return None
        for i in range(2, n + 1):
            h_i = sympy.simplify(X[i] - X[i-1])
            if h_i != h:
                print(f"Lỗi: Mốc không cách đều. Khoảng {X[i]}-{X[i-1]} ({h_i}) != {h}", file=sys.stderr)
                return None
    elif n == 0:
        h = 1 # h không quan trọng nếu chỉ có 1 điểm
    
    # --- 4. Thực hiện tính toán (Trường hợp 2: Sai phân tiến) ---
    
    # Lập "Bảng sai phân tiến" (ma trận D)
    # D[i][j] sẽ lưu Delta^j (y_i)
    D = [[sympy.sympify(0) for _ in range(n + 1)] for _ in range(n + 1)]

    # Gán cột 0: D[i][0] = Y[i]
    for i in range(n + 1):
        D[i][0] = Y[i]
        
    # Lặp j từ 1 đến n (cột - cấp sai phân)
    for j in range(1, n + 1):
        # Lặp i từ 0 đến n-j (hàng)
        for i in range(n - j + 1):
            # Công thức sai phân tiến:
            # D[i][j] = D[i+1][j-1] - D[i][j-1]
            D[i][j] = D[i+1][j-1] - D[i][j-1]

    # Lấy hệ số c_k (theo ảnh image_54e93b.png)
    # c_k = D[0][k] / (k! * h^k)
    # D[0][k] là đường chéo trên cùng (Delta^k y_0)
    
    C = []
    for k in range(n + 1):
        numerator = D[0][k]
        denominator = sympy.factorial(k) * (h**k)
        
        c_k = numerator / denominator
        C.append(c_k)

    # --- 5. Trả về Mảng C ---
    return C