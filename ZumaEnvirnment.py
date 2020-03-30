import numpy as np
import tf_agents.environments.py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from tensorflow import dtypes
from Handlers import MemoryHandler, MouseHandler, ScreenHandler


class ZumaEnvironment(py_environment.PyEnvironment):

    def __init__(self):
        resolution = [80, 60]
        npRes = np.ones(shape=resolution)

        action = [4]
        npAction = np.ones(shape=action)

        self._observation_spec = array_spec.BoundedArraySpec(shape=resolution, dtype=dtypes.int32, name='observation', minimum=npRes * 0, maximum=npRes * 255)
        self._action_spec = array_spec.BoundedArraySpec(shape=npAction, dtype=dtypes.float64, name='action', minimum=npAction * 0, maximum=npAction)


	def action_spec(self):
		return self._action_spec


	def observation_spec(self):
		return self._observation_spec


	def _reset(self):
		if 
		#launch game and initiate handlers if it is not up 
		#start level
		# return reset timestep (stating image and score)    
		return ts.restart(np.array([self._score], dtype=np.int32))


	def _step(self, action):
		# if game is closed or level is not playing: self.reset()
		if self._episode_ended:
			# The last action ended the episode. Ignore the current action and start
			# a new episode.
			return self.reset()

		# enact action using handlers and get new score
		# return new timestep with new image and new score