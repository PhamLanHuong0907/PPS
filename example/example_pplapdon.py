import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
from pplapdon import fixed_point_iteration # type: ignore

# --- Ví dụ 1: Input là số (Tìm nghiệm x = cos(x)) ---
print("=" * 40)
print("Ví dụ 1: Tìm nghiệm x = cos(x)")
g_expr_1 = "cos(x)" # Phải dùng hàm của 'math'
x0_1 = 0.5
tol_1 = 1e-8
max_iter_1 = 100
solution_1 = fixed_point_iteration(g_expr_1, x0_1, tol_1, max_iter_1)
print(f"Nghiệm của x = cos(x) là: {solution_1}")
print("=" * 40)


# --- Ví dụ 2: Input có chữ (tham số 'a') ---
# Tìm nghiệm của x = (x^2 + a) / 3
# Ta muốn giải f(x) = x^2 - 3x + a = 0
print("=" * 40)
print("Ví dụ 2: Tìm nghiệm x = (x^2 + a) / 3 với a = 2")
g_expr_2 = "(x**2 + a) / 3.0"
x0_2 = 0.0
tol_2 = 1e-6
max_iter_2 = 50
params_2 = {'a': 2.0} # Phải cung cấp giá trị cho 'a' để lặp
solution_2 = fixed_point_iteration(g_expr_2, x0_2, tol_2, max_iter_2, params_2)
# Nghiệm của x^2 - 3x + 2 = 0 là x=1 và x=2.
# Với x0=0, hàm lặp này hội tụ về x=1.
print(f"Nghiệm của x = (x^2 + 2)/3 là: {solution_2}")
print("=" * 40)

# --- Ví dụ 3: Cùng bài toán nhưng chọn x0 khác ---
print("=" * 40)
print("Ví dụ 3: Tìm nghiệm x = (x^2 + a) / 3 với a = 2, x0 = 3.0")
x0_3 = 3.0
solution_3 = fixed_point_iteration(g_expr_2, x0_3, tol_2, max_iter_2, params_2)
# Với x0=3.0, hàm lặp này hội tụ về x=2.
print(f"Nghiệm của x = (x^2 + 2)/3 là: {solution_3}")
print("=" * 40)