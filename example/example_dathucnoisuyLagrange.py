# Import hàm từ file "thư viện"
# (Đảm bảo 2 file nằm chung thư mục)
import os
import sys
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    # Đảm bảo bạn đang import file "dathucnoisuyLagrange.py" đã được chỉnh sửa
    from dathucnoisuyLagrange import xay_dung_da_thuc_lagrange
except ImportError:
    print("Lỗi: Không tìm thấy file 'dathucnoisuyLagrange.py'.")
    print("Hãy đảm bảo 2 file 'dathucnoisuyLagrange.py' và 'example_dathucnoisuyLagrange.py' nằm chung thư mục.")
    exit()
except ModuleNotFoundError:
    print("Lỗi: Không tìm thấy thư viện 'sympy'.")
    print("Bạn cần cài đặt thư viện SymPy trước khi chạy.")
    print("Hãy chạy lệnh: pip install sympy")
    exit()


def chay_cac_vi_du():
    """
    Hàm chính để chạy các ví dụ ứng dụng.
    (Hàm xay_dung_da_thuc_lagrange sẽ tự in chi tiết)
    """
    
    # --- Ví dụ 1: Đa thức bậc 2 (Parabol) ---
    print("\n--- VÍ DỤ 1: Đa thức bậc 2 (nhưng input là bậc 6) ---")
    # Yêu cầu: Tìm đa thức P(x) đi qua 3 điểm:
    # (0, 1), (1, 4), (2, 9)
    # Kết quả mong đợi (cũ): P(x) = x^2 + 2x + 1
    
    # Dữ liệu gốc trong file của bạn:
    X1 = [2.1, 2.2, 2.4, 2.5, 2.7, 2.8]
    Y1 = [3.178, 3.452, 3.597, 4.132, 4.376, 4.954]
    
    print(f"Các mốc X = {X1}")
    print(f"Các giá trị Y = {Y1}")
    
    # Gọi hàm đã import (Hàm sẽ tự in các bước 1-5)
    P_n1, A1 = xay_dung_da_thuc_lagrange(X1, Y1)
    
    if P_n1 is not None:
        # Hàm đã tự in kết quả chi tiết
        print(f"(Hàm đã chạy xong ví dụ 1)")
        # (Kết quả mong đợi cũ [x**2 + 2*x + 1] không áp dụng cho input này)

    # --- Ví dụ 2: Đa thức bậc 1 (Đường thẳng) ---
    print("\n--- VÍ DỤ 2: Đa thức bậc 1 ---")
    # Yêu cầu: Tìm đa thức P(x) đi qua 2 điểm:
    # (2, 5), (4, 9)
    # Kết quả mong đợi: P(x) = 2x + 1
    
    X2 = [2, 4]
    Y2 = [5, 9]
    
    print(f"Các mốc X = {X2}")
    print(f"Các giá trị Y = {Y2}")
    
    # Gọi hàm đã import (Hàm sẽ tự in các bước 1-5)
    P_n2, A2 = xay_dung_da_thuc_lagrange(X2, Y2)
    
    if P_n2 is not None:
        # Hàm đã tự in kết quả chi tiết, chỉ in dòng kiểm tra
        print(f"(Kiểm tra: Kết quả mong đợi: P(x) = 2*x + 1, A = [2, 1])")

# --------------------------------------------------------------------
# Khi bạn chạy file "example_dathucnoisuyLagrange.py", code bên dưới sẽ được thực thi
# --------------------------------------------------------------------
if __name__ == "__main__":
    print("--- ỨNG DỤNG CHẠY THỬ THUẬT TOÁN LAGRANGE ---")
    chay_cac_vi_du()