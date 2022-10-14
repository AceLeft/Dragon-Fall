import pygame
import ImageHolder
import ConstantHolder
import GroupHolder
class Heal(pygame.sprite.Sprite):
   def __init__(self,x,y):
      pygame.sprite.Sprite.__init__(self)
      self.image = ImageHolder.radishImage
      self.rect = self.image.get_rect()
      self.rect.y = y
      self.rect.x = x
      self.heal = 15
      self.speedx = 0
      self.speedy = 0
      #hafta give it a health attribute bc its in GroupHolder.allSprites
      self.health = 1
      GroupHolder.allHeals.add(self)
   def update(self):
      self.rect.x += self.speedx
      self.rect.y += self.speedy  
      if self.rect.bottom >= ConstantHolder.FLOOR:
         self.speedy = 0
         self.rect.bottom = ConstantHolder.FLOOR 
   