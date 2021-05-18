import pygame
import Algorithms
from random import randrange
 
#colors
empty = (0, 0, 0)
obstacle = (255, 255, 255)
path = (190, 186, 181)
fire = (134, 36, 36)
purple = (126, 65, 148)

def makeMazeArray(maze,dim): #make a maze of State objects into a 2D integer array
    rows, cols = (dim, dim)
    arr = [[0 for i in range(cols)] for j in range(rows)] 
    for i in range(cols):
        for j in range(rows):
            arr[i][j] = maze[i][j].value 

    return arr

def printDFS(dim,p,q): #print a DFS maze
    pygame.display.set_caption("DFS Maze")
    maze = Algorithms.makeMaze(dim,p)
    initial = Algorithms.State(0,0,0,None)
    goal = Algorithms.State(dim-1,dim-1,0,None)

    route = Algorithms.checkDFS(dim,maze,initial,goal)[0]

    grid = makeMazeArray(maze,dim)

    for i in range(len(route)):
        grid[route[i][0]][route[i][1]] = 3

    grid[0][0] = 4
    grid[dim-1][dim-1] = 4

    return grid

def printBFS(dim,p,q): #print a BFS maze
    pygame.display.set_caption("BFS Maze")
    maze = Algorithms.makeMaze(dim,p)
    initial = Algorithms.State(0,0,0,None)
    goal = Algorithms.State(dim-1,dim-1,0,None)

    route = Algorithms.checkBFS(dim,maze, initial, goal)[0]

    grid = makeMazeArray(maze,dim)

    for i in range(len(route)):
        grid[route[i][0]][route[i][1]] = 3
        
    grid[0][0] = 4
    grid[dim-1][dim-1] = 4
    
    return grid

def printAStar(dim,p,q): #print an A* maze
    pygame.display.set_caption("A* Maze")
    maze = Algorithms.makeMaze(dim,p)
    initial = Algorithms.State(0,0,0,None)
    goal = Algorithms.State(dim-1,dim-1,0,None)
    
    route = Algorithms.checkAStar(dim,maze, initial, goal)[0]

    grid = makeMazeArray(maze,dim)

    for i in range(len(route)):
        grid[route[i][0]][route[i][1]] = 3

    grid[0][0] = 4
    grid[dim-1][dim-1] = 4

    return grid

def printStrategy1(dim,p,q): #print a Strategy 1 maze
    pygame.display.set_caption("Strategy 1 Maze")
    maze = Algorithms.makeMaze(dim,p)
    initial = Algorithms.State(0,0,0,None)
    goal = Algorithms.State(dim-1,dim-1,0,None)
    
    i_rand = randrange(1,dim-1)
    j_rand = randrange(1,dim-1)
    maze[i_rand][j_rand].value = 2
    
    temp =  Algorithms.strategy1(dim, p, q, maze, initial, goal)
    route = temp[0]
    grid = makeMazeArray(temp[1],dim) 

    for i in range(len(route)):
        if not grid[route[i][0]][route[i][1]] ==2:
            grid[route[i][0]][route[i][1]] = 3

    grid[0][0] = 4
    grid[dim-1][dim-1] = 4

    return grid

def printStrategy2(dim,p,q): #print a Strategy 2 maze
    pygame.display.set_caption("Strategy 2 Maze")
    maze = Algorithms.makeMaze(dim,p)
    initial = Algorithms.State(0,0,0,None)
    goal = Algorithms.State(dim-1,dim-1,0,None)
    
    i_rand = randrange(1,dim-1)
    j_rand = randrange(1,dim-1)
    maze[i_rand][j_rand].value = 2
    
    temp =  Algorithms.strategy2(dim, p, q, maze, initial, goal)
    route = temp[0]
    grid = makeMazeArray(temp[1],dim) 

    for i in range(len(route)):
        if not grid[route[i][0]][route[i][1]] ==2:
            grid[route[i][0]][route[i][1]] = 3

    grid[0][0] = 4
    grid[dim-1][dim-1] = 4

    return grid

def printStrategy3(dim,p,q): #print a Strategy 3 maze
    pygame.display.set_caption("Strategy 3 Maze")
    maze = Algorithms.makeMaze(dim,p)
    initial = Algorithms.State(0,0,0,None)
    goal = Algorithms.State(dim-1,dim-1,0,None)
    
    i_rand = randrange(1,dim-1)
    j_rand = randrange(1,dim-1)
    maze[i_rand][j_rand].value = 2
    
    temp =  Algorithms.strategy3(dim, p, q, maze, initial, goal)
    route = temp[0]
    grid = makeMazeArray(temp[1],dim) 

    for i in range(len(route)):
        if not grid[route[i][0]][route[i][1]] ==2:
            grid[route[i][0]][route[i][1]] = 3

    grid[0][0] = 4
    grid[dim-1][dim-1] = 4

    return grid

def runMaze(mazeType,dim,p,q): #run corresponding maze based on input string

    width = 500/dim-1
    height = 500/dim-1
    margin = 1

    if mazeType == "DFS":
        grid = printDFS(dim,p,q)
    if mazeType == "BFS":
        grid = printBFS(dim,p,q)
    if mazeType == "AStar":
        grid = printAStar(dim,p,q)
    if mazeType == "Strategy1":
        grid = printStrategy1(dim,p,q)
    if mazeType == "Strategy2":
        grid = printStrategy2(dim,p,q)
    if mazeType == "Strategy3":
        grid = printStrategy3(dim,p,q)

    pygame.init() #start pygame
    window_size = [500, 500]
    screen = pygame.display.set_mode(window_size)
    done = False
    
    while not done:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                done = True  
                pygame.quit()
                break
        if not done:
            screen.fill(empty)
            for row in range(dim):
                for column in range(dim):
                    #set colors
                    color = obstacle
                    if grid[row][column] == 1:
                        color = empty
                    if grid[row][column] == 2:
                        color = fire
                    if grid[row][column] == 3:
                        color = path
                    if grid[row][column] == 4:
                        color = purple
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin, (margin + height) * row + margin, width, height])
            pygame.display.flip()
        
pygame.quit()
