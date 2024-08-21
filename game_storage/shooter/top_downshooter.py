import pygame , math , random
from sys import exit

"""
new pickup

more enemys
w custom imgs
points
main menu
shop

"""

pygame.init()
pygame.display.set_caption("shooter")

def get_angle(player_pos,mouse_pos):
    dx = mouse_pos[0] - player_pos[0]
    dy = mouse_pos[1] - player_pos[1]
    return math.degrees(math.atan2(-dy,dx))

class Player:
    def __init__(self):
        self.player_pos = [center[0],center[1]]
        self.player_size = 50
        self.player_img = pygame.transform.scale(pygame.image.load("player.png"),(self.player_size,self.player_size))
        self.rect = pygame.Rect(0,0,self.player_size,self.player_size)
        self.rect.center = self.player_pos
        self.health = 100
        self.speed = 10
        self.atk_dmg = 1
SCREENHEIGHT = 600
SCREENWIDTH = 800
center = (SCREENWIDTH // 2,SCREENHEIGHT // 2)
player = Player()


bullets =[]
class Bullet:
    def __init__(self,pos,angle):
        self.pos = list(pos)
        self.angle = math.radians(angle)
        self.speed = 10
        self.size = 5
        self.rect = pygame.Rect(0,0,self.size * 2,self.size * 2)
        self.rect.center = self.pos
        bullets.append(self)
    
    def update(self):
        self.pos[0] += self.speed * math.cos(self.angle)
        self.pos[1] -= self.speed * math.sin(self.angle)
        self.rect.center = self.pos

class Enemytype:
    def __init__(self,health,speed,atk_dmg,size,colour,weight):
        self.health = health
        self.speed = speed
        self.atk_dmg = atk_dmg
        self.size = size
        self.colour = colour
        self.weight = weight
enemy_types = [Enemytype(10,1,1,100,"blue",0.3),
               Enemytype(1,30,0.25,54,"red",0.4),
               Enemytype(3,2,1,50,"none",0.5)]

def choose_enemy():
    return random.choices(enemy_types,weights=[enemy_type.weight for enemy_type in enemy_types],k=1)[0]

enemies = []
class Enemy:
    def __init__(self,type):
        self.type = type
        self.size = self.type.size
        self.pos = list(self.get_edge())
        self.angle = 0
        self.speed = self.type.speed
        self.health = self.type.health
        self.colour = self.type.colour
        self.atk_dmg = self.type.atk_dmg
        self.img = pygame.transform.scale(pygame.image.load("enemy.png"),(self.size,self.size))
        self.rect = pygame.Rect(0,0,self.size,self.size)
        self.rect.center = self.pos
        enemies.append(self)
    
    def update(self):
        self.angle = get_angle(self.pos,player.player_pos)
        self.pos[0] += self.speed * math.cos(math.radians(self.angle))
        self.pos[1] -= self.speed * math.sin(math.radians(self.angle))
        self.rect.center = self.pos
    
    def get_edge(self):
        edge = random.choice(["top","bottom","left","right"])
        if edge == "top":
            return random.randint(0 - self.size,SCREENWIDTH + self.size),0
        elif edge == "bottom":
            return random.randint(0 - self.size,SCREENWIDTH + self.size),SCREENHEIGHT
        elif edge == "left":
            return  0,random.randint(0 - self.size,SCREENHEIGHT + self.size)
        elif edge == "right":
            return SCREENWIDTH,random.randint(0 - self.size,SCREENHEIGHT + self.size)

class Healthbar:
    def __init__(self,player):
        self.x = 10
        self.y = 10
        self.w = 100
        self.h = 30
        self.player = player
    def draw(self,surface):
        ratio = self.player.health / 100
        pygame.draw.rect(surface,"red",(self.x,self.y,self.w,self.h))
        pygame.draw.rect(surface,"green",(self.x,self.y,self.w * ratio,self.h))
healthbar = Healthbar(player)     

pickups = []
class Pickup:
    def __init__(self,type,power):
        self.size = 40
        self.img = pygame.transform.scale(pygame.image.load("health_pickup.png"),(self.size,self.size))
        self.pos = (random.randint(0 + self.size,SCREENWIDTH - self.size),random.randint(0 + self.size,SCREENHEIGHT - self.size))
        self.rect = pygame.Rect(0,0,self.size,self.size)
        self.rect.center = self.pos
        self.type = type
        self.power = power
        pickups.append(self)
    
    def draw(self,surface):
        surface.blit(self.img,self.rect.topleft)

Pickup("health",30)
Pickup("dmg_up",1      )

spawnrate = 2
spawnrate = 60 * spawnrate
music = pygame.mixer.Sound("music.mp3")
shoot = pygame.mixer.Sound("shoot.wav")

screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

BLACK = (0,0,0)
WHITE = (255,255,255)
DARKRED = (190,0,0)
BGCOLOUR = (66,155,88)

running = True
music.play(-1)

enemy_spawn_timer = 0

debug = False

while running:
    
    mouse_pos = pygame.mouse.get_pos()
    angle = get_angle(player.player_pos,mouse_pos)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Bullet(player.player_pos,angle)
            shoot.play()
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if player.player_pos[1] > 0 + (player.player_size // 2):
            player.player_pos[1] -= player.speed
    if keys[pygame.K_s]:
        if player.player_pos[1] < SCREENHEIGHT - (player.player_size // 2):
            player.player_pos[1] += player.speed
    if keys[pygame.K_a]:
        if player.player_pos[0] > 0 + (player.player_size // 2):
            player.player_pos[0] -= player.speed
    if keys[pygame.K_d]:
        if player.player_pos[0] < SCREENWIDTH - (player.player_size // 2):
            player.player_pos[0] += player.speed
    if keys[pygame.K_F3]:
        debug = True
    if keys[pygame.K_F4]:
        debug = False
    if keys[pygame.K_m]:
        music.set_volume(0)
        shoot.set_volume(0)
    screen.fill(BGCOLOUR)

    for pickup in pickups[:]:
        pickup.draw(screen)
        if debug:
            pygame.draw.rect(screen,(0,255,0),pickup.rect,1)
        if pickup.rect.colliderect(player.rect):
            if pickup.type == "health":
                if player.health < 100:
                    player.health += pickup.power
                    if player.health > 100:
                        player.health = 100
                    pickups.remove(pickup)
                    Pickup("health",pickup.power)
            elif pickup.type == "dmg_up":
                player.atk_dmg += pickup.power
                pickups.remove(pickup)
                Pickup("dmg_up",pickup.power)
            else:
                print(f"pickup {pickup.type} not found")

    enemy_spawn_timer += 1
    if enemy_spawn_timer >= spawnrate:
        enemytype = choose_enemy()
        Enemy(enemytype)
        enemy_spawn_timer = 0
    player.rect.center = player.player_pos
    for bullet in bullets[:]:
        bullet.update()
        pygame.draw.circle(screen,WHITE,(bullet.pos[0],bullet.pos[1]),bullet.size)
        if not (0 <= bullet.pos[0] <= SCREENWIDTH and 0 <= bullet.pos[1] <= SCREENHEIGHT):
            bullets.remove(bullet)
        if debug:
            pygame.draw.rect(screen,(0,255,0),bullet.rect,1)
            

            
    for enemy in enemies[:]:
        enemy.update()
        for bullet in bullets[:]:
            if enemy.rect.colliderect(bullet.rect):
                enemy.health -= player.atk_dmg
                bullets.remove(bullet)
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    break
        if enemy.rect.colliderect(player.rect):
            player.health -= enemy.atk_dmg
            if player.health <= 0:
                running = False
                
        #pygame.draw.circle(screen,WHITE,enemy.pos,enemy.size / 2)
        rotated_enemy_img = pygame.transform.rotate(enemy.img,enemy.angle)
        rotated_enemy_rect = rotated_enemy_img.get_rect(center=enemy.pos)
        if enemy.colour != "none":
            rotated_enemy_img.fill(enemy.colour,special_flags=pygame.BLEND_ADD)
        screen.blit(rotated_enemy_img,rotated_enemy_rect)
        if debug:
            pygame.draw.rect(screen,(0,255,0),enemy.rect,1)
    
    rotated_player_img = pygame.transform.rotate(player.player_img,angle)
    rotated_player_rect = rotated_player_img.get_rect(center=player.player_pos)
    if angle > 90 or angle < -90:
        rotated_player_img = pygame.transform.rotate(player.player_img,-angle)
        rotated_player_img = pygame.transform.flip(rotated_player_img,False,True)
        rotated_player_rect = rotated_player_img.get_rect(center=player.player_pos)
    screen.blit(rotated_player_img,rotated_player_rect)
    if debug:
        pygame.draw.rect(screen,(0,255,0),player.rect,1)
    healthbar.draw(screen)
    pygame.display.flip()
    
    pygame.time.Clock().tick(60)

pygame.quit()
exit()