import math
import sympy  # Import thư viện symbolic
import sys    # Dùng để in lỗi

def trich_xuat_diem_phu_hop(all_x_data_input, all_y_data_input, x_input, k):
    """
    Trích xuất k điểm nội suy phù hợp theo thuật toán trong ảnh.
    ĐÃ CẬP NHẬT: Có thể xử lý mảng X và x_target là biểu thức (dạng string),
    miễn là chúng có thể được đơn giản hóa thành các mốc cách đều.

    :param all_x_data_input: Mảng X (dạng list các số hoặc string biểu thức)
    :param all_y_data_input: Mảng Y (dạng list, sẽ được sao chép)
    :param x_input: Điểm cần tính (số hoặc string biểu thức)
    :param k: Số lượng điểm cần trích xuất (1 <= k <= n+1)
    :return: (X_new, Y_new) là các mảng con, hoặc (None, None) nếu thất bại
    """

    # --- Chuyển đổi input sang dạng SymPy để xử lý ---
    try:
        all_x_data = [sympy.sympify(val) for val in all_x_data_input]
        x = sympy.sympify(x_input)
    except sympy.SympifyError as e:
        print(f"Lỗi: Input không hợp lệ, không thể chuyển đổi. '{e}'", file=sys.stderr)
        return None, None
        
    # --- 1. & 2. Xác định và Kiểm tra input ---
    n = len(all_x_data) - 1 
    if n < 0:
        print("Lỗi: Dữ liệu rỗng.")
        return None, None
    if len(all_x_data) != len(all_y_data_input):
        print(f"Lỗi: Mảng X ({len(all_x_data)}) và Y ({len(all_y_data_input)}) không cùng kích thước.")
        return None, None
    if not (k >= 1 and k <= n + 1):
        print(f"Lỗi: Số điểm k={k} không hợp lệ. Phải là 1 <= k <= {n+1}.")
        return None, None
        
    print(f"--- Bắt đầu trích xuất {k} điểm cho x = {x_input} ---")
    
    # --- 4. Thực hiện tính toán (dùng SymPy) ---
    
    # Bước 4.1: Tính bước nhảy h (dùng SymPy)
    if n > 0:
        h = sympy.simplify(all_x_data[1] - all_x_data[0])
        
        # --- BẮT ĐẦU SỬA LỖI ---
        # Kiểm tra tính cách đều
        for i in range(2, n + 1):
            h_i = sympy.simplify(all_x_data[i] - all_x_data[i-1])
            
            is_close = False
            # Nếu cả 2 đều là số, dùng math.isclose để so sánh
            if h.is_number and h_i.is_number:
                is_close = math.isclose(float(h), float(h_i), rel_tol=1e-9)
            # Nếu là biểu thức, dùng so sánh symbolic
            else:
                is_close = (sympy.simplify(h_i - h) == 0)

            if not is_close:
                print(f"Lỗi: Mốc không cách đều. Khoảng h_i={h_i} != h={h}", file=sys.stderr)
                return None, None
        # --- KẾT THÚC SỬA LỖI ---
            
    else:
        h = 1
        
    # Bước 4.2: Tìm chỉ số j của mốc x_j nằm gần x nhất
    
    # * Tính j' = (x - x_0) / h
    j_prime = sympy.simplify((x - all_x_data[0]) / h)
    
    # * KIỂM TRA QUAN TRỌNG: j_prime phải là một SỐ
    if not j_prime.is_number:
        print(f"Lỗi: Không thể xác định chỉ số 'j' từ input symbolic.")
        print(f"   j' = {j_prime} (đây là một biểu thức, không phải là số).")
        print(f"   Input x={x} hoặc X[0]={all_x_data[0]} quá phức tạp.")
        return None, None

    # * Làm tròn j = round(j')
    # Vì j_prime là số, ta có thể an toàn chuyển sang float và làm tròn
    j = round(float(j_prime))
    
    # * Hiệu chỉnh j để đảm bảo j nằm trong [0, n]
    j = max(0, min(n, j))
    j = int(j) 
    
    print(f"Thông tin: j' = {float(j_prime):.4f}. Chỉ số gần nhất j = {j} (tương ứng x[{j}] = {all_x_data_input[j]})")

    # Bước 4.3: Xác định chỉ số bắt đầu start_idx
    start_idx = j - (k - 1) // 2
    
    # Bước 4.4: Hiệu chỉnh start_idx
    if start_idx < 0:
        start_idx = 0
    if start_idx + k - 1 > n:
        start_idx = n - k + 1
    start_idx = int(start_idx)
    
    print(f"Quyết định: Chọn {k} điểm từ chỉ số {start_idx} đến {start_idx + k - 1}")

    # Bước 4.5: Khởi tạo hai mảng mới (kích thước k)
    X_new = [None] * k 
    Y_new = [None] * k 
    
    # Bước 4.6 & 4.7: Sao chép k điểm
    # Trả về giá trị GỐC (dạng string/số) thay vì đối tượng SymPy
    for i in range(k):
        X_new[i] = all_x_data_input[start_idx + i]
        Y_new[i] = all_y_data_input[start_idx + i]

    # --- 5. Xác định output ---
    print("--- Hoàn tất trích xuất ---")
    return X_new, Y_new