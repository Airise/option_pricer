from core.market_data import MarketData, TwoAssetMarketData
from core.option import (
    ArithmeticAsianOption,
    ArithmeticBasketOption,
    GeometricAsianOption,
    GeometricBasketOption,
)
from engines.closed_form import ClosedFormEngine
from engines.monte_carlo import MonteCarloEngine


def test_arithmetic_asian_ci_contains_price():
    md = MarketData(s0=100, sigma=0.2, r=0.05, q=0.0, t=1.0, k=100)
    opt = ArithmeticAsianOption(option_type="call", market_data=md, n_obs=12, n_paths=3000, control_variate=True)
    price, ci = MonteCarloEngine.arithmetic_asian(opt)
    assert ci[0] <= price <= ci[1]


def test_arithmetic_asian_above_geometric_asian_for_call():
    md = MarketData(s0=100, sigma=0.2, r=0.05, q=0.0, t=1.0, k=100)
    arith_opt = ArithmeticAsianOption(option_type="call", market_data=md, n_obs=12, n_paths=6000, control_variate=True)
    geo_opt = GeometricAsianOption(option_type="call", market_data=md, n_obs=12)

    arith_price, _ = MonteCarloEngine.arithmetic_asian(arith_opt)
    geo_price = ClosedFormEngine.geometric_asian(geo_opt)

    assert arith_price >= geo_price


def test_arithmetic_basket_ci_contains_price():
    md = TwoAssetMarketData(s01=100, sigma1=0.2, s02=100, sigma2=0.25, r=0.05, t=1.0, k=100, rho=0.5)
    opt = ArithmeticBasketOption(option_type="call", market_data=md, n_paths=3000, control_variate=True)
    price, ci = MonteCarloEngine.arithmetic_basket(opt)
    assert ci[0] <= price <= ci[1]


def test_arithmetic_basket_above_geometric_basket_for_call():
    md = TwoAssetMarketData(s01=100, sigma1=0.2, s02=100, sigma2=0.25, r=0.05, t=1.0, k=100, rho=0.5)
    arith_opt = ArithmeticBasketOption(option_type="call", market_data=md, n_paths=7000, control_variate=True)
    geo_opt = GeometricBasketOption(option_type="call", market_data=md)

    arith_price, _ = MonteCarloEngine.arithmetic_basket(arith_opt)
    geo_price = ClosedFormEngine.geometric_basket(geo_opt)

    assert arith_price >= geo_price
