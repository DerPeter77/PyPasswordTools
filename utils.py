import os
from rich.console import Console
import rich
import json
from datetime import datetime
import main
console = Console(color_system="auto")


def print_spaces(n: int):
    for i in range(0, n):
        print(" ")


class Windows:
    def __init__(self):
        self.main_menu()

    def clear_screen(self):
        os.system('cls')

    def back_to_menu(self):
        print_spaces(2)
        back = input("Zurück zum Menü [j/n]: ")
        if back.lower() in ["j", "ja", "y", "yes"]:
            self.main_menu()
        else:
            self.clear_screen()
            welcomeText = open("welcomeText.txt", "r").read()
            console.print(welcomeText, style="cyan")
            return

    def main_menu(self):
        print_spaces(3)
        os.system('cls')
        welcomeText = open("welcomeText.txt", "r").read()
        console.print(welcomeText, style="cyan")
        print_spaces(2)
        print("""
                    | -------------------------------------------- |
                    | [0] - Programm beenden                       |
                    | [1] - Passwort Generieren                    |
                    | [2] - Passwort Bewerten                      |
                    | [3] - Passwort Speichern                     |
                    | [4] - Gespeicherte Passwörter anzeigen       |
                    | -------------------------------------------- |
""")
        # print("[0] - Programm beenden")
        # print("[1] - Passwort Generieren")
        # print("[2] - Passwort Bewerten")
        # print("[3] - Passwort Speichern")
        # print("[4] - Gespeicherte Passwörter anzeigen")
        print_spaces(2)
        selected_menu = input("Bitte wählen Sie eine Option:   ")
        if selected_menu == "0":
            return
        if selected_menu == "1":
            self.generate_password()
        elif selected_menu == "2":
            self.rate_password()
        elif selected_menu == "3":
            self.save_password()
        elif selected_menu == "4":
            self.show_passwords()
        else:
            self.main_menu()

    def generate_password(self):
        # Get Parameters for password generation
        while True:     # Password length
            try:
                length = int(input("Bitte geben Sie die Länge des Passworts ein: "))    # noqa
                break
            except ValueError:
                console.print(
                    "Bitte geben Sie eine [bold]Zahl[/bold] ein", style="red")
        while True:     # Password amount
            try:
                anzahl = int(input("Bitte geben Sie die Anzahl der Passwörter ein: "))  # noqa
                break
            except ValueError:
                console.print(
                    "Bitte geben Sie eine [bold]Zahl[/bold] ein", style="red")
        while True:     # Password characters
            print("Welche Zeichen sollen im Passwort enthalten sein?")
            chosen_characters = input("[1]: Buchstaben\n[2]: Zahlen\n[3]: Sonderzeichen\n")    # noqa
            if all(char in "123" for char in chosen_characters):
                break
            else:
                console.print(
                    "Bitte geben Sie eine [bold]gültige Option[/bold] ein", style="red")    # noqa

        print_spaces(2)

        # Generate and rate passwords to console
        passwords = main.generate_password(length, anzahl, chosen_characters)
        for i, password in enumerate(passwords):
            try:
                console.print(f"[bold]Passwort {
                              i+1}[/bold]: [default]{password}[/default]", style="green")   # noqa
            except rich.errors.MarkupError:
                print(f"Passwort {i+1}: {password}")
            rating = main.rate_password(password)
            if rating == "Stark":
                console.print(f"Das Passwort ist: {rating}", style="green")
            elif rating == "Mittelstark":
                console.print(f"Das Passwort ist: {rating}", style="yellow")
            else:
                console.print(f"Das Passwort ist: {rating}", style="red")
            console.print("[bold]---------------------[/bold]", style="cyan")
        print_spaces(2)

        # Print passwords for txt file
        save_to_file = input(
            "Möchten Sie die Passwörter in einer Datei speichern? [j/n] ")
        if save_to_file.lower() in ["j", "ja", "y", "yes"]:
            filename = input("Bitte geben Sie den Dateinamen ein: ")
            with open(f"{filename}.txt", "w") as file:
                for i, password in enumerate(passwords):
                    file.write(f"Passwort {i + 1}: {password}\n")
            console.print(f"Passwörter wurden in [bold]{
                          filename}.txt[/bold] gespeichert", style="green")

        # Save Passwords in Database
        save_to_json = input("Sollen die Passwörter in der Anwendung gespeichert werden? [j/n] ")    # noqa
        console.print("[bold]---------------------[/bold]", style="cyan")
        if save_to_json.lower() in ["j", "ja", "y", "yes"]:
            for i, password in enumerate(passwords):
                console.print(f"[bold]Password {
                              i+1}[/bold]: [default]{password}[/default]", style="green")   # noqa
                console.print(
                    "[bold]---------------------[/bold]", style="cyan")
                name = input("Bitte geben Sie den Namen der Website ein: ")
                username = input("Bitte geben Sie den Benutzernamen ein: ")
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

        self.back_to_menu()

    def rate_password(self):
        password = input("Bitte geben Sie das Passwort zum bewerten ein: ")
        rating = main.rate_password(password)
        if rating == "Stark":
            console.print(f"Das Passwort ist: [green bold]{rating}[/green bold]")   # noqa
        elif rating == "Mittelstark":
            console.print(f"Das Passwort ist: [yellow bold]{rating}[/yellow bold]") # noqa
        else:
            console.print(f"Das Passwort ist: [red bold]{rating}[/red bold]")
        self.back_to_menu()

    def save_password(self):
        name = input("Bitte geben Sie den Namen der Website ein: ")
        username = input("Bitte geben Sie den Benutzernamen ein: ")
        password = input("Bitte geben Sie das Passwort ein: ")
        print_spaces(2)
        main.save_password(name, username, password)
        self.back_to_menu()

    def show_passwords(self):
        passwords = main.get_passwords()
        if not passwords:
            print("Keine gespeicherten Passwörter gefunden.")
        else:
            output_choice = input(
                "Möchten Sie die Passwörter in der Konsole oder in einer Textdatei anzeigen? [konsole/datei] [k/d] ")   # noqa
            if output_choice.lower() in ["konsole", "k"]:
                console.print(
                    "[bold]---------------------[/bold]", style="cyan")
                for entry in passwords:
                    console.print(
                        f"[cyan]Name:[/cyan] [green1]{entry['name']}[/green1]", style="bold")   # noqa
                    console.print(
                        f"  [cyan]Username:[/cyan] [green1]{entry['username']}[/green1]", style="bold") # noqa
                    console.print(
                        f"  [cyan]Password:[/cyan] [green1]{entry['password']}[/green1]", style="bold") # noqa
                    if main.rate_password(entry['password']) == "Stark":
                        console.print("Das Passwort ist [green bold]Stark[/green bold]", style="bold")  # noqa
                    if main.rate_password(entry['password']) == "Mittelstark":
                        console.print("Das Passwort ist [yellow bold]Mittelstark[/yellow bold]", style="bold")  # noqa
                    if main.rate_password(entry['password']) == "Schwach":
                        console.print("Das Passwort ist [red bold]Schwach[/red bold]", style="bold")    # noqa
                    console.print(
                        "[bold]---------------------[/bold]", style="cyan")
            elif output_choice.lower() in ["datei", "d"]:
                now = datetime.now()
                filename = now.strftime("passwords_output_%Y%m%d_%H%M%S.txt")
                with open(filename, 'w') as output_file:
                    for entry in passwords:
                        output_file.write(f"Name: {entry['name']}\n")
                        output_file.write(f"  Username: {entry['username']}\n")
                        output_file.write(f"  Password: {entry['password']}\n")
                print(f"Passwörter wurden in {filename} gespeichert.")

            delete = input(
                "Möchten Sie die gespeicherten Passwörter löschen? [j/n] ")
            if delete.lower() == "j":
                which = input("Welches Passwort möchten Sie löschen? (Name) ")
                for entry in passwords:
                    if entry['name'] == which:
                        passwords.remove(entry)
                        with open('passwords.json', 'w') as file:
                            json.dump(passwords, file, indent=4)
                            print("Passwort gelöscht")

        self.back_to_menu()
