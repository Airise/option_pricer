from core.market_data import MarketData
from core.option import AmericanOption
from engines.binomial_tree import BinomialTreeEngine
from engines.closed_form import ClosedFormEngine
from core.option import EuropeanOption


def test_american_put_not_less_than_european_put():
    md = MarketData(s0=100, sigma=0.2, r=0.05, q=0.0, t=1.0, k=100)
    am_put = BinomialTreeEngine.american(AmericanOption(option_type="put", market_data=md), steps=400)
    eu_put = ClosedFormEngine.european(EuropeanOption(option_type="put", market_data=md))
    assert am_put >= eu_put


def test_american_call_close_to_european_call_when_no_dividend():
    md = MarketData(s0=100, sigma=0.2, r=0.05, q=0.0, t=1.0, k=100)
    am_call = BinomialTreeEngine.american(AmericanOption(option_type="call", market_data=md), steps=800)
    eu_call = ClosedFormEngine.european(EuropeanOption(option_type="call", market_data=md))
    assert abs(am_call - eu_call) < 5e-2
