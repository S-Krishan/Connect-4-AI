import random
import numpy as np

class Connect4Env: #sets up the connect 4 environment which the agent will learn from
    def __init__(self):
        self.rows=6
        self.columns=7
        self.board=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.turn=1
    def reset(self):
        self.board=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.turn=1
        self.game_over=False
        return self.board
    def step(self,action):
        if self.game_over:
            raise Exception("Game is over, reset environment to restart the game")
        if self.board[action][0]==self.turn:
            raise Exception("Move not possible, column is full")
        elif self.board[action][-1] == 0:

            self.board[action][-1] = self.turn
            reward = 0
        else:
            firstTime = True
            for i in range(0, len(self.board[action]) - 1):

                if self.board[action][i] == 0:
                    pass
                if self.board[action][i + 1] == self.turn and firstTime:
                    firstTime = False
                    self.board[action][i] = self.turn

            row_max = self.rows
            column_max = self.columns
            reward=None
            #win check
            # check rows
            for x in range(0, row_max):

                for y in range(0, column_max - 3):
                    if self.board[y][x] == 1 and self.board[y + 1][x] == 1 and self.board[y + 2][x] == 1 and self.board[y + 3][x] == 1:
                        reward=-1
                        self.game_over = True
                    elif self.board[y][x] == 2 and self.board[y + 1][x] == 2 and self.board[y + 2][x] == 2 and self.board[y + 3][x] == 2:
                        reward=1
                        self.game_over = True

            # check columns
            for x in range(0, column_max):

                for y in range(0, row_max - 3):
                    if self.board[x][y] == 1 and self.board[x][y + 1] == 1 and self.board[x][y + 2] == 1 and self.board[x][y + 3] == 1:
                        reward=-1
                        self.game_over = True
                    elif self.board[x][y] == 2 and self.board[x][y + 1] == 2 and self.board[x][y + 2] == 2 and self.board[x][y + 3] == 2:
                        reward=1
                        self.game_over = True

            # Check diagonals (bottom-left to top-right)
            for x in range(0, column_max - 3):
                for y in range(0, row_max - 3):
                    if self.board[x][y] == self.board[x + 1][y + 1] == self.board[x + 2][y + 2] == self.board[x + 3][y + 3] != 0:
                        if self.board[x][y] == 1:
                            reward= -1
                            self.game_over = True
                        else:
                            reward= 1
                            self.game_over = True

            # Check diagonals (top-left to bottom-right)
            for x in range(0, column_max - 3):
                for y in range(3, row_max):
                    if self.board[x][y] == self.board[x + 1][y - 1] == self.board[x + 2][y - 2] == self.board[x + 3][y - 3] != 0:
                        if self.board[x][y] == 1:
                            reward= -1
                            self.game_over = True
                        else:
                            reward= 1
                            self.game_over = True
            #draw check
            full_count=0
            if reward==None:
                for column in range(0,column_max):
                    if self.board[action][0] == 1 or self.board[action][1] == 2:
                        full_count+=1
                if full_count==column_max:
                    reward=0
                    self.game_over=True
                else: #neither win,lose nor draw
                    reward=0
                    if self.turn == 1:
                        self.turn = 2
                    if self.turn == 2:
                        self.turn = 1
        return self.board, reward, self.game_over
    def render(self):
        print(self.board)

import tensorflow
from tensorflow.keras import layers, models

def build_model():
    model = models.Sequential()
    model.add(layers.Input(shape=(42,)))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(7, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    return model
model=build_model()

class DQNAgent:
    def __init__(self, model):
        self.model = model
        self.target_model = self.build_target_model()  # Initialize target model
        self.target_update_counter=0
        self.memory = [] #initialise memory that is used for experience replay

        self.gamma = 0.95  # Discount factor - makes it so that rewards further in the future are prioritised less
        self.epsilon = 1.0  # Exploration rate - this is the percentage that represents how likely the agent is to experiment
        self.epsilon_decay = 0.995 #we want the model to explore less and rely more on the model over time as the model gets more accurate
        self.epsilon_min = 0.1 #we want the ai to experiment a little even at the end to continously learn new strategies
    def build_target_model(self):
        # Assuming 'model' is a Keras model, you can clone it for the target model
        target_model = tensorflow.keras.models.clone_model(self.model)
        target_model.set_weights(self.model.get_weights())
        return target_model
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def act(self, state):
        if np.random.rand() <= self.epsilon: #at the start the agent will experiment a lot
            return random.choice(self.available_actions(state)) #a new random move is tried
        act_values = self.model.predict(state)
        return np.argmax(act_values[0]) #otherwise the model is used to predict the highest q value

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) #all the information about the step that occured are sent to be used as training data

    def train(self, batch_size=32):
        minibatch = random.sample(self.memory, batch_size) #choose a random batch to train from to prevent catastrophic forgetting if it learns things in a sequence
        for state, action, reward, next_state, done in minibatch:
            target = reward #if we are going to a terminal state the target q value is just the reward
            if not done:
                target = reward + self.gamma * np.amax(self.target_model.predict(next_state)[0]) #If not use the Bellman equation to work out the max q value of the predicted best action of the next state (with the dicount in order to take into account future rewards) plus the immediate reward
            target_f = self.model.predict(state) #create a copy of the q network and output the values
            target_f[0][action] = target #change the q value of just the action we are analysing to the target value calculated earlier
            self.model.fit(state, target_f, epochs=1, verbose=0) #The mean squared error between the output of the q network (input is the state) and the output of the t network is calculated. This cost is then used to backpropagate throught the q network and update the weights to make better predictions in the future

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay #Lower how much the agent experiments


        self.target_update_counter += 1
        if self.target_update_counter % 10 == 0:  #Update the target network every 10 training steps
            self.update_target_model()

    def available_actions(self, state):
            # Return list of available columns (not full)
            return [col for col in range(7) if state[0, col * 6] == 0]

env = Connect4Env()  # Use your Connect 4 environment
agent = DQNAgent(model)

episodes = 1000 #amount of games played
for e in range(episodes):
    state = env.reset() #reset the connect 4 environment every episode
    state = np.reshape(state, [1, 42]) #flatten the state array so it can be used in the neural network
    for time in range(500): #500 is the max time limit before moving onto the next episode
        action = agent.act(state) #the q network uses an e greedy policy to make a move in the current state
        next_state, reward, game_over = env.step(action) #the move is sent to the enironment which returns the updated board, reward from that move, and if the game is over
        next_state = np.reshape(next_state, [1, 42]) #flatten the next_state array so it can be used in the neural network
        agent.remember(state, action, reward, next_state, game_over) #the information from that move is sent to the memory for experience replay
        state = next_state #the state is updated to the new board
        if game_over:
            print(f"Episode: {e}/{episodes}, Score: {time}, Epsilon: {agent.epsilon:.2}")
            break
        if len(agent.memory) > 32:
            agent.train(32) #Train the agent on a random minibatch of 32 once the memory has that many training examples





