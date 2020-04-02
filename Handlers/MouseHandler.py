import pyautogui

def set_mouse_position(point):
    pyautogui.moveTo(point[0], point[1])
 
def right_click():
    pyautogui.rightClick()

def left_click():
    pyautogui.leftClick()