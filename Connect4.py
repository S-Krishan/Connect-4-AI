import pygame as p
import random
import math
import time










p.init()
# Display screen
X=800
Y=600
screen=p.display.set_mode((X,Y),p.SCALED,vsync=1)

run=True

startTurn=random.randint(0,1)
if startTurn==0:
    turn="Red"
else:
    turn="Yellow"

#Fill background with sky blue
screen.fill((173,216,230))

imp = p.image.load("Subtract.png").convert_alpha()
coinR=p.image.load("coint.png").convert_alpha()
coinTransparent=p.image.load("Mask group-2.png").convert_alpha()
coinY=p.image.load("Yellow coin.png").convert_alpha()
redWin=p.image.load("Red logo.png").convert_alpha()
yellowWin=p.image.load("Yellow logo.png").convert_alpha()

coinR=p.transform.scale(coinR,(61,61))
imp=p.transform.smoothscale(imp,(525, 412.5))
coinTransparent=p.transform.scale(coinTransparent,(61,61))
coinY=p.transform.scale(coinY,(61,61))

board=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]


import numpy as np

class Connect4Env: #sets up the connect 4 environment which the agent will learn from
    def __init__(self):
        self.rows=6
        self.columns=7
        self.board=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.starting_turn=1
    def reset(self):
        self.board=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.starting_turn=random.randint(1,2)
        self.game_over=False
        return self.board
    def step(self,action,depth):
        if self.game_over:
            raise Exception("Game is over, reset environment to restart the game")
        if action==-1:
            move=bestMoveMiniMaxAI(self.board, depth)
            for i in range(len(self.board[move]) - 1, -1, -1):
                if self.board[move][i] == 0:  # Check if the slot is empty
                    self.board[move][i] = 1  # Place the current player's piece
                    break  # Exit the loop after placing the piece
            reward=0
            return self.board, reward, self.game_over

        if self.board[action][0]!=0:
            reward=-100
            self.game_over = True
            return self.board, reward, self.game_over

        initial_reward=self.calculate_reward(self.board)
        reward=0


        for i in range(len(self.board[action]) - 1, -1, -1):
                if self.board[action][i] == 0:  # Check if the slot is empty
                    self.board[action][i] = 2  # Place the current player's piece
                    break  # Exit the loop after placing the piece

        row_max = self.rows
        column_max = self.columns
        not_draw=None
        #win check
        # check rows
        for x in range(0, row_max):

                for y in range(0, column_max - 3):

                    if self.board[y][x] == 2 and self.board[y + 1][x] == 2 and self.board[y + 2][x] == 2 and self.board[y + 3][x] == 2:
                        reward=1
                        not_draw=1
                        self.game_over=True


        # check columns
        for x in range(0, column_max):

                for y in range(0, row_max - 3):

                    if self.board[x][y] == 2 and self.board[x][y + 1] == 2 and self.board[x][y + 2] == 2 and self.board[x][y + 3] == 2:
                        reward=1
                        not_draw=1
                        self.game_over = True

        # Check diagonals (bottom-left to top-right)
        for x in range(0, column_max - 3):
                for y in range(0, row_max - 3):
                    if self.board[x][y] == self.board[x + 1][y + 1] == self.board[x + 2][y + 2] == self.board[x + 3][y + 3] != 0:
                        if self.board[x][y] == 2:
                            reward=1
                            not_draw= 1

                            self.game_over = True


        # Check diagonals (top-left to bottom-right)
        for x in range(0, column_max - 3):
                for y in range(3, row_max):
                    if self.board[x][y] == self.board[x + 1][y - 1] == self.board[x + 2][y - 2] == self.board[x + 3][y - 3] != 0:
                        if self.board[x][y] == 2:
                            reward=1
                            not_draw= 1

                            self.game_over = True

        #draw check
        full_count=0
        if not_draw==None:
                for column in range(0,column_max):
                    if self.board[column][0] == 1 or self.board[column][0] == 2:
                        full_count+=1
                if full_count==column_max:

                    self.game_over=True

        final_reward = self.calculate_reward(self.board)
        if reward!=1:
            reward = final_reward - initial_reward
        else:
            reward=1
        """"
        pen_actions = []
        for x in range(0, column_max):

            for y in range(0, row_max - 3):
                sequence = [board[x][y + i] for i in range(0, 4)]
                if (sequence.count(2) == 3 and sequence.count(1) == 1) or (
                        sequence.count(2) == 2 and sequence.count(1) == 1 and sequence.count(0) == 1):
                    pen_actions.append(x)
        if action in pen_actions:
            reward -= 0.1
        """

        #minimax turn
        if self.game_over==False:
            not_draw=None
            move = bestMoveMiniMaxAI(self.board, depth)
            if self.board[move][0] != 0:
                reward = 0
                self.game_over = True
                return self.board, reward, self.game_over



            else:
                for i in range(len(self.board[move]) - 1, -1, -1):
                    if self.board[move][i] == 0:  # Check if the slot is empty
                        self.board[move][i] = 1  # Place the current player's piece
                        break  # Exit the loop after placing the piece
            #check rows
            for x in range(0, row_max):

                    for y in range(0, column_max - 3):
                        if self.board[y][x] == 1 and self.board[y + 1][x] == 1 and self.board[y + 2][x] == 1 and self.board[y + 3][x] == 1:
                            not_draw=1
                            reward=-1
                            self.game_over = True



            # check columns
            for x in range(0, column_max):

                    for y in range(0, row_max - 3):
                        if self.board[x][y] == 1 and self.board[x][y + 1] == 1 and self.board[x][y + 2] == 1 and self.board[x][y + 3] == 1:
                            not_draw=1
                            reward=-1
                            self.game_over = True


            # Check diagonals (bottom-left to top-right)
            for x in range(0, column_max - 3):
                    for y in range(0, row_max - 3):
                        if self.board[x][y] == self.board[x + 1][y + 1] == self.board[x + 2][y + 2] == self.board[x + 3][y + 3] != 0:
                            if self.board[x][y] == 1:
                                not_draw= 1
                                reward=-1
                                self.game_over = True


            # Check diagonals (top-left to bottom-right)
            for x in range(0, column_max - 3):
                    for y in range(3, row_max):
                        if self.board[x][y] == self.board[x + 1][y - 1] == self.board[x + 2][y - 2] == self.board[x + 3][y - 3] != 0:
                            if self.board[x][y] == 1:
                                not_draw= 1
                                reward=-1
                                self.game_over = True

            #draw check
            full_count=0
            if not_draw==None:
                    for column in range(0,column_max):
                        if self.board[column][0] == 1 or self.board[column][0] == 2:
                            full_count+=1
                    if full_count==column_max:

                        self.game_over=True










        return self.board, reward, self.game_over
    def calculate_reward(self,board):
        reward = 0

        two_in_a_row = 0.001
        three_in_a_row = 0.01

        block = 0.9

        def score_calculation(seq):


            if seq.count(1) == 3 and seq.count(2) == 1:
                return block


            elif seq.count(2) == 3 and seq.count(0) == 1:
                return three_in_a_row

            elif seq.count(2) == 2 and seq.count(0) == 2:
                return two_in_a_row
            return 0

        row_max = len(board[0])
        column_max = len(board)

        # Four in a row
        # check rows
        for x in range(0, row_max):

            for y in range(0, column_max - 3):
                sequence = [board[y + i][x] for i in range(0, 4)]
                reward += score_calculation(sequence)

        # check columns
        for x in range(0, column_max):

            for y in range(0, row_max - 3):
                sequence = [board[x][y + i] for i in range(0, 4)]
                reward += score_calculation(sequence)
        # Check diagonals (bottom-left to top-right)
        for x in range(0, column_max - 3):
            for y in range(0, row_max - 3):
                sequence = [board[x + i][y + i] for i in range(0, 4)]
                reward += score_calculation(sequence)
        # Check diagonals (top-left to bottom-right)
        for x in range(0, column_max - 3):
            for y in range(3, row_max):
                sequence = [board[x + i][y - i] for i in range(0, 4)]
                reward += score_calculation(sequence)

        return reward
    def render(self):
        print(self.board)

