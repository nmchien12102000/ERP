"""Bộ đăng ký dịch vụ: module gọi nhau qua đây, KHÔNG import code của nhau.

    mm = services.get("mm")      # máy có code MM -> MM thật; không có -> MM giả
    mm.issue_stock("VT001", 10)
"""
_services: dict[str, object] = {}


def register(name: str, impl: object) -> None:
    _services[name] = impl


def get(name: str):
    try:
        return _services[name]
    except KeyError:
        raise LookupError(f"Chưa có dịch vụ '{name}'") from None


def is_fake(name: str) -> bool:
    return getattr(get(name), "IS_FAKE", False)
