import pygame
from pygame.draw import *
from random import randint
import math


#FPS, расположение экрана и его размеры
FPS = 30
screen = pygame.display.set_mode((850, 650))
HEIGHT = 600
WIDTH = 900

#Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
ISS = (230, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, WHITE]
RUS = [ISS, WHITE]

#размеры и скорости
R_max = 100
R_min = 15
BACK = -20
FORWARD = 20

#максимальное количество элементов
AMOUNT = 5

def new_ball():
    """Рисуем новый шарик"""
    balls.append([])
    balls[-1].append([randint(R_max, WIDTH - R_max), randint(R_max, HEIGHT - R_max)])
    balls[-1].append(randint(R_min, R_max))
    balls[-1].append([randint(BACK, FORWARD), randint(BACK, FORWARD)])
    balls[-1].append(COLORS[randint(0, 5)])
    circle(screen, balls[-1][3], balls[-1][0], balls[-1][1])
    if treasure():
        balls[-1].append(True)
    else:
        balls[-1].append(False)

def move_ball():
    """Двигаем шары; задаём мигание и переменность специальной цели"""
    screen.fill(WHITE)
    for ball in balls:
        if ball[1] >= ball[0][0] or ball[0][0] >= (WIDTH - ball[1]):
            ball[2][0] = - ball[2][0]
        if ball[1] >= ball[0][1] or ball[0][1] >= (HEIGHT - ball[1]):
            ball[2][1] = - ball[2][1]
        ball[0][0] += ball[2][0]
        ball[0][1] += ball[2][1]
        if ball[4]:
            ball[3] = RUS[randint(0, 1)]
            if ball[1] == 0:
                ball[1] = 25
            else:
                ball[1] -= 1
        circle(screen, ball[3], (ball[0][0], ball[0][1]), ball[1])

def hit(mouse, coord, r):
    """Проверяем, попали ли мы
    mouse.pos выдаёт нам координаты точки в которую мы попали
    coord - координата соответствующего ball (ball[0])
    r - радиус соответствующего ball (ball[1])"""
    return (coord[0] - mouse.pos[0]) ** 2 + (coord[1] - mouse.pos[1]) ** 2 <= r**2

def display_score():
    """Отображение счета на экране"""
    text = font.render(f'{score}', True, BLACK)
    pixel_plus = int(math.log10(score+0.9))
    screen.blit(text, (865 - pixel_plus*15, 560))



def treasure():
    """Вероятность специальной цели"""
    return randint(1, 100) <= 5

pygame.init()

#выбор шрифта
font = pygame.font.SysFont('impact', 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.update()

#задаём начальные параметры
score = 0
balls = []

#добавляем музыкальное сопровождение (работает до первого нажатия)
pygame.mixer.music.load("bird_0.mp3")
pygame.mixer.music.play(-1)

#создаём в начале нужное количество шаров
for i in range(AMOUNT):
    new_ball()
finished = False

pygame.display.update()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
                if hit(event, ball[0], ball[1]):
                    if ball[4]:
                        score += 10
                        #звук для специальной цели
                        pygame.mixer.music.load("bird_2.mp3")
                        pygame.mixer.music.play()
                    else:
                        score += 1
                        #звук обычной цели
                        pygame.mixer.music.load("bird_1.mp3")
                        pygame.mixer.music.play()
                    balls.remove(ball)
                    new_ball()

    move_ball()
    display_score()
    pygame.display.update()

pygame.quit()