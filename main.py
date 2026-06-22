# -*- coding: utf-8 -*-
"""
main.py
--------
Điểm khởi chạy chương trình Rikkei HR Simulator Pro.
Chỉ chịu trách nhiệm hiển thị menu và điều phối (route) sang các module
feature_*.py. Toàn bộ logic nghiệp vụ nằm trong các module riêng để dễ
quản lý, mở rộng và sửa lỗi độc lập.
"""

from feature_hire_employee import feature1_hire_employee
from feature_view_info import feature2_view_info
from feature_work_kpi import feature3_work_kpi
from feature_payroll_summary import feature4_payroll_summary
from feature_compare_hours import feature5_compare_hours
from feature_disburse_salary import feature6_disburse_salary


def main():
    # State chung của toàn hệ thống
    employees = []           # Danh sách toàn bộ nhân sự đã tuyển dụng
    current_employee = None  # Nhân sự đang được chọn để thao tác

    while True:
        print("\n" + " RIKKEI EDUCATION HR SIMULATOR PRO ".center(70, "="))
        print('''
        1. Tuyển dụng nhân sự mới (Chọn loại hợp đồng nhân sự)
        2. Xem thông tin & Kiểm tra thứ tự kế thừa (MRO)
        3. Ghi nhận công nhật & Cập nhật KPI (Tính đa hình)
        4. Tổng hợp quỹ lương và ngân sách chi trả
        5. Kiểm tra gộp giờ làm việc & So sánh hiệu suất (Overloading)
        6. Giải ngân lương qua Cổng thanh toán đối tác (Duck Typing)
        7. Thoát chương trình
        ''')
        print("=" * 70)

        choice = input("Chọn chức năng (1-7): ").strip()

        match choice:
            case "1":
                new_emp = feature1_hire_employee(employees)
                if new_emp is not None:
                    current_employee = new_emp

            case "2":
                feature2_view_info(current_employee)

            case "3":
                feature3_work_kpi(current_employee)

            case "4":
                feature4_payroll_summary(current_employee)

            case "5":
                feature5_compare_hours(employees, current_employee)

            case "6":
                feature6_disburse_salary(current_employee)

            case "7":
                print("\nCảm ơn đã sử dụng hệ thống Quản lý Nhân sự Rikkei Education Pro!")
                break

            case _:
                print("\nChức năng không tồn tại!")


if __name__ == "__main__":
    main()
