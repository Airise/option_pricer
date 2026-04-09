import math

from core.math_utils import norm_cdf
from core.option import EuropeanOption, GeometricAsianOption, GeometricBasketOption


class ClosedFormEngine:
    @staticmethod
    def european(opt: EuropeanOption) -> float:
        m = opt.market_data
        if m.t <= 0:
            return max(m.s0 - m.k, 0.0) if opt.option_type == "call" else max(m.k - m.s0, 0.0)

        sig_sqrt_t = m.sigma * math.sqrt(m.t)
        if sig_sqrt_t == 0:
            fwd = m.s0 * math.exp((m.r - m.q) * m.t)
            disc = math.exp(-m.r * m.t)
            return disc * (max(fwd - m.k, 0.0) if opt.option_type == "call" else max(m.k - fwd, 0.0))

        d1 = (math.log(m.s0 / m.k) + (m.r - m.q + 0.5 * m.sigma * m.sigma) * m.t) / sig_sqrt_t
        d2 = d1 - sig_sqrt_t

        if opt.option_type == "call":
            return m.s0 * math.exp(-m.q * m.t) * norm_cdf(d1) - m.k * math.exp(-m.r * m.t) * norm_cdf(d2)
        return m.k * math.exp(-m.r * m.t) * norm_cdf(-d2) - m.s0 * math.exp(-m.q * m.t) * norm_cdf(-d1)

    @staticmethod
    def geometric_asian(opt: GeometricAsianOption) -> float:
        m = opt.market_data
        n = opt.n_obs
        if n <= 0:
            raise ValueError("n_obs must be positive")

        sigma_hat = m.sigma * math.sqrt((n + 1) * (2 * n + 1) / (6 * n * n))
        mu_hat = (m.r - m.q - 0.5 * m.sigma * m.sigma) * (n + 1) / (2 * n) + 0.5 * sigma_hat * sigma_hat

        sig_sqrt_t = sigma_hat * math.sqrt(m.t)
        d1 = (math.log(m.s0 / m.k) + (mu_hat + 0.5 * sigma_hat * sigma_hat) * m.t) / sig_sqrt_t
        d2 = d1 - sig_sqrt_t

        disc = math.exp(-m.r * m.t)
        growth = m.s0 * math.exp(mu_hat * m.t)

        if opt.option_type == "call":
            return disc * (growth * norm_cdf(d1) - m.k * norm_cdf(d2))
        return disc * (m.k * norm_cdf(-d2) - growth * norm_cdf(-d1))

    @staticmethod
    def geometric_basket(opt: GeometricBasketOption) -> float:
        m = opt.market_data
        bg0 = math.sqrt(m.s01 * m.s02)
        sigma_bg = math.sqrt(m.sigma1 * m.sigma1 + 2 * m.rho * m.sigma1 * m.sigma2 + m.sigma2 * m.sigma2) / 2.0
        mu_bg = m.r - 0.25 * (m.sigma1 * m.sigma1 + m.sigma2 * m.sigma2) + 0.5 * sigma_bg * sigma_bg

        sig_sqrt_t = sigma_bg * math.sqrt(m.t)
        d1 = (math.log(bg0 / m.k) + (mu_bg + 0.5 * sigma_bg * sigma_bg) * m.t) / sig_sqrt_t
        d2 = d1 - sig_sqrt_t

        disc = math.exp(-m.r * m.t)
        growth = bg0 * math.exp(mu_bg * m.t)

        if opt.option_type == "call":
            return disc * (growth * norm_cdf(d1) - m.k * norm_cdf(d2))
        return disc * (m.k * norm_cdf(-d2) - growth * norm_cdf(-d1))
