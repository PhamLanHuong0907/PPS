import sympy # type: ignore
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
# Đảm bảo bạn đang import file "stirling_interpolation.py" đã được chỉnh sửa
from stirling_interpolation import stirling_polynomial # type: ignore

# --- Ví dụ 1: Input là số ---
# Tìm đa thức nội suy cho (1.0, 1.0), (1.5, 2.375), (2.0, 5.0), (2.5, 9.375), (3.0, 16.0)
# (Đây là dữ liệu của P(x) = x^3 - x^2 + 1)
print("=" * 40)
print("Ví dụ 1: Dữ liệu số")
x_1 = [3.574, 3.691, 3.808, 3.925, 4.042, 4.159, 4.276, 4.393, 4.51]
y_1 = [6.3054, 6.1283, 5.9039, 5.6358, 5.3284, 4.9864, 4.6151, 4.2201, 3.8074]

# Hàm stirling_polynomial sẽ tự in tất cả các bước và kết quả
P_1 = stirling_polynomial(x_1, y_1)

# (Hàm đã tự in kết quả, chỉ in dòng kiểm tra)

print("=" * 40)

# --- Ví dụ 2: Input có symbolic ---
# (0, a), (1, b), (2, c)
print("=" * 40)
print("Ví dụ 2: Dữ liệu symbolic")
a, b, c = sympy.symbols('a b c')
x_2 = [0, 1, 2]
y_2 = [a, b, c]

# Hàm stirling_polynomial sẽ tự in tất cả các bước và kết quả
P_2 = stirling_polynomial(x_2, y_2)



print("=" * 40)