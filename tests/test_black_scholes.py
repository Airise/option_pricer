import math

from core.market_data import MarketData
from core.option import EuropeanOption
from engines.closed_form import ClosedFormEngine


def test_black_scholes_call_benchmark():
    # Standard benchmark: S=100, K=100, r=5%, q=0, sigma=20%, T=1
    # Expected call price ~= 10.4506
    md = MarketData(s0=100, sigma=0.2, r=0.05, q=0.0, t=1.0, k=100)
    opt = EuropeanOption(option_type="call", market_data=md)
    price = ClosedFormEngine.european(opt)
    assert abs(price - 10.4506) < 1e-3


def test_black_scholes_put_call_parity():
    md = MarketData(s0=100, sigma=0.2, r=0.05, q=0.01, t=1.0, k=100)
    call = ClosedFormEngine.european(EuropeanOption(option_type="call", market_data=md))
    put = ClosedFormEngine.european(EuropeanOption(option_type="put", market_data=md))

    lhs = call - put
    rhs = md.s0 * math.exp(-md.q * md.t) - md.k * math.exp(-md.r * md.t)
    assert abs(lhs - rhs) < 1e-3
