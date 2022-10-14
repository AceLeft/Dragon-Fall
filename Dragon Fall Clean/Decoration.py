import pygame
import ConstantHolder

class Decoration(pygame.sprite.Sprite):
   def __init__(self,x,y,width,height,color,type):
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
      self.rect.x = x
      self.rect.y = y
      self.speedx = 0
      self.speedy = 0
      #give it a health attribute bc its in GroupHolder.allSprites
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