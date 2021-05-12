import gym
from gym import spaces

from scipy.special import perm

class MTT_4x4_1B(gym.Env):
    def __init__(self):
        # Constants
        self.penalty_step = 1
        self.reward_finish = 20
        self.reward_move_on_goal = 5
        self.penalty_move_off_goal = -2
        self.penalty_per_dist_unit = -0.5
        self.max_steps = 16

        # Environment variables
        self.env_steps = 0
        
        self.game_state = None
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(perm(16, 1, exact=True))

    def step(self, action):
        assert action in ACTIONS

        self.env_steps += 1

        moved_to_goal, moved_off_goal = self.__move(action)

        reward = self.__reward(moved_to_goal, moved_off_goal)

        done = self.__done()

        observation = self.game_state

        info = {
            "action_move": ACTIONS[action]
        }

        return observation, reward, done, info
    
    def __move(self, action : int):
        moved_to_goal = 0
        moved_off_goal = 0
        if action == 0:
            moved_to_goal, moved_off_goal = self.game_state.swipe_left()
        elif action == 1:
            moved_to_goal, moved_off_goal = self.game_state.swipe_up()
        elif action == 2:
            moved_to_goal, moved_off_goal = self.game_state.swipe_right()
        elif action == 3:
            moved_to_goal, moved_off_goal = self.game_state.swipe_down()
    
        return moved_to_goal, moved_off_goal

    def reset(self):
        # generate gamestate
        return None

    def __done(self):
        if self.env_steps > self.max_steps:
            return True

        return self.game_state.is_game_over()

    def __reward(self, moved_to_goal, moved_off_goal):
        reward = self.penalty_step * self.env_steps

        reward += moved_to_goal * self.reward_move_on_goal
        reward += moved_off_goal * self.penalty_move_off_goal

        reward += self.penalty_per_dist_unit * self.game_state.euclidean_distance()

        reward += self.game_state.number_of_blocks_on_goals()

        if (self.game_state.is_game_over):
            reward += self.reward_finish

        return reward

ACTIONS = {
    0: "SWIPE LEFT",
    1: "SWIPE UP",
    2: "SWIPE RIGHT",
    3: "SWIPE DOWN"
}