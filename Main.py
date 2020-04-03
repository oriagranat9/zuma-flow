import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import suite_gym
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

from ZumaEnvirnment import ZumaEnvironment

env = ZumaEnvironment("f:\\Users\\oriag\\Desktop\\Zuma Deluxe\\Zuma.exe")
train_env = tf_py_environment.TFPyEnvironment(env)

q_net = q_network.QNetwork(
    train_env.observation_spec(),
    train_env.action_spec())

optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=1)

train_step_counter = tf.Variable(0)

agent = dqn_agent.DqnAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=train_step_counter)

agent.initialize()
# agent policies 
eval_policy = agent.policy
collect_policy = agent.collect_policy

