import sys

def chia_horner(coeffs, c):
    """
    Thực hiện phép chia đa thức P(x) cho (x - c) bằng sơ đồ Horner.
    Trả về các hệ số của đa thức thương Q(x) và số dư R.
    (Dựa trên thuật toán (b) trong ảnh, nhưng đã SỬA LỖI các công thức)

    Tham số:
    coeffs (list): Danh sách các hệ số A = [a_n, a_n-1, ..., a_0]
                   (Hệ số bậc cao nhất A[0] = a_n ở ĐẦU danh sách).
    c (float or int): Giá trị từ biểu thức chia (x - c).

    Trả về:
    tuple: (B_coeffs, R)
           B_coeffs (list): Danh sách hệ số của thương Q(x)
                            [b_{n-1}, b_{n-2}, ..., b_0]
           R (float or int): Số dư của phép chia (chính là P(c))
           Hoặc (None, None) nếu input không hợp lệ.
    """
    
    # --- 1. & 2. Xác định và Kiểm tra input ---
    if not coeffs:
        print("Lỗi: Danh sách hệ số không được rỗng.", file=sys.stderr)
        return None, None
        
    n = len(coeffs) - 1
    
    # Thuật toán yêu cầu n >= 1
    if n < 1:
        print(f"Lỗi: Bậc của đa thức phải >= 1. Đa thức này có bậc {n}.", file=sys.stderr)
        return None, None

    # --- 4. Thực hiện tính toán ---

    # Bước 4.1: Khởi tạo mảng B để lưu n hệ số của Q_{n-1}(x)
    B_coeffs = []
    
    # Bước 4.2: Gán b_{n-1} = a_n
    # Đây là hệ số đầu tiên của Q(x)
    b_prev = coeffs[0]
    B_coeffs.append(b_prev)
    
    # ---
    # Bước 4.3 & 4.4: Lặp i từ 1 đến n-1.
    # Chúng ta sẽ dùng vòng lặp chuẩn của Horner/chia tổng hợp:
    # b_current = a_current + b_previous * c
    # ---
    for i in range(1, n):
        # Lấy hệ số a_{n-i} (chính là coeffs[i])
        a_i = coeffs[i]
        
        # Công thức đúng: b_{n-1-i} = a_{n-i} + b_{n-i} * c
        b_current = a_i + b_prev * c
        
        # Lưu kết quả b_{n-1-i} vào mảng B (Bước 4.4)
        B_coeffs.append(b_current)
        
        # Cập nhật b_prev cho vòng lặp tiếp theo
        b_prev = b_current
        
    # Bước 4.5: Tính số dư R
    # Công thức đúng: R = a_0 + b_0 * c
    # a_0 là phần tử cuối cùng của coeffs (coeffs[n])
    # b_0 là phần tử cuối cùng ta vừa tính (hiện đang lưu trong b_prev)
    R = coeffs[n] + b_prev * c
    
    # 5. Xác định output
    return B_coeffs, R

# --------------------------------------------------------------------
# PHẦN "FILE ỨNG DỤNG" ĐỂ CHẠY THỬ THUẬT TOÁN
# --------------------------------------------------------------------
if __name__ == "__main__":
    print("--- ỨNG DỤNG THUẬT TOÁN CHIA HORNER ---")
    
    # --- Ví dụ 1: ---
    # Xét đa thức: P(x) = 3x^3 - 2x^2 + 0x - 5
    # Chia cho (x - 2)
    # n = 3
    # A = [3, -2, 0, -5]
    # c = 2
    
    # Phép chia thủ công:
    # (3x^3 - 2x^2 - 5) / (x - 2) = (3x^2 + 4x + 8) dư 11
    # Q(x) = 3x^2 + 4x + 8  => Hệ số B = [3, 4, 8]
    # R = 11
    
    he_so_A = [3, -2, 0, -5]
    diem_c = 2
    
    print(f"\n--- Ví dụ 1 ---")
    print(f"Đa thức P(x) có hệ số: {he_so_A}")
    print(f"Chia cho (x - {diem_c})")
    
    # Gọi hàm
    B, R = chia_horner(he_so_A, diem_c)
    
    if B is not None:
        print(f"Đa thức thương Q(x) có hệ số B = {B}")
        print(f"Số dư R = {R}")
        print(f"(Kết quả mong đợi: B = [3, 4, 8], R = 11)")

    # --- Ví dụ 2: ---
    # Xét đa thức: P(x) = x^2 - 4
    # Chia cho (x + 2)
    # n = 2
    # A = [1, 0, -4]
    # (x + 2) = (x - (-2)) => c = -2
    
    # Phép chia thủ công:
    # (x^2 - 4) / (x + 2) = (x - 2) dư 0
    # Q(x) = x - 2 => Hệ số B = [1, -2]
    # R = 0
    
    he_so_A_2 = [1, 0, -4]
    diem_c_2 = -2
    
    print(f"\n--- Ví dụ 2 ---")
    print(f"Đa thức P(x) có hệ số: {he_so_A_2}")
    print(f"Chia cho (x - ({diem_c_2}))")
    
    B_2, R_2 = chia_horner(he_so_A_2, diem_c_2)
    
    if B_2 is not None:
        print(f"Đa thức thương Q(x) có hệ số B = {B_2}")
        print(f"Số dư R = {R_2}")
        print(f"(Kết quả mong đợi: B = [1, -2], R = 0)")