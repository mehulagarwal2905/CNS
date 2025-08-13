def encrypt(s, t):
    t += 'X' * (-len(t) % s)
    return ''.join(t[i::s] for i in range(s))

def decrypt(s, c):
    r = len(c) // s
    return ''.join(c[j*r + i] for i in range(r) for j in range(s))

# Main
s = int(input("Block size: "))
t = input("Text: ")
c = encrypt(s, t)
print("Enc:", c)
print("Dec:", decrypt(s, c))
