"""MM giả: dữ liệu mẫu trong bộ nhớ. Phải hành xử giống MM thật (xem contract_tests/mm.py)."""
from core.errors import NotEnoughStock

SAMPLE = [
    ("VT001", "Xi măng PCB40 (bao)", 95_000, 200),
    ("VT002", "Thép D10 (cây)", 120_000, 500),
    ("VT003", "Gạch đỏ (viên)", 1_500, 10_000),
]


class FakeMM:
    IS_FAKE = True
    NotEnoughStock = NotEnoughStock

    def __init__(self):
        self._data = {c: {"code": c, "name": n, "price": p, "stock": s} for c, n, p, s in SAMPLE}

    def list_materials(self) -> list[dict]:
        return [dict(self._data[c]) for c in sorted(self._data)]

    def get_material(self, code: str) -> dict | None:
        m = self._data.get(code)
        return dict(m) if m else None

    def receive_stock(self, code: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Số lượng nhập phải lớn hơn 0")
        if code not in self._data:
            raise ValueError(f"Không có vật tư {code}")
        self._data[code]["stock"] += qty

    def issue_stock(self, code: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Số lượng xuất phải lớn hơn 0")
        if code not in self._data:
            raise ValueError(f"Không có vật tư {code}")
        if self._data[code]["stock"] < qty:
            raise NotEnoughStock(f"{code} chỉ còn {self._data[code]['stock']}, không đủ xuất {qty}")
        self._data[code]["stock"] -= qty


def create() -> FakeMM:
    return FakeMM()
