import tkinter as tk
from tkinter import ttk

def apply_modern_theme(root: tk.Tk):
    style = ttk.Style(root)
    # Use clam theme as base
    style.theme_use('clam')
    
    # Modern color palette inspired by shadcn/ui and Zoom
    bg_color = "#f8fafc"        # App overall background (slate-50)
    card_bg = "#ffffff"         # Card/Tab background (pure white)
    fg_color = "#0f172a"        # Primary text color (slate-900)
    muted_fg = "#64748b"        # Secondary text color (slate-500)
    primary = "#0f172a"         # Primary button color (deep black/slate-900)
    primary_hover = "#334155"   # Primary button hover (slate-700)
    border_color = "#e2e8f0"    # Border color (slate-200)
    input_bg = "#ffffff"        # Input background
    
    default_font = ("Segoe UI", 10)
    btn_font = ("Segoe UI", 10, "bold")
    
    # Global default config (assuming most content inside pure white cards)
    style.configure(".", background=card_bg, foreground=fg_color, font=default_font)
    
    # Frame styles
    style.configure("TFrame", background=card_bg)
    style.configure("App.TFrame", background=bg_color)
    
    # Label styles
    style.configure("TLabel", background=card_bg, foreground=fg_color, font=default_font)
    style.configure("App.TLabel", background=bg_color, foreground=fg_color, font=default_font)
    style.configure("Header.TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 24, "bold"))
    style.configure("SubHeader.TLabel", background=bg_color, foreground=muted_fg, font=("Segoe UI", 11))
    style.configure("ResultTitle.TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 12, "bold"))
    
    # Button styles (minimalist modern)
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
    
    # Checkbutton styles
    style.configure("TCheckbutton", background=card_bg, foreground=fg_color, font=default_font)
    style.map("TCheckbutton", background=[('active', card_bg)])
    
    # Entry styles
    style.configure("TEntry", 
                    fieldbackground=input_bg, 
                    foreground=fg_color, 
                    bordercolor=border_color,
                    lightcolor=input_bg,
                    darkcolor=input_bg,
                    padding=10)
    
    # Combobox styles
    style.configure("TCombobox", 
                    fieldbackground=input_bg, 
                    background=input_bg, 
                    foreground=fg_color,
                    bordercolor=border_color,
                    arrowcolor=fg_color,
                    padding=10)
    
    # Notebook (Tab container) styles
    style.configure("TNotebook", background=bg_color, borderwidth=0, padding=0)
    
    # Notebook.Tab styles - modern web-like pill/tab design
    style.configure("TNotebook.Tab", 
                    background="#f1f5f9", 
                    foreground=muted_fg, 
                    padding=(24, 12), 
                    font=default_font,
                    borderwidth=0)
    style.map("TNotebook.Tab", 
              background=[("selected", card_bg), ("active", "#e2e8f0")],
              foreground=[("selected", primary), ("active", fg_color)],
              font=[("selected", default_font)])
