import pygame

def init():
   global crunch, batDeath, playerDeath, dragonDeath, flap
   global fire, jump, quake, roar, stalBreak, slam
   global swordSwing, wind, hurt
   crunch = pygame.mixer.Sound("sounds/crunchyVeggie.wav")
   batDeath = pygame.mixer.Sound("sounds/batDeath.wav")
   playerDeath = pygame.mixer.Sound("sounds/death.wav")
   dragonDeath = pygame.mixer.Sound("sounds/death2.wav")
   flap = pygame.mixer.Sound("sounds/dragonflapVishwaJai.wav")
   fire = pygame.mixer.Sound("sounds/fire.wav")
   jump = pygame.mixer.Sound("sounds/jump.wav")
   quake = pygame.mixer.Sound("sounds/quake.wav")
   roar = pygame.mixer.Sound("sounds/roar.wav")
   stalBreak = pygame.mixer.Sound("sounds/stalactiteBreak.wav")
   slam = pygame.mixer.Sound("sounds/stomp.wav")
   swordSwing = pygame.mixer.Sound("sounds/swordSwing.wav")
   wind = pygame.mixer.Sound("sounds/windTrim.wav")
   hurt = pygame.mixer.Sound("sounds/hurt.wav")
      
   jump.set_volume(.7)
   global playerChannel, dragonChannel, windChannel, batChannel
   playerChannel = pygame.mixer.Channel(0)
   dragonChannel = pygame.mixer.Channel(1)
   windChannel = pygame.mixer.Channel(2)
   batChannel = pygame.mixer.Channel(3)
   