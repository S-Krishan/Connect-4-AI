import pygame as p
import random
import math
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
    screen.blit(coin, (column_cord,ending_row_cord))
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

def minimax(board1,depth,maximising_player):
    if depth==0 or game_over(board1):
        return evaluate(board1)

    if maximising_player:
        maxEval=-math.inf
        for move in generate_possible_moves(board1):
            newBoard=make_move(board1,move,2)
            eval=minimax(newBoard,depth-1,False)
            maxEval=max(maxEval,eval)
        return maxEval
    else:
        minEval=math.inf
        for move in generate_possible_moves(board1):
            newBoard=make_move(board1, move, 1)
            eval=minimax(newBoard,depth-1, True)
            minEval=min(minEval,eval)
        return minEval

def bestMove(board1,depth):
    bestScore=-math.inf
    bestMove=None
    for move in generate_possible_moves(board1):
        new_board=make_move(board1,move,2)
        eval=minimax(new_board,depth,False)
        if eval>bestScore:
            bestScore=eval
            bestMove=move
    return bestMove


p.display.flip()
gameOver=False
while run:
    #64
    if not gameOver:
        screen.fill((173, 216, 230))
        update_red_counters(board)
        update_yellow_counters(board)

        turn_done=True
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
                            print("Row: ",resultY,"Column: ",resultX)
                            print(board)
                            result=counter_animation(coinR,resultX,resultY)
                            turn="Yellow"
                            turn_done=False

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

    if turn=="Yellow" and turn_done and not gameOver:

        move=bestMove(board,3)


        columnNo=move
        resultX=move
        resultY=yellow_counter_drop(board, resultX)
        if resultY != "Full":
            print("Row: ", resultY, "Column: ", resultX)
            print(board)

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


