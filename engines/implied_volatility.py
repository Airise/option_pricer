from core.market_data import MarketData
from core.option import EuropeanOption
from engines.closed_form import ClosedFormEngine


def implied_volatility(
    market_price: float,
    s0: float,
    k: float,
    t: float,
    r: float,
    q: float,
    option_type: str,
    tol: float = 1e-6,
    max_iter: int = 200,
) -> float:
    low, high = 1e-6, 5.0

    for _ in range(max_iter):
        mid = 0.5 * (low + high)
        md = MarketData(s0=s0, sigma=mid, r=r, q=q, t=t, k=k)
        opt = EuropeanOption(option_type=option_type, market_data=md)
        model_price = ClosedFormEngine.european(opt)

        diff = model_price - market_price
        if abs(diff) < tol:
            return mid

        if diff > 0:
            high = mid
        else:
            low = mid

    return 0.5 * (low + high)
