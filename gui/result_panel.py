import tkinter as tk
from tkinter import ttk


class ResultPanel:
    def __init__(self, parent: tk.Widget):
        frame = ttk.LabelFrame(parent, text="结果")
        frame.pack(fill="both", expand=False, padx=8, pady=8)

        self.text = tk.Text(frame, height=10, width=100)
        self.text.pack(fill="both", expand=True, padx=6, pady=6)
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
