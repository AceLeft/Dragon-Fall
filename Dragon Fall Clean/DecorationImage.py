import pygame
import ConstantHolder

class DecorationImage(pygame.sprite.Sprite):
   def __init__(self,x,y,image):
      pygame.sprite.Sprite.__init__(self)
      self.width = image.get_width()
      self.height = image.get_height()
      self.image = image
      self.rect = image.get_rect()
      self.rect.x = x
      self.rect.y = y
      self.speedx = 0
      self.speedy = 0
      self.health = 1
      
   def update(self):
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