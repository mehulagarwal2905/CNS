def encrypt(text,s):
    result = ""

    # traverse text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)

        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)

    return result

#check the above function
text = input("Enter text to encrypt: ")
s = 3
encrypted_text = encrypt(text, s)
print (" Given text  : " + text)
print ("Shift is 3 as it is the default value for Caesar Cipher")
print ("Cipher: " + encrypted_text)

print ("Decoded: " + encrypt(encrypted_text,-s))
