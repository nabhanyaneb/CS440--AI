import random
from random import randrange
import pygame
import heapq
import numpy as np

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
MINE = (168, 89, 154)
CLICKED = (82,82,82)
UNCLICKED = (181, 181, 181)
SAFE = (128, 176, 160)
RED = (140, 21, 10)

class State: #State object that makes up the board
    uncovered = False
    total_neighbors = 0
    total_mines = 0
    total_mines_revealed = 0
    total_safes = 0
    total_safes_revealed = 0
    total_hiddens = 0
    is_mine = False
    blown_up = False
    
    def __init__(self, r, c, value): #initialize State with corresponding r, c, and value
        self.r = r 
        self.c = c 
        self.value = value #value can be 3 for a mine, 2 for a safe, or 1 for an uncovered spot

    def get_neighbors(self,grid,dim): #get all neighbors of the State
        list = []
        if self.r + 1 < dim:
            list.append(grid[self.r+1][self.c])
        if self.c + 1 < dim:
            list.append(grid[self.r][self.c+1])
        if self.c - 1 >= 0:
            list.append(grid[self.r][self.c-1])
        if self.r - 1 >= 0:
            list.append(grid[self.r-1][self.c])
        if self.r + 1 < dim and self.c + 1 < dim:
            list.append(grid[self.r+1][self.c+1])
        if self.r + 1 < dim and self.c - 1 >= 0:
            list.append(grid[self.r+1][self.c-1])
        if self.r - 1 >= 0 and self.c - 1 >= 0:
            list.append(grid[self.r-1][self.c-1])
        if self.r - 1 >= 0 and self.c + 1 < dim:
            list.append(grid[self.r-1][self.c+1])                 
        return list        

class Game(): #game structure
    def __init__(self,dim,n): #initialize game
        self.dim = dim
        self.n = n
        margin = 1
        width = (600-margin*(dim+1))/dim
        height = (600-margin*(dim+1))/dim
        self.grid = [[State(r,c,0) for r in range(self.dim)] for c in range(self.dim)] #create 2D array of States for the game board
    
    def generate_mines(self,dim,n,game): #generate n mines for the board
        tuples = []
        mines = []
        for r in range(dim):
            for c in range(dim):
                tuples.append((r,c)) #add all spots of the board to a list

        for i in range(n):
            rand = random.choice(tuples) #randomly pick a spot from the list
            mines.append(rand)
            game.grid[rand[0]][rand[1]].value = 3 #set value to 3
            tuples.remove(rand) #remove from list
        return mines

