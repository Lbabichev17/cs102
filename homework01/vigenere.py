def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i, letters in enumerate(plaintext):
        shift = ord(keyword[i % len(keyword)])
        if ord("A") <= shift <= ord("Z"):
            shift -= ord("A")
        else:
            shift -= ord("a")
        if (
            ord("A") <= ord(letters) <= ord("Z") - shift
            or ord("a") <= ord(letters) <= ord("z") - shift
        ):
            ciphertext += chr(ord(letters) + shift)
        elif ord("Z") - shift < ord(letters) <= ord("Z") or ord("z") - shift <= ord(letters) <= ord(
            "z"
        ):
            ciphertext += chr(ord(letters) + shift - (ord("Z") - ord("A") + 1))
        else:
            ciphertext += letters
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for i, letters in enumerate(ciphertext):
        shift = ord(keyword[i % len(keyword)])
        if ord("A") <= shift <= ord("Z"):
            shift -= ord("A")
        else:
            shift -= ord("a")
        if ord("A") + shift <= ord(letters) <= ord("Z") or ord("a") + shift <= ord(letters) <= ord(
            "z"
        ):
            plaintext += chr(ord(letters) - shift)
        elif (
            ord("A") <= ord(letters) < ord("A") + shift
            or ord("a") <= ord(letters) < ord("a") + shift
        ):
            plaintext += chr(ord(letters) - shift + ord("Z") - ord("A") + 1)
        else:
            plaintext += letters
    return plaintext
