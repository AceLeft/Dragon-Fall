import pygame
import ImageHolder
class Hat(pygame.sprite.Sprite):
   def __init__(self, following):
      pygame.sprite.Sprite.__init__(self) 
      self.image = ImageHolder.helmetBlueImageRight
      self.rect = self.image.get_rect()
      self.rect.bottom = following.rect.top
      self.rect.left = following.rect.left
      #have to give it a health attribute
      self.health = 1
      self.following = following
   def update(self):
      if self.following.direction == "right":
         self.image = ImageHolder.helmetBlueImageRight
         self.rect = self.image.get_rect()
         self.rect.bottom = self.following.rect.top
         self.rect.left = self.following.rect.left -4
      else:
         self.image = ImageHolder.helmetBlueImageLeft
         self.rect = self.image.get_rect()
         self.rect.bottom = self.following.rect.top
         self.rect.right = self.following.rect.right + 4
