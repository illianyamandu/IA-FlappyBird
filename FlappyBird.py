import pygame
import os
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
BIRD_PICTURES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

pygame.font.init()
FONT_SCORE = pygame.font.SysFont('arial', 50)

class Bird:
    IMGS = BIRD_PICTURES
    # animações de inclinação
    MAX_ROTATION = 25
    SPEED_ROTATION = 20
    TIME_ANIMATION = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.image.count = 0
        self.image = self.IMGS[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        # calcular deslocamento
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.speed * self.time

        # restringir o deslocamento
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        # o angulo do pássaro
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.SPEED_ROTATION

    def draw(self, screen):
        # definir qual imagem do pássaro será usada
        self.image.count += 1

        if self.image.count < self.TIME_ANIMATION:
            self.image = self.IMGS[0]
        elif self.image.count < self.TIME_ANIMATION*2:
            self.image = self.IMGS[1]
        elif self.image.count < self.TIME_ANIMATION*3:
            self.image = self.IMGS[2]
        elif self.image.count < self.TIME_ANIMATION*4:
            self.image = self.IMGS[1]
        elif self.image.count < self.TIME_ANIMATION*4 + 1:
            self.image = self.IMGS[0]
            self.image.count = 0

        # se o pássaro estiver caindo eu não vou bater asas
        if self.angle <= -80:
            self.image = self.IMGS[1]
            self.image.count = self.TIME_ANIMATION*2

        # desenhar a imagem
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        pos_image_center = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_image.get_rect(center=pos_image_center)
        screen.blit(rotated_image, rectangle.topleft)

    def get_mask(self):
        pygame.mask.from_surface(self.image)

class Pipe:
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.pos_top = 0
        self.pos_bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BASE = PIPE_IMAGE
        self.passedOn = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.pos_bottom = self.height - self.PIPE_TOP.get_height()
        self.pos_top = self.altura + self.DISTANCE

    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.pos_top))
        screen.blit(self.PIPE_BASE, (self.x, self.pos_bottom))

    def collide(self, Bird):
        Bird_mask = Bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BASE)

        top_distance = (self.x - Bird.x, self.pos_top - round(self.PIPE_TOP))
        bottom_distance = (self.x - Bird.x, self.pos_bottom - round(Bird.y))

        top_point = Bird_mask.overlap(top_mask, top_distance)
        bottom_point = Bird_mask.overlap(bottom_mask, bottom_distance)

        if top_point or bottom_point:
            return True
        else:
            return False

class Base:
    SPEED = 5
    WIDTH = BASE_IMAGE.get_width()
    IMAGE = BASE_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x1 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x2 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))

def draw_screen(screen, birds, pipes, base, points):
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    text = FONT_SCORE.render(f"Pontuação: {points}", 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
    base.draw(screen)
    pygame.display.update()
    