import sys
import math
import sympy 
import os
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    from timdiemnoisuy import trich_xuat_diem_phu_hop
    # Import cả 2 hàm Gauss I và Gauss II
    from gaussI import xay_dung_da_thuc_gauss_1
    from gaussII import xay_dung_da_thuc_gauss_2
except ImportError:
    print("LỖI: File này yêu cầu các file sau phải nằm chung thư mục:")
    print("  1. thu_vien_trich_xuat.py")
    print("  2. thu_vien_gauss.py")
    print("  3. thu_vien_newton_cach_deu.py (vì gauss cần)")
    sys.exit(1)
except ModuleNotFoundError:
    print("LỖI: Bạn cần cài đặt thư viện 'sympy'.")
    print("     Hãy chạy lệnh: pip install sympy")
    sys.exit(1)

def chay_vi_du_gauss():
    # --- Dữ liệu gốc ---
    all_x_num = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    all_y_num = [round(math.sin(x), 6) for x in all_x_num]
    all_x_sym = ["a", "a+1", "a+2", "a+3", "a+4"]
    all_y_sym = ["y0", "y1", "y2", "y3", "y4"]

    # =======================================================
    # TÌNH HUỐNG 1 & 2: GAUSS I (từ lần trước)
    # =======================================================
    
    print("=" * 50)
    print("  CHẠY VÍ DỤ NỘI SUY GAUSS I")
    print("=" * 50)
    
    # --- Tình huống 1: Gauss I (Số) ---
    print("\n--- Tình huống 1: Gauss I (Số, x = 0.35) ---")
    x_target_1 = 0.35
    k_points_1 = 5 
    X_new_1, Y_new_1 = trich_xuat_diem_phu_hop(all_x_num, all_y_num, x_target_1, k_points_1)
    
    if X_new_1 is not None:
        j0_new_1 = (k_points_1 - 1) // 2
        print(f"Đã trích xuất {k_points_1} điểm X: {X_new_1}")
        print(f"Mốc trung tâm x0 là X[{j0_new_1}] = {X_new_1[j0_new_1]}")
        
        P_n_1, P_n_1_expanded = xay_dung_da_thuc_gauss_1(X_new_1, Y_new_1, j0_new_1)
        
        if P_n_1 is not None:
            print(f" Đa thức P_Gauss_I(x) = {P_n_1_expanded}")
            x = sympy.symbols('x')
            P_val_1 = P_n_1_expanded.subs(x, x_target_1)
            print(f" Giá trị P({x_target_1}) = {P_val_1:.8f}")
    
    # --- Tình huống 2: Gauss I (Biểu thức) ---
    print("\n--- Tình huống 2: Gauss I (Biểu thức, x = 'a+0.5') ---")
    x_target_2 = "a + 0.5" 
    k_points_2 = 3
    X_new_2, Y_new_2 = trich_xuat_diem_phu_hop(all_x_sym, all_y_sym, x_target_2, k_points_2)

    if X_new_2 is not None:
        j0_new_2 = (k_points_2 - 1) // 2
        print(f"Đã trích xuất {k_points_2} điểm X: {X_new_2}")
        print(f"Mốc trung tâm x0 là X[{j0_new_2}] = {X_new_2[j0_new_2]}")

        P_n_2, P_n_2_expanded = xay_dung_da_thuc_gauss_1(X_new_2, Y_new_2, j0_new_2)
        if P_n_2 is not None:
            print(f" Đa thức P_Gauss_I(x) = {P_n_2_expanded}")


    # =======================================================
    # TÌNH HUỐNG 3 & 4: GAUSS II (mới)
    # =======================================================

    print("\n" + "=" * 50)
    print("  CHẠY VÍ DỤ NỘI SUY GAUSS II")
    print("=" * 50)

    # --- Tình huống 3: Gauss II (Số) ---
    print("\n--- Tình huống 3: Gauss II (Số, x = 0.35) ---")
    # Tận dụng X_new_1, Y_new_1, j0_new_1 từ Tình huống 1
    
    if 'X_new_1' in locals() and X_new_1 is not None:
        print(f"(Sử dụng lại 5 điểm đã trích xuất: {X_new_1})")
        print(f"(Sử dụng lại mốc trung tâm x0 = {X_new_1[j0_new_1]})")
        
        # Gọi hàm GAUSS II
        P_n_G2, P_n_G2_expanded = xay_dung_da_thuc_gauss_2(X_new_1, Y_new_1, j0_new_1)
        
        if P_n_G2 is not None:
            print(f"\nĐa thức P_Gauss_II(x) = {P_n_G2_expanded}")
            
            # So sánh
            print(f"  (So sánh P_Gauss_I(x) = {P_n_1_expanded})")
            
            x = sympy.symbols('x')
            P_val_G2 = P_n_G2_expanded.subs(x, x_target_1)
            print(f"\nGiá trị P({x_target_1}) = {P_val_G2:.8f}")
            print(f"(Giá trị thực sin(0.35) = {math.sin(0.35):.8f})")
            print("Lưu ý: Hai đa thức Gauss I và II khác nhau, nhưng khi rút gọn sẽ cho CÙNG MỘT đa thức nội suy.")
    else:
        print("LỖI: Bỏ qua Tình huống 3 vì Tình huống 1 thất bại.")

    # --- Tình huống 4: Gauss II (Biểu thức) ---
    print("\n--- Tình huống 4: Gauss II (Biểu thức, x = 'a+0.5') ---")
    
    if 'X_new_2' in locals() and X_new_2 is not None:
        print(f"(Sử dụng lại 3 điểm đã trích xuất: {X_new_2})")
        print(f"(Sử dụng lại mốc trung tâm x0 = {X_new_2[j0_new_2]})")

        # Gọi hàm GAUSS II
        P_n_G2_2, P_n_G2_2_expanded = xay_dung_da_thuc_gauss_2(X_new_2, Y_new_2, j0_new_2)
        
        if P_n_G2_2 is not None:
            print(f"\nĐa thức P_Gauss_II(x) = {P_n_G2_2_expanded}")
            print(f"  (So sánh P_Gauss_I(x) = {P_n_2_expanded})")
    else:
        print("LỖI: Bỏ qua Tình huống 4 vì Tình huống 2 thất bại.")

if __name__ == "__main__":
    chay_vi_du_gauss()