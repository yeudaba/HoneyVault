# core/shamir.py
import random
import functools

# --- התיקון: מספר ראשוני ענק (Mersenne Prime 13) שגדול יותר מהמפתח ---
# 2^521 - 1 הוא מספר עצום שמספיק לכל מפתח הצפנה
_PRIME = 2**521 - 1

def _eval_at(poly, x, prime):
    """Evaluates polynomial (coefficient tuple) at x."""
    accum = 0
    for coeff in reversed(poly):
        accum = (accum * x + coeff) % prime
    return accum

def make_random_shares(secret_int, minimum, shares):
    """
    Generates a random shamir pool for a given secret integer.
    """
    if minimum > shares:
        raise ValueError("Pool secret would be irrecoverable.")
    
    # יצירת פולינום רנדומלי שהמקדש החופשי שלו הוא הסוד
    poly = [secret_int] + [random.SystemRandom().randint(0, _PRIME - 1) for i in range(minimum - 1)]
    
    # יצירת נקודות (x, y) על הפולינום
    points = [(i, _eval_at(poly, i, _PRIME)) for i in range(1, shares + 1)]
    return points

def recover_secret(shares):
    """
    Recover the secret from share points (x, y).
    """
    if len(shares) < 2:
        raise ValueError("Need at least 2 shares")
    
    x_s, y_s = zip(*shares)
    return _lagrange_interpolate(0, x_s, y_s, _PRIME)

def _lagrange_interpolate(x, x_s, y_s, prime):
    """
    Find the y-value for the given x, given n (x, y) points.
    """
    k = len(x_s)
    assert k == len(y_s)
    
    nums = []
    dens = []
    
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        
        nums.append(functools.reduce(lambda a, b: a * (x - b) % prime, others, 1))
        dens.append(functools.reduce(lambda a, b: a * (cur - b) % prime, others, 1))
        
    den = functools.reduce(lambda a, b: a * b % prime, dens, 1)
    
    num = sum([_divmod(nums[i] * den * y_s[i] % prime, dens[i], prime) for i in range(k)])
    return (_divmod(num, den, prime) + prime) % prime

def _extended_gcd(a, b):
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y

def _divmod(num, den, p):
    inv, _ = _extended_gcd(den, p)
    return num * inv

# --- פונקציות עזר להמרה ---

def split_secret_hex(secret_hex, min_shares, num_shares):
    secret_int = int(secret_hex, 16)
    shares = make_random_shares(secret_int, min_shares, num_shares)
    return [f"{x}-{hex(y)[2:]}" for x, y in shares]

def recover_secret_hex(shares_strings):
    shares = []
    for s in shares_strings:
        if "-" in s:
            x, y_hex = s.split("-")
            shares.append((int(x), int(y_hex, 16)))
            
    secret_int = recover_secret(shares)
    h = hex(secret_int)[2:]
    return h if len(h) % 2 == 0 else "0" + h