# Background
In trying to solve the Down Under CTF challenge apbqii, I heard that the solution involved using what's known as an orthogonal lattice. Knowing very little about lattice cryptography, I decided this would be a good way to increase my understanding of the topic. I started off by reading [this](https://link.springer.com/content/pdf/10.1007/3-540-48405-1_3.pdf) paper by Ngyuen and Stern which first showcased this technique by implementing a solution to the Hidden Subset Sum Problem. In fact, the implementation details were already described, so why not I try implementing it? Boy was I in for a world of a pain!

# Subset Sum problems
The subset sum problem involves, from a set of given numbers, finding a subset of these numbers which add to some target number. There are several variations of this problem, such as by applying a modulus or considering multiple sums at the same time by using vectors, all of which turn out to be NP-hard (that is, there is no known polynomial time complexity algorithm for solving them).

One of these variations is the hidden subset sum problem. Essentially, we want to find a linear combination of *any* $n$ binary vectors which adds to some target vector. At first this problem seems easy because of how little we are restricted to choosing binary vectors and what integer coefficients to multiply them by.

However, the issue is quickly realised: unlike the subset sum problem, where we know the numbers that add to our target values are in some set, the binary vectors and their integer coefficients could be anything.

# Implementation headaches
The algorithm described in the paper makes use of a technique called the orthogonal lattice. The paper goes into in far more detail, rigour and polish than I do, but basically we want to 
