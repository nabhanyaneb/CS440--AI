import numpy
import math
import random
import heapq
from random import randrange
from queue import Queue
from queue import LifoQueue

def makeMaze(dim,p): #create initial maze
    rows, cols = (dim, dim)
    arr = [[State(0,0,0,None) for i in range(cols)] for j in range(rows)] #initialize array of dim x dim

    for i in range(cols):
        for j in range(rows):
            arr[i][j] = State(i,j,0,None) #initialize every array element
            rand = random.random() #generate random number from 0 to 1
            if rand <= p: #check if random number is less than or equal to p value
                arr[i][j].value = 1 #set value to 1, with 1 representing an obstacle

    #set value of initial and goal State to 0
    arr[0][0] = State(0,0,0,None)
    arr[dim-1][dim-1] = State(dim-1,dim-1,0,None)

    return arr

def checkDFS(dim, arr, initial, goal): #check if there is a DFS path
    fringe_DFS = LifoQueue() #fringe is a LIFO queue for DFS
    visited_DFS = []
    fringe_DFS.put(initial) #put initial onto fringe
    path = False
    current = State(0,0,0,None) #initialize a current State

    while not fringe_DFS.empty():
        current = fringe_DFS.get() #set current to the State taken off the fringe
        visited_DFS.append(current) #add current State to list of visited States
        if current.x == goal.x and current.y == goal.y: #check if current State is goal State
            path=True #DFS path found
            break
        neighbors = current.getValidNeighbors(arr,dim) #get all neighbors of current where there are no obstacles
        for i in range(len(neighbors)):
            check = in_list(neighbors[i], visited_DFS) #check to see if each neighbor has been visited yet
            check2 = in_queue(neighbors[i], fringe_DFS) #check to see if each neighbor is on the fringe yet
            if not check and not check2:
                newState = State(neighbors[i].x,neighbors[i].y,neighbors[i].value,current)
                fringe_DFS.put(newState)  #add the neighbor to the fringe

    steps = [] #store DFS path
    if not path:
        return (steps,visited_DFS)
    else:
        ptr = current #start with current as a pointer

        while not ptr.prev == None: #backtrack while adding to the path
            strStep = (ptr.x,ptr.y)
            steps.append(strStep)
            ptr = ptr.prev

        strStep = (initial.x,initial.y)
        steps.append(strStep)
        steps.reverse() #reverse the order

    return (steps,visited_DFS)

def checkBFS(dim, arr, initial, goal): #check if there is a BFS path
    fringe_BFS = Queue() #fringe is a queue for BFS
    visited_BFS = []
    fringe_BFS.put(initial) #put initial onto fringe
    path = False
    current = State(0,0,0,None) #initialize a current State

    while not fringe_BFS.empty():
        current = fringe_BFS.get() #set current to the State taken off the fringe
        visited_BFS.append(current) #add current State to list of visited States
        if current.x == goal.x and current.y == goal.y: #check if current State is goal State
            path=True #BFS path found
            break
        neighbors = current.getValidNeighbors(arr,dim) #get all neighbors of current where there are no obstacles
        for i in range(len(neighbors)):
            check = in_list(neighbors[i], visited_BFS) #check to see if each neighbor has been visited yet
            check2 = in_queue(neighbors[i], fringe_BFS) #check to see if each neighbor is on the fringe yet
            if not check and not check2:
                newState = State(neighbors[i].x,neighbors[i].y,neighbors[i].value,current)
                fringe_BFS.put(newState)  #add the neighbor to the fringe

    steps = [] # store BFS path
    if not path:
        return (steps,visited_BFS)
    else:
        ptr = current #start with current as a pointer

        while not ptr.prev == None: #backtrack while adding to the path
            strStep = (ptr.x,ptr.y)
            steps.append(strStep)
            ptr = ptr.prev

        strStep = (initial.x,initial.y)
        steps.append(strStep)
        steps.reverse() #reverse the order

    return (steps,visited_BFS)

