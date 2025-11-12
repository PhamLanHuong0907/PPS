import sys
import math
import sympy 
import os

try:
    # Giả sử file thư viện trích xuất của bạn tên là 'thu_vien_trich_xuat.py'
    # và file thư viện bessel là 'thu_vien_bessel.py'
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
    from timdiemnoisuy import trich_xuat_diem_phu_hop
    from bessel import xay_dung_da_thuc_bessel
except ImportError:
    print("LỖI: File này yêu cầu các file sau phải nằm chung thư mục:")
    print("  1. thu_vien_trich_xuat.py (từ bài trước)")
    print("  2. thu_vien_bessel.py (file mới)")
    sys.exit(1)
except ModuleNotFoundError:
    print("LỖI: Bạn cần cài đặt thư viện 'sympy'.")
    print("     Hãy chạy lệnh: pip install sympy")
    sys.exit(1)

# --- HÀM HỖ TRỢ ĐỂ IN BẢNG ĐẸP HƠN ---
def print_diff_table(D_table, title="Bảng sai phân"):
    print(f"\n--- {title} ---")
    print("(D[i][j] = Delta^j (y_i))")
    n = len(D_table)
    headers = [f"j={j} (Delta^{j})" for j in range(n)]
    
    print(f"{'Hàng (i)':<10}", end="")
    for h in headers:
        print(f"| {h:<15}", end="")
    print()
    print("-" * (11 + 17 * n))
    
    for i in range(n):
        print(f"{'i='+str(i):<10}", end="")
        for j in range(n - i):
            val = D_table[i][j]
            val_str = ""
            try:
                if val.is_number:
                    val_str = f"{float(val):.6f}"
                else:
                    val_str = str(val)
            except:
                val_str = str(val)
            print(f"| {val_str:<15}", end="")
        print()
    print("-" * 20)

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
    
    X_new_1, Y_new_1 = trich_xuat_diem_phu_hop(all_x, all_y, x_target_1, k_points_1)
    
    if X_new_1 is not None:
        # Xác định j_s: mốc ngay trước khoảng trung tâm
        # k=6. Khoảng trung tâm là [X[2], X[3]].
        # Vậy j_s = 2.
        j_s_1 = (k_points_1 // 2) - 1
        
        print(f"Đã trích xuất {k_points_1} điểm X: {X_new_1}")
        print(f"Mốc trung tâm x_s là X[{j_s_1}] = {X_new_1[j_s_1]}")
        
        P_n_1, P_n_1_expanded, D_table_1, B_coeffs_1, t_expr_1 = \
            xay_dung_da_thuc_bessel(X_new_1, Y_new_1, j_s_1)
        
        if P_n_1 is not None:
            # --- IN CÁC BƯỚC ---
            print("\n--- CÁC BƯỚC THUẬT TOÁN (Tình huống 1) ---")
            print_diff_table(D_table_1, f"Bước 4.1: Bảng sai phân tiến D (cho {k_points_1} điểm)")
            print(f"Bước 4.2: Các hệ số Bessel B[k]:")
            for k, B in enumerate(B_coeffs_1):
                print(f"  B[{k}] = {B}")
            print(f"Bước 4.3: Biểu thức t = {t_expr_1}")
            print(f"Bước 5: Đa thức P(x) (chưa rút gọn) = {P_n_1}")
            
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
    
    X_new_2, Y_new_2 = trich_xuat_diem_phu_hop(all_x_sym, all_y_sym, x_target_2, k_points_2)

    if X_new_2 is not None:
        # k=4. Khoảng trung tâm [X[1], X[2]]. j_s = 1.
        j_s_2 = (k_points_2 // 2) - 1
        
        print(f"Đã trích xuất {k_points_2} điểm X: {X_new_2}")
        print(f"Mốc trung tâm x_s là X[{j_s_2}] = {X_new_2[j_s_2]}")

        P_n_2, P_n_2_expanded, D_table_2, B_coeffs_2, t_expr_2 = \
            xay_dung_da_thuc_bessel(X_new_2, Y_new_2, j_s_2)
        
        if P_n_2 is not None:
            # --- IN CÁC BƯỚC ---
            print("\n--- CÁC BƯỚC THUẬT TOÁN (Tình huống 2) ---")
            print_diff_table(D_table_2, f"Bước 4.1: Bảng sai phân tiến D (cho {k_points_2} điểm)")
            print(f"Bước 4.2: Các hệ số Bessel B[k]:")
            for k, B in enumerate(B_coeffs_2):
                print(f"  B[{k}] = {B}")
            print(f"Bước 4.3: Biểu thức t = {t_expr_2}")
            
            # --- IN KẾT QUẢ CUỐI CÙNG ---
            print("\n--- KẾT QUẢ CUỐI CÙNG (Tình huống 2) ---")
            print(f"Đa thức P(x) (dạng rút gọn) = {P_n_2_expanded}")
            
            x = sympy.symbols('x')
            P_val_2 = P_n_2_expanded.subs(x, sympy.sympify(x_target_2))
            print(f"\nKiểm tra: Giá trị P({x_target_2}) = {sympy.simplify(P_val_2)}")
            # Mong đợi: (y1 + y2)/2 + (y2-y1)*(0.5 - 0.5) + ... = (y1+y2)/2
            print("(Mong đợi rút gọn: y1/2 + y2/2)")
            
    else:
        print("LỖI: Không thể trích xuất điểm cho Tình huống 2.")

if __name__ == "__main__":
    chay_vi_du_bessel()