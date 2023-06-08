import pygame
import random

# Initialize pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set the clock to control the game's frame rate
clock = pygame.time.Clock() 

# Set the width and height of the game window
window_width = 1200
window_height = 800
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Advanced Snake Game")

# Set the snake's initial position and movement direction
snake_pos = [(window_width // 2, window_height // 2)]
snake_size = 20
snake_speed = 5
snake_direction = "right"

# Set the initial score
score = 0

# Load the image for the snake's head
snake_head_img = pygame.image.load("assets/graphic/snake_head.png")
snake_head_img = pygame.transform.scale(snake_head_img, (snake_size, snake_size))

# Function to check if the snake's head is close to the food
def is_close_to_food():
    x_distance = abs(snake_pos[0][0] - food_pos[0])
    y_distance = abs(snake_pos[0][1] - food_pos[1])
    return x_distance <= snake_size and y_distance <= snake_size

    # Function to rotate the snake's head image
def rotate_head(image, direction):
    if direction == "up":
        return pygame.transform.rotate(image, 90)
    elif direction == "down":
        return pygame.transform.rotate(image, -90)
    elif direction == "left":
        return pygame.transform.rotate(image, 180)
    else:
        return image

# Initialize the mixer module
pygame.mixer.init()

# Load the sound effect for eating
eating_sound = pygame.mixer.Sound("assets/audio/eating_fx.mp3")

# Load the volume buttons
vol_on_img = pygame.image.load("assets/graphic/vol_on.png")
vol_on_img = pygame.transform.scale(vol_on_img, (50, 50))
vol_off_img = pygame.image.load("assets/graphic/vol_off.png")
vol_off_img = pygame.transform.scale(vol_off_img, (50, 50))


# Flag to control the sound state
mute = False

# Load the font for displaying text
font = pygame.font.Font(None, 36)
bold_font = pygame.font.Font(None, 48)

# Function to display text on the screen
def display_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Function to start the game
def start_game():
    global snake_pos, snake_direction, score, food_spawned
    snake_pos = [(window_width // 2, window_height // 2)]
    snake_direction = "right"
    score = 0
    food_spawned = True

