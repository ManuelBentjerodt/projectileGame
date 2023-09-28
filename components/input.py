import pygame
from util.colors import Colors

class InputBox:
    def __init__(self, x_pos, y_pos, width, height, label_text):
        self.x_position = x_pos
        self.y_position = y_pos
        self.width = width
        self.height = height

        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.label_text = label_text
        self.label = self.font.render(self.label_text, True, Colors.black)
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, Colors.black)


        self.background_color = Colors.white
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive

        self.active = False

        self.max_chars = 8
        self.max_value = float('inf')

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN and len(self.text) > 0:
                    # print(self.text)
                    # self.color = self.color_inactive
                    # self.active = False
                    # self.text = ''
                    pass

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    new_value = self.text + event.unicode
                    if event.unicode.isdigit() and len(self.text) < self.max_chars and float(new_value) <= self.max_value:
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, Colors.grey)

                return self.text

    def draw(self, screen):
    
        pygame.draw.rect(screen, self.background_color, self.rect)
        screen.blit(self.label, (self.rect.x, self.rect.y - 30))
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self):
        return self.text
    
    def set_max_value(self, max_val):
        self.max_value = float(max_val)