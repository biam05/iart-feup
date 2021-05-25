import numpy as np
import gym
import matchthetiles

from copy import deepcopy

from collections import defaultdict

env = gym.make("match-the-tiles-v0")

observation_space = env.observation_space
action_space = env.action_space

# Q-Table
#q_table = defaultdict(lambda: [0] * action_space.n)
q_table = np.zeros((observation_space.n, action_space.n))

states_explored = 0
states_ids = dict()

# Number of episodes
n_episodes = 1000
# Maximum number of steps per episode
max_steps = 100

# Exploration probability
exploration_prob = 1

# Exploration decay for exponential decreasing
exploration_decay = 0.001

# Minimum exploration probability
min_exploration_prob = 0.01

# Discount factor
gamma = 0.9

# Learning rate
learn_rate = 0.1

# Q-learning
reward_per_episode = list()

for ep in range(n_episodes):
    current_state = env.reset()

    done = False

    epsiode_reward = 0

    for step in range(max_steps):

        state_id = states_ids.get(current_state, states_explored)

        if (current_state not in states_ids):
            states_ids[current_state] = states_explored
            states_explored += 1

        if np.random.uniform(0, 1) < exploration_prob:
            # Mutation
            action = action_space.sample()
        else:
            action = np.argmax(q_table[state_id, :])

        next_state, reward, done, info = env.step(action)

        new_state_id = states_ids.get(next_state, states_explored)

        if (next_state not in states_ids):
            states_ids[next_state] = states_explored
            states_explored += 1

        q_table[state_id, action] = q_table[state_id, action] + learn_rate * (reward + gamma * max(q_table[new_state_id, :]) - q_table[state_id, action])

        #print(f"Episode {ep} - Step {step} - Reward : {reward} - max {max(q_table[next_state])} - current {q_table[current_state][action]}")
        epsiode_reward += reward

        if done: break

        current_state = deepcopy(next_state)

    exploration_prob = max(min_exploration_prob, np.exp(-exploration_decay * ep))
    reward_per_episode.append(epsiode_reward)

print("Q-table")
print(q_table, end="\n\n")

print("Reward per episodes")
for i in range(10):
    print(f"\tMean reward on episode {i * n_episodes // 10}-{(i+1)*n_episodes // 10 - 1} : {np.mean(reward_per_episode[i * n_episodes // 10 : (i + 1) * n_episodes // 10 - 1])}")
