def create_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    seen = set()

    for char in key:
        if char not in seen and char.isalpha():
            matrix.append(char)
            seen.add(char)

    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            matrix.append(char)

    rows = []
    for i in range(5):
        row = matrix[i*5 : (i+1)*5]  # take 5 letters
        rows.append(row)
    return rows

def find_position(matrix, letter):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col
    return None, None

def preprocess_text(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    processed = ""
    i = 0
    while i < len(text):
        a = text[i]
        if i+1 < len(text):
            b = text[i+1] 
        else:
            b = "X"
            
        if a == b:
            processed += a + "X"
            i += 1
        else:
            processed += a + b
            i += 2
    if len(processed) % 2 != 0:
        processed += "X"
    return processed

def playfair(plain_text, key, decrypt=False):
    if decrypt:
        hack = -1
        
    else:
        hack = 1
        
    matrix = create_matrix(key)
    text = preprocess_text(plain_text)
    cipher = ""

    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            cipher += matrix[r1][(c1 + hack) % 5]
            cipher += matrix[r2][(c2 + hack) % 5]
        elif c1 == c2:
            cipher += matrix[(r1 + hack) % 5][c1]
            cipher += matrix[(r2 + hack) % 5][c2]
        else:
            cipher += matrix[r1][c2]
            cipher += matrix[r2][c1]

    return cipher

# Example usage
print("Playfair Cipher Encryption")
print("Name: Ch Pawan Mohit")
print("Roll No: 160123749301")
key = input("Enter the key for Playfair cipher: ")

plaintext = input("Enter the plaintext to encrypt: ")
ciphertext = playfair(plaintext, key)
decrypted = playfair(ciphertext, key, decrypt=True)

print("Plaintext:", plaintext)
print("Encrypted:", ciphertext)
print("Decrypted:", decrypted)