def update_info(game,r,c,screen,tuples,dim,knowledge,mines_knowledge,mines_exploded,added,var_names):

    #row value that will be added to matrix
    newrow = [0 for i in range(dim*dim)] #initialize row that will be added to matrix

    screen.fill(BLACK)

    safes_update = []
    mines_update = []

    #uncover current spot
    game.grid[r][c].uncovered=True
    if game.grid[r][c].value != 3:
        game.grid[r][c].value = 1

    if game.grid[r][c].value != 3: #if current spot is not a mine
        neighbors = game.grid[r][c].get_neighbors(game.grid,dim) #get all neighbors of current spot

        #variables to update
        num_mines = 0
        num_hidden = 0
        num_mines_revealed = 0
        num_safes_revealed = 0

        #calculate values of these variables
        for i in range(len(neighbors)):
            newrow[var_names.index((neighbors[i].r,neighbors[i].c))] = 1 #set corresponding matrix locaition to 1 for all neighbors
            if game.grid[neighbors[i].r][neighbors[i].c].uncovered and not game.grid[neighbors[i].r][neighbors[i].c].is_mine:
                num_safes_revealed = num_safes_revealed + 1
            if game.grid[neighbors[i].r][neighbors[i].c].is_mine:
                num_mines_revealed = num_mines_revealed + 1
            if game.grid[neighbors[i].r][neighbors[i].c].value==3:
                num_mines = num_mines + 1
            if not game.grid[neighbors[i].r][neighbors[i].c].uncovered:
                num_hidden = num_hidden + 1

        #update values for our current spot with these variables
        game.grid[r][c].total_neighbors = len(neighbors)
        game.grid[r][c].total_mines = num_mines
        game.grid[r][c].total_safes = game.grid[r][c].total_neighbors - game.grid[r][c].total_mines
        game.grid[r][c].total_hiddens = num_hidden
        game.grid[r][c].total_mines_revealed = num_mines_revealed
        game.grid[r][c].total_safes_revealed = num_safes_revealed
        
        #if the total number of mines minus the number of revealed mines is the number of hidden neighbors, every hidden neighbor is a mine
        if (game.grid[r][c].total_mines - game.grid[r][c].total_mines_revealed) == game.grid[r][c].total_hiddens:
            for i in range(game.grid[r][c].total_neighbors):
                if game.grid[neighbors[i].r][neighbors[i].c].blown_up == False and not (neighbors[i].r,neighbors[i].c) in added and not game.grid[neighbors[i].r][neighbors[i].c].uncovered:
                    if (neighbors[i].r,neighbors[i].c) in tuples:
                        tuples.remove((neighbors[i].r,neighbors[i].c))
                    if (neighbors[i].r,neighbors[i].c) not in mines_knowledge:
                        mines_knowledge.append((neighbors[i].r,neighbors[i].c))
                    added.append((neighbors[i].r,neighbors[i].c))
                    game.grid[neighbors[i].r][neighbors[i].c].uncovered = True
                    game.grid[neighbors[i].r][neighbors[i].c].is_mine = True
                    mines_update.append((neighbors[i].r,neighbors[i].c))

        #if the total number of safe neighbors minus the number of revealed safe neighbors is the number of hidden neighbors, every hidden neighbor is safe
        if game.grid[r][c].total_safes - game.grid[r][c].total_safes_revealed == game.grid[r][c].total_hiddens:
            for i in range(len(neighbors)):
                if not (neighbors[i].r,neighbors[i].c) in added and not game.grid[neighbors[i].r][neighbors[i].c].uncovered:
                    if (neighbors[i].r,neighbors[i].c) in tuples:
                        tuples.remove((neighbors[i].r,neighbors[i].c))
                    heapq.heappush(knowledge, (0,(neighbors[i].r,neighbors[i].c)))
                    added.append((neighbors[i].r,neighbors[i].c))
                    if game.grid[neighbors[i].r][neighbors[i].c].value != 1:
                        game.grid[neighbors[i].r][neighbors[i].c].value = 2
                        game.grid[neighbors[i].r][neighbors[i].c].uncovered = True
                        safes_update.append((neighbors[i].r,neighbors[i].c))

    #if the current spot is a mine, blow it up
    if game.grid[r][c].value == 3 and not (r,c) in mines_knowledge:
        game.grid[r][c].is_mine = True
        #print("Explosion!")
        game.grid[r][c].blown_up = True
        mines_exploded.append((r,c))
        newrow[var_names.index((r,c))] = 2
        mines_update.append((r,c))
        return([-1],[-1],safes_update,mines_update) #there is no information found to add to the matrix

    #add this new row to the matrix and update safe spots and mine spots
    return (np.array(newrow),[game.grid[r][c].total_mines],safes_update,mines_update)

