"""FI giả: sổ nhật ký trong bộ nhớ. Phải hành xử giống FI thật (xem contract_tests/fi.py)."""
from datetime import datetime


class FakeFI:
    IS_FAKE = True
    ACC_RECEIVABLE = "131"
    ACC_REVENUE = "511"

    def __init__(self):
        self._entries: list[dict] = []

    def post_entry(self, ref, debit_account, credit_account, amount, note="") -> int:
        if amount <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")
        entry_id = len(self._entries) + 1
        self._entries.append({
            "id": entry_id, "posted_at": datetime.now().strftime("%Y-%m-%d %H:%M"), "ref": ref,
            "debit_account": debit_account, "credit_account": credit_account, "amount": amount, "note": note,
        })
        return entry_id

    def post_revenue(self, ref, amount, note="") -> int:
        return self.post_entry(ref, self.ACC_RECEIVABLE, self.ACC_REVENUE, amount, note)

    def list_entries(self) -> list[dict]:
        return [dict(e) for e in reversed(self._entries)]

    def total_revenue(self) -> int:
        return sum(e["amount"] for e in self._entries if e["credit_account"] == self.ACC_REVENUE)


def create() -> FakeFI:
    return FakeFI()
