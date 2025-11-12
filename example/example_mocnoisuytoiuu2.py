import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code_thuattoan')))
from mocnoisuytoiuu2 import tim_moc_noi_suy_toi_uu_v2 as v2
n_test = 5
a_test = 0.0
b_test = 10.0

print(f"\n--- Chạy Thuật toán 2 (file ảnh thứ hai) ---")
print(f"Tìm {n_test} mốc trên khoảng [{a_test}, {b_test}]:")
moc_v2 = v2(n_test, a_test, b_test)
if moc_v2:
    for i, moc in enumerate(moc_v2):
        print(f"  v2_x_{i} = {moc:.8f}")

