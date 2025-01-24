import random
import json
import utils

LOWER = 'abcdefghijklmnopqrstuvwxyz'
UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGITS = '0123456789'
PUNCTUATION = r"""!"#$%&'()*+,-.:;<=>?@^_`{|}~"""


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

    # Pattern Matching with 3 same symbols
    password_list = []
    for symbol in password:
        password_list.append(symbol)

    for index, symbol in enumerate(password_list):
        # 3 same symbols following
        try:
            next_index = index + 1
            overnext_index = next_index + 1
            if symbol == password_list[next_index] == password_list[overnext_index]:
                score -= 4
                print(score, "3 hintereinander")
                break
        except IndexError:
            pass

        # 2 same symbols following
        try:
            next_index = index + 1
            if symbol == password_list[next_index]:
                score -= 2
                print(score, "2 hintereinander")
        except IndexError:
            pass

    # Return with score
    if score > 10:
        return "Stark"
    elif score >= 7:
        return "Mittelstark"
    else:
        return "Schwach"


def save_password(name: str, username: str, password: str):
    data = {
        "name": name,
        "username": username,
        "password": password
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
    try:
        with open('passwords.json', 'r') as file:
            passwords = json.load(file)
            if not passwords:
                return False
            else:
                return passwords
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def main():
    utils.Windows().main_menu


if __name__ == "__main__":
    main()
