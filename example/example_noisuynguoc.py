import sympy # type: ignore
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
from noisuynguoc import inverse_lagrange_polynomial # type: ignore

# --- Ví dụ 1: Input là số ---
# Cho f(1)=1, f(2)=8, f(3)=27. Tìm x để f(x) = 10.
# (Hàm f(x) = x^3)
print("=" * 40)
print("Ví dụ 1: Dữ liệu số")
x_data_1 = [1, 2, 3]
y_data_1 = [1, 8, 27]
y_star_1 = 10 # Tìm x* sao cho y* = 10

# Nhớ rằng hàm nhận (y_data, x_data)
P_y_1, x_star_1 = inverse_lagrange_polynomial(y_data_1, x_data_1, y_star_1)
print(f"\nĐa thức nội suy P(y) = {P_y_1}")
print(f"Giá trị x* tại y*=10 là: x* = {x_star_1}")
# x = 10^(1/3) approx 2.154. Hãy xem kết quả nội suy:
print(f"(Giá trị số: {x_star_1.evalf()})")
print("=" * 40)


# --- Ví dụ 2: Input có symbolic ---
# Cho f(x1) = y1, f(x2) = y2. Tìm x* tại y_star.
# (Nội suy tuyến tính ngược)
print("=" * 40)
print("Ví dụ 2: Dữ liệu symbolic")
x1, x2, y1, y2, y_star = sympy.symbols('x1 x2 y1 y2 y_star')

x_data_2 = [x1, x2]
y_data_2 = [y1, y2]
y_star_2 = y_star

P_y_2, x_star_2 = inverse_lagrange_polynomial(y_data_2, x_data_2, y_star_2)

print(f"\nĐa thức nội suy P(y) = {P_y_2}")
print(f"Giá trị x* tại y*={y_star} là: x* = {x_star_2}")
# Kết quả nên là công thức nội suy tuyến tính:
# x1*(y_star - y2)/(y1 - y2) + x2*(y_star - y1)/(y2 - y1)
print("=" * 40)