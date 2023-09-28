import pygame
from util.colors import Colors

class DropDown:
    def __init__(self, x, y, width, height, options):

        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = Colors.white
        self.color_active = pygame.Color('lightskyblue3')
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.options = options
        self.active_option = 0
        self.is_open = False
        self.option_height = height

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el menú está abierto y se hace clic en una opción
            if self.is_open:
                # Ajuste: Cambiar la detección de colisiones para abarcar el menú desplegado
                extended_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.option_height * len(self.options))
                if extended_rect.collidepoint(event.pos):
                    index = (event.pos[1] - self.rect.y) // self.option_height
                    if 0 <= index < len(self.options):
                        self.active_option = index
                        self.is_open = False
                        return self.options[self.active_option]
                else:
                    # Si se hace clic fuera del menú desplegable, cierra el menú
                    self.is_open = False
            # Si se hace clic en el cuadro principal para abrir/cerrar el menú
            elif self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open

    def draw(self, screen):
        if not self.is_open:
            pygame.draw.rect(screen, self.color, self.rect)
            txt_surface = self.font.render(self.options[self.active_option], True, Colors.black)
            screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
            pygame.draw.rect(screen, self.color_active, self.rect, 2)
        else:
            for i, option in enumerate(self.options):
                rect = pygame.Rect(self.rect.x, self.rect.y + i*self.option_height, self.rect.width, self.option_height)
                pygame.draw.rect(screen, self.color, rect)
                txt_surface = self.font.render(option, True, Colors.black)
                screen.blit(txt_surface, (rect.x + 5, rect.y + 5))
                pygame.draw.rect(screen, self.color_active, rect, 2)

    def get_option(self):
        return self.options[self.active_option]