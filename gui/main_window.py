import tkinter as tk
from tkinter import ttk

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
        self.root.title("Mini Option Pricer")
        self.root.geometry("980x760")

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.result_panel = ResultPanel(root)

        writer = self.result_panel.write
        create_european_tab(notebook, writer)
        create_american_tab(notebook, writer)
        create_geometric_asian_tab(notebook, writer)
        create_arithmetic_asian_tab(notebook, writer)
        create_geometric_basket_tab(notebook, writer)
        create_arithmetic_basket_tab(notebook, writer)
        create_kiko_tab(notebook, writer)
        create_iv_tab(notebook, writer)
