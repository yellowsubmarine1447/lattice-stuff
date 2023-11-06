from Crypto.Cipher import AES
from os import urandom

KEY = urandom(16)
#from secrets import KEY

def dec(ciphertext, iv):
    aes = AES.new(KEY, AES.MODE_CBC, iv)
    return aes.decrypt(ciphertext)

print("AES is probably insecure, so I've developed my own encryption system based on it!")
print("Unfortunately encrpytion is still in development :)")

while True:
    try:
        enc = bytes.fromhex(input("Enter your ciphertext: "))
        if len(enc) % 16 != 0:
            print("Ciphertext must be 16-byte blocks")
            continue

        iv, name = dec(enc[:16], b"\x00"*16), enc[16:]
        while name:
            iv, name = dec(name[:16], iv), name[16:]
        name = iv.rstrip()
        print(f"Hello {name}!")
        print("That's... quite the strange name")
        if name == "admin":
            print("MYFLAG{i_love_flags}")
    except:
        print("Please provide the ciphertext in hexadecimal format")
