from typing import Callable
import tkinter as tk
from tkinter import ttk


def labeled_entry(parent: tk.Widget, row: int, label: str, default: str) -> tk.Entry:
    ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=4, pady=3)
    e = ttk.Entry(parent)
    e.insert(0, default)
    e.grid(row=row, column=1, sticky="ew", padx=4, pady=3)
    return e


def parse_float(entry: tk.Entry, name: str) -> float:
    try:
        return float(entry.get())
    except ValueError as exc:
        raise ValueError(f"{name} 必须是数字") from exc


def parse_int(entry: tk.Entry, name: str) -> int:
    try:
        return int(entry.get())
    except ValueError as exc:
        raise ValueError(f"{name} 必须是整数") from exc


def require_positive(value: float, name: str) -> float:
    if value <= 0:
        raise ValueError(f"{name} 必须大于 0")
    return value


def require_non_negative(value: float, name: str) -> float:
    if value < 0:
        raise ValueError(f"{name} 不能为负数")
    return value


def require_unit_interval(value: float, name: str) -> float:
    if value < -1.0 or value > 1.0:
        raise ValueError(f"{name} 必须在 [-1, 1] 区间")
    return value


def wrap_action(callback: Callable[[], None], on_error: Callable[[str], None]) -> Callable[[], None]:
    def _inner() -> None:
        try:
            callback()
        except Exception as exc:
            on_error(f"错误: {exc}")

    return _inner
