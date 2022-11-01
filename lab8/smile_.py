import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))


circle(screen, (255, 255, 0), (200, 200), 100)
circle(screen, (0, 0, 0), (200, 200), 100, 2)

rect(screen, (255, 0, 0), (150, 250, 100, 10))
rect(screen, (0, 0, 0), (150, 250, 100, 10), 4)

circle(screen, (255, 0, 0), (240, 170), 10)
circle(screen, (255, 0, 0), (160, 170), 15)
circle(screen, (0, 0, 0), (240, 170), 10, 2)
circle(screen, (0, 0, 0), (160, 170), 15, 2)


circle(screen, (0, 0, 0), (240, 170), 5)
circle(screen, (0, 0, 0), (160, 170), 7)

x1 = 230; y1 = 165
x2 = 260; y2 = 145
color = (0, 0, 0)
line(screen, color, (x1, y1), (x2, y2), 5)


x1 = 140; y1 = 135
x2 = 172; y2 = 165
color = (0, 0, 0)
line(screen, color, (x1, y1), (x2, y2), 7)





pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()