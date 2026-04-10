import tkinter as tk
from tkinter import ttk

from .theme import apply_modern_theme
from .result_panel import ResultPanel
from .european_tab import create_tab as create_european_tab
from .american_tab import create_tab as create_american_tab
from .asian_tabs import create_geometric_asian_tab, create_arithmetic_asian_tab
from .basket_tabs import create_geometric_basket_tab, create_arithmetic_basket_tab
from .kiko_tab import create_tab as create_kiko_tab
from .implied_vol_tab import create_tab as create_iv_tab


class OptionPricerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Zoom Inspired Option Pricer")
        self.root.geometry("1024x850")
        self.root.configure(bg="#f8fafc")
        
        # 应用高级感主题
        apply_modern_theme(self.root)

        # 头部标题区域 (Header)
        header_frame = ttk.Frame(root, style="App.TFrame")
        header_frame.pack(fill="x", padx=40, pady=(40, 20))
        
        ttk.Label(header_frame, text="Option Pricer", style="Header.TLabel").pack(anchor="w")
        ttk.Label(header_frame, text="Advanced Valuation Models & Analytics", style="SubHeader.TLabel").pack(anchor="w", pady=(4, 0))

        # 主内容区域 (Main Content) 增加滚动条支持
        main_container = tk.Frame(root, bg="#f8fafc")
        main_container.pack(fill="both", expand=True, padx=40, pady=(0, 40))

        canvas = tk.Canvas(main_container, bg="#f8fafc", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        content_frame = ttk.Frame(canvas, style="App.TFrame")
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=content_frame, anchor="nw", tags="frame")
        
        def on_canvas_configure(event):
            canvas.itemconfig("frame", width=event.width)
            
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # 绑定鼠标滚轮事件
        def _on_mousewheel(event):
            # 仅当内容超出可视区域时才允许滚动
            if content_frame.winfo_height() > canvas.winfo_height():
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # 绑定全局鼠标滚轮
        root.bind_all("<MouseWheel>", _on_mousewheel)

        # 选项卡
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill="both", expand=True)

        # 结果面板
        self.result_panel = ResultPanel(content_frame)

        writer = self.result_panel.write
        create_european_tab(notebook, writer)
        create_american_tab(notebook, writer)
        create_geometric_asian_tab(notebook, writer)
        create_arithmetic_asian_tab(notebook, writer)
        create_geometric_basket_tab(notebook, writer)
        create_arithmetic_basket_tab(notebook, writer)
        create_kiko_tab(notebook, writer)
        create_iv_tab(notebook, writer)
