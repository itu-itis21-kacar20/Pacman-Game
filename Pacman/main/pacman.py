import copy
from board import boards
import pygame
import math

pygame.init()

WIDTH  = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer  = pygame.time.Clock()
fps    = 60
font   = pygame.font.Font('freesansbold.ttf', 20)
level  = copy.deepcopy(boards)
color0 = 'green'
pi = math.pi
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))
blue_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
red_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
pink_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
orange_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))
player_x = 450
player_y = 663
direction = 0

#Ghosts
red_x = 56
red_y = 58
red_direction = 0
blue_x = 440
blue_y = 388
blue_direction = 2
pink_x = 440
pink_y = 438
pink_direction = 2
orange_x = 440
orange_y = 438
orange_direction = 2

counter = 0
flicker = False
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 3
score = 0
powerup = False
powerup_counter = 0
eaten_ghosts = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
red_dead = False
blue_dead = False
pink_dead = False
orange_dead = False
red_box = False
blue_box = False
pink_box = False
orange_box = False
start_counter = 0
moving = False
ghost_speeds = [3, 3, 3, 3]
lives = 3
game_over = False
game_won = False

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()
    
    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghosts[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghosts[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        # R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False

        return self.turns, self.in_box

    def move_orange(self):
        #r, l, u, d
        #turuncu hangi yön yakınsa oraya gidecek
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed 
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction        

    def move_red(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blue(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_pink(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction


def draw_other():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Defeat! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))


def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'pink', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color0, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), (i + 1) * num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color0, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, (i * num1 + (0.5 * num1))), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color0, [(j * num2 - (num2 * 0.5) + 2), (i * num1 + (num1 * 0.5) - 1), num2, num1], 0, pi/2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color0, [(j * num2 + (num2 * 0.5)), (i * num1 + (num1 * 0.5)), num2, num1], pi/2, pi, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color0, [(j * num2 + (num2 * 0.5)), (i * num1 - (num1 * 0.4)), num2, num1], pi, 3*pi/2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color0, [(j * num2 - (num2 * 0.4)) - 1, (i * num1 - (num1 * 0.4)), num2, num1], 3*pi/2, 2*pi, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, (i * num1 + (0.5 * num1))), 3)
                
def draw_player():
    # 0 = right, 1 = left, 2 = up, 3 = down
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    num3 = 15

    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move_player(play_x, play_y):
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    if direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    if direction == 3 and turns_allowed[3]:
        play_y += player_speed

    return play_x, play_y

def check_collisions(score, powerup, powerup_counter, eaten_ghosts):
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            score += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            score += 50
            powerup = True
            powerup_counter = 0
            eaten_ghosts = [False, False, False, False]

    
    return score, powerup, powerup_counter, eaten_ghosts

