def letter_to_number(letter):
    return ord(letter.upper()) - ord('A')

def number_to_letter(number):
    return chr((number % 26) + ord('A'))

def get_key_matrix(n):
    print(f"Enter the {n}x{n} key matrix row by row (A-Z only):")
    matrix = []
    for i in range(n):
        row = input(f"Row {i+1}: ").upper().replace(" ", "")
        if len(row) != n:
            raise ValueError("Row must have exactly {} characters".format(n))
        matrix.append([letter_to_number(c) for c in row])
    return matrix

# Vector × Matrix multiplication (plaintext vector * key)
def vector_matrix_mul(vector, matrix, n):
    result = [0] * n
    for j in range(n):
        for i in range(n):
            result[j] += vector[i] * matrix[i][j]
        result[j] %= 26
    return result

def matrix_determinant(matrix, n):
    if n == 2:
        return (matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]) % 26
    elif n == 3:
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        det = (a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)) % 26
        return det

def mod_inverse(a, m=26):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    raise ValueError("Modular inverse does not exist.")

def cofactor_3x3(matrix):
    cof = []
    for i in range(3):
        cof_row = []
        for j in range(3):
            minor = [[matrix[x][y] for y in range(3) if y != j] 
                                  for x in range(3) if x != i]
            val = (minor[0][0]*minor[1][1] - minor[0][1]*minor[1][0])
            cof_row.append(((-1)**(i+j)) * val % 26)
        cof.append(cof_row)
    return cof

def matrix_inverse(matrix, n):
    det = matrix_determinant(matrix, n)
    inv_det = mod_inverse(det)

    if n == 2:
        inv = [
            [matrix[1][1], -matrix[0][1]],
            [-matrix[1][0], matrix[0][0]]
        ]
        return [[(inv[i][j] * inv_det) % 26 for j in range(2)] for i in range(2)]

    elif n == 3:
        cof = cofactor_3x3(matrix)
        adj = [[cof[j][i] for j in range(3)] for i in range(3)]  # Transpose
        return [[(adj[i][j] * inv_det) % 26 for j in range(3)] for i in range(3)]

def preprocess_text(text, n):
    text = text.upper().replace(" ", "")
    while len(text) % n != 0:
        text += 'X'
    return text

# Modified encryption using plaintext × key
def encrypt(plaintext, key_matrix, n):
    plaintext = preprocess_text(plaintext, n)
    ciphertext = ''
    for i in range(0, len(plaintext), n):
        vector = [letter_to_number(c) for c in plaintext[i:i+n]]
        result = vector_matrix_mul(vector, key_matrix, n)
        ciphertext += ''.join(number_to_letter(num) for num in result)
    return ciphertext

# Modified decryption using cipher × inverse_key
def decrypt(ciphertext, key_matrix, n):
    inverse_key = matrix_inverse(key_matrix, n)
    plaintext = ''
    for i in range(0, len(ciphertext), n):
        vector = [letter_to_number(c) for c in ciphertext[i:i+n]]
        result = vector_matrix_mul(vector, inverse_key, n)
        plaintext += ''.join(number_to_letter(num) for num in result)
    return plaintext

def main():
    print("Hill Cipher (Plaintext × Key Version)")
    n = int(input("Enter matrix size (2 or 3): "))
    if n not in [2, 3]:
        print("Only 2x2 or 3x3 supported.")
        return

    key_matrix = get_key_matrix(n)
    plaintext = input("Enter plaintext: ")

    ciphertext = encrypt(plaintext, key_matrix, n)
    print("Encrypted Text:", ciphertext)

    decrypted = decrypt(ciphertext, key_matrix, n)
    print("Decrypted Text:", decrypted)

if __name__ == "__main__":
    main()
