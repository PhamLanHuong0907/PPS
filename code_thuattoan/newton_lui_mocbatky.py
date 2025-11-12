import sympy
import sys

def tim_he_so_newton_lui_bat_ky(X_input, Y_input):
    """
    Xác định các hệ số [d0, d1, ..., dn] của đa thức nội suy Newton LÙI
    sử dụng thuật toán TỶ SAI PHÂN (Trường hợp 1 trong ảnh).

    Hàm này có thể xử lý input là số, biến (dạng string), 
    hoặc biểu thức (dạng string).

    Trả về:
    list: Mảng D_coeffs = [d0, d1, ..., dn] (các hệ số Newton Lùi).
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
    
    # Lập "Bảng tỷ sai phân" (ma trận D)
    # D[i][j] sẽ lưu tỷ sai phân f[x_i, x_{i+1}, ..., x_{i+j}]
    # Bảng này GIỐNG HỆT bảng của Newton Tiến
    D_table = [[sympy.sympify(0) for _ in range(n + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        D_table[i][0] = Y[i]
        
    for j in range(1, n + 1):
        for i in range(n - j + 1):
            numerator = D_table[i+1][j-1] - D_table[i][j-1]
            denominator = X[i+j] - X[i]
            
            if sympy.simplify(denominator) == 0:
                print(f"Lỗi: Các mốc X không phân biệt. {X[i+j]} == {X[i]}", file=sys.stderr)
                return None
            
            D_table[i][j] = numerator / denominator

    # Lấy hệ số d_k từ ĐƯỜNG CHÉO DƯỚI CÙNG
    # Công thức: d_k = D_table[n-k][k]
    D_coeffs = []
    for k in range(n + 1):
        D_coeffs.append(D_table[n-k][k])

    # --- 5. Trả về Mảng D_coeffs ---
    return D_coeffs