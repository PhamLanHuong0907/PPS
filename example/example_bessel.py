import sys
import math
import sympy 
import os

try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    from timdiemnoisuy import trich_xuat_diem_phu_hop
    # Đảm bảo bạn đang import file "bessel.py" đã được chỉnh sửa
    from bessel import xay_dung_da_thuc_bessel
except ImportError:
    print("LỖI: File này yêu cầu các file sau phải nằm chung thư mục:")
    print("  1. timdiemnoisuy.py (từ bài trước)")
    print("  2. bessel.py (file mới)")
    print("  3. newton_tien_moccachdeu.py (vì bessel cần)")
    sys.exit(1)
except ModuleNotFoundError:
    print("LỖI: Bạn cần cài đặt thư viện 'sympy'.")
    print("     Hãy chạy lệnh: pip install sympy")
    sys.exit(1)

# --- HÀM CHÍNH ---
def chay_vi_du_bessel():
    print("=" * 50)
    print("  CHẠY VÍ DỤ NỘI SUY BESSEL")
    print("=" * 50)
    
    all_x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    all_y = [round(math.sin(x), 6) for x in all_x]
    
    print("TOÀN BỘ DỮ LIỆU GỐC (SỐ HỌC):")
    print(f"X = {all_x}")
    print(f"Y = {all_y}")
    
    # --- Tình huống 1: Nội suy số ---
    print("\n--- Tình huống 1: Nội suy số (x = 0.35) ---")
    x_target_1 = 0.35 # Gần giữa 0.3 và 0.4
    k_points_1 = 6    # PHẢI LÀ SỐ CHẴN
    
    # Hàm trích xuất sẽ tự in các bước của nó
    X_new_1, Y_new_1 = trich_xuat_diem_phu_hop(all_x, all_y, x_target_1, k_points_1)
    
    if X_new_1 is not None:
        # Xác định j_s: mốc ngay trước khoảng trung tâm
        # k=6. Khoảng trung tâm là [X[2], X[3]].
        # Vậy j_s = 2.
        j_s_1 = (k_points_1 // 2) - 1
        
        print(f"\nĐã trích xuất {k_points_1} điểm X: {X_new_1}")
        print(f"Mốc trung tâm x_s là X[{j_s_1}] = {X_new_1[j_s_1]}")
        
        # Hàm Bessel sẽ tự in chi tiết các bước (4.1, 4.2, 4.3, 5)
        P_n_1, P_n_1_expanded = \
            xay_dung_da_thuc_bessel(X_new_1, Y_new_1, j_s_1)
        
        if P_n_1 is not None:
            # (Hàm trên đã tự in Bảng D, Hệ số B, t, P(x))
            
            # --- IN KẾT QUẢ CUỐI CÙNG ---
            print("\n--- KẾT QUẢ CUỐI CÙNG (Tình huống 1) ---")
            print(f"Đa thức P(x) (dạng rút gọn) = {P_n_1_expanded}")

            x = sympy.symbols('x')
            P_val_1 = P_n_1_expanded.subs(x, x_target_1)
            
            print(f"\nKiểm tra: Giá trị P({x_target_1}) = {P_val_1:.8f}")
            print(f"(Giá trị thực sin(0.35) = {math.sin(0.35):.8f})")
    else:
        print("LỖI: Không thể trích xuất điểm cho Tình huống 1.")
    
    print("=" * 50)

    # --- Tình huống 2: Nội suy biểu thức ---
    print("\n--- Tình huống 2: Nội suy biểu thức (x = 'a+1.5') ---")
    
    all_x_sym = ["a", "a+1", "a+2", "a+3", "a+4", "a+5"]
    all_y_sym = ["y0", "y1", "y2", "y3", "y4", "y5"]
    
    print("DỮ LIỆU GỐC (BIỂU THỨC):")
    print(f"X = {all_x_sym}")
    print(f"Y = {all_y_sym}")
    
    x_target_2 = "a + 1.5" # Giữa "a+1" và "a+2"
    k_points_2 = 4         # PHẢI LÀ SỐ CHẴN
    
    # Hàm trích xuất sẽ tự in các bước của nó
    X_new_2, Y_new_2 = trich_xuat_diem_phu_hop(all_x_sym, all_y_sym, x_target_2, k_points_2)

    if X_new_2 is not None:
        # k=4. Khoảng trung tâm [X[1], X[2]]. j_s = 1.
        j_s_2 = (k_points_2 // 2) - 1
        
        print(f"\nĐã trích xuất {k_points_2} điểm X: {X_new_2}")
        print(f"Mốc trung tâm x_s là X[{j_s_2}] = {X_new_2[j_s_2]}")

        # Hàm Bessel sẽ tự in chi tiết các bước
        P_n_2, P_n_2_expanded = \
            xay_dung_da_thuc_bessel(X_new_2, Y_new_2, j_s_2)
        
        if P_n_2 is not None:
            # (Hàm trên đã tự in Bảng D, Hệ số B, t, P(x))

            # --- IN KẾT QUẢ CUỐI CÙNG ---
            print("\n--- KẾT QUẢ CUỐI CÙNG (Tình huống 2) ---")
            print(f"Đa thức P(x) (dạng rút gọn) = {P_n_2_expanded}")
            
            x = sympy.symbols('x')
            P_val_2 = P_n_2_expanded.subs(x, sympy.sympify(x_target_2))
            print(f"\nKiểm tra: Giá trị P({x_target_2}) = {sympy.simplify(P_val_2)}")
            print("(Mong đợi rút gọn: y1/2 + y2/2)")
            
    else:
        print("LỖI: Không thể trích xuất điểm cho Tình huống 2.")

if __name__ == "__main__":
    chay_vi_du_bessel()