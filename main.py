import math
import tensorflow as tf
from tensorflow import keras
import numpy as np
from time import time


from FieldDisplay import FieldDisplay

def train_reinforcement_network(n_neurons, thresh=0.1, gamma=0.8, eps=np.finfo(np.float32).eps.item()):
    optimizer = keras.optimizers.Adam(learning_rate=0.01)
    huber_loss = keras.losses.Huber()
    action_probs_history = []
    critic_value_history = []
    rewards_history = []

    inputs = keras.layers.Input(shape=(3,))

    common = keras.layers.Dense(n_neurons, activation="relu")(inputs)
    action = keras.layers.Dense(FieldDisplay.N_INPUTS, activation="softmax")(common)
    critic = keras.layers.Dense(1)(common)

    # The full RL model with the action layer and the critic
    model = keras.Model(inputs=inputs, outputs=[action, critic])

    running_reward = 0

    best_error = 1
    while thresh <= best_error:
        # Reward for the current run
        episode_reward = 0

        robot = FieldDisplay(ROBOT_INIT_X=10, ROBOT_INIT_Y=10, ROBOT_INIT_HEADING=-90, GUI=False, TELEMETRY=False)

        robot.set_objective("Intake", "intake", 70.5, 70.5)
        robot.set_objective("Deposit", "deposit", 100, 70.5)

        start_time = time()
        prog_bar = keras.utils.Progbar(1)
        while robot.running:
            with tf.GradientTape() as tape:
                state = tf.convert_to_tensor(robot.robot_kinematics.get_robot_state())
                state = tf.expand_dims(state, 0)

                action_probs, critic_value = model(state)
                critic_value_history.append(critic_value[0, 0])

                reward = robot.take_action(action)
                prog_bar.update(reward)
                rewards_history.append(reward)
                episode_reward += reward

                running_reward = 0.05 * episode_reward + (1 - 0.05) * running_reward

                # Calculate expected value from rewards
                returns = []
                discounted_sum = 0
                for r in rewards_history[::-1]:
                    discounted_sum = r + gamma * discounted_sum
                    returns.insert(0, discounted_sum)

                # Normalize
                returns = np.array(returns)
                returns = (returns - np.mean(returns)) / (np.std(returns) + eps)
                returns = returns.tolist()

                # Calculating loss values to update our network
                history = zip(action_probs_history, critic_value_history, returns)
                actor_losses = []
                critic_losses = []
                for log_prob, value, ret in history:
                    diff = ret - value
                    actor_losses.append(-log_prob * diff)  # actor loss

                    critic_losses.append(huber_loss(tf.expand_dims(value, 0), tf.expand_dims(ret, 0)))

                # Backpropagation
                loss_value = sum(actor_losses) + sum(critic_losses)
                grads = tape.gradient(loss_value, model.trainable_variables)
                optimizer.apply_gradients(zip(grads, model.trainable_variables))

                robot()

train_reinforcement_network(10)