def checkAStar(dim, arr, initial, goal): #check if there is a A* path
    fringe_AStar = [] #fringe is a heapq for A*
    visited_AStar = []
    heapq.heappush(fringe_AStar, (1,initial)) #push initial onto fringe
    path = False
    current = State(0,0,0,None) #initialize a current State
    total = 0 #keeps track of steps taken from the start

    while len(fringe_AStar)>=1:
        total = total + 1 #increment total to represent taking a step
        current = heapq.heappop(fringe_AStar)[1] #pops off State with lowest priority
        visited_AStar.append(current) #add current State to list of visited States
        if current.x == goal.x and current.y == goal.y: #check if current State is goal State
            path=True #A* path found
            break
        neighbors = current.getValidNeighbors(arr,dim) #get all neighbors of current where there are no obstacles
        for i in range(len(neighbors)):
            check = in_list(neighbors[i], visited_AStar) #check to see if each neighbor has been visited yet
            check2 = in_heap(neighbors[i], fringe_AStar) #check to see if each neighbor is on the fringe yet
            if not check and not check2:
                neighbors[i].total = total
                newState = State(neighbors[i].x,neighbors[i].y,neighbors[i].value,current)
                priority = neighbors[i].total + findDistance(neighbors[i],goal) #distance traveled + euclidean distance to go
                heapq.heappush(fringe_AStar,(priority,newState)) #add the neighbor and its priority to the fringe

    steps = [] # store A* path
    if not path:
        return (steps,visited_AStar)
    else:
        ptr = current #start with most recent node as a pointer

        while ptr.prev: #backtrack while adding to the path
            strStep = (ptr.x,ptr.y)
            steps.append(strStep)
            ptr = ptr.prev

        strStep = (initial.x,initial.y)
        steps.append(strStep)
        steps.reverse() #reverse the order

    return (steps,visited_AStar) #return the path

def advance_fire(dim,q,arr): #advance the fire one time
    arr2 = [[State(0,0,0,None) for i in range(dim)] for j in range(dim)]

    #make copy of array
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr2[i][j].x = arr[i][j].x
            arr2[i][j].y = arr[i][j].y
            arr2[i][j].value = arr[i][j].value
            arr2[i][j].prev = arr[i][j].prev

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j].value == 0:
                neighbor = arr[i][j].getAllNeighbors(arr,dim) #get all neighbors
                k = 0
                for z in range(len(neighbor)):
                    if neighbor[z].value == 2:
                        k = k + 1 #count number of burning neighbors
                prob = 1 - math.pow(1-q,k) #calculate probability based on k
                num = random.random()
                if num <= prob: 
                    arr2[i][j].value = 2 #based on probability calculation, set on fire

    #make sure S and G are not on fire 
    arr2[0][0].value = 0
    arr2[dim-1][dim-1].value = 0
    return arr2

def strategy1(dim, p, q, arr, initial, goal): #check if there is a path using Strategy 1
    arr2 = [[State(0,0,0,None) for i in range(dim)] for j in range(dim)]

    #make copy of array
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr2[i][j].x = arr[i][j].x
            arr2[i][j].y = arr[i][j].y
            arr2[i][j].value = arr[i][j].value
            arr2[i][j].prev = arr[i][j].prev

    pathBFS = checkBFS(dim,arr2, arr2[initial.x][initial.y], arr2[goal.x][goal.y])[0]
    path = []

    if len(pathBFS)==0: #no path found
        return(path, arr2)

    for i in range(len(pathBFS)): #step through BFS path
        path.append(pathBFS[i])
        temp = pathBFS[i]
        arr2 = advance_fire(dim,q,arr2) #advance the fire one step
        
        if arr2[temp[0]][temp[1]].value == 2: #check if agent burns down
            print ("Burned Down at ",[temp[0]],[temp[1]],"!")
            return (path,arr2)

    return (path,arr2)

def strategy2(dim, p, q, arr, initial, goal): #check if there is a path using Strategy 2
    arr2 = [[State(0,0,0,None) for i in range(dim)] for j in range(dim)]

    #make copy of array
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr2[i][j].x = arr[i][j].x
            arr2[i][j].y = arr[i][j].y
            arr2[i][j].value = arr[i][j].value
            arr2[i][j].prev = arr[i][j].prev

    pathBFS = checkBFS(dim,arr2, arr2[initial.x][initial.y], arr2[goal.x][goal.y])[0] #check if there is an initial BFS path
    path = []

    path.append((initial.x, initial.y)) #add initial to path
    last = path[len(path)-1] #keep track of last

    if len(pathBFS)==0: #no path found
        return ([], arr)

    while not (last[0] == goal.x and last[1] == goal.y):  #while G is not found
        pathBFS = checkBFS(dim,arr2, find_state(last,arr2), goal)[0] #recompute BFS path
        if len(pathBFS) == 0: #if there is no path found, we are blocked
            print("Got Blocked at ",[temp.x],[temp.y],"!")
            return (path,arr2)

        temp = find_state(pathBFS[1], arr2)

        path.append((temp.x,temp.y)) #add to path
        arr2 = advance_fire(dim,q,arr2) #advance the fire one step

        if arr2[temp.x][temp.y].value == 2: #check if agent burns down
            print ("Burned Down at ",[temp.x],[temp.y],"!")
            return (path,arr2)
        last = path[len(path)-1] #update last

    return (path,arr2)

