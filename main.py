import pygame
import sys
import ImageUtil
import Map
import Build
import City
import UI
import PathFinding

from Constants import *
from pygame.locals import *


pygame.init()

screen = pygame.display.set_mode((1280, 720), DOUBLEBUF)

done = False

font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

ImageUtil.create_image("test", "res/test.png")
ImageUtil.create_image("grass", "res/tile/tile-grass.png")
ImageUtil.create_image("house", "res/tile/tile-house.png")
ImageUtil.create_image("house1", "res/tile/tile-house1.png")
ImageUtil.create_image("house2", "res/tile/tile-house2.png")
ImageUtil.create_image("road", "res/tile/tile-road.png")
ImageUtil.create_image("water", "res/tile/tile-water-2.png")
ImageUtil.create_image("temp", "res/tile/tile-template.png")
ImageUtil.create_image("landfill", "res/tile/tile-template.png")
ImageUtil.create_image("truck1-TL", "res/trucks/truck1/truck1TL.png")
ImageUtil.create_image("truck1-TR", "res/trucks/truck1/truck1TR.png")
ImageUtil.create_image("truck1-BL", "res/trucks/truck1/truck1BL.png")
ImageUtil.create_image("truck1-BR", "res/trucks/truck1/truck1BR.png")


Map.loadMap()
Map.loadPathFindingMap()
Map.scrollX = 1000
Map.scrollY = -200
Map.loadGMap()
Map.loadTileData()
City.maptest()

PathFinding.initVehicleTypes()
PathFinding.createVehicle(0)


Zoom = 1
ZoomTick = 0

isPaused = False



#PathFinding.run()




def togglePauseGame():
    global isPaused
    isPaused = not isPaused


UI.initUI(togglePauseGame)



while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            uiclick = UI.mouseClick(mouseX, mouseY)
            if(not uiclick):
                Build.onMouseClick(mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            Build.onMouseRelease(mouseX, mouseY)

            """if(event.button == 4):
                if(Zoom > 0.5):
                    Zoom -= 0.5
            elif(event.type == 5):
                if(Zoom < 2):
                    Zoom += 0.5
            print(Zoom)
            Map.Zoom = Zoom"""


    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if(Map.scrollX < MAX_SCROLL_X):
            Map.scrollX += 20
    elif keys[pygame.K_LEFT]:
        if(Map.scrollX > MIN_SCROLL_X):
            Map.scrollX -= 20
    if keys[pygame.K_UP]:
        if(Map.scrollY > MIN_SCROLL_Y):
            Map.scrollY -= 20
    elif keys[pygame.K_DOWN]:
        if(Map.scrollY < MAX_SCROLL_Y):
            Map.scrollY += 20

    background = pygame.Surface(screen.get_size())
    background.fill((85,85,85))
    background = background.convert()
    screen.blit(background, (0,0))


    if(isPaused == False):
        Map.tick()
        City.tick()
        PathFinding.tick()



    Map.render(screen)
    Build.render(screen)
    #PathFinding.render(screen)
    UI.render(screen)
    
    fps = font.render(str(int(clock.get_fps())), True, (0, 0, 0))
    screen.blit(fps, (50,50))
    pygame.display.flip()

    clock.tick(240)

pygame.quit()
sys.exit()
