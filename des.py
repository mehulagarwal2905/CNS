# Complete DES in Python (64-bit block, 16 rounds)

# --- Tables ---
IP = [58,50,42,34,26,18,10,2,
      60,52,44,36,28,20,12,4,
      62,54,46,38,30,22,14,6,
      64,56,48,40,32,24,16,8,
      57,49,41,33,25,17,9,1,
      59,51,43,35,27,19,11,3,
      61,53,45,37,29,21,13,5,
      63,55,47,39,31,23,15,7]

FP = [40,8,48,16,56,24,64,32,
      39,7,47,15,55,23,63,31,
      38,6,46,14,54,22,62,30,
      37,5,45,13,53,21,61,29,
      36,4,44,12,52,20,60,28,
      35,3,43,11,51,19,59,27,
      34,2,42,10,50,18,58,26,
      33,1,41,9,49,17,57,25]

E = [32,1,2,3,4,5,
     4,5,6,7,8,9,
     8,9,10,11,12,13,
     12,13,14,15,16,17,
     16,17,18,19,20,21,
     20,21,22,23,24,25,
     24,25,26,27,28,29,
     28,29,30,31,32,1]

P = [16,7,20,21,29,12,28,17,
     1,15,23,26,5,18,31,10,
     2,8,24,14,32,27,3,9,
     19,13,30,6,22,11,4,25]

PC1 = [57,49,41,33,25,17,9,
       1,58,50,42,34,26,18,
       10,2,59,51,43,35,27,
       19,11,3,60,52,44,36,
       63,55,47,39,31,23,15,
       7,62,54,46,38,30,22,
       14,6,61,53,45,37,29,
       21,13,5,28,20,12,4]

PC2 = [14,17,11,24,1,5,
       3,28,15,6,21,10,
       23,19,12,4,26,8,
       16,7,27,20,13,2,
       41,52,31,37,47,55,
       30,40,51,45,33,48,
       44,49,39,56,34,53,
       46,42,50,36,29,32]

SHIFT = [1, 1, 2, 2, 2, 2, 2, 2,
         1, 2, 2, 2, 2, 2, 2, 1]

# --- All 8 S-Boxes ---
S_BOX = [
    # S1
    [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
     [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
     [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
     [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
    # S2
    [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
     [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
     [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
     [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
    # S3
    [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
     [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
     [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
     [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
    # S4
    [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
     [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
     [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
     [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
    # S5
    [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
     [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
     [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
     [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
    # S6
    [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
     [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
     [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
     [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
    # S7
    [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
     [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
     [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
     [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
    # S8
    [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
     [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
     [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
     [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]

# --- Helper functions ---
def permute(block, table):
    return [block[x-1] for x in table]

def shift_left(block, n):
    return block[n:] + block[:n]

def xor(a, b):
    return [i^j for i,j in zip(a,b)]

def sbox_substitute(bits):
    output = []
    for i in range(8):
        row = (bits[i*6]<<1) + bits[i*6+5]
        col = (bits[i*6+1]<<3) + (bits[i*6+2]<<2) + (bits[i*6+3]<<1) + bits[i*6+4]
        val = S_BOX[i][row][col]
        output += [(val>>3)&1, (val>>2)&1, (val>>1)&1, val&1]
    return output

def key_schedule(key):
    key = permute(key, PC1)
    C, D = key[:28], key[28:]
    round_keys = []
    for shift in SHIFT:
        C = shift_left(C, shift)
        D = shift_left(D, shift)
        round_keys.append(permute(C+D, PC2))
    return round_keys

def feistel(R, K):
    expanded = permute(R, E)
    temp = xor(expanded, K)
    substituted = sbox_substitute(temp)
    return permute(substituted, P)

def des_encrypt(block, key):
    block = permute(block, IP)
    L, R = block[:32], block[32:]
    keys = key_schedule(key)
    for i in range(16):
        temp = R
        R = xor(L, feistel(R, keys[i]))
        L = temp
        # Format as 32-bit string for readability
        L_str = ''.join(map(str, L))
        R_str = ''.join(map(str, R))
        print(f"Round {i+1}: L={L_str} R={R_str}")
    block = permute(R+L, FP)
    return block


# --- Decryption ---
def des_decrypt(block, key):
    block = permute(block, IP)
    L, R = block[:32], block[32:]
    keys = key_schedule(key)
    for i in range(16):
        temp = R
        R = xor(L, feistel(R, keys[15-i]))
        L = temp
        L_str = ''.join(map(str, L))
        R_str = ''.join(map(str, R))
        print(f"Decrypt Round {i+1}: L={L_str} R={R_str}")
    block = permute(R+L, FP)
    return block


# --- Example usage with dynamic input ---
# Details 
print("Name: Pawan Mohit")
print("Roll No: 160123749301")

# Input as hexadecimal strings
plaintext_hex = input("Enter 16-digit plaintext in hex (e.g., 0123456789ABCDEF): ")
key_hex = input("Enter 16-digit key in hex (e.g., 0123456789ABCDEF): ")


# Convert hex to 64-bit binary list
plaintext = [int(x) for x in '{:064b}'.format(int(plaintext_hex, 16))]
key = [int(x) for x in '{:064b}'.format(int(key_hex, 16))]

# Encrypt
cipher = des_encrypt(plaintext, key)

# Convert final cipher list to hex
cipher_hex = hex(int(''.join(map(str, cipher)), 2))[2:].upper()
print("Ciphertext:", cipher_hex)

decrypted = des_decrypt(cipher, key)
decrypted_hex = hex(int(''.join(map(str, decrypted)), 2))[2:].upper()
print("Decrypted Plaintext:", decrypted_hex)


