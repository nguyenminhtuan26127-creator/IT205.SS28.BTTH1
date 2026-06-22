# -*- coding: utf-8 -*-
"""
feature_payroll_summary.py
----------------------------
Chức năng 4: Tổng hợp quỹ lương và ngân sách chi trả.

Gọi phương thức đa hình calculate_salary() của đối tượng hiện tại để tính
toán số tiền thực nhận dựa trên các biến cấu thành đặc thù của từng lớp.
"""

from employee_models import Lecturer, AdmissionStaff, HybridManager


def feature4_payroll_summary(current_employee):
    if current_employee is None:
        print("\nHệ thống chưa có nhân sự nào được chọn. Vui lòng tuyển dụng/chọn nhân sự trước.")
        return

    print("\n--- CHI TIẾT QUỸ LƯƠNG NHÂN SỰ ---")
    print(f"Nhân sự: {current_employee.full_name} (Loại: {type(current_employee).__name__})")
    print(f"Mức lương cơ sở hệ thống: {current_employee.base_salary_rate:,.0f} VND")
    print(f"Số giờ làm việc tích lũy: {current_employee.working_hours} giờ")

    base_pay = current_employee.working_hours * current_employee.base_salary_rate
    print(f"Lương cứng tính theo giờ: {base_pay:,.0f} VND")

    # Tính phụ trội theo từng loại nhân sự (đa hình về thuộc tính hiển thị)
    if isinstance(current_employee, HybridManager):
        slot_pay = current_employee.teaching_slots * Lecturer.SLOT_BONUS
        commission = current_employee.revenue_generated * AdmissionStaff.COMMISSION_RATE
        bonus = slot_pay + commission
        print(f"Phụ cấp ca dạy + Hoa hồng tuyển sinh tích hợp: {bonus:,.0f} VND")
    elif isinstance(current_employee, Lecturer):
        slot_pay = current_employee.teaching_slots * Lecturer.SLOT_BONUS
        print(f"Phụ cấp ca dạy ({current_employee.teaching_slots} ca × 500,000): {slot_pay:,.0f} VND")
    elif isinstance(current_employee, AdmissionStaff):
        commission = current_employee.revenue_generated * AdmissionStaff.COMMISSION_RATE
        print(f"Hoa hồng doanh số (5% × {current_employee.revenue_generated:,.0f}): {commission:,.0f} VND")

    # Đa hình: calculate_salary() tự chọn đúng công thức theo lớp
    total = current_employee.calculate_salary()
    print(f"Tổng lương thực nhận tháng này: {total:,.0f} VND")

    return total
