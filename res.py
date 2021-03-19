from colorama import Fore, Back, Style

def get_health_bar(length, p, q):
    filled = int(p*length/q)
    bar = Back.GREEN + (' ' * filled)
    bar += Back.RED + (' ' * (length - filled))
    return bar