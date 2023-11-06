from hashlib import md5
from math import log2

FLAG = "MYFLAG{really_cool_flag_i_think}"
#from secrets import FLAG

assert len(FLAG) == 32
secret = int.from_bytes(FLAG.encode(), "big")
p = 3902360539587438503887804112898372526804375385242810819130471125832797798664211473
print("Ok I think I've got this randomness thing solved. Give me a seed and I'll give you ONE number!")
while True:
    h = md5(input("Enter your seed: " ).encode()).hexdigest()
    print( (int(h, 16) * secret % p) >> int(log2(secret) // 2) )
