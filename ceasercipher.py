def encrypt(text,s):
    result = ""

    # traverse text
    for char in text:
            
            # Encrypt uppercase characters
            if (char.isupper()):
                result += chr((ord(char) + s- ord("A")) % 26 + ord("A"))

            # Encrypt lowercase characters
            else:
                result += chr((ord(char) + s - ord("a")) % 26 + ord("a"))

    return result

#check the above function
print("Caesar Cipher Encryption")
print("Name: Pawan Mohit")
print("Roll No.: 160123749301")

text = input("Enter text to encrypt: ")
s = 3
encrypted_text = encrypt(text, s)
print("Pawan Mohit 160123749301")
print (" Given text  : " + text)
print ("Shift is 3 as it is the default key for Caesar Cipher")
print ("Cipher: " + encrypted_text)

print ("Decoded: " + encrypt(encrypt(text,s),-s))
