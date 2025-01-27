import gym
import numpy as np
import neural_network as nn
import random
import time

env = gym.make('CartPole-v0')

#hyperparameters
learning_rate = 0.0005
discount_rate = .99
max_steps = 500
num_episodes = 100000
num_steps_until_reset_target = 50000
batch_size = 50

#exploration rate values
eps = 1
min_eps_val = 0.01
max_eps_val = 1
eps_decay_rate = 0.001

#initialize replay memory
replay_memory = []
replay_memory_size = 50000

#initializes the networks
network = nn.Neural_Network(4, learning_rate, discount_rate)
network.add_layer(16)
network.add_layer(16)
network.add_layer(16)
network.add_layer(2)

rewards = []
avg = 0
total_steps = 0

for episode in range(num_episodes):
    # if episode % 200 == 0:
    # print(episode)
    state = env.reset()
    done = False
    current_reward = 0

    for step in range(max_steps):
        
        # if (total_steps > 10000):
        #     env.render()
        #     time.sleep(0.2)
        #updates the target network
        if total_steps % num_steps_until_reset_target == 0:
            network.update_target_network()

        #Selects action via exploration or exploitation
        if np.random.random_sample() > eps:
            action = network.return_max_q(state)
        else:
            action = env.action_space.sample()

        #execute selected action
        new_state, reward, done, info = env.step(action)

        experience = (state, action, reward, new_state, done)
        #store in replay memory
        if len(replay_memory) < replay_memory_size:
             replay_memory.append(experience)
        else:
            replay_memory[total_steps % replay_memory_size] = experience
        total_steps += 1

        if len(replay_memory) >= batch_size:
            batch = random.sample(replay_memory, batch_size)
            network.epoch(batch)

        current_reward += reward

        state = new_state

        if done == True:
            break
    
    #decays the epsilon
    eps = min_eps_val + (max_eps_val - min_eps_val) * np.exp(-eps_decay_rate*episode)
    avg += current_reward
    if episode % 1000 == 0:
        print(avg / 1000)
        avg = 0
        rewards.append(current_reward)

#displays a taxi game with final q values
# state = env.reset()
# total_rewards = 0
# for _ in range(max_steps):
#     env.render()
#     action = network.return_max_q(state)

#     new_state, reward, done, info = env.step(action)

#     state = new_state
#     total_rewards += reward

#     if done:
#         print("Score: ", total_rewards)
#         break
        
env.close()
# rewards = np.array(rewards)
# print("Average reward per thousand: ", np.mean(rewards))
# for i, r in rewards:
#     print(i*1000, ": ", r)

