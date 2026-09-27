import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)
from ascii import logo

def main():
    print(Style.BRIGHT + Fore.GREEN + logo)

if __name__ == "__main__":
    main()