import tensorflow
from tensorflow.keras import layers, models

def build_model():
    model = models.Sequential() #try replacing with a cnn
    model.add(layers.Input(shape=(42,)))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(7))
    optimizer = tensorflow.keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    return model
model=build_model()


class DQNAgent:
    def __init__(self, model):
        self.model = model
        self.target_model = self.build_target_model()  # Initialize target model
        self.target_update_counter=0
        self.memory = [] #initialise memory that is used for experience replay

        self.gamma = 0.95  # Discount factor - makes it so that rewards further in the future are prioritised less


    def build_target_model(self):
        # Assuming 'model' is a Keras model, you can clone it for the target model
        target_model = tensorflow.keras.models.clone_model(self.model)
        target_model.set_weights(self.model.get_weights())
        return target_model
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def act(self, epsilon,state):
        if np.random.rand() <= epsilon: #at the start the agent will experiment a lot
            return random.choice(self.available_actions(state)) #a new random move is tried
        act_values = self.model.predict(state)
        for i in range(0,7):
            if state[0][i*6]!=0:
                act_values[0][i]=-np.inf


        return np.argmax(act_values)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) #all the information about the step that occured are sent to be used as training data

    def train(self, batch_size=32):



        minibatch = random.sample(self.memory, batch_size) #choose a random batch to train from to prevent catastrophic forgetting if it learns things in a sequence
        for state, action, reward, next_state, done in minibatch:
            target = reward #if we are going to a terminal state the target q value is just the reward
            if not done:
                target = reward + (self.gamma * np.amax(self.target_model.predict(next_state)[0])) #If not use the Bellman equation to work out the max q value of the predicted best action of the next state (with the dicount in order to take into account future rewards) plus the immediate reward
            target_f = self.model.predict(state)
            #create a copy of the q network and output thes values
            target_f[0][action] = target #change the q value of just the action we are analysing to the target value calculated earlier


            self.model.fit(state, target_f, epochs=1, verbose=0) #The mean squared error between the output of the q network (input is the state) and the output of the t network is calculated. This cost is then used to backpropagate throught the q network and update the weights to make better predictions in the future




        self.target_update_counter += 1
        if self.target_update_counter % 10 == 0:  #Update the target network every 10 training steps
            self.update_target_model()

    def available_actions(self, state):
            # Return list of available columns (not full)
            return [col for col in range(7) if state[0, col * 6] == 0]



