import pygame
import ImageUtil
import Company
from Constants import *
import Map
import Build
import City
import SoundUtil
import PathFinding
import Notification

icons = []
activeIcon = None
pauseActive = False


isMenuCompanyOpen = False


buildingMenuOpen = False


def initUI(functionPause):
    global icons
    loadImages()

    # (imagename, id, (xpos, ypos), onClickFunction, isToggleable, isToggled, function parameter)

    icons.append(["menu-pause", 0, (0,0), functionPause, True, False, None])
    #icons.append(["menu-city", 1, (UI_ICON_SIZE*2, 0), openMenu, False, False, 1])
    #icons.append(["menu-company",2,  (UI_ICON_SIZE*3, 0), Notification.addNotification , False, False, "Citizens worry as full garbage trucks roam the city without a landfill to go to!"])
    icons.append(["menu-build-road", 3, (UI_ICON_SIZE*2, 0), setBuildMode, True, False, BUILD_MODE_ROAD])
    icons.append(["menu-build-landfill", 4, (UI_ICON_SIZE*3, 0), setBuildMode, True, False, BUILD_MODE_LANDFILL])
    icons.append(["menu-trucks", 5, (UI_ICON_SIZE*7, 0), buyTruck, False, True, 0])
    icons.append(["menu-bomb", 6, (UI_ICON_SIZE*5,0), setBuildMode, True, False, BUILD_MODE_DELETE])
    icons.append(["menu-building", 7, (UI_ICON_SIZE*4,0), openMenu, True, False, 7])
    icons.append(["menu-fire", 90, (UI_ICON_SIZE*4,UI_ICON_SIZE), setBuildMode, True, False, BUILD_MODE_FIRE])
    icons.append(["menu-recycle", 90, (UI_ICON_SIZE*5,UI_ICON_SIZE), setBuildMode, True, False, BUILD_MODE_RECYCLE])
    icons.append(["menu-blackhole", 90, (UI_ICON_SIZE*6,UI_ICON_SIZE), setBuildMode, True, False, BUILD_MODE_BLACKHOLE])
    
    

def loadImages():
    ImageUtil.create_image("menu-pause", "res/menu/menu-pause.png", False)
    ImageUtil.create_image("menu-city", "res/menu/menu-city.png", False)
    ImageUtil.create_image("menu-build-road", "res/menu/menu-build-road.png", False)
    ImageUtil.create_image("menu-company", "res/menu/menu-company.png", False)
    ImageUtil.create_image("menu-build-landfill", "res/menu/menu-landfill.png", False)
    ImageUtil.create_image("menu-trucks", "res/menu/menu-truck.png", False)
    ImageUtil.create_image("menu-building", "res/menu/menu-building.png", False)
    ImageUtil.create_image("menu-bomb", "res/menu/menu-bomb.png", False)
    ImageUtil.create_image("menu-fire", "res/menu/menu-fire.png", False)
    ImageUtil.create_image("menu-blackhole", "res/menu/menu-blackhole.png", False)
    ImageUtil.create_image("menu-recycle", "res/menu/menu-recycle.png", False)
    
    
    



def render(screen):
    global icons
    global activeIcon
    global pauseActive
    global buildingMenuOpen
    font = pygame.font.Font(None, 30)
    backrect = pygame.draw.rect(screen, (73, 130, 179), [0,0,UI_ICON_SIZE*8, UI_ICON_SIZE])
    for i in icons:
        if(i != None):
            if(i[1] != 90):
                screen.blit(ImageUtil.get_image(i[0]), (i[2][0], i[2][1]))
        
            if(i[1] == 90):
                if(buildingMenuOpen):
                    screen.blit(ImageUtil.get_image(i[0]), (i[2][0], i[2][1]))

            if(activeIcon == i):
                rect = pygame.Surface((UI_ICON_SIZE,UI_ICON_SIZE))
                rect.set_alpha(100)
                rect.fill((0,0,0))
                screen.blit(rect, (i[2][0], i[2][1]))

    if(pauseActive):
        rect = pygame.Surface((UI_ICON_SIZE, UI_ICON_SIZE))
        rect.set_alpha(100)
        rect.fill((0,0,0))
        screen.blit(rect, (0,0))


    mousePos = pygame.mouse.get_pos()
    if(mousePos[0] > icons[3][2][0] and mousePos[0] < icons[3][2][0] + UI_ICON_SIZE):
        if(mousePos[1] > icons[3][2][1] and mousePos[1] < icons[3][2][1] + UI_ICON_SIZE):
            color = (255,255,255)
            if(Company.Money < PathFinding.VehicleTypes[0][3]):
                color = (255,0,0)
            monText = font.render(str(PathFinding.VehicleTypes[0][3]) + "$", True, color)
            screen.blit(monText, (mousePos[0], mousePos[1] + 15))

    moneytext = font.render(str(Company.Money) + "$", True, (0, 0, 0))
    
    poeplestr = "Population: " + str(int(City.Population))
    poepletext = font.render(poeplestr, True, (0,0,0))

    garbagestr = "Garbage to Collect: " + str(int(City.AmoutOfTrash))
    garbagetext = font.render(garbagestr, True, (0,0,0))

    pollutionstr = "Pollution: " + str(int(Map.Pollution)) + "%"
    Pollutiontext = font.render(pollutionstr, True, (0,0,0))

    screen.blit(moneytext, (50,screen.get_height() - 40))
    screen.blit(poepletext, (screen.get_width() - poepletext.get_width() - 10, screen.get_height() - 40))
    screen.blit(garbagetext, (screen.get_width() - garbagetext.get_width() - 10, screen.get_height() - 70))
    screen.blit(Pollutiontext, (screen.get_width() - Pollutiontext.get_width() - 10, screen.get_height() - 100))




def mouseClick(x,y):
    global activeIcon
    global pauseActive
    global buildingMenuOpen
    for i in icons:
        if(x > i[2][0] and x < i[2][0] + UI_ICON_SIZE):
            if(y > i[2][1] and y < i[2][1] + UI_ICON_SIZE):
                if(i[1] == 90):
                    if(buildingMenuOpen == False):
                        continue

                SoundUtil.play_sound("click")

                if(i[4] == True):
                    i[5] = not i[5]

                if(i[1] == 0):
                    pauseActive = not pauseActive
                    setBuildMode(0, None)

                if(i[3] == openMenu or i[3] == buyTruck or i[3] == Notification.addNotification):
                    i[3](i[6])
                    return True
                if(i[3] == setBuildMode):
                    if(pauseActive == False):
                        i[3](i[6], i)
                    return True
                
                i[3]()

                return True
    return False



def setBuildMode(modeID, icon):
    global activeIcon
    global buildingMenuOpen

    if(icon == None):
        activeIcon = None
        Map.buildMode = 0
        Build.buildMode = 0
        return

    if(activeIcon == icon):
        activeIcon = None
        Map.buildMode = 0
        Build.buildMode = 0

    else:
        activeIcon = icon
        Map.buildMode = modeID
        Build.buildMode = modeID
    
    if icon[1] != 90:
        buildingMenuOpen = False


def openMenu(index):
    global buildingMenuOpen
    global activeIcon
    if(index == 7):
        if(buildingMenuOpen):
            activeIcon = None
            Build.buildMode = 0
            Map.buildMode = 0
            buildingMenuOpen = False
        else:
            buildingMenuOpen = True
            


def buyTruck(id):
    truckType = PathFinding.VehicleTypes[id]
    if(Company.Money >= truckType[3]):
        PathFinding.createVehicle(id)
        Company.Money -= truckType[3]