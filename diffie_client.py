import json
import socket
import secrets

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
    line, _, rest = buf.partition(b"\n")
    return json.loads(line.decode())

def main():
    # Set this to the SERVER PC's IP address on your LAN
    HOST = "10.21.168.228"  # <-- change to server's IP
    PORT = 5000

    with socket.create_connection((HOST, PORT)) as sock:
        print(f"[client] Connected to {HOST}:{PORT}")

        # Receive p, g, A from server
        msg = recv_json(sock)
        p = msg["p"]; g = msg["g"]; A = msg["A"]
        print(f"[client] Received p={p}, g={g}, A={A}")

        # Choose private b, compute B
        b = secrets.randbelow(p - 2) + 1
        B = pow(g, b, p)
        print(f"[client] Using b={b}, B={B}")

        # Send B back
        send_json(sock, {"B": B})

        # Compute shared secret
        s = pow(A, b, p)
        print(f"[client] Shared secret s={s}")

        # (Optional) Receive confirmation
        _ = recv_json(sock)
        print("[client] Done")

if __name__ == "__main__":
    main()