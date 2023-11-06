from hashlib import md5
from math import log2

p = 3902360539587438503887804112898372526804375385242810819130471125832797798664211473
# for convenience im just going to include this function to simulate
# interacting with the server
# note solve script doesn't know FLAG or secret (only len(FLAG)) 
def get_number(seed):
    FLAG = "MYFLAG{really_cool_flag_i_think}"
    secret = int.from_bytes(FLAG.encode(), "big")
    h = int(md5(seed.encode()).hexdigest(), 16)
    return (h * secret % p) >> int(log2(secret) // 4)

# 32-byte secret becomes 32 * 8 bit number, so this represents upper bound of lower quarter of bits
# note we subtract one from the exponent because it just so happens log2(secret) is one less than 32 * 8
# this can be educatively guessed for as all capital ASCII characters have a MSB of 0, which the flag prefix probably is
B = 1<<((32 * 8 // 4) - 1)
obs = []
hs = []
for i in range(33): # 33 observations seems optimal after calculating 
    obs.append(get_number(str(i)))
    hs.append(int(md5(str(i).encode()).hexdigest(), 16))

a = Matrix.identity(QQ, len(obs)) * p
a = a.stack(vector(hs))
a = a.stack(vector(obs) * B)
a = a.augment(vector([0 for _ in range(33)] + [B] + [0]) / p)
a = a.augment(vector([0 for _ in range(34)] + [B]))
L = a.LLL()
second_smallest = L.rows()[1]
if second_smallest[-1] == B:
    answer = int(-second_smallest[-2] * p / B)
elif second_smallest[-1] == -B:
    answer = int(second_smallest[-2] * p / B)
else:
    answer = int.from_bytes(b"rip exploit failed dunno why :((", "big")

print(answer.to_bytes(32, "big"))
