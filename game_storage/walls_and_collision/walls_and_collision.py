import pygame
from sys import exit

global level_count
level_count = 0
global starting_pos
starting_pos = []

level = [["wwwwwwwwww",
          "w   s    w",
          "w        w",
          "w        w",
          "w   f    w",
          "w        w",
          "w        w",
          "w   l    w",
          "wwwwwwwwww"
          ],["sf"],[]]

pygame.init()

window = pygame.display.set_mode((500,500))

player_speed = 10

white = (255,255,255)

class Player:
    def __init__(self):
        self.startingx = 50
        self.startingy = 50
        self.rect = pygame.Rect(self.startingx,self.startingy,20,20)
        self.img = pygame.transform.scale(pygame.image.load("pacman.png"),(20,20))
        self.angle = 0
        
player = Player()
walls = []

class Wall:
    def __init__(self,pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0],pos[1],50,50)

lavas = []
class Lava:
    def __init__(self,pos):
        lavas.append(self)
        self.rect = pygame.Rect(pos[0],pos[1],50,50)
class Finish:
    def __init__(self,pos):
        self.rect = pygame.Rect(pos[0],pos[1],50,50)
        
wx = 0
wy = 0
def load_level(wx,wy):
    for row in level[level_count]:
        for element in row:
            if element == "w":
                Wall((wx,wy))
            if element == "l":
                Lava((wx,wy))
            if element == "s":
                player.startingx = wx
                player.startingy = wy
            if element == "f":
                global the_finnish
                the_finnish = Finish((wx,wy))
            wx += 50
        wx = 0
        wy += 50
    return [player.startingx,player.startingy]
    
starting_pos = load_level(wx,wy)

running = True

while running:
    window.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    OldPlyrx , OldPlyry = player.rect.topleft
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.rect.y -= player_speed
        player.angle = -90
    if keys[pygame.K_s]:
        player.rect.y += player_speed
        player.angle = 90
    if keys[pygame.K_a]:
        player.rect.x -= player_speed
        player.angle = 0
    if keys[pygame.K_d]:
        player.rect.x += player_speed
        player.angle = 180
    
    for wall in walls:
        if player.rect.colliderect(wall):
            player.rect.topleft = OldPlyrx,OldPlyry
    for wall in walls:
        pygame.draw.rect(window,(0,0,0),wall.rect)
    
    for lava in lavas:
        if player.rect.colliderect(lava):
            player.rect.topleft = player.startingx,player.startingy
    for lava in lavas:
        pygame.draw.rect(window,(255,165,0),lava.rect)
    pygame.draw.rect(window,(255,0,0),player.rect)
    
    rotated_img = pygame.transform.rotate(player.img,player.angle)
    newrect = rotated_img.get_rect(center = player.rect.center)
    window.blit(rotated_img,newrect)
    
    pygame.draw.rect(window,(0,255,0),the_finnish.rect)
    if player.rect.colliderect(the_finnish):
        level_count += 1
        walls.clear()
        lavas.clear()
        starting_pos = load_level(wx,wy)
        player.rect.topleft = starting_pos
    pygame.display.flip()
    print(level_count)
    pygame.time.Clock().tick(60)
pygame.quit()
exit()