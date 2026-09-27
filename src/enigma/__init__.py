import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)
from ascii import logo
def main() -> None:
    print(Style.BRIGHT + Fore.GREEN + logo)
