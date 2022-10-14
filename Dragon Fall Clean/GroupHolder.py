import pygame
def init():
   global allSprites, allEnemies, allAttacks
   global allHeals, allBats, allFlames
   allSprites = pygame.sprite.Group()
   allEnemies = pygame.sprite.Group()
   allAttacks = pygame.sprite.Group()
   allHeals = pygame.sprite.Group()
   allBats = pygame.sprite.Group()
   allFlames = pygame.sprite.Group()
   global drawTopMost, drawFirst, drawMid, drawLast
   drawLast = pygame.sprite.Group()
   drawMid = pygame.sprite.Group()
   drawFirst = pygame.sprite.Group()
   drawTopMost = pygame.sprite.Group()
   global roarEffects
   roarEffects = pygame.sprite.Group()