import pygame, math
from sys import exit
import random
from main_menu import show_menu

"""

"""

pygame.init()

clock = pygame.time.Clock()

SCREENWIDTH = 800
SCREENHEIGHT = 800

screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

BLACK = (0,0,0)
WHITE = (255,255,255)
DARKRED = (190,0,0)
BGCOLOUR = (66,155,88)
PLAYERSIZE = 40
GRAV = 1
TILESIZE = 50
ENEMYSIZE = 40
idleframes = [pygame.image.load(f"idle/player_idle_{i+1}.png") for i in range(2)]
runningframes = [pygame.image.load(f"running/player_run_{i+1}.png") for i in range(2)]
fallingframes =[pygame.image.load(f"falling/player_falling_{i+1}.png") for i in range(2)]
colour1 = "black"
colour2 = "green"
colour3 = "red"
state1 = colour1
state2 = colour1
font = pygame.font.Font(None,65)

JUMPHEIGHT = -15

class Player(pygame.Rect):
    def __init__(self):
        super().__init__(SCREENWIDTH // 4, SCREENHEIGHT // 2,PLAYERSIZE,PLAYERSIZE)
        self.vy = 0
        self.vx = 0
        self.on_ground = False
        self.idle_frames = idleframes
        self.running_frames = runningframes
        self.image = self.idle_frames[0]
        self.falling_frames = fallingframes
        self.frameindex = 0
        self.animationspeed = 0.3
        self.animationtimer = 0
        
    
    def update(self,screen,platforms,dt,enemys):
        self.vy += GRAV
        self.x += self.vx
        for platform in platforms:
            if self.colliderect(platform):
                if self.vx > 0:
                    self.right = platform.left
                elif self.vx < 0:
                    self.left = platform.right
                self.vx = 0
        self.y += self.vy
        self.on_ground = False
        for platform in platforms:
            if self.colliderect(platform):
                if self.vy > 0:
                    self.bottom = platform.top
                    self.on_ground = True
                elif self.vy < 0:
                    self.top = platform.bottom
                self.vy = 0
        if self.bottom > SCREENHEIGHT:
            self.bottom = SCREENHEIGHT
            self.on_ground = True
            self.vy = 0
            
        if self.vx > 0 and self.vy <= 0 :
            self.animate(self.running_frames,dt,False)
        elif self.vx < 0 and self.vy <= 0:
            self.animate(self.running_frames,dt,True)
        elif self.vy > 0:
            self.animate(self.falling_frames,dt,False)
        else:
            self.animate(self.idle_frames,dt,False)
        
        self.image = pygame.transform.scale(self.image,(PLAYERSIZE,PLAYERSIZE))
        screen.blit(self.image,self)
        self.vx = 0
        
        for enemy in enemys:
            if self.colliderect(enemy):
                if (self.bottom - self.vy) < enemy.top:
                    enemys.remove(enemy)
                else:
                    return self.u_is_kil()
        return True
    
    def jump(self):
        if self.on_ground:
            self.vy = JUMPHEIGHT
            self.on_ground = False
            
    def animate(self,frames,dt,flipped):
        self.animationtimer += dt
        if self.animationtimer >= self.animationspeed:
            self.animationtimer = 0
            self.frameindex = (self.frameindex+1) % len(frames)
        self.image = frames[self.frameindex]
        if flipped:
            self.image = pygame.transform.flip(self.image,True,False)
    def u_is_kil(self):
        return False
            
enemys = []
class Enemy(pygame.Rect):
    def __init__(self):
        super().__init__(SCREENWIDTH // 2,SCREENHEIGHT // 2,ENEMYSIZE,ENEMYSIZE)
        self.vy = 0
        self.vx = 0
        self.on_ground = False
        enemys.append(self)
        self.states = ["r","l","j","s"]
        self.state = random.choice(self.states)
        self.timer = 0
    
    def update(self,screen,platforms):
        self.timer += random.randint(1,15)
        if self.timer >= 200:
            self.state = random.choice(self.states)
            self.timer = 0
        if self.state  == "l":
            self.vx = -5
        elif self.state  == "r":
            self.vx = 5
        elif self.state == "j":
            self.state = random.choice(self.states)
            self.timer = 0
            self.jump()
        else:
            ...
            self.vx = 0
        self.vy += GRAV
        self.x += self.vx
        for platform in platforms:
            if self.colliderect(platform):
                if self.vx > 0:
                    self.right = platform.left
                elif self.vx < 0:
                    self.left = platform.right
                self.vx = 0
        self.y += self.vy
        self.on_ground = False
        for platform in platforms:
            if self.colliderect(platform):
                if self.vy > 0:
                    self.bottom = platform.top
                    self.on_ground = True
                elif self.vy < 0:
                    self.top = platform.bottom
                self.vy = 0
        if self.bottom > SCREENHEIGHT:
            self.bottom = SCREENHEIGHT
            self.on_ground = True
            self.vy = 0
        pygame.draw.rect(screen,"green",self)
        self.vx = 0
    
    def jump(self):
        if self.on_ground:
            self.vy = JUMPHEIGHT
            self.on_ground = False
Enemy()
Enemy()
    

platforms = []
class Platform(pygame.Rect):
    def __init__(self,x,y):
        super().__init__(x,y,TILESIZE,TILESIZE)
        platforms.append(self)
        self.img = pygame.transform.scale(pygame.image.load("other_img\grass_tile.png"),(50,50))
        
        
    
    def update(self,screen):
        pygame.draw.rect(screen,BLACK,self)
        screen.blit(self.img,self.topleft)


player = Player()

level = [
    ["xxxxxxxxxxxxxxxx"],
    ["                "] ,
    ["             x  "] ,
    ["          xx    "] ,
    ["      xxx       "] ,
    ["  x       x     "] ,
    ["    xx  x     x "] ,
    ["            x   "] ,
    ["  x      xxx    "] ,
    ["    x           "] ,
    ["    xxx         "] ,
    ["           xx   "] ,
    ["      xx        "] ,
    [" xxx      xx    "] ,
    ["       xx       "] ,
    [" xxxxxx   xxxxx "]
]

for y , row in enumerate(level):
    for x , tile in enumerate(row[0]):
        if tile == "x":
            Platform(x * TILESIZE,y * TILESIZE)

running = True

show_menu(screen,font,state1,state2,colour1,colour2,colour3)

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump() 
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False 
                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if player.left != 0:
            player.vx = -10
            if player.left < 0:
                player.left = 0
    if keys[pygame.K_d]:
        if player.right != SCREENWIDTH:
            player.vx = 10
            if player.right > SCREENWIDTH:
                player.right = SCREENWIDTH
    
    screen.fill(BGCOLOUR)
    
    if player.x < SCREENWIDTH / 2 - PLAYERSIZE / 2:
        for platform in platforms:
            platform.x += 10
        player.x += 10
        for enemy in enemys:
            enemy.x += 10
    elif player.x > SCREENWIDTH / 2 + PLAYERSIZE / 2:
        for platform in platforms:
            platform.x -= 10
        player.x -= 10
        for enemy in enemys:
            enemy.x -= 10
    if running == True:
        running = player.update(screen,platforms,dt,enemys)
    for enemy in enemys:
        enemy.update(screen,platforms)
    for platform in platforms:
        platform.update(screen)
    
    pygame.display.flip()

    keys = pygame.key.get_pressed() 
    
pygame.quit
exit()