import pygame
from util.colors import Colors

class Text:
    def __init__(self, x, y, text, font_name="freesansbold.ttf", font_size=32, color=Colors.black):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.font_name = font_name
        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.color = color
        self.text_surface = self.font.render(self.text, True, self.color)

    def set_text(self, new_text):
        """Actualiza el texto y vuelve a renderizarlo."""
        self.text = new_text
        self.text_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        """Dibuja el texto en la pantalla en las coordenadas especificadas."""
        screen.blit(self.text_surface, (self.x, self.y))
