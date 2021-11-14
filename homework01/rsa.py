import random
import typing as tp


def is_prime(n: int) -> bool:
    """
    Tests to see if a number is prime.
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    k = 0
    for i in range(1, round(n ** (1 / 2)) + 1):
        if n % i == 0:
            k += 1
    if n == 2:
        n = bool(True)
    elif n == 1:
        n = bool(False)
    else:
        if k > 1:
            n = bool(False)
        else:
            n = bool(True)
    return n


def gcd(a: int, b: int) -> int:
    """
    Euclid's algorithm for determining the greatest common divisor.
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    c = min(a, b)
    m = 1
    for i in range(1, c + 1):
        if a % i == 0 and b % i == 0:
            if i > m:
                m = i
    if a == 0 or b == 0:
        m = max(a, b)
    if a == 0 and b == 0:
        m = 0
    return m


def multiplicative_inverse(e: int, phi: int) -> int:
    """
    Euclid's extended algorithm for finding the multiplicative
    inverse of two numbers.
    >>> multiplicative_inverse(7, 40)
    23
    """
    delen: list = []
    phi1 = phi
    delen.insert(0, phi // e)
    while phi % e != 0:
        c = phi % e
        phi = e
        e = c
        delen.insert(0, phi // e)
    x = 0
    y = 1
    for i in range(1, len(delen)):
        x1 = y
        y = x - x1 * delen[i]
        x = x1
    return y % phi1


def generate_keypair(p: int, q: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal")

    # n = pq
    n = p * q

    # phi = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher
