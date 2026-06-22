# -*- coding: utf-8 -*-
"""
feature_compare_hours.py
--------------------------
Chức năng 5: Kiểm tra gộp giờ làm việc & So sánh hiệu suất (Operator Overloading).

Sử dụng __lt__ (so sánh giờ công bằng toán tử <) và __add__ (gộp giờ công
bằng toán tử +) đã được nạp chồng trong BaseEmployee.
"""


def feature5_compare_hours(employees, current_employee):
    if current_employee is None:
        print("\nVui lòng tuyển dụng/chọn nhân sự hiện tại trước (Chức năng 1).")
        return

    others = [e for e in employees if e is not current_employee]
    if not others:
        print("\nHệ thống chưa có nhân sự khác để so sánh/gộp giờ công.")
        return

    print("\n--- ĐỒNG BỘ & SO SÁNH GIỜ CÔNG (OPERATOR OVERLOADING) ---")
    print(f"Nhân sự hiện tại (A): {current_employee.full_name} (Giờ công: {current_employee.working_hours} giờ)")
    print("Danh sách nhân sự khác trong hệ thống:")
    for idx, e in enumerate(others, start=1):
        print(f"{idx}. {e.emp_code} - {e.full_name} (Giờ công: {e.working_hours} giờ)")

    choice = input("Chọn nhân sự đối ứng (B) theo số thứ tự: ").strip()
    try:
        target = others[int(choice) - 1]
    except (ValueError, IndexError):
        print("Lựa chọn không hợp lệ!")
        return

    print(f"Nhân sự đối ứng (B): {target.full_name} (Giờ công: {target.working_hours} giờ)")

    # --- Toán tử __lt__ (Bẫy 3: nếu kiểu không hợp lệ, Python ném TypeError
    # vì __lt__ trả về NotImplemented khi không phải BaseEmployee) ---
    try:
        if current_employee < target:
            print("[Kết quả So sánh (__lt__)]: Giờ công cống hiến của nhân sự A ÍT HƠN nhân sự B.")
        else:
            print("[Kết quả So sánh (__lt__)]: Giờ công cống hiến của nhân sự A NHIỀU HƠN HOẶC BẰNG nhân sự B.")
    except TypeError:
        print("[Kết quả So sánh (__lt__)]: Không thể so sánh (kiểu dữ liệu không hợp lệ).")

    # --- Toán tử __add__ ---
    try:
        total_hours = current_employee + target
        print(f"[Kết quả Tổng hợp (__add__)]: Tổng số giờ làm việc của cả 2 nhân sự là: {total_hours} giờ.")
    except TypeError:
        print("[Kết quả Tổng hợp (__add__)]: Không thể cộng (kiểu dữ liệu không hợp lệ).")