def get_targets(red_x, red_y, blue_x, blue_y, pink_x, pink_y, orange_x, orange_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not red_ghost.dead and not eaten_ghosts[0]:
            red_target = (runaway_x, runaway_y)
        elif not red_ghost.dead and eaten_ghosts[0]:
            if 340 < red_x < 560 and 340 < red_y < 500:
                red_target = (400, 100)
            else:
                red_target = (player_x, player_y)
        else:
            red_target = return_target

        if not blue_ghost.dead and not eaten_ghosts[1]:
            blue_target = (runaway_x, player_y)
        elif not blue_ghost.dead and eaten_ghosts[1]:
            if 340 < blue_x < 560 and 340 < blue_y < 500:
                blue_target = (400, 100)
            else:
                blue_target = (player_x, player_y)
        else:
            blue_target = return_target

        if not pink_ghost.dead:
            pink_target = (player_x, runaway_y)
        elif not pink_ghost.dead and eaten_ghosts[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target

        if not orange_ghost.dead and not eaten_ghosts[3]:
            orange_target = (450, 450)
        elif not orange_ghost.dead and eaten_ghosts[3]:
            if 340 < orange_x < 560 and 340 < orange_y < 500:
                orange_target = (400, 100)
            else:
                orange_target = (player_x, player_y)
        else:
            orange_target = return_target
    else:
        if not red_ghost.dead:
            if 340 < red_x < 560 and 340 < red_y < 500:
                red_target = (400, 100)
            else:
                red_target = (player_x, player_y)
        else:
            red_target = return_target

        if not blue_ghost.dead:
            if 340 < blue_x < 560 and 340 < blue_y < 500:
                blue_target = (400, 100)
            else:
                blue_target = (player_x, player_y)
        else:
            blue_target = return_target

        if not pink_ghost.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target

        if not orange_ghost.dead:
            if 340 < orange_x < 560 and 340 < orange_y < 500:
                orange_target = (400, 100)
            else:
                orange_target = (player_x, player_y)
        else:
            orange_target = return_target
    return [red_target, blue_target, pink_target, orange_target]

run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    if powerup and powerup_counter < 600:
        powerup_counter += 1
    elif powerup and powerup_counter >= 600:
        powerup = False
        powerup_counter = 0
        eaten_ghosts = [False, False, False, False]

    if start_counter < 180 and not game_over and not game_won:
        moving = False
        start_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_board()
    center_x = player_x + 22
    center_y = player_y + 22
    if powerup:
        ghost_speeds = [2, 2, 2, 2]
    else:
        ghost_speeds = [3, 3, 3, 3]
    if eaten_ghosts[0]:
        ghost_speeds[0] = 3
    if eaten_ghosts[1]:
        ghost_speeds[1] = 3
    if eaten_ghosts[2]:
        ghost_speeds[2] = 3
    if eaten_ghosts[3]:
        ghost_speeds[3] = 3
    if red_dead:
        ghost_speeds[0] = 5
    if blue_dead:
        ghost_speeds[1] = 5
    if pink_dead:
        ghost_speeds[2] = 5
    if orange_dead:
        ghost_speeds[3] = 5

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
    draw_player()
    red_ghost = Ghost(red_x, red_y, targets[0], ghost_speeds[0], red_img, red_direction, red_dead, red_box, 0)
    blue_ghost = Ghost(blue_x, blue_y, targets[1], ghost_speeds[1], blue_img, blue_direction, blue_dead, blue_box, 1)
    pink_ghost = Ghost(pink_x, pink_y, targets[2], ghost_speeds[2], pink_img, pink_direction, pink_dead, pink_box, 2)
    orange_ghost = Ghost(orange_x, orange_y, targets[3], ghost_speeds[3], orange_img, orange_direction, orange_dead, orange_box, 3)
    draw_other()
    targets = get_targets(red_x, red_y, blue_x, blue_y, pink_x, pink_y, orange_x, orange_y)
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not red_ghost.dead and not red_ghost.in_box:
            red_x, red_y, red_direction = red_ghost.move_red()
        else:
            red_x, red_y, red_direction = red_ghost.move_orange()
        if not blue_ghost.dead and not blue_ghost.in_box:
            blue_x, blue_y, blue_direction = blue_ghost.move_blue()
        else:
            blue_x, blue_y, blue_direction = blue_ghost.move_orange()
        if not pink_ghost.dead and not pink_ghost.in_box:
            pink_x, pink_y, pink_direction = pink_ghost.move_pink()
        else:
            pink_x, pink_y, pink_direction = pink_ghost.move_orange()
        
        orange_x, orange_y, orange_direction = orange_ghost.move_orange()
    score, powerup, powerup_counter, eaten_ghosts = check_collisions(score, powerup, powerup_counter, eaten_ghosts)



    if not powerup:
        if (player_circle.colliderect(red_ghost.rect) and not red_ghost.dead) or \
                (player_circle.colliderect(blue_ghost.rect) and not blue_ghost.dead) or \
                (player_circle.colliderect(pink_ghost.rect) and not pink_ghost.dead) or \
                (player_circle.colliderect(orange_ghost.rect) and not orange_ghost.dead):
            if lives > 0:
                lives -= 1
                start_counter = 0
                powerup = False
                powerup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                red_x = 56
                red_y = 58
                red_direction = 0
                blue_x = 440
                blue_y = 388
                blue_direction = 2
                pink_x = 440
                pink_y = 438
                pink_direction = 2
                orange_x = 440
                orange_y = 438
                orange_direction = 2
                eaten_ghosts = [False, False, False, False]
                red_dead = False
                blue_dead = False
                pink_dead = False
                orange_dead = False
            else:
                game_over = True
                moving = False
                start_counter = 0
    if powerup and player_circle.colliderect(red_ghost.rect) and eaten_ghosts[0] and not red_ghost.dead:
        if lives > 0:
            lives -= 1
            start_counter = 0
            powerup = False
            powerup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            pink_x = 440
            pink_y = 438
            pink_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghosts = [False, False, False, False]
            red_dead = False
            blue_dead = False
            pink_dead = False
            orange_dead = False
        else:
            game_over = True
            moving = False
            start_counter = 0
    if powerup and player_circle.colliderect(blue_ghost.rect) and eaten_ghosts[1] and not blue_ghost.dead:
        if lives > 0:
            lives -= 1
            start_counter = 0
            powerup = False
            powerup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            pink_x = 440
            pink_y = 438
            pink_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghosts = [False, False, False, False]
            red_dead = False
            blue_dead = False
            pink_dead = False
            orange_dead = False
        else:
            game_over = True
            moving = False
            start_counter = 0
    if powerup and player_circle.colliderect(pink_ghost.rect) and eaten_ghosts[2] and not pink_ghost.dead:
        if lives > 0:
            lives -= 1
            start_counter = 0
            powerup = False
            powerup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            pink_x = 440
            pink_y = 438
            pink_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghosts = [False, False, False, False]
            red_dead = False
            blue_dead = False
            pink_dead = False
            orange_dead = False
        else:
            game_over = True
            moving = False
            start_counter = 0
    if powerup and player_circle.colliderect(orange_ghost.rect) and eaten_ghosts[3] and not orange_ghost.dead:
        if lives > 0:
            lives -= 1
            start_counter = 0
            powerup = False
            powerup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            pink_x = 440
            pink_y = 438
            pink_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghosts = [False, False, False, False]
            red_dead = False
            blue_dead = False
            pink_dead = False
            orange_dead = False
        else:
            game_over = True
            moving = False
            start_counter = 0
    if powerup and player_circle.colliderect(red_ghost.rect) and not red_ghost.dead and not eaten_ghosts[0]:
        red_dead = True
        eaten_ghosts[0] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    if powerup and player_circle.colliderect(blue_ghost.rect) and not blue_ghost.dead and not eaten_ghosts[1]:
        blue_dead = True
        eaten_ghosts[1] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    if powerup and player_circle.colliderect(pink_ghost.rect) and not pink_ghost.dead and not eaten_ghosts[2]:
        pink_dead = True
        eaten_ghosts[2] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    if powerup and player_circle.colliderect(orange_ghost.rect) and not orange_ghost.dead and not eaten_ghosts[3]:
        orange_dead = True
        eaten_ghosts[3] = True
        score += (2 ** eaten_ghosts.count(True)) * 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                powerup_counter = 0
                lives -= 1
                start_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                red_x = 56
                red_y = 58
                red_direction = 0
                blue_x = 440
                blue_y = 388
                blue_direction = 2
                pink_x = 440
                pink_y = 438
                pink_direction = 2
                orange_x = 440
                orange_y = 438
                orange_direction = 2
                eaten_ghosts = [False, False, False, False]
                red_dead = False
                blue_dead = False
                pink_dead = False
                orange_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False 

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction


    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897    
    
    if red_ghost.in_box and red_ghost.dead:
        red_dead = False
    if blue_ghost.in_box and blue_ghost.dead:
        blue_dead = False
    if pink_ghost.in_box and pink_ghost.dead:
        pink_dead = False
    if orange_ghost.in_box and orange_ghost.dead:
        orange_dead = False

    pygame.display.flip()
pygame.quit()