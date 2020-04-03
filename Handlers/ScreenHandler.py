import numpy
import psutil
from PIL import ImageGrab
import win32gui
import cv2


class ScreenCapture:
    def __init__(self, hwnd, selected_color=cv2.COLOR_BGR2RGB, show_image=False):
        self.selected_color = selected_color
        self.show_image = show_image
        self.hwnd = hwnd

    def get_image(self):
        bbox = win32gui.GetWindowRect(self.hwnd)
        tmp_img = ImageGrab.grab(bbox)

        n = numpy.asarray(tmp_img)
        image = cv2.cvtColor(numpy.array(tmp_img), self.selected_color)

        if self.show_image:
            cv2.imshow("captured image", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        return image

    def get_zero_position(self):
        bbox = win32gui.GetWindowRect(self.hwnd)
        return numpy.array(bbox[0:2])

    def get_resolution(self):
        bbox = win32gui.GetWindowRect(self.hwnd)
        return numpy.array(bbox[2:4])
