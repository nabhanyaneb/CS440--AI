import random
from random import randrange
import pygame
import heapq
import math
import numpy as np

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 31, 15)
FLAT = (126, 166, 137)
HILLY = (39, 161, 63)
FOREST = (10, 74, 29)
CAVES = (54, 59, 55)
TARGET = (158, 0, 250)

class State: #State object that makes up the map

    target = False 
    visited = False
    p = 0
    fn = 0
    p_found = 0
    
    def __init__(self, r, c, value): #initialize State with corresponding r, c, and value
        self.r = r 
        self.c = c 
        self.value = value 

    def get_neighbors(self,grid,dim): #get all neighbors of the State
        list = []
        if self.c + 1 < dim:
            list.append(grid[self.r][self.c+1])
        if self.r + 1 < dim:
            list.append(grid[self.r+1][self.c])
        if self.c - 1 >= 0:
            list.append(grid[self.r][self.c-1]) 
        if self.r - 1 >= 0:
            list.append(grid[self.r-1][self.c])            
        return list        

class Game(): #game structure

    steps = 0

    def __init__(self,dim): #initialize game with corresponding dimension, grid, and display measurements
        self.dim = dim
        margin = 1
        width = (600-margin*(dim+1))/dim
        height = (600-margin*(dim+1))/dim
        self.grid = [[State(r,c,0) for c in range(self.dim)] for r in range(self.dim)] #create 2D array of States for the game board
    
    def generate_environment(self,dim): #set up the initial environment
        for r in range(dim):
            for c in range(dim):

                #assign terrain type
                rand = random.randint(1,4)
                self.grid[r][c].value = rand

                #initialize probability values
                self.grid[r][c].p = 1.0/(dim*dim)
                self.grid[r][c].p_found = 1.0/(dim*dim) * self.grid[r][c].fn

                #define false-negative rates
                if rand == 1:
                    self.grid[r][c].fn = 0.1
                elif rand == 2:
                    self.grid[r][c].fn = 0.3
                elif rand == 3:
                    self.grid[r][c].fn = 0.7
                elif rand == 4:
                    self.grid[r][c].fn = 0.9

        #pick a random spot for the target
        rand_r = random.randint(0,dim-1)
        rand_c = random.randint(0,dim-1)
        self.grid[rand_r][rand_c].target = True

def get_to_next(game,current,next_state): #travel between current and next state, adjust time steps accordingly

	game.steps = game.steps + find_distance(current, next_state)
	current = next_state
	return 

def find_distance(current,goal): #manhattan distance formula
    a = [current.r,current.c]
    b = [goal.r,goal.c]
    distance = abs(a[0]-b[0])+abs(a[1]-b[1])
    return distance

def find_range(game,current): #returns a list of states with probabilities one standard deviation away from the max probability 
    probailities = []
    ranges = []
    max_p = -1
    
    for r in range(game.dim): 
        for c in range(game.dim):

        	if not (current.r == r and current.c == c):
        		probailities.append(game.grid[r][c].p_found)

    std = np.std(probailities)
    max_p = max(probailities)

    for r in range(game.dim): 
        for c in range(game.dim):
            if game.grid[r][c].p_found >= (max_p - (std)):
                ranges.append(game.grid[r][c])
                     
    return ranges

def highest_state(game, current): #returns closest state with probability within one standard deviation away from the max 
    ranges = find_range(game,current)
    distances = []

    for i in range(len(ranges)):
        distances.append(find_distance(current,ranges[i]))

    ans = ranges[distances.index(min(distances))]

    return ans

def update_info(game, current): #update knowlegde
    
    if current.target == True: 
        return
    else: 
        temp = current.p
        current.p = (current.fn * current.p) / ((1 - current.p) + (current.fn * current.p)) #calculate probability of being the target based on observations so far
        current.p_found = ((1-current.fn) * temp) #calculate probability of finding the target 

        for r in range(game.dim):
            for c in range(game.dim):
                if not (r == current.r and c == current.c): #perform calculations accordingly or the rest of the map
                    game.grid[r][c].p = (game.grid[r][c].p) / ((1 - temp) + (current.fn * temp)) 
                    game.grid[r][c].p_found = ((1-game.grid[r][c].fn) * game.grid[r][c].p)

