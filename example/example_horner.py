import sympy # type: ignore
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
from thuattoanhorner_daoham import horner_k_derivative

# --- Ví dụ 1: Input hoàn toàn là số ---
# P(x) = 3x^4 - 2x^2 + 5x - 1
# Tính P(2), P'(2), P''(2) (k=2)
print("=" * 40)
print("Ví dụ 1: P(x) = 3x^4 + 0x^3 - 2x^2 + 5x - 1 tại x0 = 2, k = 2")
coeffs_1 = [3, 0, -2, 5, -1]
x0_1 = 2
k_1 = 2
results_1 = horner_k_derivative(coeffs_1, x0_1, k_1)
print("\nKết quả cuối cùng (Ví dụ 1):")
print(results_1)
print("=" * 40)


# --- Ví dụ 2: Input có cả chữ (biến symbolic) ---
# P(x) = a*x^2 + b*x + 1
# Tính P(x0), P'(x0) (k=1)
print("=" * 40)
print("Ví dụ 2: P(x) = ax^2 + bx + 1 tại x0 = x_symbol, k = 1")
a, b, x_symbol = sympy.symbols('a b x_symbol')
coeffs_2 = [a, b, 1]
x0_2 = x_symbol
k_2 = 1
results_2 = horner_k_derivative(coeffs_2, x0_2, k_2)
print("\nKết quả cuối cùng (Ví dụ 2):")
print(results_2)
print("=" * 40)

# --- Ví dụ 3: Kiểm chứng Ví dụ 2 bằng SymPy ---
print("Kiểm chứng Ví dụ 2 bằng hàm diff() của SymPy:")
x = sympy.symbols('x')
P = a*x**2 + b*x + 1
P_val = P.subs(x, x_symbol)
P_prime = sympy.diff(P, x, 1)
P_prime_val = P_prime.subs(x, x_symbol)
print(f"P({x_symbol}) = {P_val}")
print(f"P'({x_symbol}) = {P_prime_val}")
# Kết quả nên khớp với results_2