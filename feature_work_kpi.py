# -*- coding: utf-8 -*-
"""
feature_work_kpi.py
---------------------
Chức năng 3: Ghi nhận công nhật & Cập nhật KPI (Tính đa hình).

Cùng một lệnh gọi current_employee.update_kpi(progress), nhưng hành vi
xử lý tự động thay đổi tùy loại nhân sự đang active:
- Lecturer: lưu % hoàn thành chương trình.
- AdmissionStaff: cộng dồn doanh số vào revenue_generated.
- HybridManager: gọi đích danh AdmissionStaff.update_kpi (cộng dồn doanh số).
Đây chính là Đa hình (Polymorphism).
"""

from employee_models import Lecturer, HybridManager
from utils import parse_number


def feature3_work_kpi(current_employee):
    if current_employee is None:
        print("\nHệ thống chưa có nhân sự nào được chọn. Vui lòng tuyển dụng/chọn nhân sự trước.")
        return

    print("\n--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---")
    print("1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)")
    print("2. Cập nhật tiến độ KPI / Doanh số")
    choice = input("Chọn tác vụ (1-2): ").strip()

    if choice == "1":
        _handle_conduct_class(current_employee)
    elif choice == "2":
        _handle_update_kpi(current_employee)
    else:
        print("Lựa chọn không hợp lệ!")


def _handle_conduct_class(current_employee):
    # Tác vụ đứng lớp chỉ áp dụng cho Lecturer và HybridManager
    if not isinstance(current_employee, Lecturer):
        print("\nNhân viên Tuyển sinh không có tác vụ đứng lớp.")
        return
    current_employee.conduct_class()
    print("\nGhi nhận thành công! Thầy/Cô đã hoàn thành thêm 1 ca dạy.")
    print(f"Số ca dạy hiện tại: {current_employee.teaching_slots} ca.")
    print(f"Số giờ làm việc tích lũy: +{Lecturer.HOURS_PER_SLOT} giờ.")


def _handle_update_kpi(current_employee):
    text = input("Nhập giá trị doanh số hợp đồng mới mang về: ").strip()
    try:
        progress = parse_number(text)
        # Đa hình: update_kpi() tự chọn đúng hành vi theo lớp của đối tượng
        result = current_employee.update_kpi(progress)
        print("\nCập nhật KPI thành công!")
        # Hiển thị kết quả tùy loại: Lecturer lưu %, Admission/Hybrid lưu doanh số
        if isinstance(current_employee, (type(current_employee).__mro__[0],)):
            pass
        if hasattr(current_employee, "revenue_generated"):
            print(f"Doanh số tích lũy mới: {current_employee.revenue_generated:,.0f} VND.")
        else:
            print(f"Tỷ lệ hoàn thành KPI: {result:.1f}%")
    except ValueError as e:
        print(f"Cập nhật thất bại: {e}")
