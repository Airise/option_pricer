import tkinter as tk
from tkinter import ttk

from core.market_data import TwoAssetMarketData
from core.option import ArithmeticBasketOption, GeometricBasketOption
from engines.closed_form import ClosedFormEngine
from engines.monte_carlo import MonteCarloEngine
from ._helpers import labeled_entry, parse_float, parse_int, require_non_negative, require_positive, require_unit_interval, wrap_action


def _common_two_asset_inputs(frame):
    s01_e = labeled_entry(frame, 0, "S01", "100")
    sigma1_e = labeled_entry(frame, 1, "sigma1", "0.2")
    s02_e = labeled_entry(frame, 2, "S02", "100")
    sigma2_e = labeled_entry(frame, 3, "sigma2", "0.25")
    r_e = labeled_entry(frame, 4, "r", "0.05")
    t_e = labeled_entry(frame, 5, "T", "1.0")
    k_e = labeled_entry(frame, 6, "K", "100")
    rho_e = labeled_entry(frame, 7, "rho", "0.5")
    return s01_e, sigma1_e, s02_e, sigma2_e, r_e, t_e, k_e, rho_e


def create_geometric_basket_tab(notebook: ttk.Notebook, result_writer):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="几何篮子")
    frame.columnconfigure(1, weight=1)

    s01_e, sigma1_e, s02_e, sigma2_e, r_e, t_e, k_e, rho_e = _common_two_asset_inputs(frame)

    ttk.Label(frame, text="option_type").grid(row=8, column=0, sticky="w", padx=(32, 16), pady=10)
    opt_type = tk.StringVar(value="call")
    ttk.Combobox(frame, textvariable=opt_type, values=["call", "put"], state="readonly").grid(row=8, column=1, sticky="ew", padx=(0, 32), pady=10)

    def on_calc():
        s01 = require_positive(parse_float(s01_e, "S01"), "S01")
        sigma1 = require_non_negative(parse_float(sigma1_e, "sigma1"), "sigma1")
        s02 = require_positive(parse_float(s02_e, "S02"), "S02")
        sigma2 = require_non_negative(parse_float(sigma2_e, "sigma2"), "sigma2")
        r = parse_float(r_e, "r")
        t = require_positive(parse_float(t_e, "T"), "T")
        k = require_positive(parse_float(k_e, "K"), "K")
        rho = require_unit_interval(parse_float(rho_e, "rho"), "rho")

        md = TwoAssetMarketData(
            s01=s01,
            sigma1=sigma1,
            s02=s02,
            sigma2=sigma2,
            r=r,
            t=t,
            k=k,
            rho=rho,
        )
        opt = GeometricBasketOption(option_type=opt_type.get(), market_data=md)
        price = ClosedFormEngine.geometric_basket(opt)
        result_writer(f"[几何篮子 {opt_type.get()}] 价格 = {price:.6f}")

    ttk.Button(frame, text="计算价格", command=wrap_action(on_calc, result_writer)).grid(row=9, column=0, columnspan=2, pady=(24, 32))

    return frame


def create_arithmetic_basket_tab(notebook: ttk.Notebook, result_writer):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="算术篮子")
    frame.columnconfigure(1, weight=1)

    s01_e, sigma1_e, s02_e, sigma2_e, r_e, t_e, k_e, rho_e = _common_two_asset_inputs(frame)
    n_paths_e = labeled_entry(frame, 8, "n_paths", "50000")

    ttk.Label(frame, text="option_type").grid(row=9, column=0, sticky="w", padx=(32, 16), pady=10)
    opt_type = tk.StringVar(value="call")
    ttk.Combobox(frame, textvariable=opt_type, values=["call", "put"], state="readonly").grid(row=9, column=1, sticky="ew", padx=(0, 32), pady=10)

    control_var = tk.BooleanVar(value=True)
    ttk.Checkbutton(frame, text="使用控制变量（几何篮子）", variable=control_var).grid(row=10, column=0, columnspan=2, sticky="w", padx=(32, 32), pady=10)

    def on_calc():
        s01 = require_positive(parse_float(s01_e, "S01"), "S01")
        sigma1 = require_non_negative(parse_float(sigma1_e, "sigma1"), "sigma1")
        s02 = require_positive(parse_float(s02_e, "S02"), "S02")
        sigma2 = require_non_negative(parse_float(sigma2_e, "sigma2"), "sigma2")
        r = parse_float(r_e, "r")
        t = require_positive(parse_float(t_e, "T"), "T")
        k = require_positive(parse_float(k_e, "K"), "K")
        rho = require_unit_interval(parse_float(rho_e, "rho"), "rho")
        n_paths = parse_int(n_paths_e, "n_paths")
        if n_paths <= 0:
            raise ValueError("n_paths 必须大于 0")

        md = TwoAssetMarketData(
            s01=s01,
            sigma1=sigma1,
            s02=s02,
            sigma2=sigma2,
            r=r,
            t=t,
            k=k,
            rho=rho,
        )
        opt = ArithmeticBasketOption(
            option_type=opt_type.get(),
            market_data=md,
            n_paths=n_paths,
            control_variate=control_var.get(),
        )
        price, ci = MonteCarloEngine.arithmetic_basket(opt)
        result_writer(f"[算术篮子 {opt_type.get()}] 价格 = {price:.6f}, 95% CI = [{ci[0]:.6f}, {ci[1]:.6f}]")

    ttk.Button(frame, text="计算价格", command=wrap_action(on_calc, result_writer)).grid(row=11, column=0, columnspan=2, pady=(24, 32))

    return frame
