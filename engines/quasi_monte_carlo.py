import math
from typing import List, Tuple

from core.math_utils import halton_sequence, norm_inv, sobol_sequence
from core.option import KIKOPutOption


class QuasiMonteCarloEngine:
    @staticmethod
    def _simulate_terminal_and_barriers(
        s0: float,
        r: float,
        sigma: float,
        t: float,
        n_monitors: int,
        uniforms: List[float],
    ) -> List[float]:
        dt = t / n_monitors
        s = s0
        path = []
        for i in range(n_monitors):
            u = min(max(uniforms[i], 1e-12), 1 - 1e-12)
            z = norm_inv(u)
            s *= math.exp((r - 0.5 * sigma * sigma) * dt + sigma * math.sqrt(dt) * z)
            path.append(s)
        return path

    @staticmethod
    def kiko_price(opt: KIKOPutOption, n_paths: int, use_sobol: bool = False) -> Tuple[float, Tuple[float, float]]:
        m = opt.market_data
        dim = opt.n_monitors
        seq = sobol_sequence(dim, n_paths) if use_sobol else halton_sequence(dim, n_paths)

        discounted = []
        for i in range(n_paths):
            path = QuasiMonteCarloEngine._simulate_terminal_and_barriers(
                s0=m.s0,
                r=m.r,
                sigma=m.sigma,
                t=m.t,
                n_monitors=opt.n_monitors,
                uniforms=seq[i],
            )

            knocked_out = False
            knocked_in = False

            for s in path:
                if s >= opt.u:
                    knocked_out = True
                    break
                if s <= opt.l:
                    knocked_in = True

            if knocked_out:
                payoff = opt.rebate
            elif knocked_in:
                payoff = max(m.k - path[-1], 0.0)
            else:
                payoff = 0.0

            discounted.append(math.exp(-m.r * m.t) * payoff)

        n = len(discounted)
        mean = sum(discounted) / n
        if n == 1:
            return mean, (mean, mean)
        var = sum((x - mean) ** 2 for x in discounted) / (n - 1)
        se = math.sqrt(var / n)
        half = 1.96 * se
        return mean, (mean - half, mean + half)

    @staticmethod
    def kiko_delta(opt: KIKOPutOption, n_paths: int, eps: float = 1e-4) -> float:
        m = opt.market_data

        up_mkt = type(m)(s0=m.s0 + eps, sigma=m.sigma, r=m.r, q=m.q, t=m.t, k=m.k)
        dn_mkt = type(m)(s0=max(m.s0 - eps, 1e-8), sigma=m.sigma, r=m.r, q=m.q, t=m.t, k=m.k)

        up_opt = KIKOPutOption(option_type=opt.option_type, market_data=up_mkt, l=opt.l, u=opt.u, rebate=opt.rebate, n_monitors=opt.n_monitors)
        dn_opt = KIKOPutOption(option_type=opt.option_type, market_data=dn_mkt, l=opt.l, u=opt.u, rebate=opt.rebate, n_monitors=opt.n_monitors)

        p_up, _ = QuasiMonteCarloEngine.kiko_price(up_opt, n_paths)
        p_dn, _ = QuasiMonteCarloEngine.kiko_price(dn_opt, n_paths)
        return (p_up - p_dn) / (2.0 * eps)
