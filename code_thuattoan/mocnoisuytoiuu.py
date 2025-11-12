import math

def tim_moc_noi_suy_toi_uu(n, a, b):
    """
    Hàm tính n mốc nội suy tối ưu (mốc Chebyshev) trên khoảng [a, b]
    dựa trên thuật toán bạn đã cung cấp.

    Tham số:
    n (int): Số lượng mốc nội suy cần tìm (n >= 1).
    a (float): Mút trái của khoảng nội suy.
    b (float): Mút phải của khoảng nội suy (phải thỏa mãn a < b).

    Trả về:
    list: Danh sách chứa n mốc nội suy, đã được sắp xếp tăng dần,
          hoặc None nếu input không hợp lệ.
    """
    
    # --- 2. Kiểm tra điều kiện của input ---
    if not isinstance(n, int) or n < 1:
        print(f"Lỗi: n (số mốc) phải là số nguyên >= 1. Nhận được: {n}")
        return None
    
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        print(f"Lỗi: a và b phải là số thực. Nhận được: a={a}, b={b}")
        return None

    if a >= b:
        print(f"Lỗi: Khoảng nội suy không hợp lệ. Phải là a < b. Nhận được: a={a}, b={b}")
        return None

    # --- 3. Thiết lập tính toán ---
    # Khởi tạo một danh sách (mảng) rỗng, đặt tên là X
    X = []

    # --- 4. Thực hiện tính toán (vòng lặp for i từ 0 đến n-1) ---
    for i in range(n):
        # Bước 4a: Tính mốc Chebyshev chuẩn hóa t_i trên đoạn [-1, 1]
        t = math.cos((2 * (n - 1 - i) + 1) * math.pi / (2 * n))
        
        # Bước 4b: Ánh xạ mốc t_i từ [-1, 1] về đoạn [a, b]
        x = (a + b) / 2 + (b - a) / 2 * t
        
        # Bước 4c: Lưu kết quả
        X.append(x)
        
    # --- 5. Xác định output ---
    # Trả về danh sách X (đã được sắp xếp tăng dần)
    return X