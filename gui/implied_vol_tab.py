import tkinter as tk
from tkinter import ttk

from engines.implied_volatility import implied_volatility
from ._helpers import labeled_entry, parse_float, parse_int, require_non_negative, require_positive, require_unit_interval, wrap_action


def create_tab(notebook: ttk.Notebook, result_writer):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Implied Volatility")
    frame.columnconfigure(1, weight=1)

    s0_e = labeled_entry(frame, 0, "S0", "100")
    r_e = labeled_entry(frame, 1, "r", "0.05")
    q_e = labeled_entry(frame, 2, "q", "0.0")
    t_e = labeled_entry(frame, 3, "T", "1.0")
    k_e = labeled_entry(frame, 4, "K", "100")
    p_e = labeled_entry(frame, 5, "Market Price", "10")

    ttk.Label(frame, text="Option Type").grid(row=6, column=0, sticky="w", padx=(32, 16), pady=10)
    opt_type = tk.StringVar(value="call")
    ttk.Combobox(frame, textvariable=opt_type, values=["call", "put"], state="readonly").grid(row=6, column=1, sticky="ew", padx=(0, 32), pady=10)

    def on_calc():
        market_price = parse_float(p_e, "Market Price")
        if market_price <= 0:
            raise ValueError("Market Price must be greater than 0")

        s0 = require_positive(parse_float(s0_e, "S0"), "S0")
        k = require_positive(parse_float(k_e, "K"), "K")
        t = require_positive(parse_float(t_e, "T"), "T")
        r = parse_float(r_e, "r")
        q = parse_float(q_e, "q")

        iv = implied_volatility(
            market_price=market_price,
            s0=s0,
            k=k,
            t=t,
            r=r,
            q=q,
            option_type=opt_type.get(),
        )
        result_writer(f"[Implied Volatility {opt_type.get()}] sigma = {iv:.6f}")

    ttk.Button(frame, text="Calculate Implied Volatility", command=wrap_action(on_calc, result_writer)).grid(row=7, column=0, columnspan=2, pady=(24, 32))

    return frame
