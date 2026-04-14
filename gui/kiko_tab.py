from tkinter import ttk

from core.market_data import MarketData
from core.option import KIKOPutOption
from engines.quasi_monte_carlo import QuasiMonteCarloEngine
from ._helpers import labeled_entry, parse_float, parse_int, require_non_negative, require_positive, require_unit_interval, wrap_action


def create_tab(notebook: ttk.Notebook, result_writer):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="KIKO Put")
    frame.columnconfigure(1, weight=1)

    s0_e = labeled_entry(frame, 0, "S0", "100")
    sigma_e = labeled_entry(frame, 1, "sigma", "0.2")
    r_e = labeled_entry(frame, 2, "r", "0.05")
    t_e = labeled_entry(frame, 3, "T", "1.0")
    k_e = labeled_entry(frame, 4, "K", "100")
    l_e = labeled_entry(frame, 5, "L (knock-in)", "80")
    u_e = labeled_entry(frame, 6, "U (knock-out)", "120")
    rebate_e = labeled_entry(frame, 7, "R (rebate)", "2")
    n_mon_e = labeled_entry(frame, 8, "n_monitors", "52")
    n_paths_e = labeled_entry(frame, 9, "n_paths", "20000")

    def on_calc():
        s0 = require_positive(parse_float(s0_e, "S0"), "S0")
        sigma = require_non_negative(parse_float(sigma_e, "sigma"), "sigma")
        r = parse_float(r_e, "r")
        t = require_positive(parse_float(t_e, "T"), "T")
        k = require_positive(parse_float(k_e, "K"), "K")
        l = parse_float(l_e, "L")
        u = parse_float(u_e, "U")
        rebate = require_non_negative(parse_float(rebate_e, "R"), "R")
        n_monitors = parse_int(n_mon_e, "n_monitors")
        if n_monitors <= 0:
            raise ValueError("n_monitors must be greater than 0")
        if not (l < s0 < u):
            raise ValueError("KIKO parameters must satisfy L < S0 < U")

        md = MarketData(s0=s0, sigma=sigma, r=r, q=0.0, t=t, k=k)
        opt = KIKOPutOption(
            option_type="put",
            market_data=md,
            l=l,
            u=u,
            rebate=rebate,
            n_monitors=n_monitors,
        )

        n_paths = parse_int(n_paths_e, "n_paths")
        if n_paths <= 0:
            raise ValueError("n_paths must be greater than 0")
        price, ci = QuasiMonteCarloEngine.kiko_price(opt, n_paths)
        delta = QuasiMonteCarloEngine.kiko_delta(opt, n_paths // 2)
        result_writer(f"[KIKO put] Price = {price:.6f}, 95% CI = [{ci[0]:.6f}, {ci[1]:.6f}], Delta = {delta:.6f}")

    ttk.Button(frame, text="Calculate Price & Delta", command=wrap_action(on_calc, result_writer)).grid(row=11, column=0, columnspan=2, pady=(24, 32))

    return frame
