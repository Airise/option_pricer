from core.market_data import MarketData
from core.option import EuropeanOption
from engines.closed_form import ClosedFormEngine
from engines.implied_volatility import implied_volatility


def test_implied_vol_recovers_sigma_from_bs_price():
    true_sigma = 0.2
    md = MarketData(s0=100, sigma=true_sigma, r=0.05, q=0.0, t=1.0, k=100)
    market_price = ClosedFormEngine.european(EuropeanOption(option_type="call", market_data=md))

    iv = implied_volatility(
        market_price=market_price,
        s0=100,
        k=100,
        t=1.0,
        r=0.05,
        q=0.0,
        option_type="call",
    )
    assert abs(iv - true_sigma) < 1e-4
