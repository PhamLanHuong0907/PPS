import sympy
import sys
import pandas as pd
import numpy as np

def in_bang_tich(X):
    """
    In ra Bảng Tích (Product Table) cho các mốc nội suy X.
    Bảng này hiển thị giá trị x_i - x_j.
    """
    n = len(X) - 1
    
    # 1. Tạo ma trận (n+1) x (n+1)
    # Dùng list of lists để xây dựng ma trận
    product_table = []
    
    # Lặp qua các hàng (i)
    for i in range(n + 1):
        row = []
        # Lặp qua các cột (j)
        for j in range(n + 1):
            if i == j:
                # Đường chéo chính là 0
                row.append(0.0) 
            else:
                # Tính x_i - x_j
                diff = X[i] - X[j]
                row.append(diff)
        product_table.append(row)

    # 2. Sử dụng Pandas để tạo DataFrame và in ra cho đẹp
    # Tên hàng và cột là các mốc x_i
    index_names = [f"x{i}={x}" for i, x in enumerate(X)]
    column_names = [f"x{j}={x}" for j, x in enumerate(X)]
    
    df = pd.DataFrame(product_table, index=index_names, columns=column_names)
    
    # 3. Định dạng lại (chỉ hiển thị 4 chữ số thập phân, thay 0.0 bằng '-')
    pd.options.display.float_format = '{:.4f}'.format
    
    print("\n  [Bảng Tích] TÍNH CÁC HIỆU SỐ (x_i - x_j):")
    print("  (Các giá trị trên hàng i, bỏ qua 0, nhân lại sẽ ra Mẫu số D_i)")
    print("-" * (len(column_names) * 10 + 20))
    # Sử dụng to_string và thay 0.0 bằng '-'
    df_str = df.to_string(na_rep='', float_format='{:.4f}'.format)
    df_str = df_str.replace(' 0.0000', '      -')
    df_str = df_str.replace(' 0.000', '     -')
    print(df_str)
    print("-" * (len(column_names) * 10 + 20))


