# -*- coding: utf-8 -*-
"""
employee_models.py
-------------------
Module định nghĩa toàn bộ các lớp nhân sự của hệ thống Rikkei HR Simulator
Pro: lớp trừu tượng BaseEmployee, các lớp con Lecturer / AdmissionStaff, và
lớp đa kế thừa kiểu "diamond" HybridManager.
"""

from abc import ABC, abstractmethod


class BaseEmployee(ABC):
    """
    Lớp trừu tượng (Abstract Base Class) làm bộ khung chuẩn cho mọi nhân sự.
    Không thể khởi tạo trực tiếp lớp này vì có chứa @abstractmethod (Bẫy 1:
    Python tự ném TypeError qua ABCMeta, không cần code thêm).
    """

    # Class Attributes: dùng chung toàn hệ thống
    company_name = "Rikkei Education"
    base_salary_rate = 3_000_000  # Mức lương cơ sở / giờ (VND)

    def __init__(self, emp_code, full_name, working_hours=0, **kwargs):
        self._emp_code = emp_code
        # Gọi qua property setter để tự động chuẩn hóa họ tên
        self.full_name = full_name
        # Private attribute (đóng gói giờ làm việc) -> _BaseEmployee__working_hours
        self.__working_hours = working_hours
        # Cooperative super(): đi theo MRO của lớp thực thể đang tạo ra, xem
        # giải thích chi tiết trong HybridManager.
        super().__init__(**kwargs)

    # ---------------------- PROPERTIES ----------------------
    @property
    def working_hours(self):
        """Chỉ cho đọc số giờ làm việc, không có setter để chặn sửa đổi bừa bãi."""
        return self.__working_hours

    @property
    def emp_code(self):
        return self._emp_code

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, name):
        # Chuẩn hóa: xóa khoảng trắng thừa ở 2 đầu/giữa các từ, sau đó in hoa
        self._full_name = " ".join(name.split()).upper()

    # ---------------------- PROTECTED HELPER ----------------------
    def _adjust_hours(self, delta):
        """
        Vì __working_hours bị name-mangling (chỉ BaseEmployee truy cập được
        trực tiếp), các lớp con dùng phương thức bảo vệ này để cộng/trừ giờ
        công một cách an toàn, vẫn giữ nguyên tính đóng gói (encapsulation).
        """
        self.__working_hours += delta

    # ---------------------- ABSTRACT METHODS ----------------------
    @abstractmethod
    def calculate_salary(self):
        """Mỗi loại nhân sự phải tự định nghĩa công thức tính lương (Đa hình)."""
        raise NotImplementedError

    @abstractmethod
    def update_kpi(self, progress):
        """Mỗi loại nhân sự phải tự định nghĩa cách cập nhật KPI (Đa hình)."""
        raise NotImplementedError

    # ---------------------- OPERATOR OVERLOADING ----------------------
    def __add__(self, other):
        """
        Nạp chồng toán tử +: cộng giờ làm việc của 2 nhân sự bất kỳ.
        Bẫy 3: nếu `other` không phải BaseEmployee (str, int...) -> trả về
        NotImplemented để Python tự chuyển thành TypeError chuẩn.
        """
        if not isinstance(other, BaseEmployee):
            return NotImplemented
        return self.working_hours + other.working_hours

    def __lt__(self, other):
        """
        Nạp chồng toán tử <: so sánh giờ công của 2 nhân sự.
        Bẫy 3: tương tự __add__, trả về NotImplemented nếu kiểu không hợp lệ.
        """
        if not isinstance(other, BaseEmployee):
            return NotImplemented
        return self.working_hours < other.working_hours

    # ---------------------- STATIC & CLASS METHOD ----------------------
    @staticmethod
    def validate_employee_code(emp_code):
        """
        Static method: logic kiểm tra hoàn toàn độc lập với trạng thái của
        đối tượng/lớp. Mã nhân sự phải là chuỗi đúng 10 ký tự và bắt đầu
        bằng "RKE" (ví dụ "RKE1234567").
        """
        return (
            isinstance(emp_code, str)
            and len(emp_code) == 10
            and emp_code.startswith("RKE")
        )

    @classmethod
    def update_base_salary_rate(cls, new_rate):
        """
        Class method: dùng cls để thay đổi Class Attribute `base_salary_rate`,
        áp dụng cho toàn hệ thống (mọi nhân sự đều dùng chung mức lương cơ sở
        này).
        """
        cls.base_salary_rate = new_rate

    def __repr__(self):
        return f"{type(self).__name__}({self.emp_code}, {self.full_name}, {self.working_hours}h)"