def update_probabilities(game,dim,tuples,knowledge,mines_left): #update probability calculations of remaining spots
    probabilities = []
    
    for i in range(len(tuples)): #loop through all remaining spots
        r = tuples[i][0]
        c = tuples[i][1]
        temp = False
        count = 0
        prob = 1
        neighbors = game.grid[r][c].get_neighbors(game.grid,dim)

        #if neighbors have clue values, probability is equal to 1 divided by the clue of the neighbor around it
        for n in neighbors:
            temp = False
            if game.grid[n.r][n.c].uncovered == True:
                count = count + 1 #check if neighbors are uncovered
                if game.grid[n.r][n.c].total_mines != 0:
                    prob = prob / (1/game.grid[n.r][n.c].total_mines) #account for multiple neighbors having clue values
                else:
                    #spot is safe
                    prob = 0
                    temp = True
                    
        if count == 0:
            if not mines_left == 0:
                heapq.heappush(probabilities, (1/mines_left,(r,c))) #push 1 divided by remaining mines as probability if no neighbors have clue values
            else:
                heapq.heappush(probabilities, (0,(r,c))) #push priority of 0 because spot is safe
        elif not temp:
            heapq.heappush(probabilities, (prob,(r,c))) #push calculated probability value to a priority queue
        else:
            heapq.heappush(probabilities, (0,(r,c))) #push to a priority queue with a priority of 0 because this spot is safe

    return probabilities