def xay_dung_da_thuc_lagrange(X, Y):
    """
    Xây dựng đa thức nội suy Lagrange P(x) từ các mốc X và giá trị Y.
    (Đã cập nhật để in ra Bảng Tích)
    """
    
    # --- 1. Xác định input ---
    print("\n--- Bắt đầu thuật toán xây dựng đa thức Lagrange ---")
    print(f"[Bước 1] Xác định input:")
    n = len(X) - 1 
    print(f"  X (mốc nội suy) = {X}")
    print(f"  Y (giá trị) = {Y}")
    print(f"  n (bậc đa thức) = {n}")

    x = sympy.symbols('x')
    
    # --- 2. Kiểm tra điều kiện của input ---
    print(f"[Bước 2] Kiểm tra điều kiện input:")
    if n < 0 or len(X) != len(Y) or len(set(X)) != len(X):
        print("  Lỗi: Input không hợp lệ. Vui lòng kiểm tra kích thước và tính phân biệt của mốc X.")
        return None, None
    print(f"  -> Input hợp lệ.")

    # --- 3. Thiết lập điều kiện dừng ---
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Không cần thiết lập điều kiện dừng (vòng lặp for xác định).")
    
    # --- BỔ SUNG: IN BẢNG TÍCH ---
    print(f"\n[Bổ sung] Lập Bảng Tích (Product Table) để tính Mẫu số D_i")
    in_bang_tich(X)
    
    # --- 4. Thực hiện tính toán ---
    print(f"[Bước 4] Thực hiện tính toán:")
    
    # Bước 4.1: Khởi tạo đa thức tổng P_n(x) = 0
    P_n = sympy.sympify(0)
    print(f"  [4.1] Khởi tạo đa thức tổng: P_n(x) = {P_n}")
    
    # Bước 4.2: Vòng lặp ngoài i chạy từ 0 đến n
    print(f"  [4.2] Bắt đầu vòng lặp ngoài (i = 0 đến {n}) để tính P_n = sum(Y_i * L_i(x))")

    for i in range(n + 1):
        print(f"\n    --- i = {i} (Tính L_{i}(x) và Y_{i}*L_{i}(x)) ---")
        
        # --- Bước 4.3 (Trong vòng lặp i): Xây dựng đa thức cơ sở L_i(x) ---
        print(f"    [4.3] Xây dựng đa thức cơ sở L_{i}(x):")
        
        # 4.3a: Tính tử số N_i(x)
        N_i = sympy.sympify(1) 
        D_i = sympy.sympify(1) 
        
        # In các bước tính N_i và D_i (giữ nguyên logic cũ)
        print(f"      [4.3a & 4.3b] Tính Tử số N_{i}(x) và Mẫu số D_{i}:")
        for j in range(n + 1):
            if i != j:
                # Tính N_i: N_i = N_i_cu * (x - x_j)
                N_i = N_i * (x - X[j])
                # Tính D_i: D_i = D_i_cu * (x_i - x_j)
                term = (X[i] - X[j])
                D_i = D_i * term
                # In ra bước tính toán
                print(f"          j = {j}: N_{i}(x) * (x - {X[j]}), D_{i} * ({X[i]} - {X[j]})")
        
        N_i = sympy.simplify(N_i)
        print(f"        -> N_{i}(x) (Tử số) = {N_i}")
        print(f"        -> D_{i} (Mẫu số) = {D_i} (kiểm tra với Bảng Tích: tích các số trên hàng i)")
        
        # Bước 4.3c (Tính L_i(x))
        L_i = N_i / D_i
        print(f"      [4.3c] L_{i}(x) = N_{i}(x) / D_{i}")
        print(f"             L_{i}(x) (rút gọn) = {sympy.expand(L_i)}") 

        # Bước 4.4 (Trong vòng lặp i): Cộng Y_i * L_i(x) vào đa thức tổng
        Y_i = Y[i]
        term_i = Y_i * L_i
        P_n = P_n + term_i
        
        print(f"    [4.4] Cập nhật đa thức tổng P_n(x) = P_n(x) + Y_{i} * L_{i}(x)")
        print(f"          -> P_n hiện tại (chưa rút gọn) = {P_n}")
            
    # Phần kết thúc và output (giữ nguyên)
    print("\n    --- Kết thúc vòng lặp i ---")
        
    P_n_expanded = sympy.expand(P_n)
    P_poly = sympy.Poly(P_n_expanded, x)
    A = P_poly.all_coeffs()

    print(f"  [4.5] Đa thức P_n(x) (rút gọn cuối cùng) = {P_n_expanded}")
    
    print(f"\n[Bước 5] Xác định output:")
    try:
        A = [float(coeff) if coeff.is_Float else int(coeff) for coeff in A]
    except TypeError:
        A = [coeff for coeff in A]
        
    print(f"  -> Đa thức P(x) = {P_n_expanded}")
    print(f"  -> Mảng hệ số A (từ bậc cao đến thấp) = {A}")

    print("--- Hoàn thành ---")

    return P_n_expanded, A

# ==============================================================================
# HÀM MAIN ĐỂ CHẠY CHƯƠNG TRÌNH
# ==============================================================================
def main():
    """
    Hàm chính để chạy chương trình tìm đa thức nội suy Lagrange.
    Sử dụng dữ liệu từ bài tập mẫu của bạn.
    """
    print("--- CHƯƠNG TRÌNH TÌM ĐA THỨC NỘI SUY LAGRANGE ---")
    
    # Dữ liệu từ bài tập mẫu (5 điểm đầu)
    X_mau = [2.1, 2.2, 2.4, 2.5, 2.7]
    Y_mau = [3.178, 3.752, 3.597, 4.132, 4.376]
    
    print("\n>>> Dữ liệu từ Bài tập mẫu (5 điểm đầu):")
    print(f"X = {X_mau}")
    print(f"Y = {Y_mau}")
    
    # Gọi hàm để tính toán và in ra các bước chi tiết (bao gồm Bảng Tích)
    P_n_mau, A_mau = xay_dung_da_thuc_lagrange(X_mau, Y_mau)
    
    # In kết quả tóm tắt cho ví dụ
    if P_n_mau is not None:
        print("\n=== KẾT QUẢ TÓM TẮT ===")
        print(f"Đa thức nội suy P(x) = {P_n_mau}")
        print(f"Danh sách hệ số A (từ bậc 4 đến bậc 0) = {A_mau}")
        print("====================================")
        
if __name__ == "__main__":
    main()