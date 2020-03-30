import numpy
import psutil
from PIL import ImageGrab
import win32gui
import cv2


class ScreenCapture:
    def __init__(self, program_name, selected_color=cv2.COLOR_BGR2RGB, show_image=False):
        self.selected_color = selected_color
        self.show_image = show_image
        self.all_windows = []
        for proc in psutil.process_iter():
            if program_name in proc.name():
                self.pid = int(proc.pid)
                break


    def get_image(self):
        bbox = win32gui.GetWindowRect(self.pid)
        tmp_img = ImageGrab.grab(bbox)
        image = cv2.cvtColor(numpy.array(tmp_img), self.selected_color)
        if self.show_image:
            cv2.imshow("captured image", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        return image
