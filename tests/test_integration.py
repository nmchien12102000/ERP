"""Test tích hợp: ghép các module THẬT (SD + MM). Chỉ chạy được trên máy có đủ submodule (Leader, CI)."""
import unittest

from core import services
from core.app import INSTALLED_MODULES, is_available
from tests.helpers import ErpTestCase

ALL_MODULES = all(is_available(c) for c in INSTALLED_MODULES)


@unittest.skipUnless(ALL_MODULES, "Thiếu submodule, bỏ qua test tích hợp (chỉ Leader/CI chạy)")
class TestIntegration(ErpTestCase):
    def test_ban_hang_tru_kho(self):
        mm, sd = services.get("mm"), services.get("sd")
        self.assertFalse(services.is_fake("mm"))

        order_id = sd.create_order("Công ty ABC", "VT001", 10)

        self.assertEqual(mm.get_material("VT001")["stock"], 190)
        self.assertEqual(sd.list_orders()[0]["id"], order_id)
        self.assertEqual(sd.list_orders()[0]["amount"], 950_000)
