# Create the 5x5 matrix for Playfair cipher
def create_matrix(key):
    key = key.upper().replace("J", "I").replace(" ", "")  # replace 'J' with 'I' and remove spaces
    matrix = []
    seen = set()

    for char in key:
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)

    # Add the remaining letters of the alphabet to the matrix
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            seen.add(char)
            matrix.append(char)

    return [matrix[i:i + 5] for i in range(0, len(matrix), 5)]  # Create 5x5 grid


# Helper function to find coordinates of a letter in the matrix
def find_position(letter, matrix):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == letter:
                return i, j


# Encrypt a digraph (pair of letters)
def encrypt_digraph(digraph, matrix):
    row1, col1 = find_position(digraph[0], matrix)
    row2, col2 = find_position(digraph[1], matrix)

    if row1 == row2:  # Same row
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:  # Same column
        return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
    else:  # Rectangle rule
        return matrix[row1][col2] + matrix[row2][col1]


# Decrypt a digraph
def decrypt_digraph(digraph, matrix):
    row1, col1 = find_position(digraph[0], matrix)
    row2, col2 = find_position(digraph[1], matrix)

    if row1 == row2:  # Same row
        return matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
    elif col1 == col2:  # Same column
        return matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
    else:  # Rectangle rule
        return matrix[row1][col2] + matrix[row2][col1]


# Main function to encrypt the message
def playfair_encrypt(plaintext, key):
    matrix = create_matrix(key)
    plaintext = plaintext.upper().replace("J", "I").replace(" ", "")

    # Create digraphs (pairs of letters)
    digraphs = []
    i = 0
    while i < len(plaintext):
        if i + 1 < len(plaintext) and plaintext[i] != plaintext[i + 1]:
            digraphs.append(plaintext[i] + plaintext[i + 1])
            i += 2
        else:
            digraphs.append(plaintext[i] + 'X')  # Pad with 'X' if same letter pair
            i += 1

    # Encrypt each digraph
    ciphertext = ''.join([encrypt_digraph(d, matrix) for d in digraphs])
    return ciphertext


# Main function to decrypt the message
def playfair_decrypt(ciphertext, key):
    matrix = create_matrix(key)
    ciphertext = ciphertext.upper().replace(" ", "")

    # Create digraphs (pairs of letters)
    digraphs = [ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2)]

    # Decrypt each digraph
    plaintext = ''.join([decrypt_digraph(d, matrix) for d in digraphs])
    return plaintext


# Example usage
key = "KEYWORD"
plaintext = "HELLO PLAYFAIR"
ciphertext = playfair_encrypt(plaintext, key)
print("Ciphertext:", ciphertext)

decrypted_text = playfair_decrypt(ciphertext, key)
print("Decrypted text:", decrypted_text)
