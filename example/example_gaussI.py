import sys
import math
import sympy # Import để dùng .symbols()
import os
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    from timdiemnoisuy import trich_xuat_diem_phu_hop
    # Import hàm MỚI và hàm CŨ
    # Đảm bảo bạn đang import file "gaussI.py" đã được chỉnh sửa
    from gaussI import xay_dung_da_thuc_gauss_1, tinh_gia_tri_gauss_1
except ImportError:
    print("LỖI: File này yêu cầu các file sau phải nằm chung thư mục:")
    print("  1. timdiemnoisuy.py")
    print("  2. gaussI.py")
    print("  3. newton_tien_moccachdeu.py (vì gauss cần)")
    sys.exit(1)
except ModuleNotFoundError:
    print("LỖI: Bạn cần cài đặt thư viện 'sympy'.")
    print("     Hãy chạy lệnh: pip install sympy")
    sys.exit(1)

def chay_vi_du_gauss():
    print("=" * 50)
    print("  CHẠY VÍ DỤ NỘI SUY GAUSS I")
    print("=" * 50)
    
    all_x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    all_y = [round(math.sin(x), 6) for x in all_x]
    
    print("TOÀN BỘ DỮ LIỆU GỐC (SỐ HỌC):")
    print(f"X = {all_x}")
    print(f"Y = {all_y}")
    
    # --- Tình huống 1: Nội suy số ---
    print("\n--- Tình huống 1: Nội suy số (x = 0.35) ---")
    x_target_1 = 0.35
    k_points_1 = 5 
    
    # Hàm trích xuất sẽ tự in các bước của nó
    X_new_1, Y_new_1 = trich_xuat_diem_phu_hop(all_x, all_y, x_target_1, k_points_1)
    
    if X_new_1 is not None:
        j0_new_1 = (k_points_1 - 1) // 2
        print(f"\nĐã trích xuất {k_points_1} điểm X: {X_new_1}")
        print(f"Mốc trung tâm x0 là X[{j0_new_1}] = {X_new_1[j0_new_1]}")
        
        # --- THAY ĐỔI CHÍNH ---
        # Gọi hàm XÂY DỰNG ĐA THỨC (sẽ tự in chi tiết)
        P_n_1, P_n_1_expanded = xay_dung_da_thuc_gauss_1(X_new_1, Y_new_1, j0_new_1)
        
        if P_n_1 is not None:
            # (Hàm trên đã tự in đa thức)
            # print("\nĐA THỨC GAUSS I (dạng rút gọn):")
            # print(f" P(x) = {P_n_1_expanded}")

            # Bây giờ, chúng ta có thể DÙNG đa thức đó để tính giá trị
            x = sympy.symbols('x')
            P_val_1 = P_n_1_expanded.subs(x, x_target_1)
            
            print(f"\n  Kiểm tra: Giá trị P({x_target_1}) = {P_val_1:.8f}")
            print(f"  (Giá trị thực sin(0.35) = {math.sin(0.35):.8f})")
    else:
        print("LỖI: Không thể trích xuất điểm cho Tình huống 1.")
    
    print("=" * 50)

    # --- Tình huống 2: Nội suy biểu thức ---
    print("\n--- Tình huống 2: Nội suy biểu thức (x = 'a+0.5') ---")
    
    all_x_sym = ["a", "a+1", "a+2", "a+3", "a+4"]
    all_y_sym = ["y0", "y1", "y2", "y3", "y4"]
    
    print("DỮ LIỆU GỐC (BIỂU THỨC):")
    print(f"X = {all_x_sym}")
    print(f"Y = {all_y_sym}")
    
    x_target_2 = "a + 0.5" 
    k_points_2 = 3
    
    # Hàm trích xuất sẽ tự in các bước của nó
    X_new_2, Y_new_2 = trich_xuat_diem_phu_hop(all_x_sym, all_y_sym, x_target_2, k_points_2)

    if X_new_2 is not None:
        j0_new_2 = (k_points_2 - 1) // 2
        print(f"\nĐã trích xuất {k_points_2} điểm X: {X_new_2}")
        print(f"Mốc trung tâm x0 là X[{j0_new_2}] = {X_new_2[j0_new_2]}")

        # --- THAY ĐỔI CHÍNH ---
        # Gọi hàm XÂY DỰNG ĐA THỨC (sẽ tự in chi tiết)
        P_n_2, P_n_2_expanded = xay_dung_da_thuc_gauss_1(X_new_2, Y_new_2, j0_new_2)
        
        if P_n_2 is not None:
            # (Hàm trên đã tự in đa thức)
            # print("\nĐA THỨC GAUSS I (dạng rút gọn):")
            # print(f" P(x) = {P_n_2_expanded}")
            
            # Kiểm tra giá trị tại điểm x_target
            x = sympy.symbols('x')
            P_val_2 = P_n_2_expanded.subs(x, sympy.sympify(x_target_2))
            print(f"\n  Kiểm tra: Giá trị P({x_target_2}) = {sympy.simplify(P_val_2)}")
            print("  (Mong đợi: y0/8 + 3*y1/4 + y2/8)")
            
    else:
        print("LỖI: Không thể trích xuất điểm cho Tình huống 2.")

if __name__ == "__main__":
    chay_vi_du_gauss()