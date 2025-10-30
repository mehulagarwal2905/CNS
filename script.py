# RSA

import base64 

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    for d in range(2, phi):
        if (d * e) % phi == 1:
            return d
    return None

def encrypt(message, e, n):
    """Return list[int] of RSA-encrypted code points (one per character)."""
    return [pow(ord(m), e, n) for m in message]

def decrypt(cipher_list, d, n):
    """Recover string from list[int] of RSA 'cipher numbers'."""
    return ''.join(chr(pow(c, d, n)) for c in cipher_list)

if __name__ == "__main__":
    print("Name: Pawan Mohit")
    print("Roll No.: 160123749301")

    p = int(input("Enter prime number p: "))
    q = int(input("Enter prime number q: "))
    message = input("Enter message to encrypt: ")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 2
    while e < phi:
        if gcd(e, phi) == 1:
            break
        e += 1

    d = mod_inverse(e, phi)

    print(f"\ne = {e}")
    print(f"n = {n}")
    print(f"phi(n) = {phi}")
    print(f"d = {d}")

    encrypted_list = encrypt(message, e, n)
    print("\nEncrypted (list of ints):")
    print(encrypted_list)

    decrypted_msg = decrypt(encrypted_list, d, n)
    print("\nDecrypted Message:", decrypted_msg)

# Diffie-Hellman
import random
from math import isqrt

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, isqrt(n)+1):
        if n % i == 0:
            return False
    return True

def generate_small_prime(limit=1000):
    primes = [n for n in range(2, limit) if is_prime(n)]
    return random.choice(primes)


def find_primitive_roots(p):
    phi = p-1
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

p = generate_small_prime(limit=200)  
roots = find_primitive_roots(p)
g = random.choice(roots)

a = random.randint(1, p-2) 
b = random.randint(1, p-2)  

A = pow(g, a, p)
B = pow(g, b, p)

s_A = pow(B, a, p)
s_B = pow(A, b, p)

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

# MD5
import hashlib
s = input("Enter string to be hashed: ").encode()
print(hashlib.md5(s).hexdigest())

# SHA512
import hashlib
s = input("Enter string to be hashed: ").encode()
print(hashlib.sha512(s).hexdigest())

# DSS

import secrets
import hashlib
import random
print("Pawan Mohit")
print("160123749301")
def inv_mod(a, m):
    
    return pow(a, -1, m)

def is_prime(n):
    
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(n ** 0.5)
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True

while True:
    q = random.randint(1000, 2000)
    if is_prime(q):
        for k in range(2, 3000):
            p = k * q + 1
            if is_prime(p):
                break
        if is_prime(p):
            break

h = 2
g = None
exp = (p - 1) // q
while h < p - 1:
    cand = pow(h, exp, p)
    if cand > 1:
        g = cand
        break
    h += 1

if g is None:
    raise SystemExit("No generator found. Try again.")

print("===== DIFFIE–HELLMAN KEY EXCHANGE =====")
print(f"Public prime (p)       = {p}")
print(f"Public prime (q)       = {q}")
print(f"Generator (g)          = {g}")

a = secrets.randbelow(q - 1) + 1
A = pow(g, a, p)

b = secrets.randbelow(q - 1) + 1
B = pow(g, b, p)

shared_key_A = pow(B, a, p)
shared_key_B = pow(A, b, p)

if shared_key_A != shared_key_B:
    raise SystemExit("Key exchange failed: shared keys do not match")

shared_secret = shared_key_A
print(f"Alice Private Key (a)  = {a}")
print(f"Bob Private Key (b)    = {b}")
print(f"Alice Public Key (A)   = {A}")
print(f"Bob Public Key (B)     = {B}")
print(f"Shared Secret Key      = {shared_secret}")

x = shared_secret % q
if x == 0:
    x = 2  

y = pow(g, x, p)

print("\n===== DSA KEY GENERATION =====")
print(f"Private Key (x) = {x}")
print(f"Public Key  (y) = {y}")


def dsa_sign(message_bytes):
    """Generate DSS signature using SHA-512."""
    H = int(hashlib.sha512(message_bytes).hexdigest(), 16)
    while True:
        k = secrets.randbelow(q - 1) + 1
        r = pow(g, k, p) % q
        if r == 0:
            continue
        try:
            k_inv = inv_mod(k, q)
        except ValueError:
            continue
        s = (k_inv * (H + x * r)) % q
        if s == 0:
            continue
        return (r, s, k, k_inv, H)

def dsa_verify(message_bytes, r, s):
    """Verify DSS signature using SHA-512."""
    if not (0 < r < q and 0 < s < q):
        return False
    H = int(hashlib.sha512(message_bytes).hexdigest(), 16)
    w = inv_mod(s, q)
    u1 = (H * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    return (v, v == r)


msg_input = input("\nEnter the message to sign: ").encode()

r, s, k, k_inv, H = dsa_sign(msg_input)

print("\n===== SIGNING PROCESS =====")
print(f"Message                = {msg_input.decode()}")
print(f"Message Hash (SHA-512) = 0x{H:x}")
print(f"Ephemeral Key (k)      = {k}")
print(f"Inverse of k (k^-1)    = {k_inv}")
print(f"Signature Component r  = {r}")
print(f"Signature Component s  = {s}")

v, valid = dsa_verify(msg_input, r, s)

print("\n===== VERIFICATION PROCESS =====")
print(f"Computed v             = {v}")
print(f"Expected r             = {r}")
print(f"Signature Valid        = {valid}")

