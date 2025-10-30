import json
import socket
import secrets
from math import isqrt

# --- Primality test ---
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, isqrt(n)+1):
        if n % i == 0:
            return False
    return True

# --- Generate small random prime (for demo) ---
def generate_small_prime(limit=200):
    primes = [n for n in range(2, limit) if is_prime(n)]
    return secrets.choice(primes)

# --- Find primitive roots ---
def find_primitive_roots(p):
    phi = p - 1
    factors = set()
    n = phi
    i = 2
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        factors.add(n)

    roots = []
    for g in range(2, p):
        if all(pow(g, phi // f, p) != 1 for f in factors):
            roots.append(g)
    return roots

# --- Simple JSON send/recv helpers ---
def send_json(sock, obj):
    data = (json.dumps(obj) + "\n").encode()
    sock.sendall(data)

def recv_json(sock):
    buf = b""
    while b"\n" not in buf:
        chunk = sock.recv(4096)
        if not chunk:
            raise ConnectionError("Connection closed")
        buf += chunk
    line, _, _ = buf.partition(b"\n")
    return json.loads(line.decode())

# --- Main server ---
def main():
    HOST = "0.0.0.0"   # listen on all interfaces
    PORT = 5000

    # Diffie-Hellman setup
    p = generate_small_prime(limit=200)
    roots = find_primitive_roots(p)
    g = secrets.choice(roots)
    a = secrets.randbelow(p - 2) + 1   # Alice's private key
    A = pow(g, a, p)                   # Alice's public key

    print(f"[server] Prime p={p}, generator g={g}")
    print(f"[server] Private a={a}, Public A={A}")

    # --- Create server socket manually (Windows-friendly) ---
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[server] Listening on {HOST}:{PORT} …")

        conn, addr = server.accept()
        with conn:
            print(f"[server] Connected by {addr}")

            # Send p, g, A to client
            send_json(conn, {"p": p, "g": g, "A": A})

            # Receive B from client
            msg = recv_json(conn)
            B = msg["B"]
            print(f"[server] Received B={B}")

            # Compute shared secret
            s = pow(B, a, p)
            print(f"[server] Shared secret s={s}")

            # (optional) send confirmation back
            send_json(conn, {"ok": True})
            print("[server] Done.")

if __name__ == "__main__":
    print("Name: Pawan Mohit")
    print("Roll No.: 160123749301")

    main()
