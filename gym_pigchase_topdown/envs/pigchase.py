import numpy as np
from gym_pigchase_topdown.envs.agents import RandomAgent, RandomPig
from gym_pigchase_topdown.envs.commons import DIR_DICT, DIR_SHIFT_DICT
from gym_pigchase_topdown.envs.renderer import render

sample_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 0, 0, 0, 0, 0, 1, 1],
              [1, 1, 0, 1, 0, 1, 0, 1, 1],
              [1, 2, 0, 0, 0, 0, 0, 2, 1],
              [1, 1, 0, 1, 0, 1, 0, 1, 1],
              [1, 1, 0, 0, 0, 0, 0, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1],
              ]
# Code:
# 0 = Free
# 1 = Wall
# 2 = Exit


class PigChase:

    # Define Actions:
    #   - F (forward), B(backward)
    #   - X (stay still)
    #   - L, R (rotate Left/Right 90 degrees)

    def __init__(self, agent_2=None, pig=None):

        self.agent_2 = agent_2
        self.pig = pig

        if self.agent_2 is None:
            self.agent_2 = RandomAgent()
        if self.pig is None:
            self.pig = RandomPig()

        self.reset()

    def __get_map_occupied(self):
        view = np.array(self.map == 1, dtype=np.int)
        view[tuple(self.agent_1_position['position'])] = 1
        view[tuple(self.agent_2_position['position'])] = 1
        view[tuple(self.pig_position['position'])] = 1

        return view

    def __move_agent(self, agent_pos, action):

        new_dir = agent_pos['direction']
        new_pos = np.copy(agent_pos['position'])
        successful = True

        if action == "L":
            new_dir = (new_dir - 1) % 4
            agent_pos['direction'] = new_dir
        elif action == "R":
            new_dir = (new_dir + 1) % 4
            agent_pos['direction'] = new_dir
        elif action == "F":
            shift = DIR_DICT[new_dir]
            new_pos += shift
            if not self.__get_map_occupied()[tuple(new_pos)]:
                agent_pos['position'] = new_pos
            else:
                successful = False
        elif action == "B":
            shift = DIR_DICT[new_dir]
            new_pos -= shift
            if not self.__get_map_occupied()[tuple(new_pos)]:
                agent_pos['position'] = new_pos
                successful = False

        return successful

    def __move_pig(self, action):

        shift = DIR_SHIFT_DICT[action]
        new_pos = self.pig_position['position'] + shift
        if not self.__get_map_occupied()[tuple(new_pos)]:
            self.pig_position['position'] += shift

    def reset(self):

        self.pig_position = {'position': np.array([3, 4])}
        self.agent_1_position = {'position': np.array([1, 2]), 'direction': 0}
        self.agent_2_position = {'position': np.array([5, 6]), 'direction': 2}
        self.map = np.array(sample_map)

        return

    def __get_view(self):

        view = np.array(self.map, dtype=str)

        exit_index = view == '2'
        view[tuple(self.agent_1_position['position'])] = 'R'  # Red Agent
        view[tuple(self.agent_2_position['position'])] = 'B'  # Blue Agent
        view[exit_index] = 'E'
        view[tuple(self.pig_position['position'])] = 'P'  # Pig

        return view

    def step(self, action):

        self.__move_agent(self.agent_1_position, action)

        pig_move = self.pig.step(self.__get_view())
        if pig_move is not None:
            self.__move_pig(pig_move)

        agent_2_action = self.agent_2.step(self.__get_view(), self.agent_2_position['direction'])
        self.__move_agent(self.agent_2_position, agent_2_action)

        return

    def render(self):
        entities = [self.pig_position, self.agent_1_position, self.agent_2_position]
        render(self.__get_view(), entities)

    def player_to_exit(self):
        return self.__get_view()[tuple(self.agent_1_position['position'])] == 'E' or \
                self.__get_view()[tuple(self.agent_2_position['position'])] == 'E'

    def pig_captured(self):
        return len(self.pig.get_available_moves(self.__get_view())) == 0

    def get_full_observation(self):
        number_of_elements = 8
        view = self.__get_view()
        h, k = view.shape

        result = np.zeros([h, k, number_of_elements])
        codex = np.array(["1", "E", "P", "B"])

        for x in range(h):
            for y in range(k):
                sym = view[x, y]
                code = np.where(codex == sym)[0]
                if len(code) > 0:
                    result[x, y, code[0]] = 1

        z = 4 + self.agent_1_position['direction']
        result[tuple(self.agent_1_position['position']) + (z,)] = 1

        return result

    def get_first_person_view(self):

        # 00#00
        # 0###0
        # #####

        view = self.__get_view()

        sight = 3
        position = self.agent_1_position['position']
        straight = np.array(DIR_DICT[self.agent_1_position['direction']])
        right = np.array(DIR_DICT[(self.agent_1_position['direction']+1) % 4])
        left = np.array(DIR_DICT[(self.agent_1_position['direction']-1) % 4])

        x = []
        for j in range(sight):
            for i in range(j, sight):
                x += view[tuple((position + (i)*straight + j*right) % np.array(view.shape))]
                if j != 0:
                    x += view[tuple((position + (i)*straight + j*left) % np.array(view.shape))]

        return np.array(x)


if __name__ == "__main__":

    obj = PigChase()
    print(obj.get_first_person_view())
