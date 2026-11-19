"""Cửa sổ chính của Mini ERP.

Leader quản lý file này. Mỗi module là một submodule trong modules/<mã>.
Máy nào không có code của module nào (submodule chưa tải / không có quyền) thì
module đó được thay bằng BẢN GIẢ trong core/fakes, để các module khác vẫn chạy được.
"""
import importlib
from pathlib import Path

from core import db, services

APP_TITLE = "ERP"

# Thứ tự ở đây = thứ tự tab trên giao diện.
INSTALLED_MODULES = ["sd", "mm"]
MODULE_NAMES = {"sd": "Bán hàng", "mm": "Vật tư & Kho"}

# Module nào có bản giả (module được module khác gọi tới).
FAKES = {"mm": "core.fakes.mm"}

MODULES_DIR = Path(__file__).resolve().parent.parent / "modules"


def is_available(code: str) -> bool:
    """Máy này có code thật của module không (submodule đã được tải về)."""
    return (MODULES_DIR / code / "__init__.py").exists()


def load_modules():
    """Các module có code thật trên máy này."""
    return [importlib.import_module(f"modules.{c}") for c in INSTALLED_MODULES if is_available(c)]


def register_services() -> None:
    """Đăng ký dịch vụ: có code thật thì dùng thật, không có thì dùng bản giả."""
    for code in INSTALLED_MODULES:
        if is_available(code):
            services.register(code, importlib.import_module(f"modules.{code}.public"))
    # Module không bật (hoặc không có code) mà module khác cần gọi → dùng bản giả.
    for code, fake in FAKES.items():
        if code not in INSTALLED_MODULES or not is_available(code):
            services.register(code, importlib.import_module(fake).create())


def init_database(modules) -> None:
    """Cho từng module tạo bảng của riêng nó."""
    with db.connect() as conn:
        for module in modules:
            module.setup_db(conn)


def run() -> None:
    import tkinter as tk
    from tkinter import ttk

    register_services()
    modules = {m.CODE.lower(): m for m in load_modules()}
    init_database(modules.values())

    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry("900x560")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=8, pady=8)

    for code in INSTALLED_MODULES:
        if code not in modules:
            continue  # máy này không có code module này → không hiện tab
        tab = modules[code].build_tab(notebook)
        notebook.add(tab, text=f"  {code.upper()} – {MODULE_NAMES[code]}  ")

    def on_tab_changed(_event):
        tab = root.nametowidget(notebook.select())
        if hasattr(tab, "refresh"):
            tab.refresh()

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)
    root.mainloop()
