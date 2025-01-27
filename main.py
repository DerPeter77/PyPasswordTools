import random
import json
import cryptography.fernet
import utils
from cryptography.fernet import Fernet
import cryptography

LOWER = 'abcdefghijklmnopqrstuvwxyz'
UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGITS = '0123456789'
PUNCTUATION = r"""!"#$%&'()*+,-.:;<=>?@^_`{|}~"""


def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("secret.key", "rb").read()


try:
    key = load_key()
    KEY = key
except FileNotFoundError:
    generate_key()


def encrypt_password(password: str, key: bytes) -> str:
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password.decode()


def decrypt_password(encrypted_password: str, key: bytes) -> str:
    f = Fernet(key)
    try:
        decrypted_password = f.decrypt(encrypted_password.encode())
        return decrypted_password.decode()
    except cryptography.fernet.InvalidToken:
        return "Invalid Token"


def generate_password(length: int, anzahl: int, chosen_characters: str):
    passwords = []
    characters = ""
    if "1" in chosen_characters:
        characters += LOWER + UPPER   # noqa
    if "2" in chosen_characters:
        characters += DIGITS
    if "3" in chosen_characters:
        characters += PUNCTUATION

    for i in range(anzahl):
        password = ''.join(random.choice(characters) for _ in range(length))
        passwords.append(password)

    return passwords


def rate_password(password: str):
    score = 0
    for i in password:
        if i in LOWER:
            score += 1
            break
    for i in password:
        if i in UPPER:
            score += 1
            break
    for i in password:
        if i in DIGITS:
            score += 2
            break
    for i in password:
        if i in PUNCTUATION:
            score += 2
            break
    if len(password) > 7:
        score += 2
    if len(password) > 15:
        score += 3

    # Compares with unsafe word file
    unsafewords = []
    with open('unsafewords.txt', "r") as file:
        for i in file.readlines():
            unsafewords.append(i)

    if password in unsafewords:
        return "Schwach"

    if check_same_symbols(password, 3):
        score -= 4
    elif check_same_symbols(password, 2):
        score -= 2

    # Return with score
    if score > 10:
        return "Stark"
    elif score >= 7:
        return "Mittelstark"
    else:
        return "Schwach"


def check_same_symbols(password: str, same_symbol_count: int) -> bool:
    if same_symbol_count > 1:
        for i in range(len(password) - same_symbol_count + 1):
            if password[i:i+same_symbol_count] == password[i] * same_symbol_count:  # noqa
                return True

        return False


def save_password(name: str, username: str, password: str):
    key = load_key()
    encrypted_password = encrypt_password(password, key)

    data = {
        "name": name,
        "username": username,
        "password": encrypted_password
    }

    try:
        with open('passwords.json', 'r') as file:
            passwords = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        passwords = []

    passwords.append(data)

    with open('passwords.json', 'w') as file:
        json.dump(passwords, file, indent=4)


def get_passwords():
    key = load_key()
    try:
        with open('passwords.json', 'r') as file:
            passwords = json.load(file)
            if not passwords:
                return False
            else:
                for entry in passwords:
                    entry['password'] = decrypt_password(entry['password'], key)    # noqa
                return passwords
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def main():
    utils.Windows().main_menu


if __name__ == "__main__":
    try:
        load_key()
    except FileNotFoundError:
        generate_key()
    main()
