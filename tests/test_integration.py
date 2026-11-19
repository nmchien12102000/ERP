"""Test tích hợp: ghép CẢ 3 module THẬT. Chỉ chạy được trên máy có đủ 3 submodule (Leader, CI)."""
import unittest

from core import services
from core.app import INSTALLED_MODULES, is_available
from tests.helpers import ErpTestCase

ALL_MODULES = all(is_available(c) for c in INSTALLED_MODULES)


@unittest.skipUnless(ALL_MODULES, "Thiếu submodule, bỏ qua test tích hợp (chỉ Leader/CI chạy)")
class TestIntegration(ErpTestCase):
    def test_ban_hang_tru_kho_va_ghi_doanh_thu(self):
        mm, fi, sd = services.get("mm"), services.get("fi"), services.get("sd")
        self.assertFalse(services.is_fake("mm") or services.is_fake("fi"))

        order_id = sd.create_order("Công ty ABC", "VT001", 10)

        self.assertEqual(mm.get_material("VT001")["stock"], 190)
        self.assertEqual(fi.total_revenue(), 950_000)
        self.assertEqual(fi.list_entries()[0]["ref"], f"SO{order_id:05d}")
