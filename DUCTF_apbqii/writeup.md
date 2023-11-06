# Challenge
https://github.com/DownUnderCTF/Challenges_2023_Public/tree/main/crypto/apbq-rsa-ii/src

# Solution
This challenge is a classic RSA setup with two undisclosed primes $p, q$, undisclosed private key $d$ and a secret flag $p$. The values $n = pq$, encryption key $e = 65537$ and ciphertext $c = p^e\bmod n$.
We're also given hints where, upon initialising three pairs of integers $(a_i, b_i)$ for $1 \le i \le 3$, we're told a list of values $c_i a_ip + b_iq\bmod n$. It seems our goal is to recover $p$ and $q$, or potentially calculate $\phi(n)$.
The previous challenge `apbq` upper bounded $a$ so that it was bruteforceable, from which every $a_2c_1 - a_1c_2$ could be checked if it shares a common factor with $n$ (which would be the prime $q$).
However, $a$ and $b$ are too large to bruteforce in this case ($312$ bits), however they are relatively small compared to the size of the primes ($1024$), which indicates that lattice cryptography might be useful.

It turns out the previous construction is helpful: $a_ic_j - a_jc_i = (a_ib_j - b_ia_j)q$ will be a multiple of $q$. Then, we can multiply $p$ to obtain $a_ipc_j - a_jpc_i \equiv 0\bmod n$. This is important as $a_ip$ and $a_jp$ are the smallest coefficients for a linear combination of $c_j$ and $-c_i$ to be a multiple of $n$, as neither are multiples of $n$ and must therefore have only one pair of such coefficients which are both positive and less than $n$.

So, if we can coerce these small coefficients to appear in order to make a linear combination of these be $0$, we can obtain $a_ip$ and calculate $\gcd(a_ip, n)$ quickly. We do this by applying LLL to the following matrix:
$$\begin{pmatrix}Bc_2&-Bc_1&0&1&0&0\\0&Bc_3&-Bc_2&0&1&0\\-Bc_3&0&Bc_1&0&0&1\\Bn&0&0&0&0&0\\0&Bn&0&0&0&0\\0&0&Bn&0&0&0\end{pmatrix}$$

Note that $B$ is chosen to be sufficiently large so that the LLL algorithm prioritises creating small vectors by mitigating the impact of $B$, which is best done by making linear combinations of $c_i$ and $-c_j$ equal to $0$. The bottom left entries allow us to subtract multiples of $3$ to simulate applying in modulus $3$. Finally, the top-right entries ensure that the coefficients themselves are small.
