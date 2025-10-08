import numpy as np

# Simple 4x4 S-box for demo (input 4 bits → output 4 bits)
S_BOX = np.array([
    [0,1,2,3],
    [2,0,1,3],
    [3,0,1,2],
    [1,3,2,0]
])

def str_to_bin(s):
    b = ''.join(format(ord(c), '08b') for c in s)
    return np.array(list(b.ljust(8,'0')), dtype=int)  # tiny demo: 8 bits only

def bin_to_str(b):
    b_str = ''.join(str(x) for x in b)
    chars = [b_str[i:i+8] for i in range(0, len(b_str), 8)]
    result = ''
    for c in chars:
        if len(c) < 8:
            c = c.ljust(8,'0')  # pad to 8 bits
        result += chr(int(c,2))
    return result.rstrip('\x00')

def xor(a,b):
    return np.bitwise_xor(a,b)

def f_func(R, subkey):
    R = R[:4]
    subkey = subkey[:4]
    xor_bits = xor(R, subkey)
    row = int(f"{xor_bits[0]}{xor_bits[3]}",2)
    col = int(''.join(str(x) for x in xor_bits[1:3]),2)
    s_out = format(S_BOX[row,col], '04b')
    return np.array(list(s_out), dtype=int)

def des_round(L, R, subkey):
    f_out = f_func(R, subkey)
    new_L = R
    new_R = xor(L, f_out)
    return new_L, new_R

def des_encrypt(plaintext, key):
    plain_bin = str_to_bin(plaintext)
    key_bin   = str_to_bin(key)
    block = plain_bin[::-1]  # Initial Permutation (simplified)
    L, R = block[:4], block[4:8]
    subkey = key_bin[:4]
    L, R = des_round(L, R, subkey)
    cipher = np.concatenate([L,R])[::-1]  # Final Permutation (simplified)
    return cipher

def des_decrypt(cipher_bin, key):
    key_bin = str_to_bin(key)
    block = cipher_bin[::-1]  # inverse initial permutation
    L, R = block[:4], block[4:8]
    subkey = key_bin[:4]
    L, R = des_round(L, R, subkey)
    plain = np.concatenate([L,R])[::-1]
    return bin_to_str(plain)

# Example usage
plaintext = "H"
key = "K"

cipher_bin = des_encrypt(plaintext, key)
decrypted = des_decrypt(cipher_bin, key)

print("Plaintext:", plaintext)
print("Cipher (bin):", ''.join(map(str,cipher_bin)))
print("Decrypted:", decrypted)