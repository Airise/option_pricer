import math
import random
from typing import List, Tuple

from core.math_utils import box_muller, correlated_normal
from core.option import (
    ArithmeticAsianOption,
    ArithmeticBasketOption,
    EuropeanOption,
    GeometricAsianOption,
    GeometricBasketOption,
)
from core.payoff import vanilla_payoff
from engines.closed_form import ClosedFormEngine


def generate_path(s0: float, r: float, q: float, sigma: float, t: float, n_steps: int) -> List[float]:
    dt = t / n_steps
    s = s0
    path = []
    for _ in range(n_steps):
        z, _ = box_muller()
        s *= math.exp((r - q - 0.5 * sigma * sigma) * dt + sigma * math.sqrt(dt) * z)
        path.append(s)
    return path


class MonteCarloEngine:
    @staticmethod
    def _ci_from_discounted_payoffs(values: List[float]) -> Tuple[float, Tuple[float, float]]:
        n = len(values)
        mean = sum(values) / n
        if n == 1:
            return mean, (mean, mean)
        var = sum((x - mean) ** 2 for x in values) / (n - 1)
        se = math.sqrt(var / n)
        half = 1.96 * se
        return mean, (mean - half, mean + half)

    @staticmethod
    def european(opt: EuropeanOption, n_paths: int) -> Tuple[float, Tuple[float, float]]:
        random.seed(0)
        m = opt.market_data
        values = []
        for _ in range(n_paths):
            z, _ = box_muller()
            st = m.s0 * math.exp((m.r - m.q - 0.5 * m.sigma * m.sigma) * m.t + m.sigma * math.sqrt(m.t) * z)
            payoff = vanilla_payoff(st, m.k, opt.option_type)
            values.append(math.exp(-m.r * m.t) * payoff)
        return MonteCarloEngine._ci_from_discounted_payoffs(values)

    @staticmethod
    def arithmetic_asian(opt: ArithmeticAsianOption) -> Tuple[float, Tuple[float, float]]:
        random.seed(0)
        m = opt.market_data
        dt = m.t / opt.n_obs

        geo_opt = GeometricAsianOption(option_type=opt.option_type, market_data=m, n_obs=opt.n_obs)
        geo_closed = ClosedFormEngine.geometric_asian(geo_opt)

        arith_disc = []
        geo_disc = []

        for _ in range(opt.n_paths):
            s = m.s0
            vals = []
            for _ in range(opt.n_obs):
                z, _ = box_muller()
                s *= math.exp((m.r - m.q - 0.5 * m.sigma * m.sigma) * dt + m.sigma * math.sqrt(dt) * z)
                vals.append(s)

            arith_avg = sum(vals) / len(vals)
            geo_avg = math.exp(sum(math.log(max(v, 1e-16)) for v in vals) / len(vals))

            arith_payoff = vanilla_payoff(arith_avg, m.k, opt.option_type)
            geo_payoff = vanilla_payoff(geo_avg, m.k, opt.option_type)

            disc = math.exp(-m.r * m.t)
            arith_disc.append(disc * arith_payoff)
            geo_disc.append(disc * geo_payoff)

        if opt.control_variate:
            n = opt.n_paths
            mean_a = sum(arith_disc) / n
            mean_g = sum(geo_disc) / n
            cov = sum((arith_disc[i] - mean_a) * (geo_disc[i] - mean_g) for i in range(n)) / (n - 1)
            var_g = sum((x - mean_g) ** 2 for x in geo_disc) / (n - 1)
            b = cov / var_g if var_g > 0 else 0.0
            adjusted = [arith_disc[i] - b * (geo_disc[i] - geo_closed) for i in range(n)]
            return MonteCarloEngine._ci_from_discounted_payoffs(adjusted)

        return MonteCarloEngine._ci_from_discounted_payoffs(arith_disc)

    @staticmethod
    def arithmetic_basket(opt: ArithmeticBasketOption) -> Tuple[float, Tuple[float, float]]:
        random.seed(0)
        m = opt.market_data

        geo_opt = GeometricBasketOption(option_type=opt.option_type, market_data=m)
        geo_closed = ClosedFormEngine.geometric_basket(geo_opt)

        arith_disc = []
        geo_disc = []

        for _ in range(opt.n_paths):
            z1, z2 = correlated_normal(m.rho)
            s1t = m.s01 * math.exp((m.r - 0.5 * m.sigma1 * m.sigma1) * m.t + m.sigma1 * math.sqrt(m.t) * z1)
            s2t = m.s02 * math.exp((m.r - 0.5 * m.sigma2 * m.sigma2) * m.t + m.sigma2 * math.sqrt(m.t) * z2)

            arith_b = 0.5 * (s1t + s2t)
            geo_b = math.sqrt(s1t * s2t)

            arith_payoff = vanilla_payoff(arith_b, m.k, opt.option_type)
            geo_payoff = vanilla_payoff(geo_b, m.k, opt.option_type)

            disc = math.exp(-m.r * m.t)
            arith_disc.append(disc * arith_payoff)
            geo_disc.append(disc * geo_payoff)

        if opt.control_variate:
            n = opt.n_paths
            mean_a = sum(arith_disc) / n
            mean_g = sum(geo_disc) / n
            cov = sum((arith_disc[i] - mean_a) * (geo_disc[i] - mean_g) for i in range(n)) / (n - 1)
            var_g = sum((x - mean_g) ** 2 for x in geo_disc) / (n - 1)
            b = cov / var_g if var_g > 0 else 0.0
            adjusted = [arith_disc[i] - b * (geo_disc[i] - geo_closed) for i in range(n)]
            return MonteCarloEngine._ci_from_discounted_payoffs(adjusted)

        return MonteCarloEngine._ci_from_discounted_payoffs(arith_disc)
