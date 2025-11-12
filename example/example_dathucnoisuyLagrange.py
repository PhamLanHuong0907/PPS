# Import hàm từ file "thư viện"
# (Đảm bảo 2 file nằm chung thư mục)
import os
import sys
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    from dathucnoisuyLagrange import xay_dung_da_thuc_lagrange
except ImportError:
    print("Lỗi: Không tìm thấy file 'thu_vien_lagrange.py'.")
    print("Hãy đảm bảo 2 file 'thu_vien_lagrange.py' và 'example_lagrange.py' nằm chung thư mục.")
    exit()
except ModuleNotFoundError:
    print("Lỗi: Không tìm thấy thư viện 'sympy'.")
    print("Bạn cần cài đặt thư viện SymPy trước khi chạy.")
    print("Hãy chạy lệnh: pip install sympy")
    exit()


def chay_cac_vi_du():
    """
    Hàm chính để chạy các ví dụ ứng dụng.
    """
    
    # --- Ví dụ 1: Đa thức bậc 2 (Parabol) ---
    print("\n--- VÍ DỤ 1: Đa thức bậc 2 ---")
    # Yêu cầu: Tìm đa thức P(x) đi qua 3 điểm:
    # (0, 1), (1, 4), (2, 9)
    # Kết quả mong đợi: P(x) = x^2 + 2x + 1
    
    X1 = [0, 1, 2, 3, 6, 7,10]
    Y1 = [1, 4, 9, 12, 14, 21, 31]
    
    print(f"Các mốc X = {X1}")
    print(f"Các giá trị Y = {Y1}")
    
    # Gọi hàm đã import
    P_n1, A1 = xay_dung_da_thuc_lagrange(X1, Y1)
    
    if P_n1 is not None:
        print(f"\nĐa thức P(x) tìm được: {P_n1}")
        print(f"Các hệ số A (từ bậc cao đến thấp): {A1}")
        print(f"(Kết quả mong đợi: P(x) = x**2 + 2*x + 1, A = [1, 2, 1])")

    # --- Ví dụ 2: Đa thức bậc 1 (Đường thẳng) ---
    print("\n--- VÍ DỤ 2: Đa thức bậc 1 ---")
    # Yêu cầu: Tìm đa thức P(x) đi qua 2 điểm:
    # (2, 5), (4, 9)
    # Kết quả mong đợi: P(x) = 2x + 1
    
    X2 = [2, 4]
    Y2 = [5, 9]
    
    print(f"Các mốc X = {X2}")
    print(f"Các giá trị Y = {Y2}")
    
    # Gọi hàm đã import
    P_n2, A2 = xay_dung_da_thuc_lagrange(X2, Y2)
    
    if P_n2 is not None:
        print(f"\nĐa thức P(x) tìm được: {P_n2}")
        print(f"Các hệ số A (từ bậc cao đến thấp): {A2}")
        print(f"(Kết quả mong đợi: P(x) = 2*x + 1, A = [2, 1])")

# --------------------------------------------------------------------
# Khi bạn chạy file "example_lagrange.py", code bên dưới sẽ được thực thi
# --------------------------------------------------------------------
if __name__ == "__main__":
    print("--- ỨNG DỤNG CHẠY THỬ THUẬT TOÁN LAGRANGE ---")
    chay_cac_vi_du()