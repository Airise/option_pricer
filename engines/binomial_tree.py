import math

from core.option import AmericanOption
from core.payoff import vanilla_payoff


class BinomialTreeEngine:
    @staticmethod
    def american(opt: AmericanOption, steps: int) -> float:
        if steps <= 0:
            raise ValueError("steps must be positive")

        m = opt.market_data
        dt = m.t / steps
        u = math.exp(m.sigma * math.sqrt(dt))
        d = 1.0 / u
        p = (math.exp((m.r - m.q) * dt) - d) / (u - d)
        p = min(max(p, 0.0), 1.0)
        disc = math.exp(-m.r * dt)

        values = []
        for j in range(steps + 1):
            st = m.s0 * (u ** (steps - j)) * (d ** j)
            values.append(vanilla_payoff(st, m.k, opt.option_type))

        for i in range(steps - 1, -1, -1):
            for j in range(i + 1):
                cont = disc * (p * values[j] + (1 - p) * values[j + 1])
                st = m.s0 * (u ** (i - j)) * (d ** j)
                exer = vanilla_payoff(st, m.k, opt.option_type)
                values[j] = max(cont, exer)

        return values[0]
