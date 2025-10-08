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
    cipher_nums = [pow(ord(char), e, n) for char in message]
    cipher_bytes = ' '.join(map(str, cipher_nums)).encode()
    return base64.b64encode(cipher_bytes).decode()

def decrypt(encrypted_text, d, n):
    decoded = base64.b64decode(encrypted_text).decode()
    nums = [int(x) for x in decoded.split()]
    return ''.join(chr(pow(x, d, n)) for x in nums)

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
    print(f"φ(n) = {phi}")
    print(f"d = {d}")
    encrypted_msg = encrypt(message, e, n)
    print("\nEncrypted Message:", encrypted_msg)
    decrypted_msg = decrypt(encrypted_msg, d, n)
    print("Decrypted Message:", decrypted_msg)