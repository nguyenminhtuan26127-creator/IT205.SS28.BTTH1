# Tài Liệu Phân Tích & Thiết Kế Giải Pháp
## Hệ Thống Quản Lý Nhân Sự Rikkei Education — Rikkei HR Simulator Pro

## 1. Sơ đồ kiến trúc & phân cấp kế thừa

```
                         ┌────────────────────────┐
                         │   BaseEmployee (ABC)    │
                         │  - company_name          │
                         │  - base_salary_rate      │
                         │  - __working_hours       │
                         │  + working_hours (property, read-only)│
                         │  + calculate_salary() (abstract)│
                         │  + update_kpi()       (abstract)│
                         │  + __add__ / __lt__      │
                         │  + validate_employee_code() (static) │
                         │  + update_base_salary_rate() (classmethod)│
                         └────────────┬─────────────┘
                    ┌─────────────────┴───────────────────┐
                    │                                      │
          ┌─────────▼──────────┐                 ┌─────────▼──────────┐
          │      Lecturer       │                 │   AdmissionStaff   │
          │  - teaching_slots   │                 │  - revenue_generated│
          │  + calculate_salary()│                 │  - kpi_target       │
          │    (giờ + ca dạy)   │                 │  + calculate_salary()│
          │  + update_kpi()     │                 │    (giờ + hoa hồng) │
          │    (lưu % KPI)      │                 │  + update_kpi()     │
          │  + conduct_class()  │                 │    (cộng dồn doanh số)│
          └─────────┬───────────┘                 └─────────┬──────────┘
                    │       (đa kế thừa kiểu "diamond")      │
                    └──────────────────┬─────────────────────┘
                              ┌─────────▼──────────┐
                              │    HybridManager    │
                              │  (kế thừa CẢ 2 nhánh)│
                              │  override calculate/ │
                              │  update_kpi để kết  │
                              │  hợp đúng nghiệp vụ │
                              └─────────────────────┘
```

`BaseEmployee` là bộ khung chuẩn, quy định mọi nhân sự bắt buộc phải đóng gói số giờ công (`__working_hours` private, chỉ đọc qua `property working_hours`), bắt buộc tự định nghĩa `calculate_salary()` và `update_kpi()` (abstract methods), được trang bị sẵn toán tử nạp chồng `__add__`/`__lt__`, 1 static method và 1 class method dùng chung.

`Lecturer` và `AdmissionStaff` là hai nhánh kế thừa đơn trực tiếp từ `BaseEmployee`, mỗi lớp override các phương thức theo nghiệp vụ riêng.

`HybridManager` kế thừa kiểu "hình thoi" (diamond) từ CẢ HAI lớp cha -- cả hai lớp cha đều có tổ tiên chung `BaseEmployee`, tạo ra bài toán xung đột phương thức và khởi tạo phức tạp nhất trong toàn hệ thống.

## 2. Báo cáo kỹ thuật

### 2.1. MRO của HybridManager & cách giải quyết xung đột phương thức trùng tên

Khai báo `class HybridManager(Lecturer, AdmissionStaff)` khiến Python dựng MRO theo giải thuật C3-linearization:

```
HybridManager -> Lecturer -> AdmissionStaff -> BaseEmployee -> ABC -> object
```

**Xung đột calculate_salary():** nếu `HybridManager` không tự override, Python luôn chọn `Lecturer.calculate_salary()` (đứng trước trong MRO) -- tức là chỉ tính lương theo ca dạy, bỏ sót hoàn toàn phần hoa hồng doanh số từ `AdmissionStaff`. Đây là lỗi nghiệp vụ nghiêm trọng. Vì vậy `HybridManager` override rõ ràng với công thức tổng hợp:

```python
def calculate_salary(self):
    base_pay   = self.working_hours * self.base_salary_rate    # lương cứng theo giờ
    slot_pay   = self.teaching_slots * self.SLOT_BONUS         # phụ cấp ca dạy (Lecturer)
    commission = self.revenue_generated * self.COMMISSION_RATE # hoa hồng doanh số (AdmissionStaff)
    return base_pay + slot_pay + commission
```

**Xung đột update_kpi():** `Lecturer.update_kpi()` lưu % hoàn thành chương trình, trong khi `AdmissionStaff.update_kpi()` cộng dồn doanh số. Đối với `HybridManager`, nghiệp vụ mong đợi là cộng dồn doanh số (vì đây là chỉ tiêu đo lường chính của vai trò quản lý tuyển sinh). `HybridManager` vì vậy gọi đích danh `AdmissionStaff.update_kpi(self, progress)` thay vì để MRO tự chọn `Lecturer.update_kpi()`.

