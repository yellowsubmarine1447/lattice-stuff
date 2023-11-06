# since challenge server is down, I'm basically simulating connecting to it and sending requests by calling functions and getting the relevant output

from sage.all import *
from secrets import randbelow
import signal


DECK = [f'{val}{suit}' for suit in 'CDHS' for val in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']] + ['RJ', 'BJ']
M = 2**64
nope = True


class LCG:
    def __init__(self, seed, A=None, C=None):
        self.M = M
        if A is None:
            self.A = randbelow(self.M) | 1
        else:
            self.A = A
        if C is None:
            self.C = randbelow(self.M)
        else:
            self.C = C
        self.seed = seed

    def __str__(self):
        o = f'A = {self.A}\n'
        o += f'C = {self.C}\n'
        o += f'M = {self.M}'
        return o

    def next(self):
        self.seed = (self.A * self.seed + self.C) % self.M
        return self.seed

    def between(self, lo, hi):
        r = self.next()
        return lo + (r >> 16) % (hi - lo)


def draw(rng, k):
    global nope
    hand = []
    print("[", end="")
    while len(hand) < k:
        r = rng.between(0, len(DECK))
        print(r, end=", ")
        card = DECK[r]
        if card in hand:
            nope = True
            continue
        hand.append(card)
    print("]")
    return hand


def main(seed=None):
    if seed is None:
        seed = randbelow(M)
    rng = LCG(seed)
    hand = draw(rng, 13)
    return seed, rng.A, rng.M, rng.C, [DECK.index(x) for x in hand]



# in the original program, the hand is a bunch of unique cards
# this means if the rng gets a number that already exists in the hand, it will continue to the next seed
# this is an issue for our matrix calculations as there's some uncertainty on what the seed value actually was in that case
# so, we keep getting seeds until one appears where all seeds generated unique hand values
# for the actual contest, this would correspond to running the program a bunch of times until it worked :D
if True:
    while nope:
        nope = False
        seed, A, M, C, hand = main()
    print(A, M, C, seed)

# there's still some unreliability because at the end of the day, LLL can only approximate the SVP
# it takes around 5 reruns until we get the seed right
# coupling this with the previous issue, in the actual contest, we'd have to make quite a few requests to the server to solve this chall
# lattice crypto moment
a = Matrix(QQ, 0, nrows=28, ncols=28)
for i in range(13):
    a[2*i, 2*i] = M>>48
    a[2*i, 2*i+1] = M
    a[2*i+1, 2*i+1] = 2**16*len(DECK)
    a[26, 2*i] = a[26, 2*i+1] = pow(A, i+1, M)
    a[26, 2*i] /= 2**48
    a[27, 2*i] = -2**63 + ((C * (A **(i+1) - 1) // (A - 1)) % M)
    a[27, 2*i] /= (2**48)
    a[27, 2*i+1] = -2**15-2**16 * hand[i] + ((C * (A **(i+1) - 1) // (A - 1)) % M)
a[26, 26] = 1/2**48
a[27, 27] = 1<<64
annoying_vec = vector([-2**16 * len(DECK) for _ in range(26)] + [0, 0]) / 2
#a = a.stack(annoying_vec)
#a = a.augment(vector([0 for _ in range(28)] + [1<<100]))
a_LLL = a.LLL()
sample_seed = a_LLL.rows()[-1][-2] * 2**48
print(f"Now for my guess: {sample_seed}")
draw(LCG(sample_seed, A=A, C=C), 13)
