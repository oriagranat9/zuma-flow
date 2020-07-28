import matplotlib
import matplotlib.pyplot as plt
import numpy
import tensorflow as tf
from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import q_network
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common
from tf_agents.specs import array_spec
from tensorflow import dtypes
from tf_agents.trajectories import time_step

from tf_agents.policies import random_tf_policy
from ZumaEnvirnment import ZumaEnvironment

env = ZumaEnvironment("f:\\Users\\oriag\\Desktop\\Zuma Deluxe\\Zuma.exe")
train_env = tf_py_environment.TFPyEnvironment(env)

random_policy = random_tf_policy.RandomTFPolicy(train_env.time_step_spec(),
                                                train_env.action_spec())


def compute_avg_return(environment, policy, num_episodes=1):
    total_return = 0.0
    for _ in range(num_episodes):

        time_step = environment.reset()
        episode_return = 0.0

        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = environment.step(action_step.action)
            episode_return += time_step.reward
        total_return += episode_return

    avg_return = total_return / num_episodes
    return avg_return.numpy()[0]


print(compute_avg_return(train_env, random_policy, 10))
