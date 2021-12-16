import webview
import keyboard
from screeninfo import get_monitors
import pyautogui
import psutil   # 실행중인 프로세스 및 시스템 활용 라이브러리
import time

urlList = []
viewNum = []

# keyboard.on_press_key("f11", lambda _:screenToFull())
keyboard.on_press_key("f8", lambda _:allDisplayClosed())
keyboard.on_press_key("f5", lambda _:reload())

def reload():
    for idx in range(viewNum.__len__()):
        viewNum[idx].load_url(urlList[idx])

def screenToFull():
    for idx in range(viewNum.__len__()):
        viewNum[idx].toggle_fullscreen()

def allDisplayClosed():
    MsgBox = pyautogui.confirm(text='Really Quit?', title='Exit App', buttons=['OK', 'Cancel'])
    if MsgBox == 'OK':
        for idx in range(viewNum.__len__()):
            viewNum[idx].destroy()
    else:
        return

def checkProcess():
    for proc in psutil.process_iter():
        try:
            # 프로세스 이름, PID값 가져오기
            processName = proc.name()
            processID = proc.pid

            if processName == "subprocess.exe":
                parent_pid = processID  #PID
                parent = psutil.Process(parent_pid) # PID 찾기
                for child in parent.children(recursive=True):  #자식-부모 종료
                    child.kill()
                parent.kill()

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):   #예외처리
            pass

def on_closed():
    print('pywebview window is closed')
    checkProcess()

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
    viewNum[idx].closed += on_closed

webview.start(gui='cef')