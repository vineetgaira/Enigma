import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)
from ascii import logo

def display_logo():
    print(Style.BRIGHT + Fore.GREEN + logo)

def menu():
    print("="*26)
    print("          MENU")
    print("="*26)
    print(Fore.WHITE +" [1] ", Fore.LIGHTCYAN_EX + "Encrypt message.")
    print(Fore.WHITE +" [2] ", Fore.LIGHTCYAN_EX + "Decipher message.")

def main():
    display_logo()
    menu()
    
if __name__ == "__main__":
    main()