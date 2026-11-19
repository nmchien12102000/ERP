"""Module nào có trên máy cũng phải đủ các thành phần bắt buộc."""
import unittest

from core.app import load_modules


class TestModuleStructure(unittest.TestCase):
    def test_moi_module_co_du_thanh_phan(self):
        for module in load_modules():
            for attr in ("CODE", "NAME", "setup_db", "build_tab"):
                self.assertTrue(hasattr(module, attr), f"{module.__name__} thiếu {attr}")