**Khởi tạo (cooperative multiple inheritance):** `HybridManager` cần cả `teaching_slots` (từ `Lecturer`) và `revenue_generated`, `kpi_target` (từ `AdmissionStaff`). Dự án áp dụng kỹ thuật "cooperative `super()` với `**kwargs`": mỗi lớp `__init__` chỉ xử lý tham số của riêng mình rồi chuyển tiếp phần còn lại qua `super().__init__(**kwargs)`. Chuỗi khởi tạo đi theo đúng MRO:

```
HybridManager.__init__
  → Lecturer.__init__ (gán teaching_slots, chuyển tiếp **kwargs)
    → AdmissionStaff.__init__ (gán revenue_generated, kpi_target, chuyển tiếp **kwargs)
      → BaseEmployee.__init__ (gán emp_code, full_name, working_hours)
```

Toàn bộ chuỗi này hoàn thành chỉ với một lệnh `super().__init__()` duy nhất ở `HybridManager`.

### 2.2. Vì sao Duck Typing giúp tích hợp cổng thanh toán mới mà không cần sửa code gốc

Hàm `execute_payroll(payment_service, employee, amount)` không kiểm tra `isinstance(payment_service, SomeBaseServiceClass)` và không yêu cầu các cổng ngân hàng kế thừa từ một interface chung. Điều duy nhất hàm này quan tâm là đối tượng truyền vào có sẵn phương thức `transfer_salary(employee, amount)` hay không -- triết lý Duck Typing.

Nhờ vậy, khi Rikkei Education muốn tích hợp thêm cổng mới (ví điện tử MoMo, Cake by VPBank, ngân hàng số Timo...), kỹ sư chỉ cần viết một lớp mới có `transfer_salary()` đúng chữ ký -- không đụng đến `BaseEmployee`, không đụng đến `execute_payroll()`, không đụng đến bất kỳ lớp nhân sự nào đã tồn tại. Đây là nguyên lý Open/Closed thực hiện qua Duck Typing: hệ thống mở rộng được vô hạn số lượng cổng thanh toán mới mà rủi ro phá vỡ (regression) code cũ gần như bằng không.

## 3. Xử lý các bẫy dữ liệu (Edge Cases)

| Bẫy | Vị trí xử lý | Cơ chế |
|---|---|---|
| 1. Khởi tạo trực tiếp `BaseEmployee` | `employee_models.py` | Tự động: `ABCMeta` ném `TypeError` vì `calculate_salary` và `update_kpi` là `@abstractmethod` chưa triển khai |
| 2. Giá trị công nhật / doanh số <= 0 | `Lecturer.update_kpi()`, `AdmissionStaff.update_kpi()` (và `HybridManager` gọi lại bản Admission) | Kiểm tra `if progress <= 0: raise ValueError(...)` trước khi cập nhật |
| 3. Cộng/so sánh với kiểu dữ liệu sai | `BaseEmployee.__add__` / `__lt__` | `isinstance(other, BaseEmployee)`, nếu sai kiểu `return NotImplemented` → Python tự ném `TypeError` chuẩn |
| 4. Cổng thanh toán thiếu `transfer_salary` | `payroll_service.execute_payroll()` | `try...except AttributeError`, in thông báo "Cổng dịch vụ ngân hàng doanh nghiệp không hợp lệ hoặc chưa được liên kết liên thông kỹ thuật" |

## 4. Cấu trúc module của dự án

- `employee_models.py` — toàn bộ các lớp nhân sự (BaseEmployee, Lecturer, AdmissionStaff, HybridManager).
- `payroll_service.py` — các lớp cổng thanh toán (VietcombankCorporateService, TechcombankCorporateService) và hàm `execute_payroll()`.
- `utils.py` — hàm tiện ích dùng chung (parse số từ input).
- `feature_hire_employee.py` — Chức năng 1.
- `feature_view_info.py` — Chức năng 2.
- `feature_work_kpi.py` — Chức năng 3.
- `feature_payroll_summary.py` — Chức năng 4.
- `feature_compare_hours.py` — Chức năng 5.
- `feature_disburse_salary.py` — Chức năng 6.
- `main.py` — chương trình chính, quản lý state `employees` (list) và `current_employee`.
