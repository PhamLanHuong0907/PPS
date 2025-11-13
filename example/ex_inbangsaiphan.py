import pandas as pd
import numpy as np

# --- Dữ liệu thô từ ma trận D (đã làm tròn) ---
D_raw = [
    [6.3054, -0.1771, -0.0473, 0.0036, 0.0008, -0.0005, 0.0008, -0.0014, 0.0024],
    [6.1283, -0.2244, -0.0437, 0.0044, 0.0003, 0.0003, -0.0006, 0.0010],
    [5.9039, -0.2681, -0.0393, 0.0047, 0.0006, -0.0003, 0.0004],
    [5.6358, -0.3074, -0.0346, 0.0053, 0.0003, 0.0001],
    [5.3284, -0.3420, -0.0293, 0.0056, 0.0004],
    [4.9864, -0.3713, -0.0237, 0.0060],
    [4.6151, -0.3950, -0.0177],
    [4.2201, -0.4127],
    [3.8074]
]
X = [3.574, 3.691, 3.808, 3.925, 4.042, 4.159, 4.276, 4.393, 4.51]
n = len(X) - 1

# --- Code sửa lỗi để tạo bảng căn giữa ---

# 1. Tạo một DataFrame rỗng với đúng kích thước và tên cột
col_names = ['i', 'xᵢ', 'yᵢ'] + [f'Δ^{j}y' for j in range(1, n + 1)]
# Sử dụng object để có thể chứa cả số và chuỗi rỗng
df = pd.DataFrame(columns=col_names, index=range(n + 1), dtype=object)

# 2. Điền các cột cơ bản
df['i'] = range(n + 1)
df['xᵢ'] = X
df['yᵢ'] = [row[0] for row in D_raw]

# 3. Điền các giá trị sai phân vào đúng vị trí trực quan
for j in range(1, n + 1):  # Lặp qua các cấp sai phân (cột)
    col_name = f'Δ^{j}y'
    for i in range(n - j + 1):  # Lặp qua các giá trị trong cột sai phân
        value = D_raw[i][j]
        # Vị trí hàng trực quan để đặt giá trị
        display_row = i + j // 2 
        # Đặt giá trị vào đúng ô trong bảng
        df.loc[display_row, col_name] = value

# 4. In kết quả đã định dạng
df_formatted = df.to_string(na_rep='', index=False)
print("--- BẢNG SAI PHÂN ĐÃ ĐƯỢC CĂN GIỮA CHUẨN XÁC ---")
print(df_formatted)