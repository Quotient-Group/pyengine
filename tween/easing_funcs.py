import math

# ----------------------------------------------------------------------
# Utility
# ----------------------------------------------------------------------
def clamp(t, low=0.0, high=1.0):
    """Clamp t to the range [low, high]."""
    return max(low, min(high, t))

# ----------------------------------------------------------------------
# 1. Linear
# ----------------------------------------------------------------------
def linear(t):
    return t

# ----------------------------------------------------------------------
# 2. Quadratic
# ----------------------------------------------------------------------
def ease_in_quad(t):
    return t * t

def ease_out_quad(t):
    return t * (2 - t)

def ease_in_out_quad(t):
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t

# ----------------------------------------------------------------------
# 3. Cubic
# ----------------------------------------------------------------------
def ease_in_cubic(t):
    return t * t * t

def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def ease_in_out_cubic(t):
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2

# ----------------------------------------------------------------------
# 4. Quartic
# ----------------------------------------------------------------------
def ease_in_quart(t):
    return t ** 4

def ease_out_quart(t):
    return 1 - (1 - t) ** 4

def ease_in_out_quart(t):
    if t < 0.5:
        return 8 * t ** 4
    else:
        return 1 - (-2 * t + 2) ** 4 / 2

# ----------------------------------------------------------------------
# 5. Quintic
# ----------------------------------------------------------------------
def ease_in_quint(t):
    return t ** 5

def ease_out_quint(t):
    return 1 - (1 - t) ** 5

def ease_in_out_quint(t):
    if t < 0.5:
        return 16 * t ** 5
    else:
        return 1 - (-2 * t + 2) ** 5 / 2

# ----------------------------------------------------------------------
# 6. Sine
# ----------------------------------------------------------------------
def ease_in_sine(t):
    return 1 - math.cos(t * math.pi / 2)

def ease_out_sine(t):
    return math.sin(t * math.pi / 2)

def ease_in_out_sine(t):
    return -(math.cos(math.pi * t) - 1) / 2

# ----------------------------------------------------------------------
# 7. Exponential
# ----------------------------------------------------------------------
def ease_in_expo(t):
    return 0.0 if t == 0 else 2 ** (10 * (t - 1))

def ease_out_expo(t):
    return 1.0 if t == 1 else 1 - 2 ** (-10 * t)

def ease_in_out_expo(t):
    if t == 0 or t == 1:
        return t
    if t < 0.5:
        return 2 ** (20 * t - 10) / 2
    else:
        return (2 - 2 ** (-20 * t + 10)) / 2

# ----------------------------------------------------------------------
# 8. Circular
# ----------------------------------------------------------------------
def ease_in_circ(t):
    return 1 - math.sqrt(1 - t * t)

def ease_out_circ(t):
    return math.sqrt(1 - (t - 1) ** 2)

def ease_in_out_circ(t):
    if t < 0.5:
        return (1 - math.sqrt(1 - (2 * t) ** 2)) / 2
    else:
        return (math.sqrt(1 - (-2 * t + 2) ** 2) + 1) / 2

# ----------------------------------------------------------------------
# 9. Back (with overshoot)
# ----------------------------------------------------------------------
def ease_in_back(t, overshoot=1.70158):
    return t * t * ((overshoot + 1) * t - overshoot)

def ease_out_back(t, overshoot=1.70158):
    return 1 - (1 - t) * (1 - t) * ((overshoot + 1) * (1 - t) - overshoot)

def ease_in_out_back(t, overshoot=1.70158):
    c = overshoot * 1.525
    if t < 0.5:
        return (2 * t) ** 2 * ((c + 1) * 2 * t - c) / 2
    else:
        return ( (2 * t - 2) ** 2 * ((c + 1) * (t * 2 - 2) + c) + 2 ) / 2

