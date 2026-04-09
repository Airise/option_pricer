from core.market_data import MarketData
from core.option import KIKOPutOption
from engines.quasi_monte_carlo import QuasiMonteCarloEngine


def test_kiko_runs_and_ci_contains_price():
    md = MarketData(s0=100, sigma=0.2, r=0.05, q=0.0, t=1.0, k=100)
    opt = KIKOPutOption(option_type="put", market_data=md, l=80, u=120, rebate=2.0, n_monitors=24)
    price, ci = QuasiMonteCarloEngine.kiko_price(opt, n_paths=2048)
    assert ci[0] <= price <= ci[1]


def test_kiko_delta_is_finite():
    md = MarketData(s0=100, sigma=0.2, r=0.05, q=0.0, t=1.0, k=100)
    opt = KIKOPutOption(option_type="put", market_data=md, l=80, u=120, rebate=2.0, n_monitors=24)
    delta = QuasiMonteCarloEngine.kiko_delta(opt, n_paths=2048)
    assert abs(delta) < 10
