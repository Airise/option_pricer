from dataclasses import dataclass


@dataclass
class MarketData:
    s0: float
    sigma: float
    r: float
    q: float
    t: float
    k: float


@dataclass
class TwoAssetMarketData:
    s01: float
    sigma1: float
    s02: float
    sigma2: float
    r: float
    t: float
    k: float
    rho: float
