import pygame
import random

# Initialize pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

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