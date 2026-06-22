# -*- coding: utf-8 -*-
"""
feature_hire_employee.py
--------------------------
Chức năng 1: Tuyển dụng nhân sự mới (Lecturer / AdmissionStaff / HybridManager).
"""

from employee_models import BaseEmployee, Lecturer, AdmissionStaff, HybridManager
from utils import parse_number


def feature1_hire_employee(employees):
    """
    Tạo và thêm một nhân sự mới vào danh sách `employees`.
    Trả về đối tượng nhân sự mới (để main.py gán làm current_employee),
    hoặc None nếu tuyển dụng thất bại (dữ liệu không hợp lệ).
    """
    print("\n--- CHỌN LOẠI NHÂN SỰ KHỞI TẠO ---")
    print("1. Lecturer (Giảng viên chuyên trách)")
    print("2. Admission Staff (Nhân viên Tuyển sinh)")
    print("3. Hybrid Manager (Quản lý kiêm Giảng dạy)")
    emp_type = input("Chọn loại nhân sự (1-3): ").strip()

    if emp_type not in ("1", "2", "3"):
        print("\nLoại nhân sự không hợp lệ!")
        return None

    emp_code = input("Nhập mã nhân sự 10 ký tự: ").strip()
    # Bẫy: mã nhân sự phải đúng 10 ký tự và bắt đầu bằng "RKE" -> @staticmethod
    if not BaseEmployee.validate_employee_code(emp_code):
        print("Mã nhân sự không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng RKE.")
        return None

    if any(e.emp_code == emp_code for e in employees):
        print("Mã nhân sự đã tồn tại trong hệ thống!")
        return None

    full_name_raw = input("Nhập họ và tên: ")

    try:
        if emp_type == "1":
            new_emp = Lecturer(emp_code, full_name_raw)
            print("\nTuyển dụng Giảng viên thành công!")

        elif emp_type == "2":
            kpi_text = input("Nhập chỉ tiêu doanh số KPI (VND, ví dụ 100000000): ").strip()
            kpi_target = int(parse_number(kpi_text))
            new_emp = AdmissionStaff(emp_code, full_name_raw, kpi_target=kpi_target)
            print("\nTuyển dụng Nhân viên Tuyển sinh thành công!")

        else:  # emp_type == "3"
            kpi_text = input("Nhập chỉ tiêu doanh số KPI (VND, ví dụ 200000000): ").strip()
            kpi_target = int(parse_number(kpi_text))
            new_emp = HybridManager(emp_code, full_name_raw, kpi_target=kpi_target)
            print("\nTuyển dụng Hybrid Manager thành công!")

    except ValueError:
        print("Dữ liệu nhập không hợp lệ!")
        return None

    employees.append(new_emp)
    print(f"Tên nhân sự: {new_emp.full_name}")
    return new_emp
