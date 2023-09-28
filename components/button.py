import pygame
from util.colors import Colors

class Button:
    def __init__(self, x, y, w, h, text,
                 color_inactive=Colors.grey,
                 color_disabled=Colors.blue,
                 color_active=Colors.green):
        
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = color_inactive
        self.color_disabled = color_disabled
        self.color_active = color_active
        self.color = self.color_inactive
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.text = text
        self.txt_surface = self.font.render(self.text, True, Colors.black)
        self.pressed = False
        self.enabled = True
        self.was_out = False

    def handle_event(self, event):
 
        if event.type == pygame.MOUSEBUTTONDOWN and self.enabled:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                self.color = self.color_active
        elif event.type == pygame.MOUSEBUTTONUP and self.enabled:
            # if self.rect.collidepoint(event.pos):
            self.pressed = False
            self.color = self.color_inactive

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x + (self.rect.w - self.txt_surface.get_width()) // 2,
                                       self.rect.y + (self.rect.h - self.txt_surface.get_height()) // 2))
        
class ButtonSetUp(Button):
    def __init__(self, x, y, w, h, text, color_inactive=Colors.grey, color_disabled=Colors.blue, color_active=Colors.green):
        super().__init__(x, y, w, h, text, color_inactive, color_disabled, color_active)

    def handle_event(self, event, drop_down_obstacle, drop_down_wind):
        if event.type == pygame.MOUSEBUTTONDOWN and self.enabled:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                self.color = self.color_active
                self.was_out = False  # Inicializamos la variable cuando se presiona el botón
        elif event.type == pygame.MOUSEMOTION and self.pressed:  # Detectar movimiento del mouse
            if not self.rect.collidepoint(event.pos):  # Si el mouse sale del botón mientras está siendo presionado
                self.was_out = True  # Marcamos que el usuario salió del botón
                self.color = self.color_inactive  # Cambiamos el color de vuelta a inactivo (gris)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed:  # Solo revisamos si estaba presionado
                if self.rect.collidepoint(event.pos) and not self.was_out:  # Si se soltó el clic dentro del botón y el usuario no salió antes
                    data = {"obstacle": drop_down_obstacle.get_option(), "wind": drop_down_wind.get_option()}
                    self.color = self.color_inactive
                    return data
                self.pressed = False






class ButtonLaunch(Button):
    def __init__(self, x, y, w, h, text, color_inactive=Colors.red, color_disabled=Colors.grey, color_active=Colors.rose):
        super().__init__(x, y, w, h, text, color_inactive, color_disabled, color_active)

    def handle_event(self, event, input_box1, input_box2):
        if not input_box1.text or not input_box2.text:
            self.color = self.color_disabled
            self.enabled = False
        else:
            # Solo actualizar el color a inactivo si no está presionado
            if not self.pressed:
                self.color = self.color_inactive
            self.enabled = True

        if event.type == pygame.MOUSEBUTTONDOWN and self.enabled:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                self.was_out = False  # Reiniciamos el valor de was_out cada vez que se presiona el botón
                self.color = self.color_active
                
                # Desactivar el botón inmediatamente después del primer clic
                self.enabled = False

        elif event.type == pygame.MOUSEMOTION and self.pressed:  # Detectar movimiento del mouse
            # Si el mouse sale del botón mientras está siendo presionado
            if not self.rect.collidepoint(event.pos):
                self.color = self.color_inactive if self.enabled else self.color_disabled
                self.was_out = True  # Establecemos que el mouse salió del botón
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and not self.was_out:  # Solo activar el botón si el mouse nunca salió de su área
                if self.rect.collidepoint(event.pos): # Si se soltó el clic dentro del botón
                    data = {"speed": float(input_box1.text), "angle": float(input_box2.text)}
                    
                    # Limpiar los InputBox
                    input_box1.text = ""
                    input_box1.txt_surface = input_box1.font.render(input_box1.text, True, Colors.black)
                    input_box2.text = ""
                    input_box2.txt_surface = input_box2.font.render(input_box2.text, True, Colors.black)
                    
                    # Desactivar el botón después de soltar el clic
                    self.color = self.color_disabled
                    self.enabled = False
                    self.pressed = False

                    return data
                    
                else:
                    self.color = self.color_inactive if self.enabled else self.color_disabled
                self.pressed = False
