def encrypt(key, password):
    encrypted = []

    for letter in password:
        encrypted.append(ord(letter) * key)

    for i in range(len(encrypted) - 1):
        encrypted[i] = (encrypted[i] + encrypted[i + 1]) / 2

    encrypted[-1] = encrypted[-1]

    return ','.join(str(x) for x in encrypted)


def decrypt(key, encrypted):
    decrypted = list(encrypted.split(','))

    password = ''

    for i in range(len(decrypted)):
        decrypted[i] = float(decrypted[i])

    for i in range(len(decrypted) - 1):
        decrypted[len(decrypted) - 2 - i] = decrypted[len(decrypted) - 2 - i] * 2 - decrypted[len(decrypted) - 1 - i]
    
    for i in range(len(decrypted)):
        decrypted[i] = int(decrypted[i] / key)
        password += (chr(decrypted[i]))

    return password
