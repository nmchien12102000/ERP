"""Hợp đồng của MM: những gì module khác (SD...) được phép dựa vào."""
from core.errors import NotEnoughStock


class MMContractTests:
    """Lớp test dùng chung. Lớp con phải định nghĩa make_mm()."""

    def make_mm(self):
        raise NotImplementedError

    def test_hd_list_materials_co_du_truong(self):
        materials = self.make_mm().list_materials()
        self.assertTrue(materials)
        self.assertLessEqual({"code", "name", "price", "stock"}, set(materials[0]))

    def test_hd_get_material_khong_ton_tai_tra_ve_None(self):
        self.assertIsNone(self.make_mm().get_material("KHONG-CO"))

    def test_hd_xuat_kho_thi_ton_giam_dung(self):
        mm = self.make_mm()
        before = mm.get_material("VT001")["stock"]
        mm.issue_stock("VT001", 10)
        self.assertEqual(mm.get_material("VT001")["stock"], before - 10)

    def test_hd_xuat_qua_ton_bao_NotEnoughStock_va_khong_tru(self):
        mm = self.make_mm()
        before = mm.get_material("VT001")["stock"]
        with self.assertRaises(NotEnoughStock):
            mm.issue_stock("VT001", before + 1)
        self.assertEqual(mm.get_material("VT001")["stock"], before)

    def test_hd_so_luong_khong_hop_le_bao_ValueError(self):
        with self.assertRaises(ValueError):
            self.make_mm().issue_stock("VT001", 0)
