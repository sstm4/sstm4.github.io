import pygame 
from sys import exit

pygame.init()

SCREENWIDTH = 800
SCREENHEIGHT = 800
screen = pygame.display.set_mode((SCREENHEIGHT,SCREENWIDTH))
clock = pygame.time.Clock()

def show_menu(screen,font,state1,state2,colour1,colour2,colour3):
    menu = True
    state1 = state2 = colour1
    while menu:
        clock.tick(60)
        screen.fill("white")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                menu = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    state1 = colour2
                    state2 = colour3
                if event.key == pygame.K_DOWN:
                    state1 = colour3
                    state2 = colour2
                if event.key == pygame.K_RETURN:
                    if state1 == colour2:
                        menu = False
                    elif state1 == colour3:
                        menu = False
                        pygame.quit()
                        exit()
                    else:
                        continue
        start_text_surface = font.render("start",True,state1)
        quit_text_surface = font.render("quit",True,state2)
        screen.blit(quit_text_surface,(350,500))
        screen.blit(start_text_surface,(350,400))
        
        pygame.display.flip()