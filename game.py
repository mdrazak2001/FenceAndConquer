import pygame # The participants need to install this package. Use pip install pygame
import sys
import random
import collections
from itertools import chain,product
from enum import Enum
from time import sleep,time
import Player1 # Player1 is the name of the first bot.
import Player2 # Player2 is the name of the second bot.

BLACK = (0, 0, 0)
WHITE = (150, 150, 150)
BLUE = (0, 89, 240)
GREEN = (0, 200, 20)
DBLUE = (100, 150, 250)
DGREEN = (100, 250, 150)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
OFFSET = 0


""" 
board: 
It is a variable representing the grid configuration. 
It corresponds to the variable B in the move() function in the class 'player' defined in the bots Player1.py, Player2.py, Player3.py, and Player4.py.
It is a list of N= 30 lists, each containing N=30 elements (2-D array, that represents the grid).
"""

"""
How does the grid look?
board[x][y]:    It is the element at the (x,y) position on the grid.  
                That is, it is the element at the x-th position from the left and y-th position of the top.  
                In yet other words, it is the element at the y-th row in the x-th column.
                That is:    (0,0) is the NW corner element of the grid.
                            (N=30,N=30) is the SE corner element of the grid.
                It can hold either of the three values - 0, 1, or 2.
"""
"""
Interpreting the value of board[x][y]:
    0: The cell is empty
    1: Player1 bot has conquered the cell
    2: Player2 bot has conquered the cell
"""




# Size of the board (number of columns/rows in the square board)
N=30
F=6
board = [ [0]*N for x in range(N)]
blocksize = int(WINDOW_HEIGHT/N) #Set the size of the grid block
new_fence = False

MAXSTEPS = N*N*3+N


## Players initial position

# Assumption: The bot named Player1 makes the first move
# Positions (X,Y) of the bots. Hackathon participants may change it to suitable values to test their codes.  
# Position of the first bot (Player1). The bot can be anywhere on the board.
Bot1_X, Bot1_Y = random.randint(0,N-1), random.randint(0,N-1) # Position of the first bot (Player1):  
# Position of the second bot (Player2). The bot can be anywhere on the board.
Bot2_X, Bot2_Y = random.randint(0,N-1), random.randint(0,N-1) # Position of the second bot (Player2): Hackathon participants may change it to suitable values to test their codes 
# The bots must be at different locations on the board.
while Bot1_X == Bot2_X and Bot1_Y == Bot2_Y:
    Bot2_X, Bot2_Y = random.randint(0,N-1), random.randint(0,N-1)


player = [[[Bot1_X, Bot1_Y]],[[Bot2_X, Bot2_Y]]]
player_clock = [10.0,10.0] # Each player gets a clock time of 10 seconds.

x,y = player[0][0][0], player[0][0][1]
board[x][y] = 1
x,y = player[1][0][0], player[1][0][1]
board[x][y] = 2


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT+50))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    font = pygame.font.Font(pygame.font.get_default_font(), 20)

    p = [Player1.player(), Player2.player()]


    turn = 0 
    count = 0 
    drawGrid()
    while True and count<MAXSTEPS:

        sleep(0.1)  # Participants may comment this line to speed up the computation. 
                    # However, commenting will also speed up the visualization. This 
                    # can make it difficult to understand and analyze the moves.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        timer(turn)
        pygame.display.update()
        s = score(board,N)
        score_tab(s,font,SCREEN)

        start_time = time()
        player[turn][0] = update_board(player[turn][0],p[turn],turn)
        move_time = time() - start_time
        player_clock[turn] -= move_time

        fill_fence(turn)
        turn^=1
        count+=1

    s = score(board,N)
    print("Player 1:",s[0],"\nPlayer 2:",s[1])
    if s[0] > s[1]:
        print("Player 1 wins.")
    if s[0] < s[1]:
        print("Player 2 wins.")
    if s[0] == s[1]:
        if player_clock[0]>player_clock[1]:
            print("Player 1 wins the tie-breaker.")
        else:
            print("Player 2 wins the tie-breaker.")


def score_tab(s,font,SCREEN):
        text_surface1 = font.render(f"Player 1: "+str(s[0])+" "+str(" ({:.3f}s)".format(player_clock[0])), True, BLUE)
        text_surface2 = font.render(f"Player 2: "+str(s[1])+" "+str(" ({:.3f}s)".format(player_clock[1])), True, GREEN)
        #text_surface2 = font.render(f"Player 2: "+str(s[1]), True, GREEN)
        SCREEN.fill(pygame.Color("black"),  (80,WINDOW_HEIGHT+10,140,WINDOW_HEIGHT+30) )
        SCREEN.fill(pygame.Color("black"),  (280,WINDOW_HEIGHT+10,330,WINDOW_HEIGHT+30) )
        SCREEN.blit(text_surface1, dest=(5,WINDOW_HEIGHT+10))
        SCREEN.blit(text_surface2, dest=(250,WINDOW_HEIGHT+10))

