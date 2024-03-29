import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for character in plaintext:
        if character.isupper():
            c_index = ord(character) - ord("A")
            new_index = (c_index + shift) % 26
            new_unicode = new_index + ord("A")
            new_character = chr(new_unicode)
            ciphertext += new_character
        elif character.islower():
            c_unicode = ord(character)
            c_index = ord(character) - ord("a")
            new_index = (c_index + shift) % 26
            new_unicode = new_index + ord("a")
            new_character = chr(new_unicode)
            ciphertext += new_character
        elif character.isdigit():
            c_new = int(character)
            ciphertext += str(c_new)
        else:
            ciphertext += character
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for character in ciphertext:
        if character.isupper():
            c_index = ord(character) - ord("A")
            new_index = (c_index - shift) % 26
            new_unicode = new_index + ord("A")
            new_character = chr(new_unicode)
            plaintext += new_character

        elif character.islower():
            c_unicode = ord(character)
            c_index = ord(character) - ord("a")
            new_index = (c_index - shift) % 26
            new_unicode = new_index + ord("a")
            new_character = chr(new_unicode)
            plaintext += new_character
        elif character.isdigit():
            c_new = int(character)
            plaintext += str(c_new)
        else:
            plaintext += character
    return plaintext
