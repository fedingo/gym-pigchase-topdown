import numpy as np
import random
from gym_pigchase_topdown.envs.commons import *


class RandomAgent:

    def __init__(self):
        return

    def step(self, obs, agent_orientation):
        return ACTIONS_DICT[np.random.randint(5)]


class FollowAgent:

    def __init__(self):
        return

    def step(self, obs, agent_orientation):
        agent_position = [np.array(x) for x in zip(*np.where(obs == 'B'))][0]
        flow_matrix = np.full(obs.shape, -np.inf)
        h,k = obs.shape

        flow_matrix[((obs == '0') + (obs == 'E'))] = np.inf
        flow_matrix[obs == 'P'] = 0
        flow_matrix[tuple(agent_position)] = np.inf

        current_step = 0
        while (flow_matrix == np.inf).any() and current_step < 30:
            for x in range(h):
                for y in range(k):
                    if flow_matrix[x, y] == current_step:
                        new_val = flow_matrix[x, y] + 1
                        # verticals
                        flow_matrix[x-1, y] = np.min([flow_matrix[x-1, y], new_val])
                        flow_matrix[x+1, y] = np.min([flow_matrix[x+1, y], new_val])
                        # horizontal
                        flow_matrix[x, y-1] = np.min([flow_matrix[x, y-1], new_val])
                        flow_matrix[x, y+1] = np.min([flow_matrix[x, y+1], new_val])

            current_step += 1

        flow_matrix[flow_matrix == -np.inf] = np.inf

        min = np.inf
        dir = ""

        # Find minimum direction
        for k, shift in DIR_SHIFT_DICT.items():
            if min > flow_matrix[tuple(agent_position+shift)]:
                min = flow_matrix[tuple(agent_position+shift)]
                dir = k

        # if no move is available, just stay still
        if dir == "":
            return "X"

        move = (CARDINAL_TO_DIR[dir] - agent_orientation) % 4
        action = MOVE_TO_ACTION[move]

        return action


class RandomPig:
    def __init__(self):
        return

    def get_available_moves(self, obs):

        map = (obs == '0') + (obs == 'E')
        pig_position = [np.array(x) for x in zip(*np.where(obs == 'P'))][0]

        # check for available moves
        explore_moves = DIR_SHIFT_DICT.keys()
        available_moves = []

        for m in explore_moves:
            shift = DIR_SHIFT_DICT[m]
            if map[tuple(pig_position + shift)]:
                available_moves += m

        return available_moves

    # The pig has to move each turn
    def step(self, obs):

        available_moves = self.get_available_moves(obs)
        if len(available_moves) == 0:
            return None
        return random.sample(available_moves, 1)[0]


class EscapePig:

    def __init__(self):
        return

    # The pig has to move each turn
    # He tries to go to the cell that has the most amount of possible next moves
    def step(self, obs, pig_position):
        map = obs != 0

        return np.random.randint(5)
