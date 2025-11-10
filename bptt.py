import numpy as np
import pandas as pd

# ==============================================================================
# a) THUẬT TOÁN BÌNH PHƯƠNG TỐI THIỂU TỔNG QUÁT
# ==============================================================================
def least_squares_fit(x_data, y_data, list_of_phi_functions):
    """
    Thực hiện thuật toán bình phương tối thiểu tổng quát để tìm hàm thực nghiệm.

    Args:
        x_data (array-like): Mảng hoặc danh sách chứa các giá trị x của dữ liệu.
        y_data (array-like): Mảng hoặc danh sách chứa các giá trị y của dữ liệu.
        list_of_phi_functions (list): Một danh sách các hàm cơ sở phi(x) (dạng lambda hoặc function).

    Returns:
        tuple: (coefficients, mean_squared_error)
               - coefficients: Mảng NumPy chứa các hệ số [a1, a2, ..., am] tìm được.
               - mean_squared_error: Sai số trung bình phương của hàm thực nghiệm.
    """
    # Chuyển input thành mảng NumPy để dễ dàng tính toán
    x_data = np.array(x_data)
    y_data = np.array(y_data)

    n = len(x_data)  # Số điểm dữ liệu
    m = len(list_of_phi_functions)  # Số hàm cơ sở

    # Bước 2: Kiểm tra điều kiện của input
    if n < m:
        raise ValueError("Số điểm dữ liệu (n) phải lớn hơn hoặc bằng số hàm cơ sở (m).")

    # Bước 4.1: Lập ma trận thiết kế Phi
    phi_matrix = np.zeros((n, m))
    for j, phi_func in enumerate(list_of_phi_functions):
        phi_matrix[:, j] = phi_func(x_data)

    # Bước 4.3: Thiết lập hệ phương trình tuyến tính chuẩn
    # M = Phi^T * Phi
    M = phi_matrix.T @ phi_matrix
    # b = Phi^T * y
    b = phi_matrix.T @ y_data

    # Bước 4.4: Giải hệ Ma = b để tìm vector hệ số a
    try:
        # Sử dụng numpy.linalg.solve để giải hệ phương trình hiệu quả và chính xác
        coefficients = np.linalg.solve(M, b)
    except np.linalg.LinAlgError:
        raise np.linalg.LinAlgError("Ma trận M không khả nghịch. Các hàm cơ sở có thể phụ thuộc tuyến tính.")

    # Bước 4.5: Tính sai số trung bình phương
    y_predicted = phi_matrix @ coefficients
    error_sum_of_squares = np.sum((y_data - y_predicted)**2)
    mean_squared_error = np.sqrt(error_sum_of_squares / n)

    # Bước 5: Trả về output
    return coefficients, mean_squared_error

# ==============================================================================
# b) THUẬT TOÁN CHO CÁC DẠNG HÀM ĐẶC BIỆT
# ==============================================================================

# b.1. Thuật toán cho hàm y = a * exp(b1*phi1(x) + b2*phi2(x))
def fit_exponential(x_data, y_data, phi1, phi2):
    """
    Tìm các hệ số a, b1, b2 cho hàm y = a * exp(b1*phi1(x) + b2*phi2(x)).
    Đây là hàm bao (wrapper) sử dụng thuật toán tổng quát sau khi tuyến tính hóa.
    """
    # Bước 2: Kiểm tra điều kiện y > 0
    if not np.all(np.array(y_data) > 0):
        raise ValueError("Tất cả các giá trị y phải lớn hơn 0 để có thể lấy logarit.")

    # Bước 4.1: Tuyến tính hóa
    # ln(y) = ln(a) + b1*phi1(x) + b2*phi2(x)
    # Đặt Y = ln(y), a0 = ln(a)
    Y_data = np.log(y_data)
    
    # Bước 4.2: Áp dụng thuật toán tổng quát với các hàm cơ sở {1, phi1, phi2}
    # Hàm `lambda x: np.ones_like(x)` tạo ra một vector toàn số 1, tương ứng với hệ số tự do a0
    basis_functions = [lambda x: np.ones_like(x), phi1, phi2]
    
    # Gọi hàm tổng quát
    coeffs_linear, _ = least_squares_fit(x_data, Y_data, basis_functions)
    
    a0, b1, b2 = coeffs_linear
    
    # Bước 4.3: Suy ngược lại các hệ số ban đầu
    a = np.exp(a0)
    
    # Bước 5: Trả về output
    return a, b1, b2

