from ctypes import windll

from src.app.scenes.MainScene import MainScene
from src.app.scenes.GameScene import GameScene

kernel32 = windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
  
screen1 = MainScene()
screen2 = GameScene()

try:
    screen2.draw()
except KeyboardInterrupt:
    print("\nПрограмма завершена.", end="")