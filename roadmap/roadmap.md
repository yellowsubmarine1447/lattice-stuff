# Background
I'm pretty familiar with RSA, modular arithmetic and linear algebra from passion-studying maths as well as CTF challenges featuring these concepts. My first exposure to lattice cryptography was NOT actually through CTF's, it was from a series of videos by [Matthew Bolan](https://www.youtube.com/watch?v=mc9w2iD3Gzs) on using lattices to reverse engineer Minecraft seeds.

I sort of understood what he was talking about at the time, but didn't fully digest what he was saying. Some time later, one of my friends gave a talk introducing lattice cryptography at the UNSW SCONES conference, and I also saw some Down Under CTF challenges about it. With all this talk, I decided it's high time to learn!

# Learning
I started off by reading Joseph Surin's tutorial introducing lattice cryptography and some common problems its used for. There's some interesting maths here that's easy to get lost in, such as Minkowski's theorem, which has some cool visual geometric intuition and proofs related to it. I recommend watching [this video](https://www.youtube.com/watch?v=RquUIXUMLcc) which was submitted as part of SoME2 by Euler's Basement.

A useful tool that forms the basis for estimating the success rate of your lattice in successfully reducing and finding small vectors is Minkowski's first theorem, where the smallest vector $\lambda_1(\mathcal L)$ is upper bounded by:
```math
\sqrt n|\det(\mathcal L)|^{\frac1n}
```
There's another more complicated formula for doing this, but this one is pretty good for quickly checking if your lattice will be successful. Joseph's tutorial also goes into various other problems, such as the Hidden Number Problem and the Subset Sum Problem. There's one problem that lattice reduction is slightly less useful for but helped me in understanding it.

# GCD of numbers
Essentially, lattice reduction is a way of generating small integers which satisfy some equation, or is *close* to some value (in which case we have more small numbers that we don't care about). It's an algorithm that takes in a matrix, whose rows are lattice basis vectors, and finds an almost orthogonal basis of lattice vectors, which tends to also have the small vectors that we care about. This is the first example I implemented to try and understand this technique:
```python
numbers = [12912193, 51292191, 51821491, 2338212, 12193589, 232994, 322134813, 3901024914, 11238, 249]
n = len(numbers)
a = Matrix(QQ, n, n + 1)

S = 100000000000000000000
for i, k in enumerate(numbers):
    a[i, 0] = k * S
for i in range(n):
    a[i, i + 1] = 1
reduced_a = a.LLL()
print(reduced_a)
print(f"GCD: {reduced_a.rows()[-1][0] // S}")
print(f"Our integer multiples: {reduced_a.rows()[-1][1:]}")
```
Essentially, we are generating a set of small integer coefficients which, when our given integers are taken in linear combination of, gives the smallest possible number it can. There's actually something subtle going on: if LLL generates the smallest vectors it can, why does this code work? Why is there a row in our LLL reduced matrix with the GCD of our number in the first column of the following diagram?
![Sage GCD example](gcd_example.PNG)

It turns out, the reason is because LLL must still generate a basis of vectors, so not all entries in the first column can be zero. This is actually a useful property, because if we multiply the numbers in some ecolumn by some very large bound, we can essentially punish multiple vectors giving numbers larger than the smallest possible non-zero number it can give in that column.

This is an important part of using the LLL algorithm in lattice reduction to solve problems that I haven't seen documented anywhere, though perhaps implicitly stated.

# Further learning and another technique
After this, I went on to learn about orthogonal lattices. I described this process in the HSSP writeup, but essentially this was in preparation for the Down Under CTF apbqii challenge. This took a long time to writeup, and another cool technique that I learnt from this was positive integer coercion.

Basically, if you simulate moduli in your lattice by stacking the identity multiplied by some value $N$, its likely that values larger than $\frac N2$ become negative, since when $N$ is subtracted from the positive component they are closer in magnitude to zero. So, if you have a CVP problem, you can add/subtract $\frac N2$ to your target vector: that way, the closest offset vector will be measured as the closest to $\frac N2$.

Most of what I did next was implementing solutions to CTF problems. I implemented the solution to fnv, experimented with an implementation of the hidden number problem and also played around with the low-density subset sum problem. This helped solidify what I learnt, but I think the biggest learning experience was solving the LCG Card Gimmicks Down Under CTF challenge. It pretty much reinforced the two tricks I talked about before with forcing positive integers to appear and punishing large values.

# Reflection
If I was to give feedback to my past self on how to approach this topic, I would tell myself have the patience to learn. A lot of the time I found myself jumping the gun and going straight into implementing without thinking it through. Then, I'd make a mistake, get annoyed, crash and burn and give up and move on to something else. I wish I'd taken more time to debug when things went wrong and verify that each step I took was right and made sense. Though it would've seemed slow at the time, I think I would've appreciated what I was learning a lot more.
