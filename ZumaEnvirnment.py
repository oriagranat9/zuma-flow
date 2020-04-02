import numpy as np
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from tensorflow import dtypes
from Handlers import MemoryHandler, MouseHandler, ScreenHandler, ProcessHandler
import time
import cv2


class ZumaEnvironment(py_environment.PyEnvironment):
    def __init__(self, process_path):
        self.process_handler = ProcessHandler.ProcessHandler(process_path)
        self._restart_game()

        self.game_resolution = self.screen_handler.get_resolution()
        self.div = 4
        self.vison_resolution = self.game_resolution / self.dive
        self._set_specs()

        self.max_playtime = 10 * 60  # seconds
        self.score_timeout = 5  # seconds

    def _set_specs(self):
        npRes = np.ones(shape=self.vison_resolution)
        action_shape = [4]
        npAction = np.ones(shape=action_shape)
        self._observation_spec = array_spec.BoundedArraySpec(shape=self.vison_resolution, dtype=dtypes.int32,
                                                             name='observation', minimum=npRes * 0, maximum=npRes * 255)
        self._action_spec = array_spec.BoundedArraySpec(shape=npAction, dtype=dtypes.float64, name='action',
                                                        minimum=npAction * 0, maximum=npAction)

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
        pid = self.process_handler.pid()
        hwnd = self.process_handler.hwnd()
        self.memory_handler = MemoryHandler.MemoryReader(pid)
        self.screen_handler = ScreenHandler.ScreenCapture(hwnd)

    def _reset(self):
        self._restart_game()

        # ---------------------
        # TODO: start level
        # ---------------------

        # set training timestamps
        self.start_time = time.time()
        self.last_score = 0
        self.last_score_time = self.start_time

        return ts.restart(self._observe())

    def _step(self, action):
        # if reached max playtime: ignore action and return last timestep
        if time.time() - self.start_time > self.max_playtime:
            return ts.termination(self._observe(), self._get_score())

        # if not progressing or game is not running: ignore action and restart
        if time.time() - self.last_score_time > self.score_timeout or not self.process_handler.is_running():
            return self.reset()

        self._action(action)

        score = self._get_score()

        # update training timestamps
        if self.last_score > score:
            self.last_score_time = time.time()
            self.last_score = score

        return ts.transition(self._observe(), score)

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
            percentages = np.array(action[0], action[1])
            point = self.game_resolution * percentages
            point = point.astype(int)
            absolute_point = self.screen_handler.get_zero_position() + point
            MouseHandler.set_mouse_position(absolute_point)
            MouseHandler.left_click()

    def _observe(self):
        image = self.screen_handler.get_image()
        image = cv2.resize(image, tuple(self.vison_resolution))
        return image

    def _get_score(self):
        return self.memory_handler.read_pointer()
