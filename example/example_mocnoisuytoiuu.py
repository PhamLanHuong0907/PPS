import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))

# Đảm bảo bạn đang import file "mocnoisuytoiuu.py" đã được chỉnh sửa ở trên
from mocnoisuytoiuu import tim_moc_noi_suy_toi_uu

def chay_vi_du():
    """
    Hàm chính để chạy các ví dụ ứng dụng.
    (Hàm tim_moc_noi_suy_toi_uu sẽ tự in chi tiết các bước)
    """
    print("--- ỨNG DỤNG CHẠY THUẬT TOÁN TÌM MỐC NỘI SUY TỐI ƯU ---")
    
    # --- Trường hợp 1: Chạy đúng với n = 5, [a, b] = [0, 10] ---
    print("\n--- Ví dụ 1: Tìm 5 mốc trên khoảng [0, 10] ---")
    n1 = 5
    a1 = 0.0
    b1 = 10.0
    
    # Gọi hàm đã import (Hàm sẽ tự in các bước 1-5)
    moc_noi_suy_1 = tim_moc_noi_suy_toi_uu(n1, a1, b1)
    
    # Không cần vòng lặp for để in lại kết quả ở đây,
    # vì Bước 5 trong hàm đã làm việc đó.

    # --- Trường hợp 2: Chạy đúng với n = 3, [a, b] = [-1, 1] ---
    print("\n--- Ví dụ 2: Tìm 3 mốc trên khoảng [-1, 1] (trường hợp chuẩn) ---")
    n2 = 3
    a2 = -1.0
    b2 = 1.0
    
    # Gọi hàm đã import (Hàm sẽ tự in các bước 1-5)
    moc_noi_suy_2 = tim_moc_noi_suy_toi_uu(n2, a2, b2)
        
    # --- Trường hợp 3: Thử nghiệm với n không hợp lệ (n = 0) ---
    print("\n--- Ví dụ 3: Thử nghiệm với n không hợp lệ (n = 0) ---")
    # Hàm sẽ tự in chi tiết lỗi (ở Bước 2)
    tim_moc_noi_suy_toi_uu(0, 0, 10) 
    
    # --- Trường hợp 4: Thử nghiệm với khoảng [a, b] không hợp lệ (a > b) ---
    print("\n--- Ví dụ 4: Thử nghiệm với khoảng không hợp lệ (a = 10, b = 5) ---")
    # Hàm sẽ tự in chi tiết lỗi (ở Bước 2)
    tim_moc_noi_suy_toi_uu(3, 10, 5)

# --------------------------------------------------------------------
# Khi bạn chạy file "example.py", code bên dưới sẽ được thực thi
# và gọi hàm chay_vi_du()
# --------------------------------------------------------------------
if __name__ == "__main__":
    chay_vi_du()