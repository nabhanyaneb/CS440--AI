import matplotlib.pyplot as plt
import math
import random
from random import randrange
import Algorithms

def plot_DFS(dim,p,q): #DFS Plot

    x = [0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store p values between 0 and 1
    y = [0.0 for i in range(len(x))] #store probablity that S can be reached from G at the corresponding p value

    for i in range(len(x)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        sum = 0.0 #keeps track of how many successes
        p = x[i]
        for j in range(1,51):
            array = Algorithms.makeMaze(dim,p) #new maze for current p value
            S=array[0][0]
            G=array[dim-1][dim-1]
            path = Algorithms.checkDFS(dim,array,S,G)[0] #store path from S to G
            if len(path)>0: #if there is a path
                last = path[len(path)-1]
                if last[0] == G.x and last[1] == G.y: #if G is found
                    sum = sum+1
        prob = sum/50 #calculate rate of success
        y[i] = prob

    #creating plot using matplotlib
    plt.plot(x, y,'b')
    plt.margins(0.1)
    plt.xlabel('Obstacle Density P')
    plt.ylabel('Probability that S can be Reached from G')
    plt.title('Obstacle Density p vs Probability that S can be Reached from G')
    plt.show()

def plot_BFS_AStar(dim,p,q): #BFS-A* Plot

    x = [0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store p values between 0 and 1
    y = [0.0 for i in range(len(x))] #store probablity that S can be reached from G at the corresponding p value

    for i in range(len(x)):
        p = x[i]
        sum = 0.0 #keeps track of difference in nodes
        for j in range(1,51):
            array = Algorithms.makeMaze(dim,p) #new maze for current p value
            S=array[0][0]
            G=array[dim-1][dim-1]
            visitedBFS = Algorithms.checkBFS(dim,array,S,G)[1]
            visitedAStar = Algorithms.checkAStar(dim,array,S,G)[1]
            nodesBFS = len(visitedBFS)
            nodesAStar = len(visitedAStar)
            sum = sum + (nodesBFS - nodesAStar) #calculate total difference in nodes
        y[i] = sum/50 #calculate average difference in nodes

    #creating plot using matplotlib
    plt.plot(x, y,'b')
    plt.margins(0.1)
    plt.xlabel('Obstacle Density P')
    plt.ylabel('Average Difference in Number of Nodes Explored')
    plt.title('Number of Nodes Explored by BFS - Number of Nodes Explored by A* vs Obstacle Density p')
    plt.show()

def plot_strategy1(dim,p,q,printPlot): #Strategy 1 Plot

    x = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store p values between 0 and 1
    y = [0.0 for i in range(len(x))] #store probablity that S can be reached from G at the corresponding p value
    p = 0.3

    for i in range(len(x)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        sum = 0.0 #keeps track of how many successes
        q = x[i]
        validPaths = 0 #keeps track of how many valid paths
        while validPaths < 15: #find at least 15 valid mazes
            array = Algorithms.makeMaze(dim,p) #new maze for current p value
            S=array[0][0]
            G=array[dim-1][dim-1]

            i_rand = randrange(1,dim-1)
            j_rand = randrange(1,dim-1)
            array[i_rand][j_rand].value = 0
            dfsPathToFire = Algorithms.checkDFS(dim,array,S,array[i_rand][j_rand]) #check if there is a path from initial fire location to G
            array[i_rand][j_rand].value = 2 #initialize fire

            path = Algorithms.strategy1(dim,p,q,array,S,G)[0] #store path from S to G

            if (len(path) > 0) and (len(dfsPathToFire) > 0): #if there is a path from S to G and from initial fire to G
                validPaths = validPaths + 1
                last = path[len(path)-1]
                if last[0] == G.x and last[1] == G.y: #if G is found
                    sum = sum+1

        prob = sum/validPaths #calculate rate of success
        y[i] = prob

    #creating plot using matplotlib
    if printPlot:
        plt.plot(x, y,'b')
        plt.margins(0.1)
        plt.ylim([-0.1,1.0])
        plt.xlabel('Flammability Q')
        plt.ylabel('Average Strategy 1 Success Rate')
        plt.title('Average Strategy 1 Success Rate vs Flammability Q (at p = 0.3)')
        plt.show()
    return (x,y)

def plot_strategy2(dim,p,q,printPlot): #Strategy 2 Plot

    x = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store p values between 0 and 1
    y = [0.0 for i in range(len(x))] #store probablity that S can be reached from G at the corresponding p value
    p = 0.3

    for i in range(len(x)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        sum = 0.0 #keeps track of how many successes
        q = x[i]
        validPaths = 0 #keeps track of how many valid paths
        while validPaths < 15: #find at least 15 valid mazes
            array = Algorithms.makeMaze(dim,p) #new maze for current p value
            S=array[0][0]
            G=array[dim-1][dim-1]

            i_rand = randrange(1,dim-1)
            j_rand = randrange(1,dim-1)
            array[i_rand][j_rand].value = 0
            dfsPathToFire = Algorithms.checkDFS(dim,array,S,array[i_rand][j_rand]) #check if there is a path from initial fire location to G
            array[i_rand][j_rand].value = 2 #initialize fire

            path = Algorithms.strategy2(dim,p,q,array,S,G)[0] #store path from S to G

            if (len(path) > 0) and (len(dfsPathToFire) > 0): #if there is a path from S to G and from initial fire to G
                validPaths = validPaths + 1
                last = path[len(path)-1]
                if last[0] == G.x and last[1] == G.y: #if G is found
                    sum = sum+1
       
        prob = sum/validPaths #calculate rate of success
        y[i] = prob

    #creating plot using matplotlib
    if printPlot:
        plt.plot(x, y,'r')
        plt.ylim([-0.1,1.0])
        plt.margins(0.1)
        plt.xlabel('Flammability Q')
        plt.ylabel('Average Strategy 2 Success Rate')
        plt.title('Average Strategy 2 Success Rate vs Flammability Q (at p = 0.3)')
        plt.show()
    return (x,y)

def plot_strategy3(dim,p,q,printPlot): #Strategy 3 Plot

    x = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store p values between 0 and 1
    y = [0.0 for i in range(len(x))] #store probablity that S can be reached from G at the corresponding p value
    p = 0.3

    for i in range(len(x)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        sum = 0.0 #keeps track of how many successes
        q = x[i] 
        validPaths = 0 #keeps track of how many valid paths
        while validPaths < 15: #find at least 15 valid mazes
            array = Algorithms.makeMaze(dim,p) #new maze for current p value
            S=array[0][0]
            G=array[dim-1][dim-1]

            i_rand = randrange(1,dim-1)
            j_rand = randrange(1,dim-1)
            array[i_rand][j_rand].value = 0
            dfsPathToFire = Algorithms.checkDFS(dim,array,S,array[i_rand][j_rand]) #check if there is a path from initial fire location to G
            array[i_rand][j_rand].value = 2 #initialize fire

            path = Algorithms.strategy3(dim,p,q,array,S,G)[0] #store path from S to G

            if (len(path) > 0) and (len(dfsPathToFire) > 0): #if there is a path from S to G and from initial fire to G
                validPaths = validPaths + 1
                last = path[len(path)-1]
                if last[0] == G.x and last[1] == G.y: #if G is found
                    sum = sum+1
        
        prob = sum/validPaths #calculate rate of success
        y[i] = prob

    #creating plot using matplotlib
    if printPlot:
        plt.plot(x, y,'g')
        plt.ylim([-0.1,1.0])
        plt.margins(0.1)
        plt.xlabel('Flammability Q')
        plt.ylabel('Average Strategy 3 Success Rate')
        plt.title('Average Strategy 3 Success Rate vs Flammability Q (at p = 0.3)')
        plt.show()
    return (x,y)


def plot_all_strategies(dim,p,q): #plot all three strategies

    temp = plot_strategy3(dim,p,q,False)
    x3 = temp[0]
    y3 = temp[1]
    
    temp = plot_strategy2(dim,p,q,False)
    x2 = temp[0]
    y2 = temp[1]

    temp = plot_strategy1(dim,p,q,False)
    x1 = temp[0]
    y1 = temp[1]

    #creating plot using matplotlib
    plt.plot(x1, y1,'b')
    plt.plot(x2, y2,'r')
    plt.plot(x3, y3,'g')
    plt.ylim([-0.1,1.0])
    plt.margins(0.1)
    plt.xlabel('Flammability Q')
    plt.ylabel('Average Strategy Success Rate')
    plt.title('Average Strategy Success Rate vs Flammability Q (at p = 0.3)')
    plt.show()

def runPlot(plotType,dim,p,q): #run plot corresponding to string input
    if plotType == "DFS":
        plot_DFS(dim,p,q)
    if plotType == "BFSAStar":
        plot_BFS_AStar(dim,p,q)
    if plotType == "Strategy1":
        plot_strategy1(dim,p,q,True)
    if plotType == "Strategy2":
        plot_strategy2(dim,p,q,True)
    if plotType == "Strategy3":
        plot_strategy3(dim,p,q,True)
    if plotType == "All":
        plot_all_strategies(dim,p,q)
