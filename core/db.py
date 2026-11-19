"""Kết nối database dùng chung cho mọi module (SQLite, file erp.db).

Leader quản lý file này. Dev các module KHÔNG sửa nếu chưa báo leader.
"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

_db_path = Path(__file__).resolve().parent.parent / "erp.db"


def use_database(path) -> None:
    """Đổi sang file database khác (dùng trong test)."""
    global _db_path
    _db_path = Path(path)


@contextmanager
def connect():
    """Mở kết nối: xong thì tự commit, lỗi thì tự rollback, cuối cùng tự đóng."""
    conn = sqlite3.connect(_db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
