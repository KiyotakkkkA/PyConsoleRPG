from ctypes import windll

from src.app.scenes.MainScene import MainScene
from src.app.scenes.GameScene import GameScene
from src.services.frontend.core.ScreenManager import ScreenManager

kernel32 = windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
  
ScreenManager.add_screens({
    "main": MainScene(),
    "game": GameScene()
})
ScreenManager.set_current_screen("main")

try:
    ScreenManager.draw()
except KeyboardInterrupt:
    print("\nПрограмма завершена.", end="")