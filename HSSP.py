# impl of hssp algo described in ngyugen stern paper
# suuuuuuuuuuuuuuuuuuuuuuuuuuper unreliable for large NUM, gotta increase BOUND, K and (maybe) LENGTH by a lot, and even then it still sucks
# apparently their program took 15 minutes which is wild
# so idk what the best way to do this is
# oh also they had modulus stuff so maybe that helps? but i feel like that would make stuff less reliable idk
from random import randint

BOUND = 100
K = 10000
LENGTH = 30
NUM = 3
vecs = [vector([randint(0, 1) for _ in range(LENGTH)]) for _ in range(NUM)]
a_vals = [randint(1, BOUND) for _ in range(NUM)]
h = sum([vecs[i] * a_vals[i]*K for i in range(NUM)])
A = Matrix(QQ,LENGTH,1,h).augment(Matrix.identity(LENGTH)).LLL()[:-1,1:]
A = A[:LENGTH - NUM, :].transpose()
results = A.augment(Matrix.identity(LENGTH)).augment(zero_vector(LENGTH)).stack(vector([0 for _ in range(LENGTH-NUM)] + [1/2 for _ in range(LENGTH)] + [1/2])).LLL()
ans = []
for row in results.rows():
    if not any(row[:LENGTH - NUM]) and list(row[:-1]).count(1/2) != LENGTH and list(row[:-1]).count(-1/2) != LENGTH:
        if row[-1] == -1/2:
            ans.append(row[-LENGTH-1:-1] + vector([1/2 for _ in range(LENGTH)]))
        elif row[-1] == 1/2:
            ans.append(vector([1/2 for _ in range(LENGTH)]) - row[-LENGTH-1:-1])

print("GUESS:")
for a in sorted(ans):
    print(a)
print("ACTUAL")
for a in sorted(vecs):
    print(a)
if len(ans) != len(vecs):
    print("can't find a_vals :(")
else:
    print(sorted(list(Matrix(QQ, ans).transpose().solve_right(h / K))))
    print(sorted(a_vals))
