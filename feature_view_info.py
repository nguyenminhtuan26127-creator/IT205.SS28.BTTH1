# -*- coding: utf-8 -*-
"""
feature_view_info.py
----------------------
Chức năng 2: Xem thông tin chi tiết nhân sự hiện tại & in danh sách MRO
của lớp đó (kiểm tra kỹ thuật đa kế thừa).
"""


def feature2_view_info(current_employee):
    if current_employee is None:
        print("\nHệ thống chưa có thông tin nhân sự. Vui lòng tuyển dụng ở Chức năng 1 trước.")
        return

    print("\n--- THÔNG TIN NHÂN SỰ HIỆN TẠI ---")
    print(f"Loại nhân sự: {type(current_employee).__name__}")
    print(f"Tổ chức: {current_employee.company_name}")
    print(f"Mã nhân sự: {current_employee.emp_code}")
    print(f"Họ và tên: {current_employee.full_name}")
    print(f"Số giờ làm việc: {current_employee.working_hours} giờ")

    # Hiển thị thuộc tính riêng tùy loại nhân sự (đa hình về thuộc tính)
    if hasattr(current_employee, "teaching_slots"):
        print(f"Số ca đã dạy: {current_employee.teaching_slots} ca")
    if hasattr(current_employee, "revenue_generated"):
        print(f"Doanh số mang về: {current_employee.revenue_generated:,.0f} VND")
    if hasattr(current_employee, "kpi_target"):
        print(f"Chỉ tiêu KPI: {current_employee.kpi_target:,.0f} VND")

    print("\n--- KIỂM TRA MRO (Method Resolution Order) ---")
    mro_chain = " -> ".join(cls.__name__ for cls in type(current_employee).__mro__)
    print(mro_chain)