# b.2. Thuật toán cho hàm y = a * x^b
def fit_power_law(x_data, y_data):
    """
    Tìm các hệ số a, b cho hàm y = a * x^b.
    Đây là hàm bao (wrapper) sử dụng thuật toán tổng quát sau khi tuyến tính hóa.
    """
    # Bước 2: Kiểm tra điều kiện x > 0 và y > 0
    if not (np.all(np.array(x_data) > 0) and np.all(np.array(y_data) > 0)):
        raise ValueError("Tất cả giá trị x và y phải lớn hơn 0 để có thể lấy logarit.")

    # Bước 4.1: Tuyến tính hóa
    # ln(y) = ln(a) + b*ln(x)
    # Đặt Y = ln(y), X = ln(x), A = ln(a). Ta có Y = A + b*X
    X_data = np.log(x_data)
    Y_data = np.log(y_data)
    
    # Bước 4.2: Áp dụng thuật toán tổng quát với hàm cơ sở {1, X}
    basis_functions = [lambda x: np.ones_like(x), lambda x: x] # {1, X}
    
    # Gọi hàm tổng quát trên dữ liệu đã biến đổi
    coeffs_linear, _ = least_squares_fit(X_data, Y_data, basis_functions)
    
    A, b = coeffs_linear
    
    # Bước 4.3: Suy ngược hệ số
    a = np.exp(A)
    
    # Bước 5: Trả về output
    return a, b
# Đọc dữ liệu trên file csv
def load_data_from_csv(filepath, x_col_idx, y_col_idx):
    """
    Đọc và làm sạch dữ liệu từ các cột cụ thể trong file CSV.
    """
    # Đọc file, không dùng dòng đầu tiên làm header
    df = pd.read_csv(filepath, header=None)
    # Lấy 2 cột dữ liệu theo chỉ số
    data = df.iloc[1:, [x_col_idx, y_col_idx]] # Bắt đầu từ hàng 1 để bỏ qua tiêu đề
    # Loại bỏ các hàng có giá trị rỗng
    data = data.dropna()
    # Chuyển thành số
    data = data.astype(float)
    # Trả về 2 mảng numpy
    return data.iloc[:, 0].to_numpy(), data.iloc[:, 1].to_numpy()
# ==============================================================================
# KHỐI LỆNH CHÍNH ĐỂ CHẠY VÍ DỤ
# ==============================================================================

if __name__ == '__main__':
    file_path = 'data Câu 23.csv'

    # --- Câu a) y = ax + b/x ---
    print("--- Câu a) Xác định hàm thực nghiệm dạng y = ax + b/x ---")
    x_a, y_a = load_data_from_csv(file_path, x_col_idx=1, y_col_idx=2)
    phi_a = [
        lambda x: x,        # phi1(x) = x
        lambda x: 1/x       # phi2(x) = 1/x
    ]
    coeffs_a, error_a = least_squares_fit(x_a, y_a, phi_a)
    a, b = coeffs_a
    print(f"Kết quả: a = {a:.4f}, b = {b:.4f}")
    print(f"Hàm thực nghiệm: y = {a:.4f}x + {b:.4f}/x")
    print(f"Sai số trung bình phương: {error_a:.4f}\n")

    # --- Câu b) y = ax^2 + b*cos(x) + c ---
    print("--- Câu b) Xác định hàm thực nghiệm dạng y = ax^2 + b*cos(x) + c ---")
    x_b, y_b = load_data_from_csv(file_path, x_col_idx=6, y_col_idx=7)
    phi_b = [
        lambda x: x**2,         # phi1(x) = x^2
        lambda x: np.cos(x),    # phi2(x) = cos(x)
        lambda x: np.ones_like(x) # phi3(x) = 1 (cho hệ số c)
    ]
    coeffs_b, error_b = least_squares_fit(x_b, y_b, phi_b)
    a, b, c = coeffs_b
    print(f"Kết quả: a = {a:.4f}, b = {b:.4f}, c = {c:.4f}")
    print(f"Hàm thực nghiệm: y = {a:.4f}x^2 + {b:.4f}cos(x) + {c:.4f}")
    print(f"Sai số trung bình phương: {error_b:.4f}\n")

    # --- Câu c) y = a * e^(bx + cx^2) ---
    print("--- Câu c) Xác định hàm thực nghiệm dạng y = a * exp(bx + cx^2) ---")
    x_c, y_c = load_data_from_csv(file_path, x_col_idx=11, y_col_idx=12)
    
    # Tuyến tính hóa: ln(y) = ln(a) + bx + cx^2
    Y_c = np.log(y_c)
    phi_c_linear = [
        lambda x: np.ones_like(x), # Cho ln(a)
        lambda x: x,               # Cho b
        lambda x: x**2             # Cho c
    ]
    coeffs_c_linear, _ = least_squares_fit(x_c, Y_c, phi_c_linear)
    A, b, c = coeffs_c_linear
    a = np.exp(A)
    print(f"Kết quả: a = {a:.4f}, b = {b:.4f}, c = {c:.4f}")
    print(f"Hàm thực nghiệm: y = {a:.4f} * exp({b:.4f}x + {c:.4f}x^2)\n")

    # --- Câu d) y = ax^b ---
    print("--- Câu d) Xác định hàm thực nghiệm dạng y = ax^b ---")
    x_d, y_d = load_data_from_csv(file_path, x_col_idx=16, y_col_idx=17)
    # Sử dụng hàm đã viết sẵn
    a, b = fit_power_law(x_d, y_d)
    print(f"Kết quả: a = {a:.4f}, b = {b:.4f}")
    print(f"Hàm thực nghiệm: y = {a:.4f} * x^({b:.4f})")