"""Cửa sổ chính của Mini ERP.

Leader quản lý file này. Mỗi module là một submodule trong modules/<mã>.
Máy nào không có code của module nào (submodule chưa tải / không có quyền) thì
module đó được thay bằng BẢN GIẢ trong core/fakes, để các module khác vẫn chạy được.
"""
import importlib
from pathlib import Path

from core import db, services

APP_TITLE = "Mini ERP"

# Thứ tự ở đây = thứ tự tab trên giao diện.
INSTALLED_MODULES = ["fi", "sd", "mm"]
MODULE_NAMES = {"fi": "Kế toán", "sd": "Bán hàng", "mm": "Vật tư & Kho"}

# Module nào có bản giả (module được module khác gọi tới).
FAKES = {"fi": "core.fakes.fi", "mm": "core.fakes.mm"}

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
        elif code in FAKES:
            services.register(code, importlib.import_module(FAKES[code]).create())


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
        if code in modules:
            tab = modules[code].build_tab(notebook)
            notebook.add(tab, text=f"  {code.upper()} – {MODULE_NAMES[code]}  ")
        else:
            tab = ttk.Frame(notebook, padding=40)
            note = "Các module khác đang dùng BẢN GIẢ (dữ liệu mẫu trong bộ nhớ)." if code in FAKES else ""
            ttk.Label(tab, justify="center", text=(
                f"Máy này không có code module {code.upper()}\n"
                f"(submodule modules/{code} chưa tải về hoặc bạn không có quyền).\n\n{note}"
            )).pack()
            notebook.add(tab, text=f"  {code.upper()} – (không có)  ")

    def on_tab_changed(_event):
        tab = root.nametowidget(notebook.select())
        if hasattr(tab, "refresh"):
            tab.refresh()

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)
    root.mainloop()