def red_counter_drop(board,columnNo):
    if board[columnNo][0]==1 or board[columnNo][0]==2:

        resultY="Full"
    elif board[columnNo][-1]==0:
        resultY=len(board[columnNo])-1
        board[columnNo][-1]=1
    else:
        firstTime=True
        for i in range(0,len(board[columnNo])-1):

            if board[columnNo][i]==0:
                resultY=i
            if (board[columnNo][i+1]==1 or board[columnNo][i+1]==2) and firstTime:
                firstTime=False
                board[columnNo][i] = 1
    return resultY

def yellow_counter_drop(board,columnNo):
    if board[columnNo][0]==1 or board[columnNo][0]==2:

        resultY="Full"
    elif board[columnNo][-1]==0:
        resultY=len(board[columnNo])-1
        board[columnNo][-1]=2
    else:
        firstTime = True
        for i in range(0,len(board[columnNo])-1):
            if board[columnNo][i]==0:
                resultY=i
            if (board[columnNo][i+1]==1 or board[columnNo][i+1]==2) and firstTime:
                firstTime=False
                board[columnNo][i] = 2
    return resultY


def counter_animation(coin,column,row):

    column_cord=151.7+(71.8*column)
    starting_row_cord=112.5
    ending_row_cord=112.5+(66.245*(row+1))
    value=board[column][row]
    board[column][row]=0
    velocity=0
    acceleration=0.7
    position=starting_row_cord

    while position<ending_row_cord:
        screen.fill((173, 216, 230))
        update_red_counters(board)
        update_yellow_counters(board)

        screen.blit(coin, (column_cord,position))

        screen.blit(imp, (137.5, 170))
        p.display.update()

        p.time.wait(1)
        velocity+=acceleration
        position+=velocity

        if position>ending_row_cord:
            position=ending_row_cord

    board[column][row] = value
    screen.fill((173, 216, 230))
    update_red_counters(board)
    update_yellow_counters(board)
    screen.blit(coin, (column_cord,ending_row_cord))
    screen.blit(imp, (137.5, 170))
    p.display.update()

    result = win_check(board)
    return result

