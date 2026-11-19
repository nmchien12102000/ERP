"""Ranh giới module: module KHÔNG được import code của module khác (kể cả public.py).
Muốn gọi module khác thì dùng core.services.get("<mã>").
"""
import ast
import unittest
from pathlib import Path

MODULES_DIR = Path(__file__).resolve().parent.parent / "modules"


class TestBoundaries(unittest.TestCase):
    def test_khong_import_module_khac(self):
        violations = []
        for py_file in MODULES_DIR.rglob("*.py"):
            parts = py_file.relative_to(MODULES_DIR).parts
            if len(parts) < 2:
                continue
            own = parts[0]
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    targets = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    targets = [f"{node.module}.{a.name}" for a in node.names]
                else:
                    continue
                for t in targets:
                    p = t.split(".")
                    if p[0] == "modules" and len(p) >= 2 and p[1] != own:
                        violations.append(f"{py_file.relative_to(MODULES_DIR)}:{node.lineno} import {t}")
        self.assertEqual(violations, [], "Hãy dùng core.services thay vì import module khác:\n" + "\n".join(violations))
