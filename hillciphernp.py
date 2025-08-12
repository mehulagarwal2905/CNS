import numpy as np

# Modular inverse of a number mod m
def mod_inv(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None  # No inverse exists

# Modular inverse of a matrix mod m
def matrix_mod_inv(matrix, modulus):
    det = int(round(np.linalg.det(matrix))) % modulus
    det_inv = mod_inv(det, modulus)
    if det_inv is None:
        raise ValueError(f"Matrix determinant has no inverse under modulo {modulus}")
    
    # Adjugate matrix
    matrix_adj = np.round(np.linalg.inv(matrix) * det).astype(int) % modulus
    return (det_inv * matrix_adj) % modulus

# Convert text to numbers A=0,...,Z=25
def text_to_numbers(text):
    return [ord(c) - 65 for c in text.upper() if c.isalpha()]

# Convert numbers back to text
def numbers_to_text(numbers):
    return ''.join(chr(num + 65) for num in numbers)

# Encryption
def encrypt(text, key):
    n = key.shape[0]  # Block size from matrix
    text = text.upper().replace(" ", "")

    # Padding dynamically
    while len(text) % n != 0:
        text += 'X'

    numbers = text_to_numbers(text)
    result = ""

    for i in range(0, len(numbers), n):
        block = np.array(numbers[i:i+n])
        enc = np.dot(key, block) % 26
        result += numbers_to_text(enc)

    return result

# Decryption
def decrypt(cipher, key):
    inv_key = matrix_mod_inv(key, 26)
    n = key.shape[0]
    numbers = text_to_numbers(cipher)
    result = ""

    for i in range(0, len(numbers), n):
        block = np.array(numbers[i:i+n])
        dec = np.dot(inv_key, block) % 26
        result += numbers_to_text(dec)

    return result.rstrip('X')  # Remove padding X's

# ===== Main Program =====
if __name__ == "__main__":
    size = int(input("Enter size of key matrix (n for n×n): "))

    print("Enter key matrix row-wise (letters only, e.g., ABC for 3×3):")
    key_elements = []
    for i in range(size):
        row_text = input(f"Row {i+1}: ").upper().replace(" ", "")
        row_nums = text_to_numbers(row_text)
        if len(row_nums) != size:
            raise ValueError(f"Each row must have exactly {size} letters.")
        key_elements.extend(row_nums)

    key_matrix = np.array(key_elements).reshape(size, size)

    plaintext = input("Enter plaintext: ").upper().replace(" ", "")

    cipher = encrypt(plaintext, key_matrix)
    decrypted = decrypt(cipher, key_matrix)

    print("\nKey Matrix (numeric form):\n", key_matrix)
    print("Encrypted :", cipher)
    print("Decrypted :", decrypted)
