"""Lỗi nghiệp vụ dùng chung. Module thật và bản giả đều dùng đúng các lớp lỗi này."""


class NotEnoughStock(Exception):
    """Tồn kho không đủ để xuất."""
