import sys

def tinh_gia_tri_horner(coeffs, c):
    """
    Tính giá trị của đa thức P(x) tại điểm x = c bằng sơ đồ Horner.
    (Dựa theo thuật toán a) trong ảnh bạn cung cấp)

    Tham số:
    coeffs (list): Danh sách các hệ số A = [a_n, a_n-1, ..., a_0]
                   (LƯU Ý: hệ số bậc cao nhất A[0] = a_n ở ĐẦU danh sách).
    c (float or int): Điểm cần tính giá trị P(c).

    Trả về:
    float or int: Giá trị P(c), hoặc None nếu input không hợp lệ.
    """
    
    # --- 2. Kiểm tra điều kiện input ---
    # "Bậc của đa thức n >= 0"
    if not coeffs: # Tương đương n < 0
        print("Lỗi: Danh sách hệ số không được rỗng.", file=sys.stderr)
        return None
    
    # "Mảng A phải có đúng n + 1 phần tử"
    # (Điều này được suy ra từ cách ta định nghĩa n)
    n = len(coeffs) - 1
    
    # --- 4. Thực hiện tính toán ---
    
    # Bước 4.1: Khởi tạo P = a_n (phần tử A[0])
    P = coeffs[0]
    
    # Bước 4.2: Thiết lập vòng lặp for i chạy từ 1 đến n
    # (range(1, n + 1) trong Python sẽ chạy i = 1, 2, ..., n)
    for i in range(1, n + 1):
        
        # Bước 4.3 (Trong vòng lặp): Cập nhật P = a_i + P * c
        # (Lưu ý: a_i trong công thức là coeffs[i] trong danh sách của chúng ta)
        P = coeffs[i] + P * c
        
    # Bước 4.4 & 5: Sau vòng lặp, P là giá trị cuối cùng P(c)
    return P

# --------------------------------------------------------------------
# PHẦN "FILE ỨNG DỤNG" ĐỂ CHẠY THỬ THUẬT TOÁN
# --------------------------------------------------------------------
if __name__ == "__main__":
    print("--- ỨNG DỤNG THUẬT TOÁN HORNER TÍNH GIÁ TRỊ P(c) ---")
    
    # --- Ví dụ 1: ---
    # Xét đa thức: P(x) = 3x^3 - 2x^2 + 0x - 5
    # n = 3
    # A = [a_3, a_2, a_1, a_0] = [3, -2, 0, -5]
    he_so_A = [3, -2, 0, -5]
    
    # Tính giá trị tại c = 2
    diem_c = 2
    
    print(f"\n--- Ví dụ 1 ---")
    print(f"Đa thức có hệ số: {he_so_A}")
    print(f"Tính giá trị tại c = {diem_c}")
    
    # Gọi hàm
    gia_tri_P = tinh_gia_tri_horner(he_so_A, diem_c)
    
    if gia_tri_P is not None:
        print(f"Kết quả P({diem_c}) = {gia_tri_P}")
        # Kiểm tra thủ công:
        # P(2) = 3*(2^3) - 2*(2^2) + 0*2 - 5
        #      = 3*8 - 2*4 - 5
        #      = 24 - 8 - 5
        #      = 11
        print(f"(Kiểm tra: Kết quả mong đợi là 11)")

    # --- Ví dụ 2: ---
    # Xét đa thức bậc 0: P(x) = 5
    # n = 0
    # A = [5]
    he_so_A_2 = [5]
    diem_c_2 = 100 # P(100) vẫn phải bằng 5
    
    print(f"\n--- Ví dụ 2 ---")
    print(f"Đa thức có hệ số: {he_so_A_2}")
    print(f"Tính giá trị tại c = {diem_c_2}")
    
    gia_tri_P_2 = tinh_gia_tri_horner(he_so_A_2, diem_c_2)
    if gia_tri_P_2 is not None:
        print(f"Kết quả P({diem_c_2}) = {gia_tri_P_2}")
        print(f"(Kiểm tra: Kết quả mong đợi là 5)")

    # --- Ví dụ 3: Input không hợp lệ ---
    print(f"\n--- Ví dụ 3 ---")
    print("Thử với danh sách hệ số rỗng:")
    tinh_gia_tri_horner([], 3)