import numpy as np
import gym
import matchthetiles

from copy import deepcopy
import sys

from collections import defaultdict

def q_learn(env, n_episodes = 10000, max_steps = 100, exploration_prob = 1, min_exploration_prob = 0.01, exploration_decay = 0.001, gamma = 0.9, learn_rate = 0.1):
    print("Q_LEARN")
    print(f"Exploration probability - {exploration_prob}")
    print(f"Exploration decay - {exploration_decay}")
    print(f"Gamma - {gamma}")
    print(f"Learn Rate - {learn_rate}")
    observation_space = env.observation_space
    action_space = env.action_space
    # Q-Table
    #q_table = defaultdict(lambda: [0] * action_space.n)
    q_table = np.zeros((observation_space.n, action_space.n))

    states_explored = 0
    states_ids = dict()

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

    print("Mean rewards per episodes")
    for i in range(10):
        print(f"{i * n_episodes // 10}-{(i+1)*n_episodes // 10 - 1}, {np.mean(reward_per_episode[i * n_episodes // 10 : (i + 1) * n_episodes // 10 - 1])}")
        
def sarsa(env, n_episodes = 10000, max_steps = 100, exploration_prob = 1, min_exploration_prob = 0.01, exploration_decay = 0.001, gamma = 0.9, learn_rate = 0.1):
    print("SARSA")
    print(f"Exploration probability - {exploration_prob}")
    print(f"Exploration decay - {exploration_decay}")
    print(f"Gamma - {gamma}")
    print(f"Learn Rate - {learn_rate}")
    observation_space = env.observation_space
    action_space = env.action_space
    # Q-Table
    #q_table = defaultdict(lambda: [0] * action_space.n)
    q_table = np.zeros((observation_space.n, action_space.n))

    states_explored = 0
    states_ids = dict()

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

            if np.random.uniform(0, 1) < exploration_prob:
                # Mutation
                next_action = action_space.sample()
            else:
                next_action = np.argmax(q_table[new_state_id, :])

            q_table[state_id, action] = q_table[state_id, action] + learn_rate * (reward + gamma * q_table[new_state_id, next_action] - q_table[state_id, action])

            #print(f"Episode {ep} - Step {step} - Reward : {reward} - max {max(q_table[next_state])} - current {q_table[current_state][action]}")
            epsiode_reward += reward

            if done: break

            current_state = deepcopy(next_state)

        exploration_prob = max(min_exploration_prob, np.exp(-exploration_decay * ep))
        reward_per_episode.append(epsiode_reward)

    print("Q-table")
    print(q_table, end="\n\n")

    print("Mean rewards per episodes")
    for i in range(10):
        print(f"{i * n_episodes // 10}-{(i+1)*n_episodes // 10 - 1}, {np.mean(reward_per_episode[i * n_episodes // 10 : (i + 1) * n_episodes // 10 - 1])}")


def run_algorithm(env_id):
    env = gym.make(env_id)
    sys.stdout = open("statistics/algorithms_" + env_id + ".txt", "w+")

    # Q_LEARN
    q_learn(env, exploration_prob=1, exploration_decay=0.001, gamma=0.9, learn_rate=0.1)

    q_learn(env, exploration_prob=1, exploration_decay=0.001, gamma=0.9, learn_rate=0.3)
    q_learn(env, exploration_prob=1, exploration_decay=0.001, gamma=0.9, learn_rate=0.05)

    q_learn(env, exploration_prob=1, exploration_decay=0.001, gamma=1.0, learn_rate=0.1)
    q_learn(env, exploration_prob=1, exploration_decay=0.001, gamma=0.6, learn_rate=0.1)

    q_learn(env, exploration_prob=1, exploration_decay=0.006, gamma=0.9, learn_rate=0.1)

    # SARSA
    sarsa(env, exploration_prob=1, exploration_decay=0.001, gamma=0.9, learn_rate=0.1)

    sarsa(env, exploration_prob=1, exploration_decay=0.001, gamma=0.9, learn_rate=0.3)
    sarsa(env, exploration_prob=1, exploration_decay=0.001, gamma=0.9, learn_rate=0.05)

    sarsa(env, exploration_prob=1, exploration_decay=0.001, gamma=1.0, learn_rate=0.1)
    sarsa(env, exploration_prob=1, exploration_decay=0.001, gamma=0.6, learn_rate=0.1)

    sarsa(env, exploration_prob=1, exploration_decay=0.006, gamma=0.9, learn_rate=0.1)
