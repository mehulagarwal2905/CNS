def vigenere_cipher_e(text, key):
    n=len(text)
    m=len(key)
    c=""
    for i in range (n):
        j=i%m
        c+=chr((ord(text[i])+ord(key[j])-2*ord('A'))%26+ord('A'))
        
    return c

def vigenere_cipher_d(text, key):
    n=len(text)
    m=len(key)
    c=""
    for i in range (n):
        j=i%m
        c+=chr((ord(text[i])-ord(key[j])-2*ord('A'))%26+ord('A'))
        
    return c
print("Vigenere Cipher Encryption")
print("Name: Ch Pawan Mohit")        
print("Roll No: 160123749301")
text=input("Enter plain text here ")
key=input("Enter key here ")
ct=vigenere_cipher_e(text, key)
print("Cipher text is: ", ct)
print("Plain text is: ", vigenere_cipher_d(ct, key))