def update_red_counters(board):
    for column in range(0,len(board)):
        for row in range(0,len(board[column])):
            if board[column][row]==1:
                column_cord=151.7+(71.8*column)
                row_cord = 112.5 + (66.245 * (row+1))
                screen.blit(coinR, (column_cord, row_cord))

def update_yellow_counters(board):
    for column in range(0,len(board)):
        for row in range(0,len(board[column])):
            if board[column][row]==2:
                column_cord=151.7+(71.8*column)
                row_cord = 112.5 + (66.245 * (row+1))
                screen.blit(coinY, (column_cord, row_cord))

def win_check(board):


    row_max=len(board[0])
    column_max=len(board)
    #check rows
    for x in range(0,row_max):

        for y in range(0,column_max-3):
            if board[y][x]==1 and board[y+1][x]==1 and board[y+2][x]==1 and board[y+3][x]==1:
                return "Red"
            elif board[y][x]==2 and board[y+1][x]==2 and board[y+2][x]==2 and board[y+3][x]==2:
                return "Yellow"

    #check columns
    for x in range(0,column_max):

        for y in range(0,row_max-3):
            if board[x][y]==1 and board[x][y+1]==1 and board[x][y+2]==1 and board[x][y+3]==1:
                return "Red"
            elif board[x][y]==2 and board[x][y+1]==2 and board[x][y+2]==2 and board[x][y+3]==2:
                return "Yellow"

    # Check diagonals (bottom-left to top-right)
    for x in range(0,column_max - 3):
            for y in range(0,row_max - 3):
                if board[x][y] == board[x + 1][y + 1] == board[x + 2][y + 2] == board[x + 3][y + 3] != 0:
                    if board[x][y] == 1:
                        return "Red"
                    else:
                        return "Yellow"

    # Check diagonals (top-left to bottom-right)
    for x in range(0,column_max - 3):
            for y in range(3, row_max):
                if board[x][y] == board[x + 1][y - 1] == board[x + 2][y - 2] == board[x + 3][y - 3] != 0:
                    if board[x][y] == 1:
                        return "Red"
                    else:
                        return "Yellow"




    return False


def evaluate(board):
    score=0

    two_in_a_row=+10
    three_in_a_row=+1000
    four_in_a_row=+100000
    block=+5000

    def score_calculation(seq):
        if seq.count(1)==4:
            return -four_in_a_row
        elif seq.count(2)==4:
            return four_in_a_row
        elif seq.count(1)==3 and seq.count(2)==1:
            return block
        elif seq.count(2)==3 and seq.count(1)==1:
            return -block
        elif seq.count(1)==3 and seq.count(0)==1:
            return -three_in_a_row
        elif seq.count(2)==3 and seq.count(0)==1:
            return three_in_a_row
        elif seq.count(1)==2 and seq.count(0)==2:
            return -two_in_a_row
        elif seq.count(2)==2 and seq.count(0)==2:
            return two_in_a_row
        return 0



    row_max=len(board[0])
    column_max=len(board)

    # Four in a row
    #check rows
    for x in range(0,row_max):

        for y in range(0,column_max-3):
            sequence=[board[y+i][x] for i in range(0,4)]
            score+=score_calculation(sequence)

    #check columns
    for x in range(0,column_max):

        for y in range(0,row_max-3):
            sequence = [board[x][y+i] for i in range(0, 4)]
            score += score_calculation(sequence)
    # Check diagonals (bottom-left to top-right)
    for x in range(0,column_max - 3):
            for y in range(0,row_max - 3):
                sequence = [board[x+i][y+i] for i in range(0, 4)]
                score += score_calculation(sequence)
    # Check diagonals (top-left to bottom-right)
    for x in range(0,column_max - 3):
            for y in range(3, row_max):
                sequence = [board[x + i][y - i] for i in range(0, 4)]
                score += score_calculation(sequence)

    return score

def make_move(old_board,columnNo,player):
    new_board = [column[:] for column in old_board]
    if new_board[columnNo][0]==1 or new_board[columnNo][0]==2:

        pass
    elif new_board[columnNo][-1]==0:

        new_board[columnNo][-1]=player
    else:
        firstTime = True
        for i in range(0,len(new_board[columnNo])-1):

            if (new_board[columnNo][i+1]==1 or new_board[columnNo][i+1]==2) and firstTime:
                firstTime=False
                new_board[columnNo][i] = player
    return new_board

