import pygame
import Drawer
import ConstantHolder
import ImageHolder
import GroupHolder
from Decoration import Decoration
from DecorationImage import DecorationImage
class Cutscenes:
   def __init__(self):
      self.startBG = DecorationImage(0,0,ImageHolder.startScreenUnder)
      self.endBG = DecorationImage(0,0,ImageHolder.endScreen)
      self.startBGUpper = DecorationImage(353,254,ImageHolder.startScreenAbove)
      self.lilplayer = Decoration(144,361,17,17,ConstantHolder.RED,"block")
      self.lilblue = Decoration(ConstantHolder.WIDTH-20,361,17,17,ConstantHolder.BLUE,"block")
      self.draw1st = pygame.sprite.Group()
      self.draw2nd = pygame.sprite.Group()
      self.draw3rd = pygame.sprite.Group()
      self.blue = Decoration(ConstantHolder.WIDTH+1,ConstantHolder.FLOOR-50,50,50,ConstantHolder.BLUE,"block")
      self.red = Decoration(ConstantHolder.WIDTH+1,ConstantHolder.FLOOR-50,50,50,ConstantHolder.RED,"block") 
      self.red.direction = "right"
      self.firstCutsceneOver = False
      self.musicPlayed = False
      self.windowClosed = False
      self.controlsText = "(Use the arrowkeys to move and hold spacebar to attack)"
      self.textColor = ConstantHolder.WHITE
      
   def doStartScreen(self, clock):
      pygame.mixer.music.load("music/TheForest.wav")
      pygame.mixer.music.set_volume(.6)
      pygame.mixer.music.play(loops=-1)
      #now that everything is initilized but nothing has been created, do the start surface
      self.draw1st.add(self.startBG)
      self.draw2nd.add(self.lilplayer)
      self.draw2nd.add(self.lilblue)
      self.draw3rd.add(self.startBGUpper)

      start = True
      while start and self.windowClosed == False:
         clock.tick(ConstantHolder.FPS)
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               start = False
               self.windowClosed = True
            if event.type == pygame.KEYUP:
               self.lilplayer.speedx = 3
               pygame.mixer.music.fadeout(900)
         if self.lilplayer.rect.x >= ConstantHolder.WIDTH-50:
            start = False
            
         self.lilplayer.update()
         self.drawCutsceneDrawLayers()
         Drawer.drawText( "Dragon Fall",52,ConstantHolder.WIDTH/2,10, self.textColor)
         Drawer.drawText("Press any key to begin.",16,ConstantHolder.WIDTH/2,75, self.textColor)
         Drawer.drawText( self.controlsText, 16, ConstantHolder.WIDTH/2, 100, self.textColor)
         pygame.display.flip()
      
      #next time draw1st is used, it should be the end cutscene
      self.startBG.kill()
      self.draw1st.add(self.endBG)
   
   def drawCutsceneDrawLayers(self):
      Drawer.fillScreenBlack()
      self.draw1st.draw(Drawer.screen)
      self.draw2nd.draw(Drawer.screen)
      self.draw3rd.draw(Drawer.screen)
      
   def gameover(self, clock):
      Drawer.fillScreenBlack()
      xPosition = ConstantHolder.WIDTH/2
      Drawer.drawText("You Died!",82,xPosition,ConstantHolder.HEIGHT/4, self.textColor)
      Drawer.drawText("Tip: white radishes restore health!", 24, xPosition, ConstantHolder.HEIGHT/2, self.textColor)
      Drawer.drawText("Press enter to try again",19,xPosition,ConstantHolder.HEIGHT*3/4-35, self.textColor)
      Drawer.drawText(self.controlsText, 16, xPosition, ConstantHolder.HEIGHT*3/4 +10, self.textColor)
      pygame.display.flip()
      waiting = True
      while waiting and self.windowClosed == False:
         clock.tick(ConstantHolder.FPS)
         self.checkForQuit()
         keystate = pygame.key.get_pressed()
         if keystate[pygame.K_RETURN]:
            waiting = False
            
   def showFirstEndCutscene(self, player, sword, hat, startTime):
      now = pygame.time.get_ticks()
      if now-startTime <1000:
         player.speedx = 0
         player.direction = "right"
         player.removecontrols = True
         player.update()
         player.checkIfHitFloor()
         sword.stopMoving = True
         sword.rect.left = player.rect.centerx +5
         sword.rect.bottom = player.rect.bottom
         sword.image = ImageHolder.swordAnim["right"][0]
         sword.update()
         hat.update()
      elif now - startTime >= 1000 and now-startTime<2000:
         if player.v == False:
            #kill the player and replace them with a decoration
            self.red.rect.center = player.rect.center
            hat.following = self.red
            GroupHolder.drawLast.add(self.red)
            self.blue.speedx = -1
            GroupHolder.drawFirst.add(self.blue)
            player.v == True
            player.kill()
         self.blue.update()
         self.red.update()
      elif now - startTime >=2000 and now-startTime <2600:
         self.blue.speedx = 0
      elif now-startTime >= 2600  and self.red.rect.right > -10:
         self.blue.speedx = -1
         if self.blue.rect.right < self.red.rect.left-10:
            self.red.speedx = -1
            self.red.direction = "left"
         self.blue.update()
         self.red.update()
         hat.update()
      if self.red.rect.right <= 0:
         self.firstCutsceneOver = True
      if self.firstCutsceneOver == False:
         self.checkForQuit()
         Drawer.fillScreenBlack()
         Drawer.screen.blit(ImageHolder.background,ImageHolder.background.get_rect())
         Drawer.drawFloor()
         Drawer.drawGroups()
         pygame.display.flip()
      
   def showSecondEndCutscene(self):
      now = pygame.time.get_ticks()
      self.checkForQuit()
       
      if self.lilplayer.rect.x > 144:
         self.lilplayer.speedx = -1
         self.lilblue.speedx = -1
      else:
         self.lilplayer.speedx = 0
         self.lilblue.speedx = 0
      self.lilplayer.update()
      self.lilblue.update()
      self.drawCutsceneDrawLayers()
      Drawer.drawText("You Win!",52,ConstantHolder.WIDTH/2,10, ConstantHolder.WHITE)
      pygame.display.flip()   
           
   def checkForQuit(self):
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            self.windowClosed = True