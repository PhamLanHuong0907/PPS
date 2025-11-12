# Import hàm từ file thư viện (phải nằm chung thư mục)
import os
import sys
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    from timdiemnoisuy import trich_xuat_diem_phu_hop
except ImportError:
    print("Lỗi: Không tìm thấy file 'thu_vien_trich_xuat.py'.")
    print("Hãy đảm bảo 2 file 'thu_vien_trich_xuat.py' và 'example_trich_xuat.py' nằm chung thư mục.")
    exit()

# === VÍ DỤ SỬ DỤNG ===
# (Phần code này sẽ chạy khi bạn thực thi file example_trich_xuat.py)

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

# Gọi hàm đã import
x1, y1 = trich_xuat_diem_phu_hop(all_x, all_y, target_1, points_1)

if x1: # Kiểm tra xem hàm có trả về kết quả không
    print(f"\nKết quả cho x = {target_1}:")
    print(f" 	X đã chọn: {x1}")
    print(f" 	Y đã chọn: {y1}")
print("=" * 50)

# 3. Tình huống 2: Nội suy ở gần biên (cận dưới)
# Muốn nội suy tại x = 0.3 (dùng 5 điểm)
target_2 = 0.3
points_2 = 5

# Gọi hàm đã import
x2, y2 = trich_xuat_diem_phu_hop(all_x, all_y, target_2, points_2)

if x2:
    print(f"\nKết quả cho x = {target_2}:")
    print(f" 	X đã chọn: {x2}")
    print(f" 	Y đã chọn: {y2}")
print("=" * 50)

# 4. Tình huống 3: Nội suy ở gần biên (cận trên)
# Muốn nội suy tại x = 2.9 (dùng 9 điểm)
target_3 = 2.9
points_3 = 9 # Đổi k=9 như trong ví dụ gốc của bạn

# Gọi hàm đã import
x3, y3 = trich_xuat_diem_phu_hop(all_x, all_y, target_3, points_3)

if x3:
    print(f"\nKết quả cho x = {target_3}:")
    print(f" 	X đã chọn: {x3}")
    print(f" 	Y đã chọn: {y3}")
print("=" * 50)
print("\n" + "=" * 50)
print("TOÀN BỘ DỮ LIỆU GỐC (BIỂU THỨC):")
all_x_sym = ["a", "a+1", "a+2", "a+3", "a+4", "a+5"]
all_y_sym = ["y0", "y1", "y2", "y3", "y4", "y5"]
print(f"X = {all_x_sym}")
print(f"Y = {all_y_sym}")
print("=" * 50)

target_4 = "a + 3.8" # Gần "a+4"
points_4 = 3
x4, y4 = trich_xuat_diem_phu_hop(all_x_sym, all_y_sym, target_4, points_4)
# Mong đợi:
# h = (a+1) - a = 1
# j' = ((a+3.8) - a) / 1 = 3.8
# j = round(3.8) = 4
# start_idx = 4 - (3-1)//2 = 3
# end_idx = 3 + 3 = 6
# Sẽ chọn X = ["a+3", "a+4", "a+5"]
if x4:
    print(f"\nKết quả cho x = {target_4}:")
    print(f" 	X đã chọn: {x4}")
    print(f" 	Y đã chọn: {y4}")
print("=" * 50)

# 6. Tình huống 5: Dùng mảng BIỂU THỨC (Thất bại)
print("\n--- Tình huống 5: Thử nghiệm thất bại (đúng như mong đợi) ---")
target_5 = "b" # Biến không liên quan
points_5 = 3
x5, y5 = trich_xuat_diem_phu_hop(all_x_sym, all_y_sym, target_5, points_5)
# Mong đợi:
# j' = (b - a) / 1 = b - a (không phải là số)
if x5 is None:
    print("-> Thất bại như mong đợi vì j' là biểu thức 'b - a'")
print("=" * 50)