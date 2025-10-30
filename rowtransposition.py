# Row Transposition Cipher
print("Name: Pawan Mohit")
print("Roll No.: 160123749301")

# Encryption
plaintext = input("Enter plaintext: ").replace(" ", "").upper()
key = input("Enter key (e.g., 3142): ")

# Convert key to list of integers
key_order = [int(x) for x in key]

cols = len(key_order)
rows = -(-len(plaintext) // cols)  # ceiling division

# Pad plaintext with 'X' if needed
plaintext += "X" * (rows * cols - len(plaintext))

# Create matrix row-wise
matrix = []
index = 0
for _ in range(rows):
    row = []
    for _ in range(cols):
        row.append(plaintext[index])
        index += 1
    matrix.append(row)

# Encrypt: read columns based on key order
cipher = ""
for num in sorted(key_order):
    col_index = key_order.index(num)
    for r in range(rows):
        cipher += matrix[r][col_index]

# Decryption
# Create empty matrix
dec_matrix = [[''] * cols for _ in range(rows)]
index = 0
for num in sorted(key_order):
    col_index = key_order.index(num)
    for r in range(rows):
        dec_matrix[r][col_index] = cipher[index]
        index += 1

# Read row-wise for plaintext
decrypted = ''.join(''.join(row) for row in dec_matrix)

print("Pawan Mohit 160123749301")
print("Encrypted text:", cipher)
print("Decrypted text:", decrypted)