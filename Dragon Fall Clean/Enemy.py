import pygame
import ConstantHolder

class Enemy(pygame.sprite.Sprite):
   def __init__(self,health,x,y,width,height,color,hit,type):
      pygame.sprite.Sprite.__init__(self) 
      self.width = width
      self.height = height
      #type is either block or image
      self.type = type
      if self.type == "image":
         self.image = color
      else:
         self.image = pygame.Surface((width,height))
         self.image.set_colorkey(ConstantHolder.BLACK)
         self.image.fill(color)
      self.rect = self.image.get_rect()
      self.rect.centerx = x + width/2
      self.rect.bottom = y + height
      self.health = health
      self.speedx = 0
      self.speedy = 0
      self.hit = hit #the damage done to something
      self.knockedback = True
      self.lastUpdate = pygame.time.get_ticks()
      self.justHit = False
     
   def update(self):
      oldwidth = self.rect.right - self.rect.left
      newleft = self.rect.left + self.width -oldwidth
      oldheight = self.rect.bottom - self.rect.top
      newbottom = self.rect.bottom + self.height - oldheight
      #prevent scaling to a negative size
      if self.width <= 0:
         self.width = 1
      if self.height <= 0:
         self.height = 1
      self.image = pygame.transform.scale(self.image,(self.width,self.height))
      self.rect = self.image.get_rect()
      self.rect.bottom = newbottom
      self.rect.left = newleft
      self.rect.x += self.speedx
      self.rect.y += self.speedy
      self.checkIfOffscreen()
      
   def checkIfOffscreen(self):
      if self.rect.right < -20:
         self.kill()
      if self.rect.left > ConstantHolder.WIDTH+20:
         self.kill()
      if self.rect.top > ConstantHolder.HEIGHT+10:
         self.kill()
      
   def takeDamageGoLeft(self,damage):
      self.health -= damage
      if(self.knockedback == True):
         self.speedx -=20
         
   def takeDamageGoRight(self,damage):
      self.health -= damage
      if(self.knockedback == True):
         self.speedx +=20