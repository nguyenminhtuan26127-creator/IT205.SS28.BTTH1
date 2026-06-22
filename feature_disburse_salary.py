# -*- coding: utf-8 -*-
"""
feature_disburse_salary.py
----------------------------
Chức năng 6: Giải ngân lương qua Cổng thanh toán đối tác (Duck Typing).
"""

from payroll_service import VietcombankCorporateService, TechcombankCorporateService, execute_payroll
from utils import parse_number


def feature6_disburse_salary(current_employee):
    if current_employee is None:
        print("\nVui lòng tuyển dụng/chọn nhân sự trước khi giải ngân lương.")
        return

    print("\n--- CHI TRẢ LƯƠNG QUA CỔNG ĐỐI TÁC TRUNG GIAN ---")
    print("1. Chi trả qua tài khoản Doanh nghiệp Vietcombank")
    print("2. Chi trả qua tài khoản Doanh nghiệp Techcombank")
    choice = input("Chọn cổng ngân hàng (1-2): ").strip()

    if choice == "1":
        service = VietcombankCorporateService()
    elif choice == "2":
        service = TechcombankCorporateService()
    else:
        print("Cổng ngân hàng không hợp lệ!")
        return

    text = input("Nhập số tiền giải ngân: ").strip()
    try:
        amount = parse_number(text)
    except ValueError:
        print("Số tiền không hợp lệ!")
        return

    # execute_payroll không quan tâm `service` thuộc class ngân hàng nào
    # (Duck Typing). Bẫy 4 (AttributeError) được xử lý bên trong
    # execute_payroll() nếu service thiếu transfer_salary.
    execute_payroll(service, current_employee, amount)
