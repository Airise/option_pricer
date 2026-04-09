import math
import random
from typing import List, Tuple


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_pdf(x: float) -> float:
    return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)


def norm_inv(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        raise ValueError("p must be in (0,1)")

    # Peter J. Acklam's rational approximation
    a = [
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    ]
    b = [
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464968e00,
        2.938163982698783e00,
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e00,
        3.754408661907416e00,
    ]

    plow = 0.02425
    phigh = 1 - plow

    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (
            (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
            / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
        )
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(
            (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
            / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
        )

    q = p - 0.5
    r = q * q
    return (
        (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q
    ) / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def box_muller() -> Tuple[float, float]:
    u1 = random.random()
    u2 = random.random()
    r = math.sqrt(-2.0 * math.log(max(u1, 1e-16)))
    theta = 2.0 * math.pi * u2
    return r * math.cos(theta), r * math.sin(theta)


def normal_rand(n: int) -> List[float]:
    out: List[float] = []
    while len(out) < n:
        z1, z2 = box_muller()
        out.append(z1)
        if len(out) < n:
            out.append(z2)
    return out


def _van_der_corput(index: int, base: int) -> float:
    vdc = 0.0
    denom = 1.0
    i = index
    while i > 0:
        i, remainder = divmod(i, base)
        denom *= base
        vdc += remainder / denom
    return vdc


def _first_n_primes(n: int) -> List[int]:
    if n <= 0:
        return []
    primes: List[int] = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        limit = int(math.sqrt(candidate))
        for p in primes:
            if p > limit:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes


def halton_sequence(dim: int, n: int) -> List[List[float]]:
    if dim <= 0:
        raise ValueError("dim must be positive")
    if n <= 0:
        return []

    primes = _first_n_primes(dim)
    seq: List[List[float]] = []
    for i in range(1, n + 1):
        seq.append([_van_der_corput(i, primes[d]) for d in range(dim)])
    return seq


def sobol_sequence(dim: int, n: int) -> List[List[float]]:
    # Simplified fallback to Halton per assignment guidance.
    return halton_sequence(dim, n)


def correlated_normal(rho: float) -> Tuple[float, float]:
    z1, z2 = box_muller()
    z2_corr = rho * z1 + math.sqrt(max(1.0 - rho * rho, 0.0)) * z2
    return z1, z2_corr