def timer(turn):
    if player_clock[turn] <= 0.0:
        s = score(board,N)
        print("Player 1:",s[0],"\nPlayer 2:",s[1])
        print("Player",2-turn,"wins based on time.")
        exit(0)

        
def update_board(player,p,player_no):
    x = player[0]
    y = player[1]
    if board[x][y]==0:
        board[x][y] = player_no+1
    cur_move = p.move(board,N,x,y)

    if(cur_move not in [ (1,0),(0,1),(0,-1), (-1,0),(0,0) ]):
        print("Invalid move by player",player_no+1)
        print("Player",2-player_no,"wins.")
        exit(0)
        
    new_x,new_y = [sum(x) for x in zip(player,cur_move)]
    new_x %= N
    new_y %= N
    return (new_x,new_y)


def score(B,N):
    frequency = collections.Counter( chain(*B) )
    return (frequency[1],frequency[2])


def drawGrid():
    for x in range(0, N): 
        for y in range(0, N): 
            rect = pygame.Rect(x*blocksize+OFFSET, y*blocksize+OFFSET, blocksize, blocksize)
            pygame.draw.rect(SCREEN, WHITE, rect,1)
            rect = pygame.Rect(x+1+OFFSET, y+1+OFFSET, blocksize-1, blocksize-1)
            


def fill_square(a,b,color):
    rect = pygame.Rect(a*blocksize+OFFSET, b*blocksize+OFFSET, blocksize-1, blocksize-1)
    pygame.draw.rect(SCREEN, color, rect)


def make_rectangle(x1,y1,x2,y2):
    cells = [ (x,y1) for x in range(x1,x2) ]
    cells.extend( [ (x,y2) for x in range(x1,x2) ])
    cells.extend( [ (x1,y) for y in range(y1,y2) ])
    cells.extend( [ (x2,y) for y in range(y1,y2+1) ])
    return cells

def make_solid_rectangle(x1,y1,x2,y2):
    cells = []
    for i in range(x1,x2+1):
        for j in range(y1,y2+1):
            cells.append( (i,j) )
    return cells

def conquer_fence(x1,y1,x2,y2,turn):
    for i in range(x1,x2):
        for j in range(y1,y2):
            board[i][j] = turn+1
            


def draw_board(grid):
    for x in range(0, N): 
        for y in range(0, N): 
            if board[x][y]==1:
                color = BLUE
            elif board[x][y]==2:
                color = GREEN
            else:
                color = BLACK
            #elif grid[x][y]<0:
            #    color = [sum(x) for x in zip(BLACK,(-grid[x][y]*5,0,0))]


            fill_square(x,y,color)

    fill_square(player[0][0][0],player[0][0][1],DBLUE)
    fill_square(player[1][0][0],player[1][0][1],DGREEN)





def same_color(cells,turn):
    """
    Do all the cells in parameter cells belong to the current player?
    Input: cells -> List of cell coordinates. turn -> 0 for Player 1 and 1 for Player 2
    """
    for x,y in cells:
        if board[x][y] != turn+1:
            return False
    return True


def same_color_or_empty(cells,turn):
    """
    Do all the cells in parameter cells belong to the current player or are empty?
    Input: cells -> List of cell coordinates. turn -> 0 for Player 1 and 1 for Player 2
    """
    for x,y in cells:
        if board[x][y] == 2-turn:
            return False
    return True



def fill_board(region,turn):
    """
    Gives all the cells in the region to the current player. 
    """
    global new_fence
    for x,y in region:
        if board[x][y] == 0: 
            new_fence = True
        board[x][y] = turn + 1 

def search_fence(turn):
   global new_fence
   new_fence = True # To keep track of cascades.
   while(new_fence):
       new_fence = False
       for i in range(N):
           for j in range(N):
               if board[i][j] == turn + 1:
                   for w in range(2,F):
                       for h in range(2,F):
                           if i+w<N and j+h<N:
                               frame = make_rectangle(i,j,i+w,j+h)
                               if same_color(frame,turn):
                                   region = make_solid_rectangle(i,j,i+w,j+h)
                                   if same_color_or_empty(region,turn):
                                       fill_board(region,turn)
                                   #print("Fence at",i,j,w,h)
                           




def fill_fence(turn):
   grid = [ [0]*N for x in range(N)]
   for i in range(N):
            for j in range(N):
                grid[i][j] = board[i][j]

   search_fence(turn)
   draw_board(grid)

main()




