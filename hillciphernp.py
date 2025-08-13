import numpy as np

def mod_inv(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def matrix_mod_inv(matrix, modulus):
    det_full = int(round(np.linalg.det(matrix)))   # use full integer det
    det_mod = det_full % modulus                   # reduce only for mod inverse
    det_inv = mod_inv(det_mod, modulus)
    matrix_adj = np.round(np.linalg.inv(matrix) * det_full).astype(int) % modulus
    return (det_inv * matrix_adj) % modulus

def text_to_numbers(text):
    return [ord(c) - 65 for c in text]

def numbers_to_text(numbers):
    return ''.join(chr(num + 65) for num in numbers)

def encrypt(text, key):
    n = key.shape[0]
    while len(text) % n != 0:
        text += 'X'
    nums = text_to_numbers(text)
    out = ""
    for i in range(0, len(nums), n):
        block = np.array(nums[i:i+n])
        enc = np.dot(key, block) % 26
        out += numbers_to_text(enc)
    return out

def decrypt(cipher, key):
    inv_key = matrix_mod_inv(key, 26)
    n = key.shape[0]
    nums = text_to_numbers(cipher)
    out = ""
    for i in range(0, len(nums), n):
        block = np.array(nums[i:i+n])
        dec = np.dot(inv_key, block) % 26
        out += numbers_to_text(dec)
    return out

# ---- main ----
size = int(input("Enter size of key matrix (n for n×n): "))
print("Enter key matrix row-wise (letters only, e.g., ABC for 3×3):")
key_elements = []
for i in range(size):
    row = input().strip()
    key_elements.extend(text_to_numbers(row))
key_matrix = np.array(key_elements).reshape(size, size)

plaintext = input("Enter plaintext: ")

cipher = encrypt(plaintext, key_matrix)
decrypted = decrypt(cipher, key_matrix)

print("\nKey Matrix (numeric):")
print("Hill Cipher")
print("Name: Mehul Agarwal")
print("Roll No: 160123749047")
print(key_matrix)
print("Encrypted :", cipher)
print("Decrypted :", decrypted)
