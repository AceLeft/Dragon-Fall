
import pygame
import ConstantHolder

def init():
   global stalactiteImage, background, bodyImage, headImage
   global radishImage, diamondImage, chestImage, candelabraImage
   global helmetRedImage, helmetBlueImageLeft, helmetBlueImageRight
   global hornImage, startScreenUnder, startScreenAbove
   global endScreen, batImages
   pygame.init()
   stalactiteImage = pygame.image.load("images/stalactite.gif").convert()
   background = pygame.image.load("images/cave.gif").convert()
   bodyImage = pygame.image.load("images/body.gif").convert()
   headImage = pygame.image.load("images/head.gif").convert()
   radishImage = pygame.image.load("images/radish.gif").convert()
   diamondImage = pygame.image.load("images/diamond.gif").convert()
   chestImage = pygame.image.load("images/chest.gif").convert()
   candelabraImage = pygame.image.load("images/candelabra.gif").convert()
   helmetRedImage = pygame.image.load("images/helmetR.gif").convert()
   helmetBlueImageLeft = pygame.image.load("images/helmetB.gif").convert()
   helmetBlueImageRight = pygame.image.load("images/helmetB2.gif").convert()
   hornImage = pygame.image.load("images/horn.gif").convert()
   startScreenUnder = pygame.image.load("images/startUnder.gif").convert()
   startScreenAbove = pygame.image.load("images/startUpper.gif").convert()
   endScreen = pygame.image.load("images/endUnder.gif").convert()
   batImage1 = pygame.image.load("images/batClosed.gif").convert()
   batImage2 = pygame.image.load("images/batOpen.gif").convert()
   batImages = [batImage1,batImage2]
   
   global swordAnim
   swordAnim = {}
   swordAnim["right"] = []
   swordAnim["left"] = []
   for i in range(1,6,1):
      filename = "images/sword{}.gif".format(i)
      img = pygame.image.load(filename).convert()
      img.set_colorkey(ConstantHolder.BLACK)
      swordAnim["right"].append(img)
   
   img = pygame.image.load("images/sword1.gif").convert()
   swordAnim["right"].append(img)
   swordAnim["left"].append(img)
   for i in range(6,1,-1):
      filename = "images/sword{}.gif".format(i)
      img = pygame.image.load(filename).convert()
      img.set_colorkey(ConstantHolder.BLACK)
      swordAnim["left"].append(img)
      
      