import gym
from gym import spaces

from gym_pigchase_topdown.envs.pigchase import PigChase
from gym_pigchase_topdown.envs.renderer import get_action
from gym_pigchase_topdown.envs.agents import *
import sys
import time

class PigChaseEnv(gym.Env):

    metadata = {"render.modes": ["human"], }
    ACTION = ["F", "B", "L", "R"]

    def __init__(self, agent_2_mode="", pig_mode=""):

        self.max_steps = 25
        self.steps = 0
        self.agent_2 = None
        self.pig = None
        self.game = None

        self.obs_shape = [9,7]
        self.action_space = spaces.Discrete(len(self.ACTION))
        self.observation_space = spaces.Box(low=0, high=1, shape=self.obs_shape, dtype=np.int)

        self.reset()

    def get_state(self, action_index):
        state = self.game.get_first_person_view()
        s = []
        syms = ['1', 'P', 'B']
        for x in syms:
            s.append(state == x)

        result = np.array(s, dtype=np.int).flatten()
        action = np.zeros(len(self.ACTION))
        if action_index != -1:
            action[action_index] = 1
        result = np.append(result, action)

        return result

    def step(self, action_index):
        # Assertion to check Action is valid
        assert self.action_space.contains(action_index)

        self.steps += 1

        self.game.step(self.ACTION[action_index])
        state = self.get_state(action_index)

        exited = self.game.player_to_exit()
        pig_capture = self.game.pig_captured()
        max_reached = self.steps >= self.max_steps

        reward = -0.04
        if exited:
            reward = 0.2
        if pig_capture:
            reward = 1

        done = exited or pig_capture or max_reached
        add_info = {"steps": self.steps}

        return state, reward, done, add_info

    def reset(self, training = True):

        if np.random.rand() > 0:
            self.agent_2 = RandomAgent()
        else:
            self.agent_2 = FollowAgent()

        self.pig = RandomPig()
        self.game = PigChase(agent_2=self.agent_2, pig=self.pig)

        self.game.reset()
        self.steps = 0

        return self.get_state(-1)

    def render(self, mode='human', close=False):

        self.game.render()
        time.sleep(0.4)
        if close:
            sys.exit(0)

    def read_action(self):
        return get_action()


if __name__ == "__main__":

    env = PigChaseEnv()
    state = env.reset()
    env.render()

    while True:
        action = env.read_action()
        if action != -1:
            state, reward, done, _ = env.step(action) #env.action_space.sample())
            env.render()
            print(state.shape)

            if done:
                break
