import tkinter as tk
from tkinter import ttk

def apply_modern_theme(root: tk.Tk):
    style = ttk.Style(root)
    # 使用 clam 主题作为基础
    style.theme_use('clam')
    
    # 灵感来自 shadcn/ui 和 Zoom 的高级感配色
    bg_color = "#f8fafc"        # App 整体背景 (slate-50)
    card_bg = "#ffffff"         # 卡片/选项卡背景 (纯白)
    fg_color = "#0f172a"        # 主要文字颜色 (slate-900)
    muted_fg = "#64748b"        # 次要文字颜色 (slate-500)
    primary = "#0f172a"         # 主按钮颜色 (深邃黑/slate-900)
    primary_hover = "#334155"   # 主按钮悬停 (slate-700)
    border_color = "#e2e8f0"    # 边框颜色 (slate-200)
    input_bg = "#ffffff"        # 输入框背景
    
    default_font = ("Segoe UI", 10)
    btn_font = ("Segoe UI", 10, "bold")
    
    # 全局默认配置 (假设大部分内容在纯白卡片内)
    style.configure(".", background=card_bg, foreground=fg_color, font=default_font)
    
    # Frame 样式
    style.configure("TFrame", background=card_bg)
    style.configure("App.TFrame", background=bg_color)
    
    # Label 样式
    style.configure("TLabel", background=card_bg, foreground=fg_color, font=default_font)
    style.configure("App.TLabel", background=bg_color, foreground=fg_color, font=default_font)
    style.configure("Header.TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 24, "bold"))
    style.configure("SubHeader.TLabel", background=bg_color, foreground=muted_fg, font=("Segoe UI", 11))
    style.configure("ResultTitle.TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 12, "bold"))
    
    # Button 样式 (黑白极简高级感)
    style.configure("TButton", 
                    background=primary, 
                    foreground="white", 
                    font=btn_font,
                    borderwidth=0,
                    focusthickness=0,
                    padding=(20, 10))
    style.map("TButton", 
              background=[('active', primary_hover), ('disabled', '#cbd5e1')],
              foreground=[('disabled', '#f8fafc')])
    
    # Checkbutton 样式
    style.configure("TCheckbutton", background=card_bg, foreground=fg_color, font=default_font)
    style.map("TCheckbutton", background=[('active', card_bg)])
    
    # Entry 样式
    style.configure("TEntry", 
                    fieldbackground=input_bg, 
                    foreground=fg_color, 
                    bordercolor=border_color,
                    lightcolor=input_bg,
                    darkcolor=input_bg,
                    padding=10)
    
    # Combobox 样式
    style.configure("TCombobox", 
                    fieldbackground=input_bg, 
                    background=input_bg, 
                    foreground=fg_color,
                    bordercolor=border_color,
                    arrowcolor=fg_color,
                    padding=10)
    
    # Notebook (选项卡容器) 样式
    style.configure("TNotebook", background=bg_color, borderwidth=0, padding=0)
    
    # Notebook.Tab (选项卡) 样式 - 类似现代 Web 的胶囊/标签设计
    style.configure("TNotebook.Tab", 
                    background="#e2e8f0", 
                    foreground=muted_fg, 
                    padding=(24, 12), 
                    font=default_font,
                    borderwidth=0)
    style.map("TNotebook.Tab", 
              background=[("selected", card_bg), ("active", "#cbd5e1")],
              foreground=[("selected", fg_color), ("active", fg_color)],
              font=[("selected", ("Segoe UI", 10, "bold"))])
