import tkinter as tk
from tkinter import ttk

from core.market_data import MarketData
from core.option import ArithmeticAsianOption, GeometricAsianOption
from engines.closed_form import ClosedFormEngine
from engines.monte_carlo import MonteCarloEngine
from ._helpers import labeled_entry, parse_float, parse_int, require_non_negative, require_positive, require_unit_interval, wrap_action


def create_geometric_asian_tab(notebook: ttk.Notebook, result_writer):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="几何亚式")
    frame.columnconfigure(1, weight=1)

    s0_e = labeled_entry(frame, 0, "S0", "100")
    sigma_e = labeled_entry(frame, 1, "sigma", "0.2")
    r_e = labeled_entry(frame, 2, "r", "0.05")
    q_e = labeled_entry(frame, 3, "q", "0.0")
    t_e = labeled_entry(frame, 4, "T", "1.0")
    k_e = labeled_entry(frame, 5, "K", "100")
    n_e = labeled_entry(frame, 6, "n_obs", "12")

    ttk.Label(frame, text="option_type").grid(row=7, column=0, sticky="w", padx=(32, 16), pady=10)
    opt_type = tk.StringVar(value="call")
    ttk.Combobox(frame, textvariable=opt_type, values=["call", "put"], state="readonly").grid(row=7, column=1, sticky="ew", padx=(0, 32), pady=10)

    def on_calc():
        s0 = require_positive(parse_float(s0_e, "S0"), "S0")
        sigma = require_non_negative(parse_float(sigma_e, "sigma"), "sigma")
        r = parse_float(r_e, "r")
        q = parse_float(q_e, "q")
        t = require_positive(parse_float(t_e, "T"), "T")
        k = require_positive(parse_float(k_e, "K"), "K")
        n_obs = parse_int(n_e, "n_obs")
        if n_obs <= 0:
            raise ValueError("n_obs 必须大于 0")

        md = MarketData(s0=s0, sigma=sigma, r=r, q=q, t=t, k=k)
        opt = GeometricAsianOption(option_type=opt_type.get(), market_data=md, n_obs=n_obs)
        price = ClosedFormEngine.geometric_asian(opt)
        result_writer(f"[几何亚式 {opt_type.get()}] 价格 = {price:.6f}")

    ttk.Button(frame, text="计算价格", command=wrap_action(on_calc, result_writer)).grid(row=8, column=0, columnspan=2, pady=(24, 32))

    return frame


def create_arithmetic_asian_tab(notebook: ttk.Notebook, result_writer):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="算术亚式")
    frame.columnconfigure(1, weight=1)

    s0_e = labeled_entry(frame, 0, "S0", "100")
    sigma_e = labeled_entry(frame, 1, "sigma", "0.2")
    r_e = labeled_entry(frame, 2, "r", "0.05")
    q_e = labeled_entry(frame, 3, "q", "0.0")
    t_e = labeled_entry(frame, 4, "T", "1.0")
    k_e = labeled_entry(frame, 5, "K", "100")
    n_obs_e = labeled_entry(frame, 6, "n_obs", "12")
    n_paths_e = labeled_entry(frame, 7, "n_paths", "50000")

    ttk.Label(frame, text="option_type").grid(row=8, column=0, sticky="w", padx=(32, 16), pady=10)
    opt_type = tk.StringVar(value="call")
    ttk.Combobox(frame, textvariable=opt_type, values=["call", "put"], state="readonly").grid(row=8, column=1, sticky="ew", padx=(0, 32), pady=10)

    control_var = tk.BooleanVar(value=True)
    ttk.Checkbutton(frame, text="使用控制变量（几何亚式）", variable=control_var).grid(row=9, column=0, columnspan=2, sticky="w", padx=(32, 32), pady=10)

    def on_calc():
        s0 = require_positive(parse_float(s0_e, "S0"), "S0")
        sigma = require_non_negative(parse_float(sigma_e, "sigma"), "sigma")
        r = parse_float(r_e, "r")
        q = parse_float(q_e, "q")
        t = require_positive(parse_float(t_e, "T"), "T")
        k = require_positive(parse_float(k_e, "K"), "K")
        n_obs = parse_int(n_obs_e, "n_obs")
        n_paths = parse_int(n_paths_e, "n_paths")
        if n_obs <= 0:
            raise ValueError("n_obs 必须大于 0")
        if n_paths <= 0:
            raise ValueError("n_paths 必须大于 0")

        md = MarketData(s0=s0, sigma=sigma, r=r, q=q, t=t, k=k)
        opt = ArithmeticAsianOption(
            option_type=opt_type.get(),
            market_data=md,
            n_obs=n_obs,
            n_paths=n_paths,
            control_variate=control_var.get(),
        )
        price, ci = MonteCarloEngine.arithmetic_asian(opt)
        result_writer(f"[算术亚式 {opt_type.get()}] 价格 = {price:.6f}, 95% CI = [{ci[0]:.6f}, {ci[1]:.6f}]")

    ttk.Button(frame, text="计算价格", command=wrap_action(on_calc, result_writer)).grid(row=10, column=0, columnspan=2, pady=(24, 32))

    return frame
