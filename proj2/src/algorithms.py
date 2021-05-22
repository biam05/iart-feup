import numpy as np
import gym
import matchthetiles

env = gym.make("match-the-tiles-v0")

observation_space = env.observation_space
action_space = env.action_space

# Q-Table
q_table = np.zeros((observation_space, action_space))

# Number of episodes
n_episodes = 10000
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

        if np.random.uniform(0, 1) < exploration_prob:
            # Mutation
            action = np.random.randint(0, action_space)
        else:
            action = np.argmax(q_table[current_state, :])

        next_state, reward, done, info = env.step(action)

        q_table[current_state, action] = (1 - learn_rate) * q_table[current_state, action] + learn_rate * (reward + gamma * max(q_table[next_state, :]))

        epsiode_reward += reward

        if done: break

        current_state = next_state

    exploration_prob = max(min_exploration_prob, np.exp(-exploration_decay * ep))
    reward_per_episode.append(epsiode_reward)

print("Reward per episodes")

for i in range(10):
    print(f"Mean reward on episode {i * 1000}-{(i+1)*1000 - 1} : {np.mean(reward_per_episode[i * 1000 : (i + 1) * 1000 - 1])}")