# ----------------------------------------------------------------------
# 10. Elastic (with optional amplitude and period)
# ----------------------------------------------------------------------
def ease_in_elastic(t, amplitude=1.0, period=0.3):
    if t == 0 or t == 1:
        return t
    s = period / (2 * math.pi) * math.asin(1 / amplitude) if amplitude < 1 else period / 4
    return -(amplitude * 2 ** (10 * (t - 1)) * math.sin((t - 1 - s) * (2 * math.pi) / period))

def ease_out_elastic(t, amplitude=1.0, period=0.3):
    if t == 0 or t == 1:
        return t
    s = period / (2 * math.pi) * math.asin(1 / amplitude) if amplitude < 1 else period / 4
    return amplitude * 2 ** (-10 * t) * math.sin((t - s) * (2 * math.pi) / period) + 1

def ease_in_out_elastic(t, amplitude=1.0, period=0.3):
    if t == 0 or t == 1:
        return t
    s = period / (2 * math.pi) * math.asin(1 / amplitude) if amplitude < 1 else period / 4
    if t < 0.5:
        return -0.5 * (amplitude * 2 ** (20 * t - 10) * math.sin((20 * t - 10 - s) * (2 * math.pi) / period))
    else:
        return amplitude * 2 ** (-20 * t + 10) * math.sin((20 * t - 10 - s) * (2 * math.pi) / period) * 0.5 + 1

# ----------------------------------------------------------------------
# 11. Bounce
# ----------------------------------------------------------------------
def ease_out_bounce(t):
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375

def ease_in_bounce(t):
    return 1 - ease_out_bounce(1 - t)

def ease_in_out_bounce(t):
    if t < 0.5:
        return (1 - ease_out_bounce(1 - 2 * t)) / 2
    else:
        return (1 + ease_out_bounce(2 * t - 1)) / 2

# ----------------------------------------------------------------------
# Dictionary mapping names to functions (for easy lookup)
# ----------------------------------------------------------------------
EASING_FUNCTIONS = {
    "linear": linear,

    "ease_in_quad": ease_in_quad,
    "ease_out_quad": ease_out_quad,
    "ease_in_out_quad": ease_in_out_quad,

    "ease_in_cubic": ease_in_cubic,
    "ease_out_cubic": ease_out_cubic,
    "ease_in_out_cubic": ease_in_out_cubic,

    "ease_in_quart": ease_in_quart,
    "ease_out_quart": ease_out_quart,
    "ease_in_out_quart": ease_in_out_quart,

    "ease_in_quint": ease_in_quint,
    "ease_out_quint": ease_out_quint,
    "ease_in_out_quint": ease_in_out_quint,

    "ease_in_sine": ease_in_sine,
    "ease_out_sine": ease_out_sine,
    "ease_in_out_sine": ease_in_out_sine,

    "ease_in_expo": ease_in_expo,
    "ease_out_expo": ease_out_expo,
    "ease_in_out_expo": ease_in_out_expo,

    "ease_in_circ": ease_in_circ,
    "ease_out_circ": ease_out_circ,
    "ease_in_out_circ": ease_in_out_circ,

    "ease_in_back": ease_in_back,
    "ease_out_back": ease_out_back,
    "ease_in_out_back": ease_in_out_back,

    "ease_in_elastic": ease_in_elastic,
    "ease_out_elastic": ease_out_elastic,
    "ease_in_out_elastic": ease_in_out_elastic,

    "ease_in_bounce": ease_in_bounce,
    "ease_out_bounce": ease_out_bounce,
    "ease_in_out_bounce": ease_in_out_bounce,
}

# ----------------------------------------------------------------------
# Example usage
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Interpolate from 0 to 100 using ease_out_cubic at t = 0.25
    t = 0.25
    start, end = 0, 100
    value = start + (end - start) * ease_out_cubic(t)
    print(f"ease_out_cubic at t={t}: {value}")

    # List all available functions
    print("\nAvailable easing functions:")
    for name in sorted(EASING_FUNCTIONS.keys()):
        print(f"  {name}")