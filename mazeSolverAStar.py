# A* search Algorithm for mazes - Max Malacari 20/02/2017

import pygame as pg
import sys # to handle quit event
import random as rand
from math import *

# Some options to set!
wWidth = 800 # dimensions of the drawing window
wHeight = 800
cols = 50 # number of cells in each dimension
rows = 50
start_i = 0 # start and end cell coordinates
start_j = 0
end_i = cols - 1
end_j = rows -1
showPathAtEnd = True # only show the whole path once it's been found
showProcess = True # only show the solution process if we want to see it

# Some colours
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
yellow = (255,255,0)

w = wWidth / cols
h = wHeight / rows

pg.init()
screen = pg.display.set_mode((wWidth+2,wHeight+2))
screen.fill(black)

# Class to hold the properties of a cell
class Cell():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbours = []
        self.previous = 0
        self.isWall = [False, False, False, False]

    def show(self, colour):
        pg.draw.rect(screen, colour, (self.i*w+2, self.j*h+2, w-2, h-2), 0)

    def showCellBoundary(self): # Draw the cell walls
        if self.isWall[0] == True:
            pg.draw.lines(screen, white, False, ((self.i*w,self.j*h),((self.i+1)*w,self.j*h)), 2)
        if self.isWall[1] == True:
            pg.draw.lines(screen, white, False, (((self.i+1)*w,self.j*h),((self.i+1)*w,(self.j+1)*h)), 2)
        if self.isWall[2] == True:
            pg.draw.lines(screen, white, False, ((self.i*w,(self.j+1)*h),((self.i+1)*w,(self.j+1)*h)), 2)
        if self.isWall[3] == True:
            pg.draw.lines(screen, white, False, ((self.i*w,self.j*h),(self.i*w,(self.j+1)*h)), 2)

    def addNeighbours(self, grid):
        i = self.i
        j = self.j
        if grid[i][j].isWall[1] == False: # right
            self.neighbours.append(grid[i+1][j])
        if grid[i][j].isWall[2] == False: # bottom
            self.neighbours.append(grid[i][j+1])
        if grid[i][j].isWall[3] == False: # left
            self.neighbours.append(grid[i-1][j])
        if grid[i][j].isWall[0] == False: # top
            self.neighbours.append(grid[i][j-1])

def main():

    grid = []
    setup(grid, cols, rows)
    # Show walls (these are static)
    for i in range(0,cols):
        for j in range(0,rows):
            grid[i][j].showCellBoundary()
    pg.display.update()

    start = grid[start_i][start_j]
    end = grid[end_i][end_j]

    openSet = []
    closedSet = []

    openSet.append(start)
    finished = False

    while finished==False:

        path = []

        if showProcess == True:
            # Show cells in the open set
            for i in range(0,len(openSet)):
                openSet[i].show(green)
            # Show cells in the closed set
            for i in range(0,len(closedSet)):
                closedSet[i].show(red)

        # Algorithm
        if len(openSet) > 0:
            lowestCostIndex = 0
            current = openSet[lowestCostIndex]

            for i in range(0,len(openSet)):
                if openSet[i].f < openSet[lowestCostIndex].f:
                    lowestCostIndex = i
                    current = openSet[lowestCostIndex]
            if current == end:
                finished = True
                path = calculatePath(current) # get optimal path
                print "Solution found!"

            else:
                closedSet.append(current)
                openSet.remove(current)

                neighbours = current.neighbours
                for i in range(0,len(neighbours)):
                    neighbour = neighbours[i]
                    neighbour.h = heuristic(neighbour, end)
                    if neighbour in closedSet:
                        continue
                    temp_g = current.g + 1 # 1 movement cost to get to neighbour
                    if neighbour in openSet: # is neighbour already in the open set?
                        if temp_g < neighbour.g: # did we get there more efficiently?
                            neighbour.g = temp_g
                            neighbour.f = neighbour.h + neighbour.g
                            neighbour.previous = current
                    else:
                        neighbour.g = temp_g
                        neighbour.f = neighbour.h + neighbour.g
                        neighbour.previous = current
                        openSet.append(neighbour)

                    path = calculatePath(current) # get the current path to this cell

        else:
            finished = True # to quit the loop
            print "No solution!"

        # Show the current path
        ptList = [] # to show line instead of filling squares
        for i in range(0,len(path)):
            #path[i].show(blue)
            ptList.append((path[i].i*w + w/2, path[i].j*h + h/2))
        if showPathAtEnd == False and showProcess == True: # only show the path once it's found
            if len(ptList) > 1:
                showLine(ptList, blue)

        # show end points
        start.show(yellow)
        end.show(yellow)

        # Update the display with new draw objects
        if showProcess == True:
            pg.display.update()

    if len(ptList) > 1: # show path once solution has been found
        showLineAnimated(ptList, blue)
        start.show(yellow)
        end.show(yellow)
        pg.display.update()

    # save completed maze as an image
    pg.image.save(screen,"testSolved.jpg")

    # Stop from instantly closing on finish
    while(True):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(); sys.exit();

# Set up the grid of cell objects
def setup(grid, cols, rows):
    for i in range(0,cols):
        grid.append([])
        for j in range(0,rows):
            grid[i].append(Cell(i,j))

    # add in the maze walls from maze file
    addMazeWalls(grid)

    # add neighbours once grid is initialized
    for i in range(0,cols):
        grid.append([])
        for j in range(0,rows):
            grid[i][j].addNeighbours(grid)

def heuristic(cell1, cell2):
    h = abs(cell1.i - cell2.i) + abs(cell1.j - cell2.j)
    #h = sqrt((cell1.i-cell2.i)**2 + (cell1.j-cell2.j)**2)
    return h

def calculatePath(current): # get current optimal path up to current cell
    path = []
    temp = current
    path.append(temp)
    while temp.previous:
        path.append(temp.previous)
        temp = temp.previous
    return path

def addMazeWalls(grid): # add walls to the maze from maze wall file
    mazeFile = open("./mazeOut.dat","r")
    for line in mazeFile:
        counter = 0
        i = 0
        j = 0
        wall0 = 0
        wall1 = 0
        wall2 = 0
        wall3 = 0
        line = line.strip() # remove \n from end
        for entry in line.split(' '):
            if counter == 0:
                i = int(entry)
            if counter == 1:
                j = int(entry)
            if counter == 2:
                wall0 = isTrue(entry)
            if counter == 3:
                wall1 = isTrue(entry)
            if counter == 4:
                wall2 = isTrue(entry)
            if counter == 5:
                wall3 = isTrue(entry)
            counter = counter + 1
        grid[i][j].isWall[0] = wall0
        grid[i][j].isWall[1] = wall1
        grid[i][j].isWall[2] = wall2
        grid[i][j].isWall[3] = wall3
    mazeFile.close()

def isTrue(entry): # check if string is true or false boolean
    if entry == 'True':
        return True
    elif entry == 'False':
        return False

def showLine(ptList, colour): # show line instead of colouring squares
    pg.draw.lines(screen, colour, False, ptList, 7)

def showLineAnimated(ptList, colour): # animated version for end of algorithm!
    for i in range(0,len(ptList)-1):
        pg.draw.line(screen, colour, ptList[i], ptList[i+1], w/2)
        pg.display.update()

main()
