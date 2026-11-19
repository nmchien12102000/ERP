"""Hợp đồng của FI: những gì module khác (SD...) được phép dựa vào."""


class FIContractTests:
    """Lớp test dùng chung. Lớp con phải định nghĩa make_fi()."""

    def make_fi(self):
        raise NotImplementedError

    def test_hd_ghi_doanh_thu_thi_tong_doanh_thu_tang(self):
        fi = self.make_fi()
        before = fi.total_revenue()
        fi.post_revenue("SO99999", 500_000, "test")
        self.assertEqual(fi.total_revenue(), before + 500_000)

    def test_hd_but_toan_moi_nhat_o_dau_no_131_co_511(self):
        fi = self.make_fi()
        fi.post_revenue("SO99998", 100_000)
        entry = fi.list_entries()[0]
        self.assertEqual((entry["ref"], entry["debit_account"], entry["credit_account"]), ("SO99998", "131", "511"))

    def test_hd_so_tien_khong_hop_le_bao_ValueError(self):
        with self.assertRaises(ValueError):
            self.make_fi().post_revenue("SO99997", 0)
