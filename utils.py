# -*- coding: utf-8 -*-
"""
utils.py
---------
Các hàm tiện ích dùng chung cho toàn hệ thống.
"""


def parse_number(text):
    """
    Chuyển chuỗi người dùng nhập (có thể có dấu phẩy phân cách) thành số
    thực (float). Ném ValueError nếu chuỗi không hợp lệ.
    """
    cleaned = text.replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        raise ValueError("Giá trị nhập không hợp lệ, vui lòng chỉ nhập số.")
