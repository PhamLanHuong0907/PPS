import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==============================================================================
# 1. HÀM LÕI: GIẢI BÀI TOÁN TỔNG QUÁT VÀ IN MA TRẬN
# ==============================================================================

def least_squares_detailed(x, y, basis_funcs, case_name=""):
    """
    Hàm lõi để khớp mô hình tổng quát và in ra các ma trận trung gian.
    Trả về một dictionary chứa hệ số, y dự đoán, và sai số.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    # 1. Xây dựng ma trận theta (Φ) từ các hàm cơ sở
    theta = np.column_stack([[f(xi) for xi in x] for f in basis_funcs])
    
    # 2. Tính toán các ma trận trung gian
    theta_T = theta.T
    m_matrix = theta_T @ theta
    b_vector = theta_T @ y

    # 3. In các ma trận ra màn hình
    np.set_printoptions(precision=4, suppress=True)
    print(f"\n===== CÁC MA TRẬN TRUNG GIAN ({case_name}) =====")
    print("Ma trận theta (Φ):\n", theta)
    print("\nMa trận m = Φᵀ * Φ:\n", m_matrix)
    print("\nVector b = Φᵀ * Y:\n", b_vector)
    print("=" * (45 + len(case_name)))

    # 4. Giải hệ phương trình để tìm các hệ số
    coeffs, *_ = np.linalg.lstsq(theta, y, rcond=None)
    
    # 5. Tính toán kết quả
    y_pred = theta @ coeffs
    rmse = np.sqrt(np.mean((np.asarray(y) - y_pred) ** 2))
    
    return {"coeffs": coeffs, "y_pred": y_pred, "rmse": rmse}

# ==============================================================================
# 2. CÁC HÀM CHUYÊN BIỆT (GỌI ĐẾN HÀM LÕI)
# ==============================================================================

# 2.1. Hàm cho mô hình y = a * exp(b1*phi1(x) + b2*phi2(x))
def fit_exponential_detailed(x_data, y_data, phi1, phi2, case_name="Hàm Mũ"):
    """
    Tìm hệ số cho hàm mũ và in ma trận của bài toán đã tuyến tính hóa.
    """
    print(f"--- Bắt đầu xử lý {case_name} ---")
    
    # Tuyến tính hóa: ln(y) = ln(a) + b1*phi1(x) + b2*phi2(x)
    # Đặt Y = ln(y), a0 = ln(a). Y = a0*1 + b1*phi1(x) + b2*phi2(x)
    if not np.all(np.array(y_data) > 0):
        raise ValueError("Lỗi hàm mũ: Tất cả giá trị y phải > 0 để lấy logarit.")
    
    Y_data = np.log(y_data)
    basis_funcs_linear = [lambda x: 1, phi1, phi2]
    
    # Gọi hàm lõi cho bài toán đã tuyến tính hóa (với Y = log(y))
    results_linear = least_squares_detailed(x_data, Y_data, basis_funcs_linear, case_name)
    a0, b1, b2 = results_linear["coeffs"]
    
    # Suy ngược lại hệ số gốc 'a'
    a = np.exp(a0)
    
    # Tính lại y_pred và sai số trên thang đo gốc
    y_pred_original = a * np.exp(b1 * phi1(x_data) + b2 * phi2(x_data))
    rmse_original = np.sqrt(np.mean((y_data - y_pred_original) ** 2))
    
    return {"a": a, "b1": b1, "b2": b2, "rmse": rmse_original}

# 2.2. Hàm cho mô hình y = a * x^b
def fit_power_law_detailed(x_data, y_data, case_name="Hàm Lũy Thừa", min_positive=1e-9):
    """
    Tìm hệ số cho hàm lũy thừa, tự động TỊNH TIẾN dữ liệu y nếu có giá trị không dương.
    In ma trận của bài toán đã tuyến tính hóa.
    """
    print(f"--- Bắt đầu xử lý {case_name} ---")
    x = np.asarray(x_data, dtype=float)
    y = np.asarray(y_data, dtype=float)

    # Bước 1: Kiểm tra và tịnh tiến dữ liệu nếu cần
    shift_y = 0.0
    y_processed = y

    # Chỉ tịnh tiến y nếu có giá trị y <= 0
    if np.any(y <= 0):
        # Lượng tịnh tiến = giá trị nhỏ nhất của y (sẽ là số âm) + một số rất nhỏ
        shift_y = -np.min(y) + min_positive
        y_processed = y + shift_y
        print(f"(!) Cảnh báo: Dữ liệu y có giá trị không dương. Tự động tịnh tiến y lên {shift_y:.4f} đơn vị.")
    
    # Kiểm tra x (thường x đã > 0, nhưng để an toàn)
    if np.any(x <= 0):
        raise ValueError(f"Lỗi {case_name}: Tất cả giá trị x phải > 0.")

    # Bước 2: Tuyến tính hóa trên dữ liệu đã được xử lý
    # log(y_processed) = b*log(x) + log(a)
    log_x = np.log(x)
    log_y = np.log(y_processed)
    basis_funcs_linear = [lambda X: 1, lambda X: X]
    
    # Bước 3: Gọi hàm lõi để giải và in ma trận
    results_linear = least_squares_detailed(log_x, log_y, basis_funcs_linear, case_name)
    a0, b = results_linear["coeffs"]
    
    # Bước 4: Suy ngược lại hệ số gốc 'a'
    a = np.exp(a0)

    # Bước 5: Tính lại y_pred và sai số trên thang đo GỐC
    # Hàm thực nghiệm sẽ có dạng g(x) = a * x^b - shift_y
    y_pred_original = a * (x**b) - shift_y
    rmse_original = np.sqrt(np.mean((y_data - y_pred_original)**2))

    # Trả về các giá trị bao gồm cả lượng đã tịnh tiến
    return {"a": a, "b": b, "shift_y": shift_y, "rmse": rmse_original}

# ==============================================================================
# 3. PHẦN THỰC THI CHÍNH (ĐÃ SỬA LỖI)
# ==============================================================================

if __name__ == '__main__':
    try:
        # ---- SỬA LỖI ĐỌC DỮ LIỆU ----
        # 1. Sửa đường dẫn thành 'data.csv'
        # 2. Thêm header=None để pandas không đọc dòng đầu làm tiêu đề
        # 3. Thêm encoding='utf-8' để đọc đúng tiếng Việt
        df = pd.read_csv('File csv/data.csv', header=None, encoding='utf-8')
        print("✓ Đã đọc dữ liệu từ 'data.csv' thành công.\n")

        # ---- Xử lý dữ liệu cho từng câu bằng VỊ TRÍ CỘT ----
        # .iloc[1:, CỘT] -> Lấy từ dòng thứ hai trở đi, ở cột có chỉ số CỘT
        # .astype(float) -> Chuyển dữ liệu sang dạng số để tính toán
        
        # Dữ liệu Câu a: cột 1 (x) và cột 2 (y)
        x_a = df.iloc[1:, 1].astype(float)
        y_a = df.iloc[1:, 2].astype(float)

        # Dữ liệu Câu b: cột 6 (x) và cột 7 (y)
        x_b = df.iloc[1:, 6].astype(float)
        y_b = df.iloc[1:, 7].astype(float)
        
        # Dữ liệu Câu c: cột 11 (x) và cột 12 (y)
        x_c = df.iloc[1:, 11].astype(float)
        y_c = df.iloc[1:, 12].astype(float)
        
        # Dữ liệu Câu d: cột 16 (x) và cột 17 (y)
        x_d = df.iloc[1:, 16].astype(float)
        y_d = df.iloc[1:, 17].astype(float)


        # #######################################################################
        # --- TRƯỜNG HỢP a: y = ax + b/x (Sử dụng dữ liệu của Câu a) ---
        # #######################################################################
        print("--- Bắt đầu xử lý TRƯỜNG HỢP a: y = ax + b/x ---")
        basis_funcs_a = [lambda x: x, lambda x: 1/x]
        results_a = least_squares_detailed(x_a, y_a, basis_funcs_a, case_name="Trường hợp a")
        
        a_val_a, b_val_a = results_a["coeffs"]
        sigma_a = results_a["rmse"]
        print(f"\n===== KẾT QUẢ CUỐI CÙNG (Trường hợp a) =====")
        print(f"   Các hệ số: a = {a_val_a:.4f}, b = {b_val_a:.4f}")
        print(f"   Hàm thực nghiệm g(x) = {a_val_a:.4f}*x + {b_val_a:.4f}/x")
        print(f"   Sai số trung bình phương σ = {sigma_a:.4f}")
        print("="*45, "\n\n")

        # #######################################################################
        # --- TRƯỜNG HỢP b: y = a + b*cos(x) + c*sin(x) (Sử dụng dữ liệu của Câu b) ---
        # #######################################################################
        print("--- Bắt đầu xử lý TRƯỜNG HỢP b: y = a + b*cos(x) + c*sin(x) ---")
        basis_funcs_b = [lambda x: x*x, lambda x: np.cos(x), lambda x: 1]
        results_b = least_squares_detailed(x_b, y_b, basis_funcs_b, case_name="Trường hợp b")
        
        a_val_b, b_val_b, c_val_b = results_b["coeffs"]
        sigma_b = results_b["rmse"]
        print(f"\n===== KẾT QUẢ CUỐI CÙNG (Trường hợp b) =====")
        print(f"   Các hệ số: a = {a_val_b:.4f}, b = {b_val_b:.4f}, c = {c_val_b:.4f}")
        print(f"   Hàm thực nghiệm g(x) = {a_val_b:.4f} + {b_val_b:.4f}*cos(x) + {c_val_b:.4f}*sin(x)")
        print(f"   Sai số trung bình phương σ = {sigma_b:.4f}")
        print("="*45, "\n\n")

        # #######################################################################
        # --- TRƯỜNG HỢP c: HÀM MŨ y = a * exp(b1*x) (Sử dụng dữ liệu của Câu c) ---
        # #######################################################################
        # Ví dụ đơn giản hóa y = a * exp(b1*x), nên phi2(x) = 0
        phi1_c = lambda x: x
        phi2_c = lambda x: 0 # Hàm phi2 không dùng đến
        results_c = fit_exponential_detailed(x_c, y_c, phi1_c, phi2_c, case_name="Trường hợp c - Hàm Mũ")

        a_val_c, b1_val_c, _ = results_c["a"], results_c["b1"], results_c["b2"]
        sigma_c = results_c["rmse"]
        print(f"\n===== KẾT QUẢ CUỐI CÙNG (Trường hợp c - Hàm Mũ) =====")
        print(f"   Các hệ số: a = {a_val_c:.4f}, b1 = {b1_val_c:.4f}")
        print(f"   Hàm thực nghiệm g(x) = {a_val_c:.4f} * exp({b1_val_c:.4f}*x)")
        print(f"   Sai số trung bình phương σ = {sigma_c:.4f}")
        print("="*55, "\n\n")
        
         # #######################################################################
        # --- TRƯỜNG HỢP d: HÀM LŨY THỪA y = a * x^b (Sử dụng dữ liệu của Câu d) ---
        # #######################################################################
        results_d = fit_power_law_detailed(x_d, y_d, case_name="Trường hợp d - Hàm Lũy Thừa")

        # In kết quả cuối cùng, có hiển thị cả lượng tịnh tiến
        a_val_d, b_val_d = results_d["a"], results_d["b"]
        shift_y_d = results_d["shift_y"]
        sigma_d = results_d["rmse"]
        
        print(f"\n===== KẾT QUẢ CUỐI CÙNG (Trường hợp d - Hàm Lũy Thừa) =====")
        print(f"   Các hệ số (trên dữ liệu tịnh tiến): a = {a_val_d:.4f}, b = {b_val_d:.4f}")
        
        if shift_y_d > 0:
            print(f"   Dữ liệu y đã được tịnh tiến lên: {shift_y_d:.4f}")
            print(f"   Hàm thực nghiệm g(x) = {a_val_d:.4f} * x^({b_val_d:.4f}) - {shift_y_d:.4f}")
        else:
            print(f"   Hàm thực nghiệm g(x) = {a_val_d:.4f} * x^({b_val_d:.4f})")
            
        print(f"   Sai số trung bình phương σ = {sigma_d:.4f}")
        print("="*60)

    except FileNotFoundError:
        print("\nLỖI: Không tìm thấy file 'data.csv'. Vui lòng đảm bảo file tồn tại trong cùng thư mục.")
    except Exception as e:
        print(f"\nĐÃ XẢY RA LỖI: {e}")