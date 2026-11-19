"""Test tích hợp: ghép các module THẬT. Chỉ chạy được trên máy có đủ submodule (Leader, CI).

Hiện các module mới chỉ hiển thị giao diện, chưa có logic nghiệp vụ,
nên ở đây chỉ kiểm tra: mọi module thật nạp được cùng nhau và tạo bảng không lỗi.
Khi thêm logic (vd SD tạo đơn → MM trừ kho) thì viết thêm test ghép nghiệp vụ vào đây.
"""
import unittest

from core import services
from core.app import INSTALLED_MODULES, is_available, load_modules
from tests.helpers import ErpTestCase

ALL_MODULES = all(is_available(c) for c in INSTALLED_MODULES)


@unittest.skipUnless(ALL_MODULES, "Thiếu submodule, bỏ qua test tích hợp (chỉ Leader/CI chạy)")
class TestIntegration(ErpTestCase):
    def test_nap_du_cac_module_that(self):
        codes = sorted(m.CODE.lower() for m in load_modules())
        self.assertEqual(codes, sorted(INSTALLED_MODULES))
        for code in INSTALLED_MODULES:
            self.assertFalse(services.is_fake(code), f"{code} đang dùng bản giả")