def run_game(d):
    #will hold current location of agent
    current_r = -1
    current_c = -1

    #initialize game and variables
    dim = d
    t = 0
    target_found = False
    game =  Game(dim)
    game.generate_environment(dim)

    #initialize display
    size = (700,800)
    screen = pygame.display.set_mode(size)
   

    margin = 0.9
    width = (700-margin*(dim+1))/dim
    height = (700-margin*(dim+1))/dim

    #start pygame
    pygame.init()
    done = False
    
    pygame.display.set_caption('Probabilistic Search (and Destory)')
    screen.fill(BLACK)

    font_size = int(width/5)
    font = pygame.font.Font("19919.ttf",font_size)

    #add every (r,c) position on map to a list for easy access
    tuples = []
    for r in range(dim):
        for c in range(dim):
            tuples.append((r,c))

    #randomly pick a starting spot
    rand = random.choice(tuples)
    current_r = rand[0]
    current_c = rand[1]
    current = game.grid[current_r][current_c]


    while not done: #while loop for game
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #break out of while look when done
                done = True
                break

        if not done:
            if not target_found:

                update_info(game, current) #updates probability values across the map               
                
                if current.target == True: 
                    print("Target at: ",current.r,current.c)
                    print("Time Step Total: ", game.steps)
                    target_found = True

                    font_size = 30 #display time steps taken 
                    font = pygame.font.Font("19919.ttf",font_size)
                    time_string = 'Time Steps: ' + str(game.steps)
                    textsurface = font.render(time_string, True, TARGET)
                    screen.blit(textsurface, (250,725))

                    #pygame.quit()
                    #return (current.fn, game.steps)

                else:
                    print("Current: ",current.r,current.c)
                    print("Time Steps: ", game.steps)
                    print()
                    next_state = highest_state(game, current) #declares next state to be state that is closeest with a high probality of being the target

                    #predicts what will happen if the search fails and chooses the next step accordingly
                    temp_board = [[State(r,c,game.grid[r][c].value) for c in range(game.dim)] for r in range(game.dim)]

                    for r in range(game.dim):
                    	for c in range(game.dim):
                    		temp_board[r][c].p = game.grid[r][c].p
                    		temp_board[r][c].fn = game.grid[r][c].fn
                    		temp_board[r][c].p_found = game.grid[r][c].p_found

                    temp_current = temp_board[current.r][current.c]

                    temp_current.p = (current.fn * current.p) / ((1 - current.p) + (current.fn * current.p))
                    temp_current.p_found = (1 - current.fn) * temp_current.p

                    for r in range(game.dim):
                    	for c in range(game.dim):
                    		if not (r == current.r and c == current.c): #perform similar calculations for the rest of the map
                    			temp_board[r][c].p = (temp_board[r][c].p) / ((1 - current.p) + (current.fn * current.p)) 
                    			temp_board[r][c].p_found = ((1-temp_board[r][c].fn) * temp_board[r][c].p)       

                    temp_next = highest_state(game, temp_current)

                    dist_real = find_distance(current, next_state)
                    dist_temp = find_distance(temp_current, temp_next) 

                    if dist_real <= dist_temp: 
                    	get_to_next(game, current, next_state) #
                    	current = next_state 
                    else: 
                    	get_to_next(game, temp_current, temp_next)
                    	current = temp_next 

                    
                    game.steps = game.steps + 1
  
                #print()
               
            for row in range(game.dim):
                for column in range(game.dim):
                    #set color based on terrain type
                    color = BLACK
                    if game.grid[row][column].value == 1:
                        color = FLAT
                    if  game.grid[row][column].value == 2:
                        color = HILLY
                    if game.grid[row][column].value == 3:
                        color = FOREST
                    if game.grid[row][column].value == 4:
                        color = CAVES

                    #draw the board to the screen
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin, (margin + height) * row + margin, width, height])

                    #draw where the target is
                    if game.grid[row][column].target == True:
                        textsurface = font.render('X', True, TARGET)
                        screen.blit(textsurface,((margin + width) * column + margin + width/3, (margin + height) * row + margin + height/3))

                    #draw where the agent is
                    if row == current.r and column == current.c:
                        textsurface = font.render('A', True, RED)
                        screen.blit(textsurface,((margin + width) * column + margin, (margin + height) * row + margin))

                    #draw probabilities to the screen
                    if not target_found:
	                    textsurface = font.render((str(round(game.grid[row][column].p,5))), True, BLACK)
	                    screen.blit(textsurface,((margin + width) * column + margin, (margin + height) * row + margin))


                #slow down game so we can see steps
                pygame.time.delay(50)
                

        pygame.display.flip()

    #end game and return score
    pygame.quit()
    return (current.fn, game.steps)

#run the game with the dimension
run_game(5)
