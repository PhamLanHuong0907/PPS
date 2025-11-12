import math

def find_stirling_points(all_x_data, all_y_data, x_target, num_points):
    """
    Tìm các điểm phù hợp (cách đều và ở tâm) để nội suy Stirling
    từ một bộ dữ liệu lớn đã được sắp xếp.

    :param all_x_data: List TOÀN BỘ các mốc x (phải được sắp xếp)
    :param all_y_data: List TOÀN BỘ các giá trị y
    :param x_target: Giá trị x mà bạn muốn nội suy (dùng để chọn tâm)
    :param num_points: Số lượng điểm bạn muốn sử dụng (ví dụ: 5, 7, ...)
    :return: (selected_x, selected_y) là các list con, hoặc (None, None) nếu thất bại
    """
    
    print(f"--- Bắt đầu tìm {num_points} điểm cho x_target = {x_target} ---")
    
    n = len(all_x_data)
    if n != len(all_y_data):
        print("Lỗi: Dữ liệu x và y không cùng kích thước.")
        return None, None
        
    if n < num_points:
        print(f"Lỗi: Dữ liệu chỉ có {n} điểm, yêu cầu {num_points} điểm.")
        return None, None

    # --- Bước 1: Tìm chỉ số (index) của mốc x gần x_target nhất ---
    # (Chúng ta có thể dùng thuật toán tìm kiếm nhị phân, 
    # nhưng cách đơn giản này cũng hiệu quả với dữ liệu đã sắp xếp)
    
    closest_idx = 0
    min_diff = float('inf')
    
    for i, x_val in enumerate(all_x_data):
        diff = abs(x_val - x_target)
        if diff < min_diff:
            min_diff = diff
            closest_idx = i
        else:
            # Tối ưu: Vì x_data đã sắp xếp, khi khoảng cách bắt đầu tăng
            # nghĩa là chúng ta đã đi qua điểm gần nhất.
            break
            
    print(f"Thông tin: Mốc x gần nhất trong dữ liệu là x[{closest_idx}] = {all_x_data[closest_idx]}")

    # --- Bước 2: Xác định chỉ số bắt đầu (start_idx) ---
    # Mục tiêu là đặt 'closest_idx' ở giữa của 'num_points'
    # Chúng ta lùi lại (num_points - 1) // 2 bước
    start_idx = closest_idx - (num_points - 1) // 2
    
    # --- Bước 3: Xử lý các trường hợp ở biên (quan trọng) ---
    
    # 3a. Xử lý cận dưới: Nếu lùi lại mà < 0, ta phải bắt đầu từ 0
    start_idx = max(0, start_idx)
    
    # 3b. Xử lý cận trên: Nếu (start_idx + num_points) vượt quá
    # chiều dài, ta phải lùi start_idx lại.
    # Vị trí start_idx cuối cùng có thể là (n - num_points).
    start_idx = min(start_idx, n - num_points)
    
    # Chỉ số kết thúc
    end_idx = start_idx + num_points
    
    print(f"Quyết định: Chọn {num_points} điểm từ chỉ số {start_idx} đến {end_idx - 1}")

    # --- Bước 4: Trích xuất dữ liệu và kiểm tra tính cách đều ---
    selected_x = all_x_data[start_idx:end_idx]
    selected_y = all_y_data[start_idx:end_idx]
    
    # Kiểm tra tính cách đều của các điểm VỪA CHỌN
    if len(selected_x) >= 2:
        h = selected_x[1] - selected_x[0]
        for i in range(1, len(selected_x) - 1):
            # Dùng math.isclose để xử lý sai số dấu phẩy động
            if not math.isclose(selected_x[i+1] - selected_x[i], h):
                print(f"CẢNH BÁO: Các mốc x được chọn KHÔNG cách đều!")
                print(f"  Bước 1: {h}")
                print(f"  Bước {i+1}: {selected_x[i+1] - selected_x[i]}")
                print("  Thuật toán Stirling có thể thất bại hoặc không chính xác.")
                # Vẫn trả về dữ liệu, nhưng kèm cảnh báo
    
    print("--- Hoàn tất lựa chọn ---")
    return selected_x, selected_y

# === VÍ DỤ SỬ DỤNG ===
if __name__ == "__main__":
    
    # 1. Tạo một bộ dữ liệu mẫu LỚN (giả sử là bảng tra cứu)
    # Dữ liệu từ 0.0 đến 3.0, bước 0.25
    all_x = [i * 0.25 for i in range(13)] 
    # Dùng hàm y = x^3 + x^2
    all_y = [round(x**3 + x**2, 4) for x in all_x]
    
    print("=" * 50)
    print("TOÀN BỘ DỮ LIỆU GỐC:")
    print(f"X = {all_x}")
    print(f"Y = {all_y}")
    print("=" * 50)

    # 2. Tình huống 1: Nội suy ở giữa
    # Muốn nội suy tại x = 1.6 (dùng 5 điểm)
    target_1 = 1.6
    points_1 = 5
    
    x1, y1 = find_stirling_points(all_x, all_y, target_1, points_1)
    # Mong đợi:
    # Gần nhất là x=1.5 (index 6)
    # start_idx = 6 - (5-1)//2 = 4
    # end_idx = 4 + 5 = 9
    # Sẽ chọn x = [1.0, 1.25, 1.5, 1.75, 2.0]
    print(f"\nKết quả cho x = {target_1}:")
    print(f"  X đã chọn: {x1}")
    print(f"  Y đã chọn: {y1}")
    print("=" * 50)
    
    # 3. Tình huống 2: Nội suy ở gần biên (cận dưới)
    # Muốn nội suy tại x = 0.3 (dùng 5 điểm)
    target_2 = 0.3
    points_2 = 5
    
    x2, y2 = find_stirling_points(all_x, all_y, target_2, points_2)
    # Mong đợi:
    # Gần nhất là x=0.25 (index 1)
    # start_idx = 1 - (5-1)//2 = -1
    # Xử lý cận dưới: start_idx = max(0, -1) = 0
    # Xử lý cận trên: start_idx = min(0, 13-5) = 0
    # end_idx = 0 + 5 = 5
    # Sẽ chọn x = [0.0, 0.25, 0.5, 0.75, 1.0]
    print(f"\nKết quả cho x = {target_2}:")
    print(f"  X đã chọn: {x2}")
    print(f"  Y đã chọn: {y2}")
    print("=" * 50)
    
    # 4. Tình huống 3: Nội suy ở gần biên (cận trên)
    # Muốn nội suy tại x = 2.9 (dùng 5 điểm)
    target_3 = 2.9
    points_3 = 9
    
    x3, y3 = find_stirling_points(all_x, all_y, target_3, points_3)
    # Mong đợi:
    # Gần nhất là x=3.0 (index 12)
    # start_idx = 12 - (5-1)//2 = 10
    # Xử lý cận dưới: start_idx = max(0, 10) = 10
    # Xử lý cận trên: start_idx = min(10, 13-5) = min(10, 8) = 8
    # end_idx = 8 + 5 = 13
    # Sẽ chọn x = [2.0, 2.25, 2.5, 2.75, 3.0]
    print(f"\nKết quả cho x = {target_3}:")
    print(f"  X đã chọn: {x3}")
    print(f"  Y đã chọn: {y3}")
    print("=" * 50)