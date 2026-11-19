"""Hỗ trợ viết test: mỗi test chạy trên database tạm + dịch vụ mới (bản giả được tạo lại)."""
import os
import tempfile
import unittest

from core import db
from core.app import init_database, load_modules, register_services


class ErpTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        db.use_database(os.path.join(self._tmp.name, "test.db"))
        register_services()
        init_database(load_modules())

    def tearDown(self):
        self._tmp.cleanup()
