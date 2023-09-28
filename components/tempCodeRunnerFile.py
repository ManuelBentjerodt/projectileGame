import pygame
import math
from util.colors import Colors

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, v0, angle, ax=0, gravity=9.8):
        super().__init__()
        
        self.image = pygame.Surface([5, 5])
        self.image.fill(Colors.red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gravity = gravity
        
        # Descomposición de la velocidad inicial
        self.vx = v0 * math.cos(math.radians(angle))
        self.vy = -v0 * math.sin(math.radians(angle)) # Nota el signo negativo para ajustar la dirección en pygame
        self.ax = ax
        self.t = 0

    def update(self):
        dt = 0.1
        self.rect.x += int(self.vx * dt + 0.5 * self.ax * dt**2)
        self.rect.y += int(self.vy * dt + 0.5 * self.gravity * dt**2)

        # Actualizar las velocidades
        self.vx += self.ax * dt
        self.vy += self.gravity * dt
        self.t += dt

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def check_collision(self, other):
        return self.rect.colliderect(other)

    def is_out_of_bounds(self, height, width):
        return self.rect.y > height or self.rect.x > width or self.rect.x < 0
