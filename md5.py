import struct

def left_rotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

# --- Simple MD5 implementation ---
def md5(message):
    # Constants
    s = [7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
         5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
         4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
         6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21]
    K = [int(abs(__import__('math').sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

    # Initial hash values
    a0 = 0x67452301
    b0 = 0xEFCDAB89
    c0 = 0x98BADCFE
    d0 = 0x10325476

    # Pre-processing
    msg_bytes = bytearray(message, 'utf-8')
    orig_len_bits = (8 * len(msg_bytes)) & 0xFFFFFFFFFFFFFFFF
    msg_bytes.append(0x80)
    while (len(msg_bytes) % 64) != 56:
        msg_bytes.append(0)
    msg_bytes += struct.pack('<Q', orig_len_bits)

    # Process each 512-bit chunk
    for offset in range(0, len(msg_bytes), 64):
        chunk = msg_bytes[offset:offset+64]
        M = list(struct.unpack('<16I', chunk))
        A, B, C, D = a0, b0, c0, d0

        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | (~B & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | (~D & C)
                g = (5*i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3*i + 5) % 16
            else:
                F = C ^ (B | ~D)
                g = (7*i) % 16
            F = (F + A + K[i] + M[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + left_rotate(F, s[i])) & 0xFFFFFFFF

        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF

    # Output
    return ''.join(f'{x:02x}' for x in struct.pack('<4I', a0, b0, c0, d0))

print("Pawan Mohit")
print("160123749301")
text = input("Enter text here: ")
print("MD5 Hash:", md5(text))