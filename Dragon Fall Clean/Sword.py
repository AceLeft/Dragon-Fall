import ImageHolder
import ConstantHolder
import SoundHolder
import GroupHolder
import pygame
class Sword(pygame.sprite.Sprite):
   def __init__(self,player):
      pygame.sprite.Sprite.__init__(self)
      self.width = 10
      self.height = 25
      self.player = player
      #there are 6 images but 7 positions, pos 7 is just image 1
      self.image = ImageHolder.swordAnim["right"][0]
      self.rect = self.image.get_rect()
      self.rect.x = player.rect.centerx
      self.rect.bottom = ConstantHolder.FLOOR
      self.health = player.health
      self.damage = 10
      self.doing = False
      self.lastUpdate = pygame.time.get_ticks()
      self.frameRate = 50
      self.frame = 0
      self.swordCoords = {}
      self.setSwordCoords()
      self.direction = player.direction
      self.stopMoving = False
      
   def update(self):
      self.setSwordCoords()
      if self.player.direction == "left" and self.doing == False:
         self.rect.right = self.player.rect.centerx - 5
         self.rect.bottom = self.player.rect.bottom
      elif self.player.direction == "right" and self.doing == False:
         self.rect.left = self.player.rect.centerx +5
         self.rect.bottom = self.player.rect.bottom
      keystate = pygame.key.get_pressed()
      if keystate[pygame.K_SPACE] and self.doing == False and self.player.stopMoving == False and self.stopMoving == False:
         self.doing = True
         self.direction = self.player.direction
         SoundHolder.playerChannel.play(SoundHolder.swordSwing)
      now = pygame.time.get_ticks()
      if now-self.lastUpdate > self.frameRate and self.doing == True:
         self.lastUpdate = now
         self.frame +=1
         if self.frame == len(ImageHolder.swordAnim["left"]):
            self.image = ImageHolder.swordAnim[self.player.direction][0]
            self.rect = self.image.get_rect()
            self.doing = False
            self.frame = 0
            if self.player.direction == "left":
               self.rect.right = self.player.rect.centerx - 5
            elif self.player.direction == "right":
               self.rect.left = self.player.rect.centerx +5
            self.rect.bottom = self.player.rect.bottom

            for enem in GroupHolder.allEnemies:
               enem.justHit = False
         else:
            if self.direction == "right":
               self.image = ImageHolder.swordAnim["right"][self.frame]
               self.rect = self.image.get_rect()
               self.rect.left = self.swordCoords["right"][self.frame]
            if self.direction == "left":
               self.image = ImageHolder.swordAnim["left"][self.frame]
               self.rect = self.image.get_rect()
               self.rect.right = self.swordCoords["left"][self.frame]
            self.rect.bottom = self.swordCoords["y"][self.frame]
            
   def setSwordCoords(self):
      self.swordCoords["right"] = [self.player.rect.centerx +10, 
                                   self.player.rect.centerx+15+.25*self.width,
                                   self.player.rect.centerx+15+.5*(self.width), 
                                   self.player.rect.centerx+15+(self.width),
                                   self.player.rect.centerx+15+.5*(self.width),
                                   self.player.rect.centerx+15+.25*(self.width),
                                   self.player.rect.centerx +10]
      self.swordCoords["left"] = [self.player.rect.centerx -10,
                                  self.player.rect.centerx-15-.5*(self.width),
                                  self.player.rect.centerx-15-.75*(self.width), 
                                  self.player.rect.centerx-15-(self.width),
                                  self.player.rect.centerx-15-.75*(self.width),
                                  self.player.rect.centerx-15-.5*(self.width),
                                  self.player.rect.centerx -10]
      self.swordCoords["y"] =  [self.player.rect.bottom, 
                                self.player.rect.bottom+2,
                                self.player.rect.bottom,
                                self.player.rect.bottom-self.height,
                                self.player.rect.bottom-self.height,
                                self.player.rect.bottom-self.height-2,
                                self.player.rect.top+10]

   
   def checkIfHitting(self):
      for enemy in GroupHolder.allEnemies:
         enemyList = [enemy]
         h = pygame.sprite.spritecollide(self,enemyList,False)
         if h and self.doing == True and enemy.justHit == False:
            enemy.justHit = True
            if(enemy.rect.centerx > self.player.rect.centerx):
               enemy.takeDamageGoLeft(self.damage)
            else:
               enemy.takeDamageGoRight(self.damage)