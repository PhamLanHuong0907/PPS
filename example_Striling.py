import sympy # type: ignore
from stirling_interpolation import stirling_polynomial # type: ignore

# --- Ví dụ 1: Input là số ---
# Tìm đa thức nội suy cho (1.0, 1.0), (1.5, 2.375), (2.0, 5.0), (2.5, 9.375), (3.0, 16.0)
# (Đây là dữ liệu của P(x) = x^3 - x^2 + 1)
print("=" * 40)
print("Ví dụ 1: Dữ liệu số")
x_1 = [1.0, 1.5, 2.0, 2.5, 3.0]
y_1 = [1.0, 2.375, 5.0, 9.375, 16.0]
P_1 = stirling_polynomial(x_1, y_1)
print("\nĐa thức P_1(x) = ", P_1)
print("=" * 40)


# --- Ví dụ 2: Input có symbolic ---
# (0, a), (1, b), (2, c)
print("=" * 40)
print("Ví dụ 2: Dữ liệu symbolic")
a, b, c = sympy.symbols('a b c')
x_2 = [0, 1, 2]
y_2 = [a, b, c]
P_2 = stirling_polynomial(x_2, y_2)
print("\nĐa thức P_2(x) = ", P_2)
# Kết quả nên là đa thức bậc 2 đi qua 3 điểm (Lagrange)
# P(x) = a(x-1)(x-2)/2 + b(x)(x-2)/(-1) + c(x)(x-1)/2
# P(x) = a(x^2-3x+2)/2 - b(x^2-2x) + c(x^2-x)/2
# P(x) = x^2(a/2 - b + c/2) + x(-3a/2 + 2b - c/2) + a
# Kết quả của Stirling (với x0=1, t=x-1) nên tương đương
print("=" * 40)