from dataclasses import dataclass
from typing import Literal

from .market_data import MarketData, TwoAssetMarketData

OptionType = Literal["call", "put"]


@dataclass
class Option:
    option_type: OptionType


@dataclass
class EuropeanOption(Option):
    market_data: MarketData


@dataclass
class AmericanOption(Option):
    market_data: MarketData


@dataclass
class GeometricAsianOption(Option):
    market_data: MarketData
    n_obs: int


@dataclass
class ArithmeticAsianOption(Option):
    market_data: MarketData
    n_obs: int
    n_paths: int
    control_variate: bool = True


@dataclass
class GeometricBasketOption(Option):
    market_data: TwoAssetMarketData


@dataclass
class ArithmeticBasketOption(Option):
    market_data: TwoAssetMarketData
    n_paths: int
    control_variate: bool = True


@dataclass
class KIKOPutOption(Option):
    market_data: MarketData
    l: float
    u: float
    rebate: float
    n_monitors: int
