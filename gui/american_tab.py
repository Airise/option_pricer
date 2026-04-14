import tkinter as tk
from tkinter import ttk

from core.market_data import MarketData
from core.option import AmericanOption
from engines.binomial_tree import BinomialTreeEngine
from ._helpers import labeled_entry, parse_float, parse_int, require_non_negative, require_positive, require_unit_interval, wrap_action


def create_tab(notebook: ttk.Notebook, result_writer):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="American")
    frame.columnconfigure(1, weight=1)

    s0_e = labeled_entry(frame, 0, "S0", "100")
    sigma_e = labeled_entry(frame, 1, "sigma", "0.2")
    r_e = labeled_entry(frame, 2, "r", "0.05")
    t_e = labeled_entry(frame, 3, "T", "1.0")
    k_e = labeled_entry(frame, 4, "K", "100")
    n_e = labeled_entry(frame, 5, "steps", "200")

    ttk.Label(frame, text="Option Type").grid(row=6, column=0, sticky="w", padx=(32, 16), pady=10)
    opt_type = tk.StringVar(value="put")
    ttk.Combobox(frame, textvariable=opt_type, values=["call", "put"], state="readonly").grid(row=6, column=1, sticky="ew", padx=(0, 32), pady=10)

    def on_calc():
        s0 = require_positive(parse_float(s0_e, "S0"), "S0")
        sigma = require_positive(parse_float(sigma_e, "sigma"), "sigma")
        r = parse_float(r_e, "r")
        t = require_positive(parse_float(t_e, "T"), "T")
        k = require_positive(parse_float(k_e, "K"), "K")
        steps = parse_int(n_e, "steps")
        if steps <= 0:
            raise ValueError("steps must be greater than 0")

        md = MarketData(s0=s0, sigma=sigma, r=r, q=0.0, t=t, k=k)
        opt = AmericanOption(option_type=opt_type.get(), market_data=md)
        price = BinomialTreeEngine.american(opt, steps)
        result_writer(f"[American {opt_type.get()}] Price = {price:.6f}")

    ttk.Button(frame, text="Calculate Price", command=wrap_action(on_calc, result_writer)).grid(row=7, column=0, columnspan=2, pady=(24, 32))

    return frame
