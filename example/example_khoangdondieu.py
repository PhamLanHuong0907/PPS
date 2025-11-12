import sys
import sympy 
import os
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    from khoangdondieu import tim_khoang_don_dieu
except ImportError:
    print("LỖI: Không tìm thấy file 'thu_vien_don_dieu.py'.")
    print("     Hãy đảm bảo 2 file nằm chung thư mục.")
    sys.exit(1)
except ModuleNotFoundError:
    print("LỖI: Bạn cần cài đặt thư viện 'sympy'.")
    print("     Hãy chạy lệnh: pip install sympy")
    sys.exit(1)

def chay_vi_du_don_dieu():
    print("=" * 60)
    print("  CHẠY VÍ DỤ TÌM KHOẢNG ĐƠN ĐIỆU")
    print("=" * 60)

    # --- Trường hợp 1: Mảng SỐ ---
    print("\n--- TRƯỜNG HỢP 1: Mảng SỐ ---")
    X_num = [0, 1, 2, 3, 4, 5, 6]
    Y_num = [0, 5, 10, 8, 6, 6, 7] # Tăng (2), Giảm (2), Hằng (1), Tăng (1)
    
    print("Input:")
    print(f"  X = {X_num}")
    print(f"  Y = {Y_num}")
    
    # Gọi hàm với verbose=True để in các bước
    ket_qua_1 = tim_khoang_don_dieu(X_num, Y_num, verbose=True)
    
    print("\nKết quả cuối cùng (Trường hợp 1):")
    print(f"Các khoảng đơn điệu: {ket_qua_1}")
    print("(Mong đợi: [[0, 2], [2, 5], [5, 6]])")
    
    print("\n" + "=" * 60)

    # --- Trường hợp 2: Mảng BIỂU THỨC (X là biểu thức) ---
    print("\n--- TRƯỜNG HỢP 2: Mảng BIỂU THỨC (X là biểu thức) ---")
    # Cần cú pháp SymPy đúng 'a+2*h'
    X_sym = ["a", "a+h", "a+2*h", "a+3*h"]
    Y_sym = [10, 5, 2, 5] # Giảm (2), Tăng (1)
    
    print("Input:")
    print(f"  X = {X_sym}")
    print(f"  Y = {Y_sym}")
    
    ket_qua_2 = tim_khoang_don_dieu(X_sym, Y_sym, verbose=True)
    
    print("\nKết quả cuối cùng (Trường hợp 2):")
    print(f"Các khoảng đơn điệu: {ket_qua_2}")
    print("(Mong đợi: [['a', 'a+2*h'], ['a+2*h', 'a+3*h']])")

    print("\n" + "=" * 60)
    
    # --- Trường hợp 3: Thử nghiệm thất bại (Y là biểu thức) ---
    print("\n--- TRƯỜNG HỢP 3: Thử nghiệm thất bại (Y là biểu thức) ---")
    X_fail = [0, 1]
    Y_fail = ["y", "y+0.3"]
    
    print("Input:")
    print(f"  X = {X_fail}")
    print(f"  Y = {Y_fail}")
    
    ket_qua_3 = tim_khoang_don_dieu(X_fail, Y_fail, verbose=True)
    print(f"\nKết quả cuối cùng (Trường hợp 3): {ket_qua_3}")
    print("(Mong đợi: [] và có thông báo lỗi)")

if __name__ == "__main__":
    chay_vi_du_don_dieu()