class Lecturer(BaseEmployee):
    """Giảng viên chuyên trách: lương theo giờ + phụ cấp ca dạy."""

    SLOT_BONUS = 500_000      # Phụ cấp mỗi ca dạy (VND)
    HOURS_PER_SLOT = 2        # Số giờ công tích lũy mỗi lần đứng lớp

    def __init__(self, emp_code, full_name, working_hours=0,
                 teaching_slots=0, **kwargs):
        self.teaching_slots = teaching_slots
        # super().__init__() tái sử dụng logic khởi tạo của lớp cha (kế thừa).
        # Trong ngữ cảnh đa kế thừa HybridManager, super() sẽ đi theo MRO
        # chứ không nhất thiết trỏ thẳng tới BaseEmployee.
        super().__init__(emp_code, full_name, working_hours, **kwargs)

    def calculate_salary(self):
        """
        Ghi đè (override): Lương giảng viên = working_hours * base_salary_rate
        + teaching_slots * 500,000.
        """
        base_pay = self.working_hours * self.base_salary_rate
        slot_pay = self.teaching_slots * self.SLOT_BONUS
        return base_pay + slot_pay

    def update_kpi(self, progress):
        """
        Ghi đè (override): Cập nhật tỷ lệ hoàn thành khung chương trình và
        đánh giá từ học viên (lưu vào kpi_progress dạng %).
        Bẫy 2: không chấp nhận progress <= 0.
        """
        if progress <= 0:
            raise ValueError("Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0")
        self.kpi_progress = progress
        return progress

    def conduct_class(self):
        """
        Ghi nhận một ca đứng lớp: tăng teaching_slots thêm 1 và cộng thêm 2
        giờ công vào hệ thống thông qua _adjust_hours() (protected helper của
        lớp cha).
        """
        self.teaching_slots += 1
        self._adjust_hours(self.HOURS_PER_SLOT)


class AdmissionStaff(BaseEmployee):
    """Nhân viên Tuyển sinh: lương theo giờ + hoa hồng 5% doanh số."""

    COMMISSION_RATE = 0.05  # Tỷ lệ hoa hồng doanh số

    def __init__(self, emp_code, full_name, working_hours=0,
                 revenue_generated=0, kpi_target=100_000_000, **kwargs):
        self.revenue_generated = revenue_generated
        self.kpi_target = kpi_target
        super().__init__(emp_code, full_name, working_hours, **kwargs)

    def calculate_salary(self):
        """
        Ghi đè (override): Lương tuyển sinh = working_hours * base_salary_rate
        + revenue_generated * 5% (hoa hồng doanh số).
        """
        base_pay = self.working_hours * self.base_salary_rate
        commission = self.revenue_generated * self.COMMISSION_RATE
        return base_pay + commission

    def update_kpi(self, progress):
        """
        Ghi đè (override): Cộng dồn doanh số mới vào revenue_generated.
        Bẫy 2: không chấp nhận progress <= 0.
        """
        if progress <= 0:
            raise ValueError("Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0")
        self.revenue_generated += progress
        return self.revenue_generated


