import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)
def main() -> None:
    print(Style.BRIGHT + Fore.GREEN + "Hello from enigma!")