def game_over(board):
    row_max = len(board[0])
    column_max = len(board)
    # check rows
    for x in range(0, row_max):

        for y in range(0, column_max - 3):
            if board[y][x] == 1 and board[y + 1][x] == 1 and board[y + 2][x] == 1 and board[y + 3][x] == 1:
                return True
            elif board[y][x] == 2 and board[y + 1][x] == 2 and board[y + 2][x] == 2 and board[y + 3][x] == 2:
                return True

    # check columns
    for x in range(0, column_max):

        for y in range(0, row_max - 3):
            if board[x][y] == 1 and board[x][y + 1] == 1 and board[x][y + 2] == 1 and board[x][y + 3] == 1:
                return True
            elif board[x][y] == 2 and board[x][y + 1] == 2 and board[x][y + 2] == 2 and board[x][y + 3] == 2:
                return True

    # Check diagonals (bottom-left to top-right)
    for x in range(0, column_max - 3):
        for y in range(0, row_max - 3):
            if board[x][y] == board[x + 1][y + 1] == board[x + 2][y + 2] == board[x + 3][y + 3] != 0:
                if board[x][y] == 1:
                    return True
                else:
                    return True

    # Check diagonals (top-left to bottom-right)
    for x in range(0, column_max - 3):
        for y in range(3, row_max):
            if board[x][y] == board[x + 1][y - 1] == board[x + 2][y - 2] == board[x + 3][y - 3] != 0:
                if board[x][y] == 1:
                    return True
                else:
                    return True
    return False

def generate_possible_moves(board1):
    possible_moves=[]
    for column in range(0,len(board1)):
        if board1[column][0]==0:
            possible_moves.append(column)
    return possible_moves

def minimax(board1,depth,alpha,beta,maximising_player):
    if depth==0 or game_over(board1):
        return evaluate(board1)

    if maximising_player:
        maxEval=-math.inf
        for move in generate_possible_moves(board1):
            newBoard=make_move(board1,move,2)
            eval=minimax(newBoard,depth-1,alpha,beta,False)
            maxEval=max(maxEval,eval)
            alpha=max(alpha,eval)
            if alpha>=beta:
                break

        return maxEval
    else:
        minEval=math.inf
        for move in generate_possible_moves(board1):
            newBoard=make_move(board1, move, 1)
            eval=minimax(newBoard,depth-1,alpha,beta, True)
            minEval=min(minEval,eval)
            beta=min(beta,eval)
            if beta<=alpha:
                break

        return minEval

def bestMoveMiniMaxAI(board1,depth):
    bestScore=-math.inf
    bestMove=None
    for move in generate_possible_moves(board1):
        new_board=make_move(board1,move,2)
        eval=minimax(new_board,depth-1,-math.inf,math.inf,False)
        if eval>bestScore:
            bestScore=eval
            bestMove=move
    return bestMove












def trainDQN():
    env = Connect4Env()  # Use your Connect 4 environment
    agent = DQNAgent(model)

    episodes = 2000  # amount of games played
    steps=0
    depth=2
    epsilon = 1.0  # Exploration rate - this is the percentage that represents how likely the agent is to experiment
    epsilon_decay = 0.9987  # we want the model to explore less and rely more on the model over time as the model gets more accurate
    epsilon_min = 0.1


    for e in range(episodes+1):

        state = env.reset()  # reset the connect 4 environment every episode

        if env.starting_turn==1: #if the minimax algorithm starts
            action=-1
            next_state, reward, game_over = env.step(action,depth)

            next_state = np.reshape(next_state, [1, 42])
            state = next_state
        state = np.reshape(state, [1, 42])
        if e%500==0:
            q_values = model.predict(state)[0]
            print(q_values)
        # flatten the state array so it can be used in the neural network
        for time in range(500):  # 500 is the max time limit before moving onto the next episode
            action = agent.act(epsilon,state)  # the q network uses an e greedy policy to make a move in the current state

            next_state, reward, game_over = env.step(action,depth)  # the move is sent to the enironment which returns the updated board, reward from that move, and if the game is over

            next_state = np.reshape(next_state, [1, 42])  # flatten the next_state array so it can be used in the neural network
            agent.remember(state, action, reward, next_state,game_over)  # the information from that move is sent to the memory for experience replay
            state = next_state  # the state is updated to the new board
            if game_over:
                print(f"Episode: {e}/{episodes}, Score: {time}, Epsilon: {epsilon:.2}")
                if epsilon > epsilon_min:
                    epsilon *= epsilon_decay  # Lower how much the agent experiments
                break
            if len(agent.memory) > 32 and steps%4==0:

                agent.train(32)  #Train the agent on a random minibatch of 32 once the memory has that many training examples
            steps=steps+1
    model.save('Connect4DQN-Mark-V.h5')