class HybridManager(Lecturer, AdmissionStaff):
    """
    Nhân sự lai cao cấp (Giảng viên kiêm Quản lý Tuyển sinh): đa kế thừa
    (Multiple Inheritance) kiểu "diamond" từ CẢ Lecturer VÀ AdmissionStaff
    -- cả hai đều kế thừa từ BaseEmployee.

    MRO (Method Resolution Order) theo C3-linearization của Python:
        HybridManager -> Lecturer -> AdmissionStaff -> BaseEmployee -> ABC -> object
    Kiểm tra trực tiếp bằng HybridManager.__mro__.

    XUNG ĐỘT PHƯƠNG THỨC: cả Lecturer và AdmissionStaff đều định nghĩa
    calculate_salary() và update_kpi() với công thức khác nhau. Nếu
    HybridManager không tự override, Python chọn Lecturer (đứng trước trong
    MRO) cho cả hai -- điều này SAI với yêu cầu nghiệp vụ (HybridManager cần
    TỔ HỢP cả phụ cấp ca dạy VÀ hoa hồng doanh số). Vì vậy ta override rõ
    ràng, kết hợp đúng logic từ cả hai lớp cha.

    KHỞI TẠO (cooperative __init__): dùng super() hợp tác với **kwargs để
    toàn bộ chuỗi MRO được đi qua đúng thứ tự:
    HybridManager -> Lecturer -> AdmissionStaff -> BaseEmployee
    đảm bảo cả teaching_slots (Lecturer) và revenue_generated, kpi_target
    (AdmissionStaff) đều được gán đầy đủ chỉ với một lệnh super().__init__()
    duy nhất.
    """

    def __init__(self, emp_code, full_name, working_hours=0,
                 teaching_slots=0, revenue_generated=0, kpi_target=100_000_000):
        super().__init__(
            emp_code, full_name, working_hours,
            teaching_slots=teaching_slots,
            revenue_generated=revenue_generated,
            kpi_target=kpi_target,
        )

    def calculate_salary(self):
        """
        Giải quyết xung đột: HybridManager hưởng ĐỒng THỜI cả phụ cấp ca
        dạy của Lecturer lẫn hoa hồng doanh số của AdmissionStaff.
        Công thức tổng hợp:
            Lương cứng = working_hours * base_salary_rate
            Phụ trội    = teaching_slots * 500,000 + revenue_generated * 5%
        """
        base_pay = self.working_hours * self.base_salary_rate
        slot_pay = self.teaching_slots * self.SLOT_BONUS
        commission = self.revenue_generated * self.COMMISSION_RATE
        return base_pay + slot_pay + commission

    def update_kpi(self, progress):
        """
        Giải quyết xung đột: HybridManager cập nhật KPI theo nghiệp vụ tuyển
        sinh (cộng dồn doanh số) -- gọi đích danh AdmissionStaff.update_kpi
        thay vì để MRO tự chọn Lecturer.update_kpi (vốn chỉ lưu % hoàn thành
        chương trình, không phù hợp với vai trò tổng hợp).
        """
        return AdmissionStaff.update_kpi(self, progress)


if __name__ == "__main__":
    # Demo nhanh Bẫy 1: khởi tạo trực tiếp lớp trừu tượng BaseEmployee
    try:
        e = BaseEmployee("RKE0000001", "test")
    except TypeError as e_err:
        print(f"[Bẫy 1 - OK] Không thể khởi tạo BaseEmployee trực tiếp: {e_err}")

    print("\nMRO của HybridManager:")
    for cls in HybridManager.__mro__:
        print(" ->", cls.__name__)

    print("\nDemo khởi tạo HybridManager và kiểm tra cả 2 thuộc tính cha:")
    hm = HybridManager("RKE0012345", "  le hoang nam  ",
                        working_hours=160, teaching_slots=20,
                        revenue_generated=50_000_000, kpi_target=200_000_000)
    print(hm)
    print("teaching_slots:", hm.teaching_slots)
    print("revenue_generated:", f"{hm.revenue_generated:,} VND")
    print("Salary:", f"{hm.calculate_salary():,} VND")
