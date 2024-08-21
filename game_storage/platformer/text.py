import pygame
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((600,600))
font = pygame.font.Font(None,74)
text_surface = font.render("hello this is text",True,"white")
running = True
while running:
    clock.tick(60)
    screen.blit(text_surface,(0,300))
    pygame.display.flip()