def loadDQN():
    from tensorflow import keras

    model = tensorflow.keras.models.load_model('Connect4DQN-Mark-V.h5')  # Load the model from a file
    return model
model1=loadDQN()
def bestMoveDQN(board):
    state=np.reshape(board,[1,42])
    print(state)
    q_values = model1.predict(state)[0]
    print(q_values)
    valid_moves=[col for col in range(0,7) if board[col][0]==0]
    masked_q_values=np.full_like(q_values,-np.inf)
    for col in valid_moves:
        masked_q_values[col]=q_values[col]
    move=np.argmax(masked_q_values)


    return move

def play100():
    MiniMaxWins=0
    DQNWins=0
    for x in range(0,100):
        board=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        game_over=False
        turnNo = random.randint(1, 2)
        prob=0.6
        while not game_over:

            if turnNo==1:
                if random.uniform(0,1)<prob:
                    move=bestMoveMiniMaxAI(board,2)
                else:
                    move=random.randint(0,6)

                resultX = move

                resultY = red_counter_drop(board, resultX)
                result=win_check(board)
                if result=="Red":
                    MiniMaxWins+=1
                    break
                turnNo=2
            if turnNo==2:
                move=bestMoveDQN(board)

                resultX = move
                resultY = yellow_counter_drop(board, resultX)
                result=win_check(board)
                if result=="Yellow":
                    DQNWins+=1
                    break
                turnNo=1
    return MiniMaxWins,DQNWins









p.display.flip()
gameOver=False
while run:
    #64
    if not gameOver:
        screen.fill((173, 216, 230))
        update_red_counters(board)
        update_yellow_counters(board)

        turn_done = True
        screen.blit(imp, (137.5, 170))

    if turn=="Red" and not gameOver:
        mx,my=p.mouse.get_pos()
        for checkNo in range(0,7):
            if mx>=137.5+(75*checkNo) and mx<=212.5+(75*checkNo):
                screen.blit(coinTransparent, (152+(71.75*checkNo), 113))
                for event in p.event.get():

                    if event.type==p.MOUSEBUTTONDOWN:

                        resultX=checkNo
                        resultY = red_counter_drop(board, resultX)
                        if resultY!="Full":

                            result=counter_animation(coinR,resultX,resultY)
                            turn="Yellow"
                            turn_done = False


                            if result == "Red":
                                winner="Red"
                                gameOver=True
                                print("Red wins")
                                screen.blit(redWin, (204, 238.5))


                            if result == "Yellow":
                                winner="Yellow"
                                gameOver = True

                                print("Yellow wins")
                                screen.blit(yellowWin, (148, 238.5))
                        break



    if turn=="Yellow" and turn_done and not gameOver:
        start=time.process_time()
        move=bestMoveDQN(board)
        print(time.process_time() - start)

        columnNo=move
        resultX=move

        resultY=yellow_counter_drop(board, resultX)
        if resultY != "Full":


            result=counter_animation(coinY,resultX, resultY)


            turn = "Red"



            if result == "Red":
                winner = "Red"
                gameOver = True
                print("Red wins")
                screen.blit(redWin, (204, 238.5))


            if result == "Yellow":
                winner = "Yellow"
                gameOver = True

                print("Yellow wins")
                screen.blit(yellowWin, (148, 238.5))


    for event in p.event.get():
        if event.type==p.QUIT:
            run=False
    p.display.update()

p.quit()





