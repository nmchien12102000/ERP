"""Bản giả phải qua đúng bộ test hợp đồng mà bản thật phải qua."""
import unittest

from core.contract_tests.fi import FIContractTests
from core.contract_tests.mm import MMContractTests
from core.fakes import fi as fake_fi
from core.fakes import mm as fake_mm


class TestFakeMM(MMContractTests, unittest.TestCase):
    def make_mm(self):
        return fake_mm.create()


class TestFakeFI(FIContractTests, unittest.TestCase):
    def make_fi(self):
        return fake_fi.create()
