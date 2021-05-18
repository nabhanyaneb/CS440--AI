import matplotlib.pyplot as plt
import math
import random
from random import randrange
import minesweeper_basic_agent
import minesweeper_advanced_agent
import minesweeper_basic_better_decisions
import minesweeper_advanced_better_decisions
import minesweeper_basic_global_information
import minesweeper_advanced_global_information
import numpy as np

def plot_basic(dim): #basic agent plot

    x = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store mine density values between 0 and 1
    y = [0.0 for i in range(len(x))] #store average score
    count = 10

    for i in range(len(x)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        total = 0.0 #keeps track of score
        mine_density = round(x[i]*dim*dim) #calculate number of mines based on board dimensions
        if mine_density != 0:
            for j in range(0,count):
                total = total + minesweeper_basic_agent.run_game(dim,mine_density)/mine_density #run the game
        y[i] = total/count #find average

    #creating plot using matplotlib
    plt.plot(x, y,'r')
    plt.margins(0.1)
    plt.xlabel('Mine Density')
    plt.ylabel('Average Final Score')
    plt.title('Mine Density vs Average Final Score')
    plt.show()

def plot_advanced(dim): #advanced agent plot

    x = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store mine density values between 0 and 1
    y = [0.0 for i in range(len(x))] #store average score
    count = 10

    for i in range(len(x)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        total = 0.0 #keeps track of score
        mine_density = round(x[i]*dim*dim) #calculate number of mines based on board dimensions
        if mine_density != 0:
            for j in range(0,count):
                total = total + minesweeper_advanced_agent.run_game(dim,mine_density)/mine_density #run the game
        y[i] = total/count #find average

    #creating plot using matplotlib
    plt.plot(x, y,'b')
    plt.margins(0.1)
    plt.xlabel('Mine Density')
    plt.ylabel('Average Final Score')
    plt.title('Mine Density vs Average Final Score')
    plt.show()

def plot_both(dim): #basic agent and advanced agent plot

    x1 = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store mine density values between 0 and 1
    y1 = [0.0 for i in range(len(x1))] #store average score for advanced agent

    x2 = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store mine density values between 0 and 1
    y2 = [0.0 for i in range(len(x2))] #store average score for basic agent
    
    count = 10

    #advanced agent
    for i in range(len(x1)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        total = 0.0 #keeps track of score
        mine_density = round(x1[i]*dim*dim) #calculate number of mines based on board dimensions
        if mine_density > 0:
            for j in range(0,count):
                total = total + minesweeper_advanced_agent.run_game(dim,mine_density)/mine_density #run the game
        y1[i] = total/count #find average

    #basic agent
    for i in range(len(x2)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        total = 0.0 #keeps track of score
        mine_density = round(x2[i]*dim*dim) #calculate number of mines based on board dimensions
        if mine_density > 0:
            for j in range(0,count):
                total = total + minesweeper_basic_agent.run_game(dim,mine_density)/mine_density #run the game

        y2[i] = total/count #find average
    
    #creating plot using matplotlib
    plt.plot(x1, y1,'r')
    plt.plot(x2, y2,'b')
    plt.margins(0.1)
    plt.xlabel('Mine Density')
    plt.ylabel('Average Final Score')
    plt.title('Mine Density vs Average Final Score')
    plt.show()

def plot_basic_random(dim): #basic agent and basic agent with better decisions plot

    x1 = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store mine density values between 0 and 1
    y1 = [0.0 for i in range(len(x1))] #store average score for basic agent

    x2 = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store mine density values between 0 and 1
    y2 = [0.0 for i in range(len(x2))] #store average score for basic agent with better decisions
    
    count = 10

    #basic agent
    for i in range(len(x1)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        total = 0.0 #keeps track of score
        mine_density = round(x1[i]*dim*dim) #calculate number of mines based on board dimensions
        if mine_density > 0:
            for j in range(0,count):
                total = total + minesweeper_basic_agent.run_game(dim,mine_density)/mine_density #run the game
        y1[i] = total/count #find average

    #basic agent with better decisions
    for i in range(len(x2)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        total = 0.0 #keeps track of score
        mine_density = round(x2[i]*dim*dim) #calculate number of mines based on board dimensions
        if mine_density > 0:
            for j in range(0,count):
                total = total + minesweeper_basic_better_decisions.run_game(dim,mine_density)/mine_density #run the game

        y2[i] = total/count #find average
    
    #creating plot using matplotlib
    plt.plot(x1, y1,'b')
    plt.plot(x2, y2,'g')
    plt.margins(0.1)
    plt.xlabel('Mine Density')
    plt.ylabel('Average Final Score')
    plt.title('Mine Density vs Average Final Score')
    plt.show()

def plot_advanced_random(dim): #advanced agent and advanced agent with better decisions plot

    x1 = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store mine density values between 0 and 1
    y1 = [0.0 for i in range(len(x1))] #store average score for advanced agent

    x2 = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store mine density values between 0 and 1
    y2 = [0.0 for i in range(len(x2))] #store average score for advanced agent with better decisions
    
    count = 10

    #advanced agent
    for i in range(len(x1)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        total = 0.0 #keeps track of score
        mine_density = round(x1[i]*dim*dim) #calculate number of mines based on board dimensions
        if mine_density > 0:
            for j in range(0,count):
                total = total + minesweeper_advanced_agent.run_game(dim,mine_density)/mine_density #run the game
        y1[i] = total/count #find average

    #advanced agent with better decisions
    for i in range(len(x2)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        total = 0.0 #keeps track of score
        mine_density = round(x2[i]*dim*dim) #calculate number of mines based on board dimensions
        if mine_density > 0:
            for j in range(0,count):
                total = total + minesweeper_advanced_better_decisions.run_game(dim,mine_density)/mine_density #run the game

        y2[i] = total/count #find average
    
    #creating plot using matplotlib
    plt.plot(x1, y1,'r')
    plt.plot(x2, y2,'g')
    plt.margins(0.1)
    plt.xlabel('Mine Density')
    plt.ylabel('Average Final Score')
    plt.title('Mine Density vs Average Final Score')
    plt.show()

def plot_basic_mines(dim): #basic agent and basic agent with global information plot

    x1 = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store mine density values between 0 and 1
    y1 = [0.0 for i in range(len(x1))] #store average score for basic agent

    x2 = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store mine density values between 0 and 1
    y2 = [0.0 for i in range(len(x2))] #store average score for basic agent with global information
    
    count = 10

    #basic agent
    for i in range(len(x1)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        total = 0.0 #keeps track of score
        mine_density = round(x1[i]*dim*dim) #calculate number of mines based on board dimensions
        if mine_density > 0:
            for j in range(0,count):
                total = total + minesweeper_basic_agent.run_game(dim,mine_density)/mine_density #run the game
        y1[i] = total/count #find average

    #basic agent with global information
    for i in range(len(x2)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        total = 0.0 #keeps track of score
        mine_density = round(x2[i]*dim*dim) #calculate number of mines based on board dimensions
        if mine_density > 0:
            for j in range(0,count):
                total = total + minesweeper_basic_global_information.run_game(dim,mine_density)/mine_density #run the game

        y2[i] = total/count #find average
    
    #creating plot using matplotlib
    plt.plot(x1, y1,'b')
    plt.plot(x2, y2,'m')
    plt.margins(0.1)
    plt.xlabel('Mine Density')
    plt.ylabel('Average Final Score')
    plt.title('Mine Density vs Average Final Score')
    plt.show()

def plot_advanced_mines(dim): #advanced agent and advanced agent with global information plot

    x1 = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store mine density values between 0 and 1
    y1 = [0.0 for i in range(len(x1))] #store average score for advanced agent

    x2 = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0] #store mine density values between 0 and 1
    y2 = [0.0 for i in range(len(x2))] #store average score for advanced agent with global information
    
    count = 10

    #advanced agent
    for i in range(len(x1)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        total = 0.0 #keeps track of score
        mine_density = round(x1[i]*dim*dim) #calculate number of mines based on board dimensions
        if mine_density > 0:
            for j in range(0,count):
                total = total + minesweeper_advanced_agent.run_game(dim,mine_density)/mine_density #run the game
        y1[i] = total/count #find average

    #advanced agent with global information
    for i in range(len(x2)):
        prob = 0.0 #holds the value that will go into the corresponding y index
        total = 0.0 #keeps track of score
        mine_density = round(x2[i]*dim*dim) #calculate number of mines based on board dimensions
        if mine_density > 0:
            for j in range(0,count):
                total = total + minesweeper_advanced_global_information.run_game(dim,mine_density)/mine_density #run the game

        y2[i] = total/count #find average
    
    #creating plot using matplotlib
    plt.plot(x1, y1,'r')
    plt.plot(x2, y2,'m')
    plt.margins(0.1)
    plt.xlabel('Mine Density')
    plt.ylabel('Average Final Score')
    plt.title('Mine Density vs Average Final Score')
    plt.show()

def run_plot(plotType,dim): #run plot corresponding to string input
    if plotType == "plot_basic":
        plot_basic(dim)
    if plotType == "plot_advanced":
        plot_basic(dim)
    if plotType == "plot_both":
        plot_both(dim)
    if plotType == "plot_basic_random":
        plot_basic_random(dim)
    if plotType == "plot_advanced_random":
        plot_advanced_random(dim)
    if plotType == "plot_basic_mines":
        plot_basic_mines(dim)
    if plotType == "plot_advanced_mines":
        plot_advanced_mines(dim)

#run_plot("plot_basic",10)
#run_plot("plot_advanced",10)
#run_plot("plot_both",10)
#run_plot("plot_basic_random",10)
#run_plot("plot_advanced_random",10)
#run_plot("plot_basic_mines",10)
#run_plot("plot_advanced_mines",10)
