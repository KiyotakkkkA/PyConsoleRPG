import subprocess
import time
import pyautogui

process = subprocess.Popen(
    args=["powershell", "-NoExit"],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)

time.sleep(2)

pyautogui.hotkey('alt', 'enter')
time.sleep(3)

pyautogui.write(r'.\scripts\windows\env.ps1')
pyautogui.press('enter')

time.sleep(1)

pyautogui.write(r'python main.py')
pyautogui.press('enter')