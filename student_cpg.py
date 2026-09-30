"""Student template for Lab 03.

 Keep function names and return structures unchanged so the
grader and experiment runner can load this file.
"""

from __future__ import annotations

import math


TRIPOD_SIGN = {"LF": 1.0, "RM": 1.0, "LH": 1.0,
               "RF": -1.0, "LM": -1.0, "RH": -1.0}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def so2_step(o1: float, o2: float, alpha: float, phi: float) -> tuple[float, float]:
    """Return o1(t+1), o2(t+1) using a simultaneous update."""
    a1 = alpha * (math.cos(phi) * o1 + math.sin(phi) * o2)
    a2 = alpha * (-math.sin(phi) * o1 + math.cos(phi) * o2)
    return math.tanh(a1), math.tanh(a2)


def decode_tripod(o1: float, o2: float, stride_half: float,
                   lift_height: float) -> dict[str, dict[str, float | bool]]:
    """Return x_rel, lift, and contact for all six legs."""
    result = {}
    for leg, sign in TRIPOD_SIGN.items():
        phase_val = o1 * sign
        x_rel = stride_half * phase_val
        lift = lift_height * max(0.0, o2 * sign)
        contact = (o2 * sign) <= 0.0
        result[leg] = {
            "x_rel": x_rel,
            "lift": lift,
            "contact": contact
        }
    return result


def bounded_modulation(m: float, phi0: float = 0.20,
                       phi_gain: float = 0.20,
                       phi_bounds: tuple[float, float] = (0.10, 0.45),
                       stride0: float = 0.055,
                       stride_gain: float = 0.010,
                       stride_bounds: tuple[float, float] = (0.040, 0.070),
                       ) -> tuple[float, float]:
    """Map slow input m to bounded phi and stride commands."""
    phi_cmd = clamp(phi0 + phi_gain * m, phi_bounds[0], phi_bounds[1])
    stride_cmd = clamp(stride0 + stride_gain * m, stride_bounds[0], stride_bounds[1])
    return phi_cmd, stride_cmd