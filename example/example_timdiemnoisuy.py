# Import hàm từ file thư viện (phải nằm chung thư mục)
import os
import sys
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    # Đảm bảo bạn đang import file "timdiemnoisuy.py" đã được chỉnh sửa
    from timdiemnoisuy import trich_xuat_diem_phu_hop
except ImportError:
    print("Lỗi: Không tìm thấy file 'timdiemnoisuy.py'.")
    print("Hãy đảm bảo 2 file 'timdiemnoisuy.py' và 'example_timdiemnoisuy.py' nằm chung thư mục.")
    exit()

# === VÍ DỤ SỬ DỤNG ===

# 1. Tạo một bộ dữ liệu mẫu LỚN (giả sử là bảng tra cứu)
# ... (Dữ liệu all_x và all_y giữ nguyên) ...
all_x = [1,
1.117,
1.234,
1.351,
1.468,
1.585,
1.702,
1.819,
1.936,
2.053,
2.17,
2.287,
2.404,
2.521,
2.638,
2.755,
2.872,
2.989,
3.106,
3.223,
3.34,
3.457,
3.574,
3.691,
3.808,
3.925,
4.042,
4.159,
4.276,
4.393,
4.51,
4.627,
4.744,
4.861,
4.978,
5.095,
5.212,
5.329,
5.446,
5.563,
5.68,
5.797,
5.914,
6.031,
6.148,
6.265,
6.382,
6.499,
6.616,
6.733,
6.85,
6.967,
7.084,
7.201,
7.318,
7.435,
7.552,
7.669,
7.786,
7.903,
8.02,
8.137,
8.254,
8.371,
8.488,
8.605,
8.722,
8.839,
8.956,
9.073,
9.19,
9.307,
9.424,
9.541,
9.658,
9.775,
9.892,
10.009,
10.126,
10.243,
10.36,
10.477,
10.594,
10.711,
10.828,
10.945,
11.062,
11.179,
11.296,
11.413,
11.53,
11.647,
11.764,
11.881,
11.998,
12.115,
12.232,
12.349,
12.466,
12.583,
12.7,
12.817,
12.934,
13.051,
13.168,
13.285
]
all_y = [-0.747,
-0.2589,
0.2491,
0.7717,
1.303,
1.8373,
2.3683,
2.89,
3.3963,
3.8813,
4.3392,
4.7648,
5.1531,
5.4996,
5.8004,
6.0521,
6.2522,
6.3985,
6.4899,
6.5257,
6.5061,
6.4321,
6.3054,
6.1283,
5.9039,
5.6358,
5.3284,
4.9864,
4.6151,
4.2201,
3.8074,
3.3832,
2.9538,
2.5258,
2.1053,
1.6988,
1.3123,
0.9516,
0.6221,
0.3288,
0.0763,
-0.1315,
-0.2913,
-0.4004,
-0.4569,
-0.4596,
-0.4078,
-0.3019,
-0.1429,
0.0675,
0.3269,
0.6322,
0.9796,
1.3648,
1.783,
2.2288,
2.6967,
3.1807,
3.6744,
4.1717,
4.666,
5.1511,
5.6207,
6.0689,
6.4897,
6.878,
7.2288,
7.5377,
7.8007,
8.0149,
8.1775,
8.2867,
8.3414,
8.3413,
8.2867,
8.1787,
8.0192,
7.8107,
7.5564,
7.2602,
6.9265,
6.5601,
6.1665,
5.7514,
5.3208,
4.8809,
4.4381,
3.9988,
3.5694,
3.156,
2.7647,
2.4011,
2.0706,
1.7779,
1.5275,
1.323,
1.1676,
1.0638,
1.0133,
1.0171,
1.0755,
1.188,
1.3533,
1.5696,
1.8342,
2.1438
]


print("=" * 50)
print("TOÀN BỘ DỮ LIỆU GỐC:")
print(f"X = {all_x}")
print(f"Y = {all_y}")
print("=" * 50)

# 2. Tình huống 1: Nội suy ở giữa
target_1 = 4
points_1 = 9
print(f"\n--- Tình huống 1: x = {target_1}, k = {points_1} ---")
# Gọi hàm đã import (Hàm sẽ tự in các bước)
x1, y1 = trich_xuat_diem_phu_hop(all_x, all_y, target_1, points_1)
print("=" * 50)

# 3. Tình huống 2: Nội suy ở gần biên (cận dưới)
target_2 = 0.3
points_2 = 5
print(f"\n--- Tình huống 2: x = {target_2}, k = {points_2} ---")
# Gọi hàm đã import (Hàm sẽ tự in các bước)
x2, y2 = trich_xuat_diem_phu_hop(all_x, all_y, target_2, points_2)
print("=" * 50)

# 4. Tình huống 3: Nội suy ở gần biên (cận trên)
target_3 = 2.9
points_3 = 9 
print(f"\n--- Tình huống 3: x = {target_3}, k = {points_3} ---")
# Gọi hàm đã import (Hàm sẽ tự in các bước)
x3, y3 = trich_xuat_diem_phu_hop(all_x, all_y, target_3, points_3)
print("=" * 50)


# 5. Tình huống 4: Dùng mảng BIỂU THỨC (Thành công)
print("\n" + "=" * 50)
print("TOÀN BỘ DỮ LIỆU GỐC (BIỂU THỨC):")
all_x_sym = ["a", "a+1", "a+2", "a+3", "a+4", "a+5"]
all_y_sym = ["y0", "y1", "y2", "y3", "y4", "y5"]
print(f"X = {all_x_sym}")
print(f"Y = {all_y_sym}")
print("=" * 50)

target_4 = "a + 3.8" # Gần "a+4"
points_4 = 3
print(f"\n--- Tình huống 4: x = {target_4}, k = {points_4} ---")
x4, y4 = trich_xuat_diem_phu_hop(all_x_sym, all_y_sym, target_4, points_4)
if x4:
    print(f"  (Kiểm tra: X mong đợi = ['a+3', 'a+4', 'a+5'])")
print("=" * 50)

# 6. Tình huống 5: Dùng mảng BIỂU THỨC (Thất bại)
print(f"\n--- Tình huống 5: x = 'b', k = 3 (Thử nghiệm thất bại) ---")
target_5 = "b" # Biến không liên quan
points_5 = 3
x5, y5 = trich_xuat_diem_phu_hop(all_x_sym, all_y_sym, target_5, points_5)
# (Hàm sẽ tự in lỗi "j' là biểu thức")
if x5 is None:
    print("  -> Thất bại như mong đợi.")
print("=" * 50)