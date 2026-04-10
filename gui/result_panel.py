import tkinter as tk
from tkinter import ttk


class ResultPanel:
    def __init__(self, parent: tk.Widget):
        frame = ttk.Frame(parent, style="App.TFrame")
        frame.pack(fill="both", expand=False, pady=(24, 0))

        # 标题
        ttk.Label(frame, text="Terminal Output", style="ResultTitle.TLabel").pack(anchor="w", pady=(0, 12))

        # 文本框外层容器（用于实现细边框效果）
        text_container = tk.Frame(frame, bg="#e2e8f0", padx=1, pady=1)
        text_container.pack(fill="both", expand=True)

        # 极客/高级感的深色终端输出框
        self.text = tk.Text(text_container, height=10, width=100,
                            font=("Cascadia Code", 10),
                            bg="#0f172a",
                            fg="#f8fafc",
                            relief="flat",
                            highlightthickness=0,
                            padx=20, pady=20)
        self.text.pack(fill="both", expand=True)
        self.text.configure(state="disabled")

    def write(self, message: str) -> None:
        # 同时输出到 GUI 和终端，便于调试。
        print(message)
        self.text.configure(state="normal")
        self.text.insert("end", message + "\n")
        self.text.see("end")
        self.text.configure(state="disabled")

    def clear(self) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")
