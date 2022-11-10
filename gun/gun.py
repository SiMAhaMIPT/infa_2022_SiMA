import numpy as np
from random import choice, randint
import math
import pygame
from pygame.draw import *

pygame.init()

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

#задаю начальные координаты снаряда
y_0 = 450
def move_x(step=2):
    global y_0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        y_0-=step
    if keys[pygame.K_s]:
        y_0+=step
x_0 = 40
def move_y(step=2):
    global x_0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x_0-=step
    if keys[pygame.K_d]:
        x_0+=step

#сняряды
class Ball:
    def __init__(self, screen: pygame.Surface):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x_0
        self.y = y_0
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.g = 1
        self.coc = randint(1, 100)

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        screen.fill(WHITE)
        self.x += self.vx
        self.y -= self.vy
        if 10 < self.x < 750 and 10 < self.y < 550:
            self.vy -= self.g
        if 10 > self.x or self.x > 750:
            self.vx = -self.vx*0.5
        if 10 > self.y or self.y > 550:
            self.vy = -self.vy*0.5-self.g
        
        if self.x < 10:
            self.x = 10
        if self.x > 750:
            self.x = 750
        if self.y < 10:
            self.y = 10
        if self.y > 550:
            self.y = 550

        if self.coc <= 10:
            self.r = 10 + randint(-1, 6)
            self.color = BLACK

        if np.abs(self.vx)+np.abs(self.vy) < 10**(-2):
            self.live = 0
        elif np.abs(self.vx)<10**(-3):
            self.live = 0
        elif np.abs(self.vy)<10**(-1) and self.y > 500 :
            self.live = 0

        


    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, (96, 96, 96), (self.x, self.y), self.r, 2)


    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (obj.x-self.x)**2+(obj.y-self.y)**2 <= (obj.r+self.r)**2:
            return True
        else:
            return False

#пушка
class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.x = 20
        self.y = 450
        self.speed = 2
        self.color = GREY
    
    def move_body(self,step=2):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.x+=step
        if keys[pygame.K_a]:
            self.x-=step
        if keys[pygame.K_w]:
            self.y-=step
        if keys[pygame.K_s]:
            self.y+=step

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)*0.4
        new_ball.vy = - self.f2_power * math.sin(self.an)*0.4
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0]-self.x == 0:
                self.an = math.atan((event.pos[1]-self.y) / 0.00000001)
            elif event.pos[0]-self.x < 0:
                self.an = math.pi+math.atan((event.pos[1]-self.y) / (event.pos[0]-self.x))
            else:
                self.an = math.atan((event.pos[1]-self.y) / (event.pos[0]-self.x))

        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        coords = [(self.x + 10 * 0.5 * math.sin(self.an), self.y - 10 * 0.5 * math.cos(self.an)),
                  (self.x + 10 * 0.5 * math.sin(self.an) + self.f2_power * math.cos(self.an), self.y - 10 * 0.5 * math.cos(self.an) + self.f2_power * math.sin(self.an)),
                  (self.x - 10 * 0.5 * math.sin(self.an) + self.f2_power * math.cos(self.an), self.y + 10 * 0.5 * math.cos(self.an) + self.f2_power * math.sin(self.an)),
                  (self.x - 10 * 0.5 * math.sin(self.an), self.y + 10 * 0.5 * math.cos(self.an))]

        pygame.draw.polygon(screen, self.color, coords)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

#первый вид целей (красные)
class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.x = 100
        self.y = 100
        self.r = 150
        self.vx = 2.5
        self.vy = 2.5
        self.color = BLACK
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = randint(2, 50)
        self.live = 1
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        circle(screen, self.color, (self.x, self.y), self.r)
        circle(screen, BLACK, (self.x, self.y), self.r, 2)
    
    def move(self):
        screen.fill(WHITE)
        self.x += self.vx
        self.y -= self.vy
        if 150 > self.x or self.x > 750:
            self.vx = -self.vx
        if 50 > self.y or self.y > 550:
            self.vy = -self.vy
        
        if self.x < 150:
            self.x = 150
        if self.x > 750:
            self.x = 750
        if self.y < 50:
            self.y = 50
        if self.y > 550:
            self.y = 550

#второй вид целей (белые)
class Cobe:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.x = 100
        self.y = 100
        self.r = 150
        self.vx = randint(20, 40)/10
        self.vy = randint(20, 40)/10
        self.color = BLACK
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = randint(10, 40)
        self.vx = randint(2, 4)
        self.vy = randint(2, 4)
        self.live = 1
        color = self.color = WHITE

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        circle(screen, self.color, (self.x, self.y), self.r)
        circle(screen, choice([BLACK, BLACK, BLACK, BLACK, BLACK, WHITE]), (self.x, self.y), self.r, 4)
    
    def move(self):
        screen.fill(WHITE)
        self.x += self.vx
        self.y -= self.vy
        if 350 > self.x or self.x > 750:
            self.vx, self.vy = -self.vx*(np.abs(self.vy/self.vx))*2.1, self.vy*(np.abs(self.vx/self.vy))*0.5
        if 50 > self.y or self.y > 550:
            self.vy, self.vx = -self.vy*(np.abs(self.vx/self.vy))*2.1, self.vx*(np.abs(self.vy/self.vx))*0.5
        
        if self.x < 350:
            self.x = 350
        if self.x > 750:
            self.x = 750
        if self.y < 50:
            self.y = 50
        if self.y > 550:
            self.y = 550


#Задаём начальные параметры
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
cobe = Cobe()
finished = False


def display_score():
    """Отображение счета, на экране"""
    text_1 = font.render(f'SCORE : {score}', True, BLACK)
    screen.blit(text_1, (20, 15))
    text_2 = font.render(f'время, потраченное на текущую цель: {tries}', True, GREEN)
    screen.blit(text_2, (20, 35))    
    text_3 = font.render(f'количество попыток на текущую цель: {triis}', True, RED)
    screen.blit(text_3, (20, 55))

def display_score_plus():
    """Отображение на экране при попадании"""
    text_1 = font.render(f'вы потратили на цель {uhu} попыток', True, BLACK)
    screen.blit(text_1, (50, 570))
    text_1 = font.render(f'вы потратили на цель {huh} секунды', True, BLACK)
    screen.blit(text_1, (50, 550))


#выбор шрифтов
font = pygame.font.SysFont('impact', 20)

#переменные для счёта и времени
score = 0
tries = 0
triis = 0
trys = 0
uhu = 0
huh = 0

while not finished:

    screen.fill(WHITE)
    gun.draw()
    gun.move_body()
    move_x()
    move_y()
    print(y_0, x_0)
    target.draw()
    cobe.draw()
    for b in balls:
        b.draw()
        if b.live == 0:
            balls.remove(b)
    trys += 1
    tries = int(trys/FPS)
    if trys < FPS*2 and score != 0:
        display_score_plus()
    display_score()

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
            triis += 1
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    
    target.move()
    cobe.move()

    for b in balls:
        b.move()
        if b.hittest(target):
            score += 1
            huh = int(trys/FPS)
            trys = 0
            uhu = triis
            triis = 0

        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()

    for b in balls:
        b.move()
        if b.hittest(cobe):
            score += 1
            huh = int(trys/FPS)
            trys = 0
            uhu = triis
            triis = 0

        if b.hittest(cobe) and cobe.live:
            cobe.live = 0
            cobe.hit()
            cobe.new_target()
    gun.power_up()

pygame.quit()