def strategy3(dim, p, q, arr, initial, goal): #check if there is a path using Strategy 3
    arr2 = [[State(0,0,0,None) for i in range(dim)] for j in range(dim)]

    #make copy of array
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr2[i][j].x = arr[i][j].x
            arr2[i][j].y = arr[i][j].y
            arr2[i][j].value = arr[i][j].value
            arr2[i][j].prev = arr[i][j].prev

    pathBFS = checkBFS(dim,arr2, initial, goal)[0] #check if there is an initial BFS path
    path = []
    path.append((initial.x, initial.y)) #add initial to path
    last = path[len(path)-1] #keep track of last

    next = [[State(0,0,0,None) for i in range(dim)] for j in range(dim)]
    for i in range(len(arr2)):
        for j in range(len(arr2[i])):
            next[i][j].x = arr2[i][j].x
            next[i][j].y = arr2[i][j].y
            next[i][j].value = arr2[i][j].value
            next[i][j].prev = arr2[i][j].prev

    if len(pathBFS)==0:
        return ([], arr2)

    while not last[0] == goal.x or not last[1] == goal.y: #while G is not found
        pathBFS = checkBFS(dim,arr2, find_state(last,arr2), goal)[0] #recompute BFS path
        arr2 = advance_fire(dim,q,arr2) #advance fire one step
        next = advance_fire(dim,q,arr2) #advance already advanced fire one step to use as a prediction
        tempBFS = checkBFS(dim,next, find_state(last,next), goal)[0] #store path of prediction

        if len(pathBFS) == 0: #if there is no path found, we are blocked
            print("Got Blocked at ",[temp.x],[temp.y],"!")
            return (path,arr2)

        if len(tempBFS) > 0: #if there is a predicted BFS path found, update the BFS path
            pathBFS = tempBFS

        temp = find_state(pathBFS[1], arr2)
        path.append((temp.x,temp.y)) #add to path

        if arr2[temp.x][temp.y].value == 2: #check if agent burned down
            print ("Burned Down at ",[temp.x],[temp.y],"!")
            return (path,arr2)

        last = path[len(path)-1] #update last
    
    return (path,arr2)

def find_state(obj, arr): #find state object in array based on x and y coordinate
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j].x == obj[0] and arr[i][j].y == obj[1]:
                return arr[i][j]
    return None


def in_list(obj, visited): #checks to see if an object is in the visited list
    for v in visited:
        if obj.x == v.x and obj.y == v.y:
            return True
    return False

def in_queue(obj, fringe): #checks to see if an object is in the fringe for DFS and BFS
    for f in list(fringe.queue):
        if obj.x == f.x and obj.y == f.y:
            return True
    return False

def in_heap(obj, fringe): #checks to see if an object is in the fringe for A*
    for h in fringe:
        if obj.x == h[1].x and obj.y == h[1].y:
            return True
    return False

def findDistance(current,goal): #euclidean distance formula
    a = [current.x,current.y]
    b = [goal.x,goal.y]
    distance = math.sqrt( ((a[0]-b[0])**2)+((a[1]-b[1])**2) )
    return distance

def printArray(arr): #print an array in Maze format
    for i in range(len(arr)):
        for j in range(len(arr[i])):
           arr[i][j].printElement()
        print()
        
class State:
    total = 0 #store steps taken for A*

    def __init__(self, x, y, value, prev):
        self.x = x #the x coordinate in the maze array
        self.y = y #the y coordinate in the maze array
        self.value=value #integer value to determine if restricted
        self.prev=prev #State that was previously visited

    def __lt__(self, other):
        return True

    def printElement(self):
        print (self.value,end='')

    def getValidNeighbors(self,array,dim): #checks for up, down, left, right neighbors and returns the unrestricted States
        list = []
        if self.x + 1 < dim:
            if array[self.x+1][self.y].value == 0:
                list.append(array[self.x+1][self.y])
        if self.y + 1 < dim:
            if array[self.x][self.y+1].value == 0:
                list.append(array[self.x][self.y+1])
        if self.y - 1 >= 0:
            if array[self.x][self.y-1].value == 0:
                list.append(array[self.x][self.y-1])
        if self.x - 1 >= 0:
            if array[self.x-1][self.y].value == 0:
                list.append(array[self.x-1][self.y])
        return list

    def getAllNeighbors(self, array,dim): #checks for up, down, left, right neighbors and returns all
        list = []
        if self.x + 1 < dim:
           list.append(array[self.x+1][self.y])
        if self.y + 1 < dim:
            list.append(array[self.x][self.y+1])
        if self.y - 1 >= 0:
           list.append(array[self.x][self.y-1])
        if self.x - 1 >= 0:
            list.append(array[self.x-1][self.y])
        return list
