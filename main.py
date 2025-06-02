from ctypes import windll

from src.Game import Game

kernel32 = windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

if __name__ == "__main__":
    Game.init()
