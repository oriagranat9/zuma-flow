import pyautogui

def set_mouse_position(x,y):
    pyautogui.moveTo(x,y)

def right_click():
    pyautogui.rightClick()

def left_click():
    pyautogui.leftClick()