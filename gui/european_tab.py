import tkinter as tk
from tkinter import ttk

from core.market_data import MarketData
from core.option import EuropeanOption
from engines.closed_form import ClosedFormEngine
from ._helpers import labeled_entry, parse_float, parse_int, require_non_negative, require_positive, require_unit_interval, wrap_action


def create_tab(notebook: ttk.Notebook, result_writer):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="欧式期权")
    frame.columnconfigure(1, weight=1)

    s0_e = labeled_entry(frame, 0, "S0", "100")
    sigma_e = labeled_entry(frame, 1, "sigma", "0.2")
    r_e = labeled_entry(frame, 2, "r", "0.05")
    q_e = labeled_entry(frame, 3, "q", "0.0")
    t_e = labeled_entry(frame, 4, "T", "1.0")
    k_e = labeled_entry(frame, 5, "K", "100")

    ttk.Label(frame, text="option_type").grid(row=6, column=0, sticky="w", padx=(32, 16), pady=10)
    opt_type = tk.StringVar(value="call")
    ttk.Combobox(frame, textvariable=opt_type, values=["call", "put"], state="readonly").grid(row=6, column=1, sticky="ew", padx=(0, 32), pady=10)

    def on_calc():
        s0 = require_positive(parse_float(s0_e, "S0"), "S0")
        sigma = require_non_negative(parse_float(sigma_e, "sigma"), "sigma")
        r = parse_float(r_e, "r")
        q = parse_float(q_e, "q")
        t = require_positive(parse_float(t_e, "T"), "T")
        k = require_positive(parse_float(k_e, "K"), "K")

        md = MarketData(
            s0=s0,
            sigma=sigma,
            r=r,
            q=q,
            t=t,
            k=k,
        )
        opt = EuropeanOption(option_type=opt_type.get(), market_data=md)
        price = ClosedFormEngine.european(opt)
        result_writer(f"[欧式 {opt_type.get()}] 价格 = {price:.6f}")

    ttk.Button(frame, text="计算价格", command=wrap_action(on_calc, result_writer)).grid(row=7, column=0, columnspan=2, pady=(24, 32))

    return frame
