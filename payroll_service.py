# -*- coding: utf-8 -*-
"""
payroll_service.py
--------------------
Minh họa kỹ thuật Duck Typing: VietcombankCorporateService và
TechcombankCorporateService là 2 lớp HOÀN TOÀN ĐỘC LẬP, không kế thừa từ
một interface/abstract chung nào. Hàm execute_payroll() chỉ quan tâm đối
tượng truyền vào có phương thức transfer_salary(employee, amount) hay không.
"""


class VietcombankCorporateService:
    """Cổng chi trả doanh nghiệp Vietcombank - độc lập, không kế thừa BaseEmployee."""

    def transfer_salary(self, employee, amount):
        print(f"[Hệ thống VCB Corporate]: Đang kết nối tới cổng chi trả Rikkei...")
        return True


class TechcombankCorporateService:
    """Cổng chi trả doanh nghiệp Techcombank - độc lập, không kế thừa BaseEmployee."""

    def transfer_salary(self, employee, amount):
        print(f"[Hệ thống TCB Corporate]: Đang kết nối tới cổng chi trả Rikkei...")
        return True


def execute_payroll(payment_service, employee, amount):
    """
    Hàm toàn cục độc lập, KHÔNG quan tâm payment_service thuộc class ngân
    hàng nào. Miễn là đối tượng truyền vào có hàm transfer_salary(employee,
    amount) thì hàm này hoạt động được -- tinh thần Duck Typing, cho phép
    tích hợp hàng trăm cổng thanh toán mới (ví điện tử, ngân hàng số...)
    mà không cần sửa code ở lớp nhân sự gốc hay ở hàm này.

    Bẫy 4: nếu đối tượng truyền vào không có transfer_salary -> bắt AttributeError.
    """
    try:
        payment_service.transfer_salary(employee, amount)
        print("Xác thực đối tác bằng Duck Typing thành công!")
        print(f"Ngân hàng đối tác đã giải ngân thành công số tiền: "
              f"{amount:,.0f} VND tới nhân sự {employee.emp_code}.")
    except AttributeError:
        print("Cổng dịch vụ ngân hàng doanh nghiệp không hợp lệ hoặc chưa được liên kết liên thông kỹ thuật")
