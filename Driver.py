import time
import math
import random
from random import randrange
import Algorithms
import Plots
import MazeDisplay

start = time.time() #used to keep track of how long the program takes to execute

dim = 5 #dimension of the maze
p = 0.3 #probablity a State is an obstacle
q = 0.3 #rate of flammability

#display mazes using pygame
#MazeDisplay.runMaze("DFS",dim,p,q)
#MazeDisplay.runMaze("BFS",dim,p,q)
#MazeDisplay.runMaze("AStar",dim,p,q)
#MazeDisplay.runMaze("Strategy1",dim,p,q)
#MazeDisplay.runMaze("Strategy2",dim,p,q)
#MazeDisplay.runMaze("Strategy3",dim,p,q)

#display plots using matplotlib
#Plots.runPlot("DFS",dim,p,q)
#Plots.runPlot("BFSAStar",dim,p,q)
#Plots.runPlot("Strategy1",dim,p,q)
#Plots.runPlot("Strategy2",dim,p,q)
#Plots.runPlot("Strategy3",dim,p,q)
#Plots.runPlot("All",dim,p,q)

#make maze based on dimension and p
array = Algorithms.makeMaze(dim,p)
#set initial and goal
initial=array[0][0]
goal=array[dim-1][dim-1]

#DFS
print ("DFS path:")
solDFS = Algorithms.checkDFS(dim, array, initial, goal)[0]
print (solDFS)
print()

#BFS
print ("BFS path:")
solBFS = Algorithms.checkBFS(dim, array, initial, goal)[0]
print(solBFS)
print()

#A*
print ("A* path:")
solAStar= Algorithms.checkAStar(dim, array, initial, goal)[0]
print(solAStar)
print()

#make a copy of array
array2 = [[Algorithms.State(0,0,0,None) for i in range(dim)] for j in range(dim)]
for i in range(len(array)):
    for j in range(len(array[i])):
        array2[i][j].x = array[i][j].x
        array2[i][j].y = array[i][j].y
        array2[i][j].value = array[i][j].value
        array2[i][j].prev = array[i][j].prev

#set random location for initial fire
i_rand = randrange(1,dim-1)
j_rand = randrange(1,dim-1)
array2[i_rand][j_rand].value = 2

#Strategy 1
print("Strategy1 Path:")
sol1 = Algorithms.strategy1(dim, p, q, array2, initial, goal)[0]
print(sol1)
print()

#Strategy 2
print("Strategy2 Path:")
sol2 = Algorithms.strategy2(dim, p, q, array2, initial, goal)[0]
print(sol2)
print()

#Strategy 3
print("Strategy3 Path:")
sol3 = Algorithms.strategy3(dim, p, q, array2, initial, goal)[0]
print(sol3)
print()

print('It took', time.time()-start, 'seconds.') #print time taken
