import numpy as np
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from Handlers import MemoryHandler, MouseHandler, ScreenHandler, ProcessHandler
import time
import cv2


class ZumaEnvironment(py_environment.PyEnvironment):
    def __init__(self, process_path):
        self.screen_handler = None
        self.process_handler = ProcessHandler.ProcessHandler(process_path)
        self._restart_game()

        self.game_resolution = self.screen_handler.get_resolution()
        self.div = 4
        self.vison_resolution = self.game_resolution / self.div
        self.vison_resolution = self.vison_resolution.astype(int)
        self._set_specs()

        self.max_playtime = 10 * 60  # seconds
        self.score_timeout = 5  # seconds

    def _set_specs(self):
        image_shape = np.append(np.flip(self.vison_resolution), 3)
        image_ones = np.ones(shape=image_shape)
        self._observation_spec = array_spec.BoundedArraySpec(shape=image_shape, dtype=np.int32,
                                                             name='observation', minimum=image_ones * 0, maximum=image_ones * 255)
        self._action_spec = array_spec.BoundedArraySpec(shape=(4,), dtype=np.float64, name='action',
                                                        minimum=np.zeros(4), maximum=np.ones(4))

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _restart_game(self):
        # if the game is running: close the current instance
        if self.process_handler.is_running():
            self.process_handler.terminate()

        self.process_handler.run()
        # IMPORTANT!!! to initialize PID before HWND
        # time.sleep(10)
        pid = self.process_handler.pid()
        hwnd = self.process_handler.hwnd()
        self.memory_handler = MemoryHandler.MemoryReader(pid)
        self.screen_handler = ScreenHandler.ScreenCapture(hwnd)

    def _reset(self):
        self._restart_game()

        # ---------------------
        # TODO: start level
        # ---------------------
        self._start_game()
        # set training timestamps
        self.start_time = time.time()
        self.last_score = 0
        self.last_progress_time = self.start_time

        return ts.restart(self._observe())

    def _step(self, action):
        # if reached max playtime: ignore action and return last timestep
        if time.time() - self.start_time > self.max_playtime:
            return ts.termination(self._observe(), self._get_reward())

        # if not progressing or game is not running: ignore action and restart
        if time.time() - self.last_progress_time > self.score_timeout or not self.process_handler.is_running():
            return self.reset()

        self._action(action)

        reward = self._get_reward()

        # update training timestamps
        if reward > 0:
            self.last_progress_time = time.time()

        return ts.transition(self._observe(), reward)

    def _action(self, action):
        ''' Action specs:   
            Action is a numpy array with 4 elements: [x, y, lc, rc]
            x/y - mouse position written as percantages of screen width/hight (from top left) 
            lc - bool for left clicking
            rc - bool for right clicking
            
            how to calculate meaningful values:
            bool = element > 0
            position = length * element
            out logic:

            how to do the action:
            if 'rc':
                right click
            if 'lc':
                calculate mouse position
                set mouse position
                left click
        '''
        if action[3]:
            MouseHandler.right_click()
        if action[2]:
            percentages = np.array(action[0:2])
            print(f"y,x: {percentages}")
            point = self.game_resolution * percentages 
            point = point.astype(int)
            absolute_point = self.screen_handler.get_zero_position() + point #TODO: bug: out of bounds
            MouseHandler.set_mouse_position(absolute_point)
            MouseHandler.left_click()

    def _observe(self):
        image = self.screen_handler.get_image()
        size = (self.vison_resolution[0], self.vison_resolution[1])
        image = cv2.resize(image, size)
        return image

    def _get_reward(self):
        current_score = self.memory_handler.read_pointer(0x001A531C, [0x300, 0x58, 0x30, 0xC4, 0xE8, 0x10, 0xE8])
        reward = current_score - self.last_score
        self.last_score = current_score
        return reward

    def _start_game(self):

        pos = lambda array: self.screen_handler.get_zero_position() + np.array(array)
        time.sleep(2)
        # 1st screen:
        MouseHandler.set_mouse_position(pos([308, 482]))  # "click here to play" button
        MouseHandler.left_click()
        # 2nd screen:
        MouseHandler.set_mouse_position(pos([500, 200]))  # "gauntlet" button
        MouseHandler.left_click()
        # 3rd screen:
        # if there is a "new game?" popup:
        MouseHandler.set_mouse_position(pos([400, 366]))  # "new game" button
        MouseHandler.left_click()
        # 4th screen:
        # todo: later make level select here
        MouseHandler.set_mouse_position(pos([337, 493]))  # "play" button
        MouseHandler.left_click()
