import tkinter as tk

from gui.main_window import OptionPricerApp


if __name__ == "__main__":
    root = tk.Tk()
    app = OptionPricerApp(root)
    root.mainloop()
