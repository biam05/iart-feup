from matchthetiles.gamestate.gamestate import GameState
import gym
from gym import spaces

from scipy.special import perm

class MTT_4x4_1B(gym.Env):
    def __init__(self):
        # Constants
        self.penalty_step = -1
        self.reward_finish = 20

        # Environment variables
        self.env_steps = 0
        self.max_steps = 100

        self.blocks = 1
        self.walls = 4
        self.rows = 4
        self.cols = 4
        
        self.game_state = self.reset()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(perm(self.rows * self.cols, self.blocks, exact=True))

    def step(self, action):
        assert action in ACTIONS

        self.env_steps += 1

        self.__move(action)

        reward = self.__reward()

        done = self.__done()

        observation = self.game_state

        info = {
            "action_move": ACTIONS[action]
        }

        return observation, reward, done, info
    
    def __move(self, action : int):
        if action == 0:
            self.game_state.swipe_left()
        elif action == 1:
            self.game_state.swipe_up()
        elif action == 2:
            self.game_state.swipe_right()
        elif action == 3:
            self.game_state.swipe_down()
    
    def reset(self):
        self.env_steps = 0

        self.game_state = GameState.generate_game_state(self.blocks, self.walls, self.rows, self.cols)
        return self.game_state

    def render(self, mode='human'):
        if (mode == 'human'):
            print(self.game_state)

    def __done(self):
        if self.env_steps > self.max_steps:
            return True

        return self.game_state.is_game_over()

    def __reward(self):
        if self.__done(): return self.reward_finish
        return self.penalty_step * self.env_steps

ACTIONS = {
    0: "SWIPE LEFT",
    1: "SWIPE UP",
    2: "SWIPE RIGHT",
    3: "SWIPE DOWN"
}