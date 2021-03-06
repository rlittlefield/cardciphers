import random
import string

def _pad_message(message):
    """ A PKCS#7 padding implementation for the end of the plaintext message.

    Args:
        message (str): The full plaintext message.

    Returns:
        str: A PKCS#7 padded message.

    """

    pad = len(message) % 5
    if pad is 0:
        message += 'ZZZZZ'
    elif pad is 1:
        message += 'YYYY'
    elif pad is 2:
        message += 'XXX'
    elif pad is 3:
        message += 'WW'
    else:
        message += 'V'
    return message

def _unpad_message(message):
    """ Remove the padding off a decrypted ciphertext message.

    Args:
        message (str): The full decrypted ciphertext message.

    Returns:
        str: The decrypted message without PKCS#7 padding.

    """

    pad = message[-1:]
    if 'V' in pad:
        message = message[:-1]
    elif 'W' in pad:
        message = message[:-2]
    elif 'X' in pad:
        message = message[:-3]
    elif 'Y' in pad:
        message = message[:-4]
    elif 'Z' in pad:
        message = message[:-5]
    return message

def _create_iv(n):
    """ Create a random initialization vector.

    Prepend a plaintext message with 5 random characters in the same ciphertext
    character base as the rest of the ciphertext.

    Args:
        n (int): The number of random characters to generate.

    Returns:
        str: An initialization vector string.

    """

    r = random.SystemRandom()
    return "".join(r.choice(string.uppercase) for i in xrange(n))

def encrypt(message, alg, deck, n):
    """ Encrypt a plaintext message.

    Args:
        message (str): The plaintext message.
        alg (object): The specific cipher object.
        deck (list): A full 52-card deck. State is maintained.
        n (int): The number of initialization vector characters.

    Returns:
        str: An encrypted message prepended with an initialization vector.

    """

    ct = []
    iv = _create_iv(n)

    for char in message:
        if not char in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            message = message.replace(char, '')

    # mixing the deck with the IV (uses the right alphabet/pile)
    for char in iv:
        alg.prng(deck, char)

    msg = iv + message
    message = _pad_message(msg)
    message = message[n:] # strip iv for encryption

    # encrypt the plaintext message sans IV
    for char in message:
        ct.append(alg.prng(deck, char))

    return list(iv) + ct

def decrypt(message, alg, deck, n):
    """ Decrypt a ciphertext message.

    Args:
        message (str): The ciphertext message.
        alg (object): The specific cipher object.
        deck (list): A full 52-card deck. State is maintained.
        n (int): The number of characters of the initialization vector.

    Returns:
        str: An decrypted message without the initialization vector.

    """
    pt = []
    iv = message[:n]
    message = message[n:]

    # mixing the deck with the IV (uses the right alphabet/pile)
    for char in iv:
        alg.prng(deck, char)

    # decrypt the ciphertext message sans IV
    for char in message:
        pt.append(alg.prng(deck, char, method='decrypt'))

    return _unpad_message(pt)