def run_game(d,num):
    #will hold current location of agent
    current_x = -1
    current_y = -1

    #knowledge arrays
    knowledge = []
    mines_knowledge = []
    mines_exploded = []
    added = []

    #update matrix with safe spots and mine spots
    safes_to_update = []
    mines_to_update = []

    #initialize game and variables
    dim = d
    n = num
    score = 0
    game =  Game(dim,n)

    
    var_names = [(r,c) for r in range(dim) for c in range(dim)] #column names that correspond to matrix

    #matrix to store data
    variables = np.empty((0,dim*dim), int)
    
    #matrix that stores the clues
    clues = np.empty((0,1), int)
    temp = np.empty((0,1), int)
    
    #initialize screen
    size = (600,700)
    screen = pygame.display.set_mode(size)
    done = False

    #start pygame
    pygame.init()
    
    pygame.display.set_caption('MineSweeper')
    screen.fill(BLACK)
    font = pygame.font.Font("Raleway-Medium.ttf",30)

    #add every spot in 2D array to an array
    tuples = []
    for r in range(dim):
        for c in range(dim):
            tuples.append((r,c))

    #to start randomly pick a spot and remove it from the array
    rand = random.choice(tuples)
    current_x = rand[0]
    current_y = rand[1]
    tuples.remove(rand)

    #calculate values used in display
    margin = 1
    width = (600-margin*(dim+1))/dim
    height = (600-margin*(dim+1))/dim

    mines = game.generate_mines(dim,n,game) #generate n mines for the game board

    while not done: #start while loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #break out of while look when done
                done = True
                break

        if not done:
            if current_x != -1 and current_y != -1: #if game is still running
                #print("Agent at ",current_x,current_y)
                    
                (newrow,newclue,sa,mi) = update_info(game,current_x,current_y,screen,tuples,dim,knowledge,mines_knowledge,mines_exploded,added,var_names) #send agent to next spot
                probabilities = update_probabilities(game,dim,tuples,knowledge,len(mines_knowledge)+len(mines_exploded)) #update probabilities of remaining spots to pick from

                #update safe spots and mine spots so we can update the matrix
                for i in range(len(sa)):
                    if sa[i] not in safes_to_update:
                        safes_to_update.append(sa[i])
                for i in range(len(mi)):
                    if mi[i] not in mines_to_update:
                        mines_to_update.append(mi[i])
                        
                if newrow[0] != -1: #if the new row has data to add
                    
                    #update the augmented matrix with the new row and new clue
                    variables = np.vstack([variables, newrow])
                    clues = np.append(clues,newclue)
                    temp = np.vstack([temp, newclue])

                    matrix = np.append(variables, temp, axis=1) #add the new row to the matrix

                    #create a copy of both variables and clues so we can perform operations
                    var = np.copy(variables)
                    clu = np.copy(clues)

                    #based on the data in the matrix, find out if spots are safe or mines
                    for i in range(len(var)):
                        ones=0 #store number of ones in each row
                        for j in range(len(var[i])):
                            if var[i][j]==1:
                                ones+=1 #if the matrix spot is a 1, update ones
    
                            #based on the data in the matrix, find out if spots are mines
                            if clues[i] == 0 and var[i][j]==1: #if the clue value is 0 then set all variables in this row to 0 too to mark them as safe
                                if not (var_names[j][0],var_names[j][1]) in added and not game.grid[var_names[j][0]][var_names[j][1]].uncovered:
                                    if var_names[j] not in safes_to_update:
                                        safes_to_update.append(var_names[j])
                                    if (var_names[j][0],var_names[j][1]) in tuples:
                                        tuples.remove((var_names[j][0],var_names[j][1]))
                                    heapq.heappush(knowledge, (0,(var_names[j][0],var_names[j][1])))
                                    added.append((var_names[j][0],var_names[j][1]))
                                    if game.grid[var_names[j][0]][var_names[j][1]].value != 1:
                                        game.grid[var_names[j][0]][var_names[j][1]].value = 2
                                        game.grid[var_names[j][0]][var_names[j][1]].uncovered = True

                        #based on the data in the matrix, find out if spots are mines
                        if clues[i] != 0 and clues[i] == ones: #if the clue value is equal to the number of ones then set all variables in this row as mines
                            for j in range(len(var[i])):
                                if var[i][j]==1:
                                    if game.grid[var_names[j][0]][var_names[j][1]].blown_up == False and not (var_names[j][0],var_names[j][1]) in added and not game.grid[var_names[j][0]][var_names[j][1]].uncovered:
                                        if var_names[j] not in mines_to_update:
                                            mines_to_update.append(var_names[j])
                                        if (var_names[j][0],var_names[j][1]) in tuples:
                                            tuples.remove((var_names[j][0],var_names[j][1]))
                                        if (var_names[j][0],var_names[j][1]) not in mines_knowledge:
                                            mines_knowledge.append((var_names[j][0],var_names[j][1]))
                                        added.append((var_names[j][0],var_names[j][1]))
                                        game.grid[var_names[j][0]][var_names[j][1]].uncovered = True
                                        game.grid[var_names[j][0]][var_names[j][1]].is_mine = True

                    #perform matrix operations for mine spots
                    for x in range (len(mines_to_update)):
                        index = var_names.index(mines_to_update[x])
                        for i in range(len(var)):
                            for j in range(len(var[i])):
                                if j == index and var[i][j] == 1: #for each mine, go through the column and set the value to 0 anywhere else it appears and subtract 1 from the clue
                                    var[i][j] = 0
                                    clu[i] = clu[i] - 1

                    #perform matrix operations for safe spots
                    for x in range (len(safes_to_update)):
                        index = var_names.index(safes_to_update[x])
                        for i in range(len(var)):
                            for j in range(len(var[i])):
                                if j == index and var[i][j] == 1: #for each safe spot, go through the column and set the value to 0 anywhere else it appears
                                    var[i][j] = 0

                    #now redo the calculations from before to determine if a spot is a mine or is safe using this new simplified matrix
                    for i in range(len(var)):
                        ones=0 #count the number of ones in each row
                        for j in range(len(var[i])):
                            if var[i][j]==1:
                                ones+=1 #if the matrix spot is a 1, update ones
                                
                            #based on the data in the matrix, find out if spots are mines
                            if clu[i] == 0 and var[i][j]==1: #if the clue value is 0 then set all variables in this row to 0 too to mark them as safe
                                if not (var_names[j][0],var_names[j][1]) in added and not game.grid[var_names[j][0]][var_names[j][1]].uncovered:
                                    if var_names[j] not in safes_to_update:
                                        safes_to_update.append(var_names[j])
                                    if (var_names[j][0],var_names[j][1]) in tuples:
                                        tuples.remove((var_names[j][0],var_names[j][1]))
                                    heapq.heappush(knowledge, (0,(var_names[j][0],var_names[j][1])))
                                    added.append((var_names[j][0],var_names[j][1]))
                                    if game.grid[var_names[j][0]][var_names[j][1]].value != 1:
                                        game.grid[var_names[j][0]][var_names[j][1]].value = 2
                                        game.grid[var_names[j][0]][var_names[j][1]].uncovered = True
                                        
                        #based on the data in the matrix, find out if spots are mines 
                        if clu[i] != 0 and clu[i] == ones: #if the clue value is equal to the number of ones then set all variables in this row as mines
                            for j in range(len(var[i])):
                                if var[i][j]==1: 
                                    if game.grid[var_names[j][0]][var_names[j][1]].blown_up == False and not (var_names[j][0],var_names[j][1]) in added and not game.grid[var_names[j][0]][var_names[j][1]].uncovered:
                                        if var_names[j] not in mines_to_update:
                                            mines_to_update.append(var_names[j])
                                        if (var_names[j][0],var_names[j][1]) in tuples:
                                            tuples.remove((var_names[j][0],var_names[j][1]))
                                        if (var_names[j][0],var_names[j][1]) not in mines_knowledge:
                                            mines_knowledge.append((var_names[j][0],var_names[j][1]))
                                        added.append((var_names[j][0],var_names[j][1]))
                                        game.grid[var_names[j][0]][var_names[j][1]].uncovered = True
                                        game.grid[var_names[j][0]][var_names[j][1]].is_mine = True
                                
                if len(tuples) > 0 or len(knowledge) > 0: #if there are spots left on the board
                    if len(knowledge) > 0:
                        next_spot = heapq.heappop(knowledge) #pick next spot to go to based on priority from the heapq
                        current_x = next_spot[1][0]
                        current_y = next_spot[1][1]                         
                    else:
                        #remove from queue of spots remaining based on probability calculations to pick next spot
                        if len(probabilities) > 0:
                            next_spot = heapq.heappop(probabilities)
                            current_x = next_spot[1][0]
                            current_y = next_spot[1][1]
                            if (current_x,current_y) in tuples:
                                tuples.remove((current_x,current_y))                   
                else:
                    #there are no more spots remaining so game is over
                    current_x = -1
                    current_y = -1
                    score = len(mines_knowledge) #score is number of mines discovered
                    score_string = "Score = " + str(score) + "/" + str(n)
                    textsurface = font.render(score_string, True, WHITE)
                    screen.blit(textsurface,(230,630))
            
                    #use to end game automatically
                    pygame.quit() 
                    return score

            for row in range(game.dim):
                for column in range(game.dim):
                    #set color based on value
                    if game.grid[row][column].value == 3:
                        color = MINE
                    if  game.grid[row][column].value == 2:
                        color = SAFE
                    if game.grid[row][column].value == 1:
                        color = CLICKED
                    if not game.grid[row][column].uncovered:
                        color = UNCLICKED

                    #draw the board to the screen
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin, (margin + height) * row + margin, width, height])
                    if (row,column) in mines_exploded:
                        textsurface = font.render("B", True, WHITE)
                        screen.blit(textsurface,((margin + width) * column + margin, (margin + height) * row + margin)) #draw a B for blown up mines                      
                    if game.grid[row][column].value == 1:
                        num_mines = game.grid[row][column].total_mines
                        textsurface = font.render(str(num_mines), True, WHITE)
                        screen.blit(textsurface,((margin + width) * column + margin, (margin + height) * row + margin)) #draw the clue to each spot

                #use delay to show steps
                #pygame.time.delay(500)

        pygame.display.flip()

    score = len(mines_knowledge) #score is number of mines discovered

    #end game and return score
    pygame.quit()
    return score

#run the game
#print("Score: ",run_game(10,60))
