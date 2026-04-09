from typing import Literal

OptionType = Literal["call", "put"]


def vanilla_payoff(s: float, k: float, option_type: OptionType) -> float:
    if option_type == "call":
        return max(s - k, 0.0)
    return max(k - s, 0.0)
