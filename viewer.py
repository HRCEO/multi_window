import webview
import time
import keyboard
from screeninfo import get_monitors
import pyautogui

urlList = []
viewNum = []

keyboard.on_press_key("f", lambda _:screenToFull())
keyboard.on_press_key("d", lambda _:allDisplayClosed())

def screenToFull():
    for idx in range(viewNum.__len__()):
        time.sleep(5)
        viewNum[idx].toggle_fullscreen()

def allDisplayClosed():
    MsgBox = pyautogui.confirm(text='Really Quit?', title='Exit App', buttons=['OK', 'Cancel'])
    if MsgBox == 'OK':
        for idx in range(viewNum.__len__()):
            viewNum[idx].destroy()
    else:
        return;

with open('config.text', 'r') as file:
    for line in file:
        urlList.append(line.strip('\n'))

for idx, display_num in enumerate(get_monitors()):
    viewNum.append(
        webview.create_window(
            'Monitoring System Viewer',
            urlList[idx],
            x=display_num.x,
            y=display_num.y,
            width=display_num.width,
            height=display_num.height,
            on_top=True,
        )
    )

webview.start(gui='cef')