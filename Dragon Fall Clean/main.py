import pygame
import random
import math
from Player import Player
from Sword import Sword
from Hat import Hat
from Heal import Heal
from Bat import Bat
from Decoration import Decoration
from DecorationImage import DecorationImage
from Dragon import Dragon
from Cutscenes import Cutscenes
import Drawer
import ConstantHolder
import SoundHolder
import ImageHolder
import GroupHolder
#dragon flap noise thanks to VishwaJai on opengameart
#music by nene on opengameart
#wind sound thanks to DanSevenStar.com
#end/start music by Wolfgang on opengameart


pygame.init()
pygame.mixer.init()
ConstantHolder.init()
SoundHolder.init()
GroupHolder.init()
Drawer.init()
pygame.display.set_caption("Dragon Fall")
clock = pygame.time.Clock()
ImageHolder.init()
cutscenes = Cutscenes()

            
def stopSounds():
   SoundHolder.dragonChannel.stop()
   SoundHolder.windChannel.stop()
   pygame.mixer.music.stop()
   SoundHolder.playerChannel.stop()
   
def resetPlayer():
   player.health = 75
   player.speedx = 0
   player.speedy = 0
   player.rect.centerx = ConstantHolder.WIDTH /4
   player.rect.bottom = ConstantHolder.FLOOR
   player.removecontrols = False
   player.stopMoving = False
   player.dead = False

def killEverythingExceptPlayerThings():
   for attack in GroupHolder.allAttacks:
      attack.kill()
   for bat in GroupHolder.allBats:
      bat.kill()
   for radish in GroupHolder.allHeals:
      radish.kill()
   for enemy in GroupHolder.allEnemies:
      enemy.kill()
   for flam in GroupHolder.allFlames:
      flam.kill()
   for effect in GroupHolder.roarEffects:
      effect.kill()
      
def positionHorn():
   horn.rect.right = dragon.head.rect.right + 10
   horn.rect.centery = dragon.head.rect.top
   
def checkForSpriteDeath():
   for sprite in GroupHolder.allSprites:
         if sprite.health <=0 and player.dead == False:
            sprite.kill()
   checkToKillFlame()
   
def checkToKillFlame():
   for flame in GroupHolder.allFlames:
      if flame.rect.right <=0:
         flame.kill()
      if flame.rect.left >= ConstantHolder.WIDTH:
         flame.kill()  
          
def checkForBatDeath():
   for bat in GroupHolder.allBats:
      if bat.health <=0:
         SoundHolder.batChannel.play(SoundHolder.batDeath)
         spawnBatRadish(bat)
         
def spawnBatRadish(bat):
   radish = Heal(bat.rect.x, bat.rect.y)
   radish.speedy = 1
   GroupHolder.allSprites.add(radish)
   GroupHolder.drawTopMost.add(radish) 



cutscenes.doStartScreen(clock)
cutscenes.checkForQuit()

pygame.mixer.music.load("music/musicnene.wav")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(loops=-1)

player = Player(ConstantHolder.RED)
sword = Sword(player)
hat = Hat(player)
dragon = Dragon(player)
horn = DecorationImage(300,95,ImageHolder.hornImage)

GroupHolder.allSprites.add(sword, player, hat, horn)
GroupHolder.drawLast.add(player)
GroupHolder.drawMid.add(dragon.dragonParts, sword, hat)
GroupHolder.drawMid.remove(dragon.foot,dragon.wing)
GroupHolder.drawFirst.add(dragon.foot,dragon.wing)
GroupHolder.drawFirst.add(horn)

running = True
win = False


#----gameplay loop----
while running == True and cutscenes.windowClosed == False:
   
   if player.dead == True:
      stopSounds()
      SoundHolder.playerChannel.play(SoundHolder.playerDeath)
      cutscenes.gameover(clock)
      pygame.mixer.music.play(loops=-1)
      resetPlayer()
      killEverythingExceptPlayerThings()
      #dragon got killed so reinitlize it (it needed to be killed)
      dragon = Dragon(player)
      GroupHolder.drawMid.add(dragon.dragonParts)
      GroupHolder.drawMid.remove(dragon.foot,dragon.wing)
      GroupHolder.drawFirst.add(dragon.foot,dragon.wing)

   #keep the loop running at the right fps
   clock.tick(ConstantHolder.FPS)
   for event in pygame.event.get(): 
      if event.type == pygame.QUIT:
         running = False

   GroupHolder.allSprites.update()
   dragon.updateHealth()
   dragon.doAttack()
   positionHorn()

   player.checkIfHitFloor()
   player.checkForDamage()
   sword.checkIfHitting()
   
   if player.health <=0:
      player.dead = True
   if dragon.head.health <= 0:
      dragon.doing = True
      dragon.dead = True
      SoundHolder.dragonChannel.play(SoundHolder.dragonDeath)
      killEverythingExceptPlayerThings()
      horn.kill()
      win = True
      running = False

   checkForBatDeath()
   checkForSpriteDeath()
   Drawer.drawEverything(player, dragon)
#---End gameplay loop---

if win == True:
   startTime = pygame.time.get_ticks()
   pygame.mixer.music.pause()
   while cutscenes.windowClosed == False:
      clock.tick(ConstantHolder.FPS)
      SoundHolder.windChannel.stop()
      cutscenes.showFirstEndCutscene(player, sword, hat, startTime)
      if cutscenes.firstCutsceneOver:
         if cutscenes.musicPlayed == False:
            pygame.mixer.music.load("music/TheForest.wav")
            pygame.mixer.music.set_volume(.6)
            pygame.mixer.music.play(loops=-1)
            cutscenes.musicPlayed = True
            print("")
            print("Thanks for playing!")
            print("Special thanks:")
            print("Chloe- Radish consultant")
            print("Jeevan- Valuable play tester")
            print("Adrienne- Overall consultant")
         cutscenes.showSecondEndCutscene()

pygame.quit()


