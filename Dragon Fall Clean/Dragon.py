import pygame
import SoundHolder
import ImageHolder
import ConstantHolder
import GroupHolder
from Enemy import Enemy
from Bat import Bat
from Decoration import Decoration
from Heal import Heal
import random
#bc the dragon is like a boss, make it its own class
class Dragon:
   def __init__(self, player):
      self.body = Enemy(500,300,250,350,125,ImageHolder.bodyImage,10,"image")
      self.wing = Enemy(500,350,300,300,25,ConstantHolder.BROWN,10,"block")
      self.head = Enemy(500,250,115,100,65,ImageHolder.headImage,10,"image")
      self.jaw = Enemy(500,250,180,100,10,ConstantHolder.DARKGREEN,10,"block")
      self.foot = Enemy(500,350,350,75,100,ConstantHolder.BROWN,10,"block")
      self.neckHighest = Enemy(500,300,190,50,20,ConstantHolder.DARKGREEN,10,"block") 
      self.neckUpperMid = Enemy(500,300,205,50,20,ConstantHolder.DARKGREEN,10,"block") 
      self.neckLowerMid = Enemy(500,300,220,50,20,ConstantHolder.DARKGREEN,10,"block") 
      self.neckLowest = Enemy(500,300,235,50,20,ConstantHolder.DARKGREEN,10,"block") 
      
      self.dragonParts = [self.body, self.wing, self.head, self.jaw, self.foot, self.neckHighest,
                          self.neckUpperMid, self.neckLowerMid, self.neckLowest]
      #set knockback to false on all dragon parts
      for part in self.dragonParts:
         part.knockedback = False
         GroupHolder.allSprites.add(part)
         GroupHolder.allEnemies.add(part)
      self.connectNecks()
      self.jaw.rect.bottom = self.neckHighest.rect.top
      self.head.rect.bottom = self.jaw.rect.top
      #because the group thing doesnt have consistent indexes make neck a list
      self.neck = [self.neckHighest,self.neckUpperMid,self.neckLowerMid,self.neckLowest]
      self.headradius = self.head.rect.centery - self.body.rect.top
      self.hit = self.head.hit
      self.doing = False
      self.soundPlayed = False
      self.hasHitCeiling = False
      self.lastAttack = pygame.time.get_ticks()
      self.currentAttack = ""
      self.groundx = self.body.rect.left
      self.attacksList = ["breatheFire", "slamGround","slamRoof","flapWings", "roar"]
      self.attackInterval = 5000
      self.dead = False
      self.player = player
   
   def updateHealth(self):
      for part in self.dragonParts:
         if part.health < self.head.health:
            self.head.health = part.health
            
   def takeDamage(self,recipient,damage):
      recipient.health = recipient.health- damage
      
   def connectNecks(self):
      self.neckLowest.rect.bottom = self.body.rect.top
      self.neckLowerMid.rect.bottom = self.neckLowest.rect.top
      self.neckUpperMid.rect.bottom = self.neckLowerMid.rect.top
      self.neckHighest.rect.bottom = self.neckUpperMid.rect.top   
   
   def doAttack(self):
      if self.dead != True:
         if self.doing == False:
            GroupHolder.allAttacks.empty()
            self.doing = True
            self.V = False
            self.lastAttack = pygame.time.get_ticks()
            self.currentAttack = random.choice(self.attacksList)
         elif self.currentAttack == "breatheFire":
            self.breatheFire()
         elif self.currentAttack == "slamGround":
            self.slamGround()
         elif self.currentAttack == "slamRoof":
            self.slamRoof()
         elif self.currentAttack == "flapWings":
            self.flapWings()
         elif self.currentAttack == "roar":
            self.roar()

      
   def breatheFire(self):
      mouthx = self.jaw.rect.left - 2
      mouthy = self.jaw.rect.top
      now = pygame.time.get_ticks()
      #fire attack will last 3000 or something
      #ok this is real important- anytime its doing an attack, self.doing
      #  has to be turned to true when the attack is called
      if now-self.lastAttack <250 and now%5 ==0:
         self.jaw.rect.top += 1
         self.neckHighest.height = self.neckUpperMid.rect.top-self.head.rect.bottom
         self.neckHighest.rect.top = self.head.rect.bottom
      elif now-self.lastAttack >=250 and now - self.lastAttack < 2900:
         if self.soundPlayed == False:
            SoundHolder.dragonChannel.play(SoundHolder.fire)
            self.soundPlayed = True 
         color = random.choice(ConstantHolder.fireColors)
         size = random.randrange(15,25)
         flame = Enemy(1,mouthx,mouthy,size,size,color,self.hit,"block")
         #because i don't want the fire to be very compact, add in a random decimal
         flame.speedy = random.randrange(-30,20)/10
         flame.speedx = random.randrange(-5,-2)
         GroupHolder.allSprites.add(flame)
         GroupHolder.allAttacks.add(flame)
         GroupHolder.allFlames.add(flame)
         GroupHolder.drawFirst.add(flame)
      elif now-self.lastAttack >= 2900 and now-self.lastAttack <3000:
         if self.jaw.rect.top > self.head.rect.bottom:
            self.jaw.rect.top -=1
            self.neckHighest.height -=2
            self.neckHighest.rect.top +=2
      if now-self.lastAttack > 3000:
         self.neckHighest.rect.top = self.jaw.rect.bottom
         self.neckHighest.height = self.neckUpperMid.rect.top-self.jaw.rect.bottom
         self.doing = False
         self.soundPlayed = False
         
   def slamGround(self):
      now = pygame.time.get_ticks()
      if now - self.lastAttack < 750:
         self.foot.rect.y -= 2
      elif now - self.lastAttack >= 750 and now - self.lastAttack < 1000:
         self.foot.rect.y += 6
      elif now - self.lastAttack >= 1000 and now - self.lastAttack < 3000 and now %4 == 0:
         if self.soundPlayed == False:
            SoundHolder.dragonChannel.play(SoundHolder.slam)
            SoundHolder.dragonChannel.play(SoundHolder.quake)
            self.soundPlayed = True
         
         self.foot.rect.bottom = ConstantHolder.FLOOR
         slab = Enemy(1,self.groundx,ConstantHolder.FLOOR,25,250,ConstantHolder.FLOORCOLOR,self.head.hit,"block")
         self.groundx -= 25
         slab.speedy = (self.groundx - self.foot.rect.centerx ) /25
         GroupHolder.allSprites.add(slab)
         GroupHolder.allAttacks.add(slab)
         GroupHolder.drawFirst.add(slab)
      for attack in GroupHolder.allAttacks:
         attack.speedy += 1
      if now-self.lastAttack > 3000:
         self.doing = False
         self.groundx = self.body.rect.left
         self.soundPlayed = False

         
   def roar(self):
      now = pygame.time.get_ticks()
      roarTime = SoundHolder.roar.get_length()*1000
      if now-self.lastAttack <250 and now%5 ==0:
         self.jaw.rect.top += 1
         self.neckHighest.height = self.neckUpperMid.rect.top-self.head.rect.bottom
         self.neckHighest.rect.top = self.head.rect.bottom
      elif now-self.lastAttack >=250 and now-self.lastAttack < 250+roarTime:
         if self.soundPlayed == False:
            SoundHolder.dragonChannel.play(SoundHolder.roar)
            x = self.jaw.rect.x
            y = self.jaw.rect.y
            effectT = Decoration(x,y,3,3,ConstantHolder.WHITE,"block")
            effectR = Decoration(x,y,3,3,ConstantHolder.WHITE,"block")
            effectL = Decoration(x,y,3,3,ConstantHolder.WHITE,"block")
            effectB = Decoration(x,y,3,3,ConstantHolder.WHITE,"block")
            GroupHolder.drawTopMost.add(effectT, effectR, effectL, effectB) 
            GroupHolder.roarEffects.add(effectT,effectR,effectL,effectB)
            effectT.speedy = -3
            effectB.speedy = 3
            effectR.speedx = 3
            effectL.speedx = -3
            self.soundPlayed = True
            bat = Bat(self.player)
            
         self.player.removecontrols = True
         self.player.stopMoving = True
         self.player.speedx = 0
         if self.player.rect.bottom <= ConstantHolder.FLOOR:
            self.player.rect.bottom += self.player.speedy
         for effect in GroupHolder.roarEffects:
            effect.update()
            if effect.speedy !=0:
               effect.width +=6
               effect.rect.centerx = self.jaw.rect.x
            if effect.speedx !=0:
               effect.height +=6
               effect.rect.centery = self.jaw.rect.y
      
      elif now-self.lastAttack >= 250+roarTime and now-self.lastAttack <350+roarTime:
         self.player.stopMoving = False
         
         for bat in GroupHolder.allBats:
            bat.go = True
         if self.jaw.rect.top > self.head.rect.bottom:
            self.jaw.rect.top -=1
            self.neckHighest.height -=2
            self.neckHighest.rect.top +=2
            
      if now-self.lastAttack > 1500+roarTime:
         for e in GroupHolder.roarEffects:
            e.kill()
         self.doing = False
         self.soundPlayed = False
         
      
   def flapWings(self):
      now = pygame.time.get_ticks()
      #dragon flaps wings, player gets pushed to side of screen, and objects fly at player. jump to avoid
      if now- self.lastAttack < 500:
         if self.wing.height < 100:
            self.wing.rect.y-=2
            self.wing.height +=2
         self.yDirection = 1
         self.heightDirection = -1
         
      elif now-self.lastAttack >= 500 and now-self.lastAttack <6000:
         #-1 is up 1 is down
         if self.soundPlayed == False:
            SoundHolder.windChannel.play(SoundHolder.wind)
            self.soundPlayed = True
         if self.wing.height >= 100:
            self.heightDirection =-1
            self.yDirection *=-1
            SoundHolder.dragonChannel.play(SoundHolder.flap)
         if self.wing.height <=25:
            self.heightDirection = 1
            self.yDirection -=1
         self.wing.rect.y += 4*self.yDirection
         self.wing.height += 4*self.heightDirection
         if self.player.speedx > -28:
            self.player.speedx -=2
            
         if now% 50 == 0:
            d = random.randint(0,100)
            if  d <=35 :
               #chest
               flyer = Enemy(1,500,random.randint(self.neckLowerMid.rect.centery,ConstantHolder.FLOOR-40),50,50,ImageHolder.chestImage,5,"image")
               GroupHolder.allAttacks.add(flyer)
            elif  d >35 and d <=50:  
               #sword             
               flyer = Enemy(1,500,random.randint(self.neckLowerMid.rect.centery,ConstantHolder.FLOOR-40),40,10,ConstantHolder.STEEL,5,"block")
               GroupHolder.allAttacks.add(flyer)
            elif  d >50 and d <=75: 
               #helmet              
               flyer = Enemy(1,500,random.randint(self.neckLowerMid.rect.centery,ConstantHolder.FLOOR-40),30,30,ImageHolder.helmetRedImage,5,"image")
               GroupHolder.allAttacks.add(flyer)
            elif  d >75 and d <=80: 
               #radish              
               flyer = Heal(500,random.randint(self.neckLowest.rect.centery,ConstantHolder.FLOOR-40))
            elif  d >80 and d <=90:  
               #candelabra             
               flyer = Enemy(1,500,random.randint(self.neckLowerMid.rect.centery,ConstantHolder.FLOOR-40),45,45,ImageHolder.candelabraImage,5,"image")
               GroupHolder.allAttacks.add(flyer)
            elif  d >90: 
               #diamond              
               flyer = Enemy(1,500,random.randint(self.neckLowerMid.rect.centery,ConstantHolder.FLOOR-40),25,25,ImageHolder.diamondImage,5,"image")
               GroupHolder.allAttacks.add(flyer)
            flyer.speedx = -8
            GroupHolder.allSprites.add(flyer)
            GroupHolder.drawTopMost.add(flyer)
         
      elif now-self.lastAttack > 6000 and now-self.lastAttack <=7000:
         if self.wing.height > 25:
            self.wing.height -= 1
         if self.wing.rect.y > 300:
            self.wing.rect.y -= 1
            
      if now-self.lastAttack >7000:
         self.doing = False
         self.soundPlayed = False
         SoundHolder.wind.stop()
         
         
         
   def slamRoof(self):
      now = pygame.time.get_ticks()
      #head is going to go down for a bit, then hit the ceiling
      reelBackInterval = now- self.lastAttack < 1500
      pauseInterval = now - self.lastAttack >= 1500 and now - self.lastAttack < 2000
      launchInterval = now - self.lastAttack >=2000 and now - self.lastAttack < 3500
      returnToPositionInterval = now - self.lastAttack >=3500 and now - self.lastAttack < 5500
      headBelowCeiling = self.head.rect.top > 0
      headAtCeiling = self.head.rect.top <= 0
      if reelBackInterval:
         if now% 2 == 0:
            self.head.rect.x += 1
            self.jaw.rect.x +=1
            self.jaw.rect.y += 1
            self.head.rect.y += 1
            self.neckHighest.rect.y += 1
            self.neckHighest.rect.x += 1
         if now% 3 == 0:
            self.neckUpperMid.rect.x +=1
            self.neckUpperMid.rect.y +=1
         if now% 5 == 0:
            self.neckLowerMid.rect.x +=1
            self.neckLowerMid.rect.y +=1
      elif pauseInterval:
         self.head.rect.x +=0
      elif launchInterval:
         #shoot up to hit the ceiling, and when hit spawn a stalactite and change direction
         if headBelowCeiling and self.hasHitCeiling == False:
            self.head.speedy = -6
            self.jaw.speedy = -6
            i = 4
            for neckpiece in self.neck:
                  d = (self.body.rect.top- self.jaw.rect.bottom)
                  neckpiece.height = round(d/4)
                  neckpiece.rect.y = self.body.rect.top- i *round(d/4)
                  i -=1
            if now% 2 == 0:
               self.head.rect.x -= 4
               self.jaw.rect.x -=4
               self.neckHighest.rect.x -= 4
               
            if now% 3 == 0:
               self.neckUpperMid.rect.x -=6
               
            if now% 5 == 0:
               self.neckLowerMid.rect.x -=6
         elif headAtCeiling and self.hasHitCeiling == False:
            self.takeDamage(self.head,10)
            self.spawnStalactite(7)
            self.spawnStalactite(5)
            SoundHolder.dragonChannel.play(SoundHolder.slam)
            self.hasHitCeiling = True
            self.head.speedy = 9
            self.jaw.speedy = 9
            self.head.speedx = -8
            self.jaw.speedx = -8
            self.neckHighest.rect.right = self.jaw.rect.right
            self.neckUpperMid.rect.right = self.jaw.rect.right
            self.neckLowerMid.rect.right = self.jaw.rect.right
            i = 0
            for neckpiece in self.neck:
               neckpiece.speedx = -8 + i
               i +=2
               
         elif self.hasHitCeiling:
            if self.neckLowest.height == 1:
               self.head.speedy = 0
               self.jaw.speedy = 0
            if self.head.speedx != 0 and now% 5 == 0:
               self.head.speedx +=1
               self.jaw.speedx +=1
            for neckpiece in self.neck:
               if neckpiece.speedx != 0 and now% 5 == 0:
                     neckpiece.speedx +=1
               
            if self.head.speedy != 0 and now% 3 == 0:
               self.head.speedy -=1
               self.jaw.speedy -=1
               
            i = 4
            for neckpiece in self.neck:
                  d = (self.body.rect.top- self.jaw.rect.bottom)
                  neckpiece.height = round(d/4)
                  neckpiece.rect.y = self.body.rect.top- i *round(d/4)
                  i -=1
                  
            d2 =  self.body.rect.left - self.head.rect.right
            #original width is 50
            if d2 >= 50 and self.head.speedx !=0:
               self.head.speedx = -1
               self.jaw.speedx = -1
               for neckpiece in self.neck:
                  neckpiece.speedx =0
            
         self.connectNecks()
      elif returnToPositionInterval:
         #slowly return to original position, which was head at 250,115 and neckU at 300,190
         #original neck height was 20
         if self.head.rect.x != 250:
            self.head.rect.x +=1
            self.jaw.rect.x +=1
         if self.neckHighest.height < 20 and now%2 ==0:
            
            self.head.rect.y -=1
            self.jaw.rect.y -=1
         i = 4
         for neckpiece in self.neck:
            d = (self.body.rect.top- self.jaw.rect.bottom)
            neckpiece.height = round(d/4)
            neckpiece.rect.y = self.body.rect.top- i *round(d/4)
            i -=1
            if neckpiece.rect.x != 300:
               neckpiece.rect.x +=1
      #check if any stalactite hit the ground and stop them
      for attack in GroupHolder.allAttacks:
         if attack.rect.bottom >=ConstantHolder.FLOOR:
            attack.rect.bottom = ConstantHolder.FLOOR
            attack.speedy = 0
            attack.kill()
            SoundHolder.windChannel.play(SoundHolder.stalBreak)
      if now-self.lastAttack > 5500:
         self.doing = False
         self.hasHitCeiling = False
         for attack in GroupHolder.allAttacks:
            attack.kill()
            
   def spawnStalactite(self, speed):
      stalactite = Enemy(1, random.randrange(10,100),-100,68,74,ImageHolder.stalactiteImage,20,"image")
      stalactite.speedy = speed
      GroupHolder.allSprites.add(stalactite)
      GroupHolder.allAttacks.add(stalactite)
      GroupHolder.allEnemies.add(stalactite)
      GroupHolder.drawFirst.add(stalactite)