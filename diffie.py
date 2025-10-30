import random
from math import isqrt

# --- Primality test ---
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, isqrt(n)+1):
        if n % i == 0:
            return False
    return True

# --- Generate small random prime ---
def generate_small_prime(limit=1000):
    primes = [n for n in range(2, limit) if is_prime(n)]
    return random.choice(primes)

# --- Find all primitive roots ---
def find_primitive_roots(p):
    phi = p-1
    # find prime factors of phi
    factors = set()
    n = phi
    i = 2
    while i*i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        factors.add(n)
    
    roots = []
    for g in range(2, p):
        if all(pow(g, phi//f, p) != 1 for f in factors):
            roots.append(g)
    return roots

# --- Diffie-Hellman Key Exchange ---
p = generate_small_prime(limit=200)  # small prime under 200
roots = find_primitive_roots(p)
g = random.choice(roots)

# Private keys
a = random.randint(1, p-2)  # Alice private
b = random.randint(1, p-2)  # Bob private

# Public keys
A = pow(g, a, p)
B = pow(g, b, p)

# Shared secret
s_A = pow(B, a, p)
s_B = pow(A, b, p)

# --- Output ---
print(f"Prime p = {p}")
print("Name: Pawan Mohit")
print("Roll No.: 160123749301")
print(f"All primitive roots: {roots}")
print(f"Selected generator g = {g}\n")
print(f"Alice private key: {a}")
print(f"Alice public key: {A}")
print(f"Bob private key: {b}")
print(f"Bob public key: {B}\n")
print(f"Shared secret (Alice) = {s_A}")
print(f"Shared secret (Bob)   = {s_B}")
print(f"Shared secrets match: {s_A == s_B}")