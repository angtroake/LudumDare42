import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import csv
import random
import json
import Map
import ImageUtil
from Constants import *



#                                 0                    1          2           3          4        5        6        
#    STRUCTURE:     [(currentCordX, currentCoordY), typeID, targetPosNode, Capacity, AmountFill, path, pathindex, ]
LiveVehicles = []

#                           0       1        2(0=TL,1=TR,2=BR,3=BL)
#    STRUCTURE:     [id, (name, capacity, images)]
VehicleTypes = {}

finder = AStarFinder()

CurrentTick = 0
MaxTick = 40


def initVehicleTypes():
    global VehicleTypes
    with open("vehicle.json") as jsonFile:
        tempData = json.load(jsonFile)
        for val in tempData:
            images = (tempData[val]["image-name-TL"], tempData[val]["image-name-TR"], tempData[val]["image-name-BR"], tempData[val]["image-name-BL"])
            VehicleTypes[tempData[val]["id"]] = (tempData[val]["name"], tempData[val]["capacity"], images)


def createVehicle(id):
    global VehicleTypes
    global LiveVehicles

    startCoords = getNewRoadTarget()
    randomTarget = getNewRoadTarget()

    path = getPath(startCoords, randomTarget)


    vehicle = [(startCoords[0], startCoords[1]), id, randomTarget, VehicleTypes[id][0], 0, path, 0]
    LiveVehicles.append(vehicle)





def tick():
    global LiveVehicles
    global CurrentTick
    global MaxTick
    if(CurrentTick >= MaxTick):
        for vehicle in LiveVehicles:
            currentpos = vehicle[0]
            path = vehicle[5]
            pathindex = vehicle[6]
            endpos = vehicle[2]
            #print("Current Pos: " + str(currentpos) + "   End Pos: " + str(endpos) + "   Path Length: " + str(len(path)) + "   Path Index: " + str(pathindex))


            if((currentpos[0] == endpos[0] and currentpos[1] == endpos[1]) or endpos[0] == None or len(path) <= 0 or pathindex >= len(path)):
                vehicle[2] = getNewRoadTarget()
                startpos = currentpos
                vehicle[5] = getPath(startpos, vehicle[2])
                vehicle[6] = 0
                Map.testTruckEnd = endpos
                continue

            #vehicle[0] = [path[pathindex][0], path[pathindex][1]]
            vehicle[0] = [path[pathindex][0], path[pathindex][1]]
            vehicle[6] += 1

        CurrentTick = 0
    else:
        CurrentTick += 1


def render(screen):
    global LiveVehicles
    for vehicle in LiveVehicles:
        renderVehicle(vehicle, screen)



def renderVehicle(vehicle, screen):
    currentpos = vehicle[0]
    images = VehicleTypes[vehicle[1]][2]
    image = ImageUtil.get_image(images[3])
    isoPos = Map.getScreenPositionOfCoord(currentpos[0], currentpos[1])
    if(vehicle[6] < len(vehicle[5])):
        nextpos = vehicle[5][vehicle[6]]
        #pygame.draw.rect(screen, (255,0,0), [isoPos[0]-25, isoPos[1]-25, 50, 50])

        if(nextpos[0] > currentpos[0]):
            image = ImageUtil.get_image(images[1])
        elif(nextpos[0] < currentpos[0]):
            image = ImageUtil.get_image(images[3])
        elif(nextpos[1] > currentpos[1]):
            image = ImageUtil.get_image(images[2])
        elif(nextpos[1] < currentpos[1]):
            image = ImageUtil.get_image(images[0])
        
        isoPos[0] += (TILE_WIDTH/2 - image.get_width()/2)
        isoPos[1] -= image.get_height()/2
            
    screen.blit(image, isoPos)


"""
returns vehicle if there is one in that tile
if not it returns false
"""
def tileHasVehicle(x, y):
    global LiveVehicles
    for vehicle in LiveVehicles:
        if(vehicle[0][0] == x and vehicle[0][1] == y):
            return vehicle

    return False





#---------------------------------PATH FINDING FUNCTIONS-------------------------------------



"""
gets the path from start pos to end on PATHMAP. returns a list of positions (AKA move to this pos next)
"""
def getPath(start, end):
    RoadMap = Map.PATHMAP
    global finder

    grid = Grid(matrix = RoadMap)
    start = grid.node(start[0], start[1])
    end = grid.node(end[0], end[1])
    path, runs = finder.find_path(start, end, grid)
    #print(grid.grid_str(path=path, start=start, end=end))

    return path



"""
Returns a random spot on PATHMAP where there is a road
"""
def getNewRoadTarget():
    RoadMap = Map.PATHMAP
    returns = [0,0]
        
    while RoadMap[returns[0]][returns[1]] != '1' and RoadMap != None:
        returns = random.choice([(j,i) for i, row in enumerate(RoadMap) for j, val in enumerate(row) if val=='1'])

    return returns










#--------- OLD CODE USED FOR TESTING
"""
def run():
    matrix = None

    with open("maps/pathfindingtestmap.csv") as csvmap:
        reader = csv.reader(csvmap)
        matrix = list(reader)
    

    grid = Grid(matrix = matrix)
    start = grid.node(1,4)
    end = grid.node(26,13)

    print(len(matrix))

    while(matrix[start.x][start.y] != '1'):
        start = grid.node(random.randint(0, len(matrix[0]))-1, random.randint(0, len(matrix))-1)
        

    finder = AStarFinder()
    path, runs = finder.find_path(start, end, grid)

    print("RUNS: ", runs, "path length: ", len(path))
    print(grid.grid_str(path=path, start=start, end=end))
    print(path[0])
    print(path[1])
"""
