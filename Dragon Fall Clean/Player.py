import pygame
import ConstantHolder
import SoundHolder
import GroupHolder

class Player(pygame.sprite.Sprite):
   
   def __init__(self,color):
      pygame.sprite.Sprite.__init__(self) 
      #width, height
      self.image = pygame.Surface((50,50))
      self.image.fill(color)
      self.rect = self.image.get_rect()
      self.rect.centerx = ConstantHolder.WIDTH /4
      self.rect.bottom = ConstantHolder.FLOOR
      self.speedx = 0
      self.speedy = 0
      self.health = 75
      self.iframes = 750
      self.icounter = pygame.time.get_ticks()
      self.jumpcounter = 0
      self.removecontrols = False
      self.direction = "right"
      self.stopMoving = False
      self.dead = False
      self.v = False

   def update(self):
      if self.health > 75:
         self.health = 75
      self.experienceGravity()
      self.checkForHeal()
      if self.stopMoving == False:
         if self.speedx > 0:
            self.speedx -= 1
         if self.speedx <0:
            self.speedx +=1
         if self.speedx == 0 or self.rect.left == 0:
            self.removecontrols = False
         keystate = pygame.key.get_pressed()
         if keystate[pygame.K_LEFT] and self.removecontrols == False:
            self.direction = "left"
            if self.speedx > -6:
               self.speedx -= 2
            else:
               self.speedx = -6
               
         if keystate[pygame.K_RIGHT] and self.removecontrols == False:
            self.direction = "right"
            if self.speedx < 6:
               self.speedx += 2
            else:
               self.speedx = 6
         if keystate[pygame.K_UP] and self.jumpcounter <2 and self.removecontrols == False:
             SoundHolder.playerChannel.play(SoundHolder.jump)
             self.speedy -= 10
             self.jumpcounter +=1
         
         self.rect.x += self.speedx
         if self.rect.right > ConstantHolder.WIDTH:
             self.rect.right = ConstantHolder.WIDTH
         if self.rect.left < 0:
             self.rect.left = 0
         self.rect.y += self.speedy
         
   def checkForDamage(self):
      self.checkForDamageFromGroup(GroupHolder.allEnemies, True)
      self.checkForDamageFromGroup(GroupHolder.allAttacks, False)

   def checkForDamageFromGroup(self, group, removecontrols):
       for member in group:
         memberList = [member]
         collision = pygame.sprite.spritecollide(self,memberList,False)
         if collision and pygame.time.get_ticks()-self.icounter > self.iframes:
            self.icounter = pygame.time.get_ticks()
            self.removecontrols = removecontrols
            if(member.rect.centerx > self.rect.centerx):
               self.takeDamageGoLeft(member.hit)
            else:
               self.takeDamageGoRight(member.hit)
            SoundHolder.playerChannel.play(SoundHolder.hurt)
          
   def takeDamageGoLeft(self,damage):
      self.health -= damage
      self.speedx -=20
      
   def takeDamageGoRight(self,damage):
      self.health -= damage
      self.speedx +=20
      
   def checkForHeal(self):
      for radish in GroupHolder.allHeals:
         radishList = [radish]
         collision = pygame.sprite.spritecollide(self,radishList,False)
         if collision:
            self.health += radish.heal
            SoundHolder.playerChannel.play(SoundHolder.crunch)
            radish.kill() 
              
   def checkIfHitFloor(self):
      if self.rect.bottom >= ConstantHolder.FLOOR:
         self.speedy = 0
         self.rect.bottom = ConstantHolder.FLOOR
         self.jumpcounter = 0
         
   def experienceGravity(self):
      if self.rect.bottom < ConstantHolder.FLOOR:
         self.speedy +=1
