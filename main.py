import pygame
from components.input import InputBox
from components.button import ButtonSetUp, ButtonLaunch
from components.dropdown import DropDown
from components.text import Text
from util.colors import Colors
from components.rectangle import Rectangle
from components.projectile import Projectile
import random


# ------------------------------------------------ SETUP ------------------------------------------------
pygame.init()

# Dimensions
HEIGHT_SCREEN = 280
WIDTH_SCREEN = 330

# Screen setup
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("Setup")
clock = pygame.time.Clock()


width_obstacle = 10
text_obstacle = Text(width_obstacle, 0, "Obstacle")
options = ["None", "Easy", "Medium", "Hard"]
drop_down_obstacle = DropDown(
    width_obstacle, text_obstacle.font_size, 150, 40, options)

width_wind = width_obstacle + drop_down_obstacle.width + 10
text_wind = Text(width_wind, 0, "Wind")
options = ["None", "Easy", "Medium", "Hard"]
drop_down_wind = DropDown(width_wind, text_wind.font_size, 150, 40, options)

button = ButtonSetUp(80, 200, 160, 50, "Continue")

setup_options = None

while setup_options is None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        obstacle_selected_option = drop_down_obstacle.handle_event(event)
        wind_selected_option = drop_down_wind.handle_event(event)
        setup_options = button.handle_event(
            event, drop_down_obstacle, drop_down_wind)
        if setup_options:
            break

    screen.fill(Colors.white)

    text_obstacle.draw(screen)
    drop_down_obstacle.draw(screen)

    text_wind.draw(screen)
    drop_down_wind.draw(screen)

    button.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

# ------------------------------------------------ GAME ------------------------------------------------
pygame.init()
pygame.mixer.init()

# Dimensions
HEIGHT_SCREEN = 600
WIDTH_GAME_SCREEN = 700 + 300
WIDTH_LAUNCH_SCREEN = 300
WIDTH_SCREEN = WIDTH_GAME_SCREEN + WIDTH_LAUNCH_SCREEN

# Screen setup
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("Projectil game")
clock = pygame.time.Clock()


launch_panel = Rectangle(WIDTH_GAME_SCREEN, 0,
                         WIDTH_LAUNCH_SCREEN, HEIGHT_SCREEN, Colors.light_grey)

ground_height = 100
ground = Rectangle(0, HEIGHT_SCREEN - ground_height,
                   WIDTH_GAME_SCREEN, HEIGHT_SCREEN, Colors.black)


obstacle_height = {
    "None": 0,
    "Easy": random.randint(50, 150),
    "Medium": random.randint(150, 250),
    "Hard": random.randint(250, 350),
}

obstacle_width = 8

obstacle = Rectangle(WIDTH_GAME_SCREEN // 2 - obstacle_width // 2,
                     HEIGHT_SCREEN - ground_height -
                     obstacle_height[setup_options["obstacle"]],
                     obstacle_width,
                     obstacle_height[setup_options["obstacle"]],
                     Colors.black)


margin_player = 10
size_box_player = 40

left_box_player = Rectangle(margin_player,
                            HEIGHT_SCREEN - ground_height - size_box_player,
                            size_box_player,
                            size_box_player,
                            Colors.red)


right_box_player = Rectangle(WIDTH_GAME_SCREEN - margin_player - size_box_player,
                             HEIGHT_SCREEN - ground_height - size_box_player,
                             size_box_player,  size_box_player,
                             Colors.red)


margin_input = 10

input_speed = InputBox(WIDTH_GAME_SCREEN + margin_player,
                       50, 200, 50, "Initial velocity")
input_speed.set_max_value(120)

input_angle = InputBox(WIDTH_GAME_SCREEN + margin_player,
                       150, 200, 50, "Angle")
input_angle.set_max_value(90)

button_launch = ButtonLaunch(
    WIDTH_GAME_SCREEN + margin_player, 250, 200, 50, "Launch")

player_text = Text(WIDTH_GAME_SCREEN + margin_player, 350, "Player turn: left")

def random_number(inf, sup):
    return inf + (sup - inf) * random.random()

def wind_simulator():
    wind_values = {
        "None": 0,                          
        "Easy": random_number(0.5, 1),
        "Medium": random_number(1, 2),
        "Hard": random_number(2, 3.5),
    }

    wind_magnitud = wind_values[setup_options["wind"]]
    wind_direction = random.choice([-1, 1])
    wind = wind_magnitud * wind_direction

    return wind


wind = wind_simulator()

winner = None

current_player = "left"  # Comienza el jugador de la izquierda
projectile = None  # Inicialmente no hay proyectil

while winner is None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        input_speed.handle_event(event)
        input_angle.handle_event(event)

        data = button_launch.handle_event(event, input_speed, input_angle)
        if data and not projectile:
            pygame.mixer.music.load("sounds/shoot.mp3")
            pygame.mixer.music.play()

            speed = data["speed"]
            angle = data["angle"]

            if current_player == "left":
                starting_pos = (left_box_player.x_pos +
                                left_box_player.width, left_box_player.y_pos)
            else:
                angle = 180 - angle
                starting_pos = (right_box_player.x_pos, right_box_player.y_pos)

            wind = wind_simulator()
            print(wind, "<-" if wind < 0 else "->")

            projectile = Projectile(
                starting_pos[0], starting_pos[1], speed, angle, wind)

    screen.fill(Colors.white)
    ground.draw(screen)
    obstacle.draw(screen)
    launch_panel.draw(screen)

    left_box_player.draw(screen)
    right_box_player.draw(screen)

    input_speed.draw(screen)
    input_angle.draw(screen)
    button_launch.draw(screen)

    player_text.draw(screen)

    if projectile:
        projectile.update()
        projectile.draw(screen)
        projectile.draw_path(screen)

        if current_player == "left":
            if projectile.check_collision(right_box_player):
                pygame.mixer.music.load("sounds/explotion.mp3")
                pygame.mixer.music.play()
                pygame.time.delay(3000)
                winner = "left"
        else:
            if projectile.check_collision(left_box_player):
                pygame.mixer.music.load("sounds/explotion.mp3")
                pygame.mixer.music.play()
                pygame.time.delay(3000)
                winner = "right"

        if projectile.check_collision(obstacle) or \
                projectile.check_collision(ground) or \
                projectile.is_out_of_bounds(HEIGHT_SCREEN, WIDTH_GAME_SCREEN):

            pygame.mixer.music.load("sounds/explotion.mp3")
            pygame.mixer.music.play()

            projectile = None
            current_player = "right" if current_player == "left" else "left"
            player_text.set_text(f"Player turn: {current_player}")

    pygame.display.update()
    clock.tick(60)


pygame.quit()

# ------------------------------------------------ WINNER ------------------------------------------------

pygame.init()

WIDTH_WINNER_SCREEN = 400
HEIGHT_WINNER_SCREEN = 200

# screen to display winner
screen = pygame.display.set_mode((WIDTH_WINNER_SCREEN, HEIGHT_WINNER_SCREEN))
pygame.display.set_caption("Winner")
clock = pygame.time.Clock()

padding = 10
# Las coordenadas no importan aquí porque las ajustaremos después
text = Text(0, 0, f"Player {winner.upper()} wins!")

text_width, text_height = text.text_surface.get_size()
text.x = (WIDTH_WINNER_SCREEN - text_width) // 2
text.y = (HEIGHT_WINNER_SCREEN - text_height) // 2

pygame.mixer.music.load("sounds/celebration.mp3")
pygame.mixer.music.play()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill(Colors.white)
    text.draw(screen)

    pygame.display.update()
    clock.tick(60)

