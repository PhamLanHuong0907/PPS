import sympy # type: ignore
import os
import sys

# Dòng này tìm thư mục 'code_thuattoan' ở bên ngoài thư mục 'example'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))

try:
    # Đảm bảo bạn đang import file "noisuynguoc.py" đã được chỉnh sửa
    from noisuynguoc import inverse_lagrange_polynomial # type: ignore
except ImportError:
    print("LỖI: Không tìm thấy file 'noisuynguoc.py'.")
    print("Hãy kiểm tra cấu trúc thư mục của bạn.")
    sys.exit(1)
except ModuleNotFoundError:
    print("LỖI: Bạn cần cài đặt thư viện 'sympy'.")
    print("     Hãy chạy lệnh: pip install sympy")
    sys.exit(1)

# --- Bật cờ VERBOSE để in ra các bước ---
VERBOSE_MODE = True

# --- Ví dụ 1: Input là số (Thành công) ---
print("=" * 40)
print("Ví dụ 1: Dữ liệu số (Thành công)")
x_data_1 = [1, 2, 3]
y_data_1 = [1, 8, 27] # (Đơn điệu, Phân biệt)
y_star_1 = 10 

# Hàm sẽ tự in các bước 1-5
P_y_1, x_star_1 = inverse_lagrange_polynomial(y_data_1, x_data_1, y_star_1, verbose=VERBOSE_MODE)

if P_y_1 is not None:
    print("\n--- KẾT QUẢ (VÍ DỤ 1) ---")
    # (Kết quả P(y) và x* đã được in ở Bước 5)
    print(f"(Kiểm tra giá trị số: {x_star_1.evalf()})")
print("=" * 40)


# --- Ví dụ 2: Input là symbolic (Thành công) ---
print("=" * 40)
print("Ví dụ 2: Dữ liệu symbolic (Thành công)")
x1, x2, y1, y2, y_star = sympy.symbols('x1 x2 y1 y2 y_star')
x_data_2 = [x1, x2]
y_data_2 = [y1, y2]
y_star_2 = y_star

# Hàm sẽ tự in các bước 1-5
P_y_2, x_star_2 = inverse_lagrange_polynomial(y_data_2, x_data_2, y_star_2, verbose=VERBOSE_MODE)

if P_y_2 is not None:
    print("\n--- KẾT QUẢ (VÍ DỤ 2) ---")
    print("(Hàm đã chạy thành công)")
print("=" * 40)


# --- Ví dụ 3: Thất bại (Không đơn điệu) ---
print("=" * 40)
print("Ví dụ 3: Dữ liệu số (Thất bại - Không đơn điệu)")
x_data_3 = [1, 2, 3]
y_data_3 = [1, 5, 2] # Lỗi: Lên rồi xuống
y_star_3 = 3

# Hàm sẽ tự in lỗi ở Bước 2
P_y_3, x_star_3 = inverse_lagrange_polynomial(y_data_3, x_data_3, y_star_3, verbose=VERBOSE_MODE)

if P_y_3 is None:
    print("\n--- KẾT QUẢ (VÍ DỤ 3) ---")
    print("Thuật toán đã dừng lại như mong đợi do Y không đơn điệu.")
print("=" * 40)


# --- Ví dụ 4: Thất bại (Không phân biệt) ---
print("=" * 40)
print("Ví dụ 4: Dữ liệu số (Thất bại - Không phân biệt)")
x_data_4 = [1, 2, 3]
y_data_4 = [1, 5, 5] # Lỗi: 5 bị lặp lại
y_star_4 = 3

# Hàm sẽ tự in lỗi ở Bước 2
P_y_4, x_star_4 = inverse_lagrange_polynomial(y_data_4, x_data_4, y_star_4, verbose=VERBOSE_MODE)

if P_y_4 is None:
    print("\n--- KẾT QUẢ (VÍ DỤ 4) ---")
    print("Thuật toán đã dừng lại như mong đợi do Y không phân biệt.")
print("=" * 40)