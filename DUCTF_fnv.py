m = 16 # experiment with
K = 0x00000100000001b3
n = 0xffffffffffffffff + 1
TARGET = 0x1337133713371337
h = 0xcbf29ce484222325
A = Matrix(QQ, nrows=m+2, ncols=m+2)
for i in range(m):
    A[i, 0] = pow(K, i, n) << 100
    A[i, i+1] = 1
A[m, 0] = n << 100
A[m+1, 0] = ((TARGET - pow(K, m, n) * h) % n) << 100
A[m+1,m+1] = 2^200
vals = A.LLL().rows()[-1][1:-1] * -1
s = 0
for i in range(len(vals)):
    s += pow(K, i, n) * vals[i]


print(hex((s + pow(K, m, n)*h) % n))
ans = b""
for val in vals:
    ans += bytes([int(TARGET) ^^ (int(TARGET - val))])
    TARGET -= val
    
    TARGET *= pow(K, -1, n)
    TARGET %= n
print(hex(TARGET))
print(ans)
