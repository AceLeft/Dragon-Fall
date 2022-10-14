import pygame
import SoundHolder
import ImageHolder
import ConstantHolder
import GroupHolder
class Bat(pygame.sprite.Sprite):
   def __init__(self,player):
      pygame.sprite.Sprite.__init__(self) 
      self.image = ImageHolder.batImages[1]
      self.rect = self.image.get_rect()
      self.rect.x = ConstantHolder.WIDTH+5
      self.health = 5
      self.hit = 5
      self.player = player
      self.lastFlap = pygame.time.get_ticks()
      self.flapTimer = 300
      self.flapCooldown = 100
      self.speedx = -6
      self.speedy = 0
      self.width = self.rect.right-self.rect.left
      self.height = self.rect.bottom-self.rect.top
      self.flip = False
      self.go = False
      self.knockedback = True
      #give it a justHit attribute for stuff
      self.justHit = False
      GroupHolder.allSprites.add(self)
      GroupHolder.drawFirst.add(self)
      GroupHolder.allEnemies.add(self)
      GroupHolder.allBats.add(self)
   def update(self):
      if self.rect.bottom >= ConstantHolder.FLOOR:
         self.speedy = 0
         self.rect.bottom = ConstantHolder.FLOOR
      if self.go == True:
         self.width = self.rect.right-self.rect.left
         self.height = self.rect.bottom-self.rect.top
         oldwidth = self.rect.right - self.rect.left
         newleft = self.rect.left + self.width -oldwidth
         oldheight = self.rect.bottom - self.rect.top
         newbottom = self.rect.bottom + self.height - oldheight
         self.image = pygame.transform.scale(self.image,(self.width,self.height))
         self.rect = self.image.get_rect()
         self.rect.bottom = newbottom
         self.rect.left = newleft
         self.rect.x += self.speedx
         self.rect.y += self.speedy
         now = pygame.time.get_ticks()
         
         
         if(now-self.lastFlap > self.flapCooldown):
            oldcenter = self.rect.center
            self.image = ImageHolder.batImages[1]
            if self.flip == True:
               self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect()
            self.rect.center = oldcenter
         
         self.speedy +=1
         if( now-self.lastFlap > self.flapTimer):
            self.flap(-5)
         if(self.player.rect.left-20 < self.rect.right):
            if self.speedx >-6:
               self.flip = False
         if(self.player.rect.right+20 > self.rect.right):
            if self.speedx <6:
               self.flip = True
         if self.flip == False and self.speedx >-6 and now%5 == 0:
            self.speedx-=1
         if self.flip == True and self.speedx <6 and now%5 == 0:
            self.speedx +=1
            
         if self.rect.centery >= self.player.rect.top +10:
            self.flap(-15)
      
   def flap(self, speed):
      self.speedy = speed
      oldcenter = self.rect.center
      self.image = ImageHolder.batImages[0]
      if self.flip == True:
            self.image = pygame.transform.flip(self.image, True, False)
      self.rect = self.image.get_rect()
      self.rect.center = oldcenter
      self.lastFlap = pygame.time.get_ticks() 

   def takeDamageGoLeft(self,damage):
      self.health -= damage
      if(self.knockedback == True):
         self.speedx -=20
         
   def takeDamageGoRight(self,damage):
      self.health -= damage
      if(self.knockedback == True):
         self.speedx +=20