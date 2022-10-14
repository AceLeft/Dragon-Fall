import pygame
import ConstantHolder
import GroupHolder
import ImageHolder

def init():
   global screen
   screen = pygame.display.set_mode((ConstantHolder.WIDTH, ConstantHolder.HEIGHT))

def fillScreenBlack():
    screen.fill(ConstantHolder.BLACK)

def drawText(text,size,x,y, color):
   font = pygame.font.Font(pygame.font.match_font("helvetica", True, False), size)
   textSurface = font.render(text, True ,color)
   textRect = textSurface.get_rect()
   textRect.midtop = (x,y)
   screen.blit(textSurface,textRect)
   
def drawHealthBar(x,y,health):
   if health <0:
      health = 0
   fill = (health/75)*100
   outlineRect = pygame.Rect(x,y,100,10)
   fillRect = pygame.Rect(x,y,fill,10)
   pygame.draw.rect(screen,ConstantHolder.RED,fillRect)
   pygame.draw.rect(screen,ConstantHolder.WHITE,outlineRect,2)
   
def drawEnemyBar(x,y,health):
   if health <0:
      health = 0
   fill = (health/500)*200
   outlineRect = pygame.Rect(x,y,200,10)
   fillRect = pygame.Rect(x,y,fill,10)
   pygame.draw.rect(screen,ConstantHolder.GREEN,fillRect)
   pygame.draw.rect(screen,ConstantHolder.WHITE,outlineRect,2)
   
def drawFloor():
   floor = pygame.Rect(0,ConstantHolder.FLOOR,ConstantHolder.WIDTH,ConstantHolder.HEIGHT-ConstantHolder.FLOOR)
   pygame.draw.rect(screen,ConstantHolder.FLOORCOLOR,floor)
   
def drawGroups():
   GroupHolder.drawLast.draw(screen)
   GroupHolder.drawMid.draw(screen)
   GroupHolder.drawFirst.draw(screen)
   GroupHolder.drawTopMost.draw(screen)

def drawEverything(player, dragon):
   screen.fill(ConstantHolder.BLACK)
   screen.blit(ImageHolder.background,ImageHolder.background.get_rect())
   drawHealthBar(5,5,player.health)
   drawEnemyBar(295,5,dragon.head.health)
   drawFloor()
   drawGroups()
   pygame.display.flip()