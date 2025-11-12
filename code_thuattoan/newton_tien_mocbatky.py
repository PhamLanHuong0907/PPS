import sympy
import sys

def tim_he_so_newton_bat_ky(X_input, Y_input):
    """
    Xác định các hệ số [c0, c1, ..., cn] của đa thức nội suy Newton
    sử dụng thuật toán TỶ SAI PHÂN (Trường hợp 1 trong ảnh).

    Hàm này có thể xử lý input là số, biến (dạng string), 
    hoặc biểu thức (dạng string).

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
        
    # --- 4. Thực hiện tính toán (Trường hợp 1: Tỷ sai phân) ---
    D = [[sympy.sympify(0) for _ in range(n + 1)] for _ in range(n + 1)]

    # Gán cột 0: D[i][0] = Y[i]
    for i in range(n + 1):
        D[i][0] = Y[i]
        
    # Lặp j từ 1 đến n (cột)
    for j in range(1, n + 1):
        # Lặp i từ 0 đến n-j (hàng)
        for i in range(n - j + 1):
            
            numerator = D[i+1][j-1] - D[i][j-1]
            denominator = X[i+j] - X[i]
            
            if sympy.simplify(denominator) == 0:
                print(f"Lỗi: Các mốc X không phân biệt. {X[i+j]} == {X[i]}", file=sys.stderr)
                return None
            
            D[i][j] = numerator / denominator

    # Lấy hệ số c_k từ đường chéo trên cùng: c_k = D[0][k]
    C = [D[0][k] for k in range(n + 1)]

    # --- 5. Trả về Mảng C ---
    return C