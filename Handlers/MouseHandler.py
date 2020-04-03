import pyautogui
import keyboard

def set_mouse_position(point):
    if not keyboard.is_pressed('p'):
        pyautogui.moveTo(point[0], point[1])
 
def right_click():
    if not keyboard.is_pressed('p'):
        pyautogui.rightClick()

def left_click():
    if not keyboard.is_pressed('p'):
        pyautogui.leftClick()