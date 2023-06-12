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
window_width = 1024
window_height = 1024
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Advanced Snake Game")

# Load the background image
background_img = pygame.image.load("assets/graphic/background.png")
background_img = pygame.transform.scale(background_img, window_size)

# Load the game over image
game_over_img = pygame.image.load("assets/graphic/game_over.png")
game_over_img = pygame.transform.scale(game_over_img, window_size)

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

# Create the food at a random position
food_pos = (
    random.randint(0, (window_width - snake_size) // snake_size) * snake_size,
    random.randint((50 + snake_size) // snake_size, (window_height - snake_size) // snake_size) * snake_size,
)
food_spawned = True

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

# Main game loop
running = True
game_started = False  # Flag to check if the game has started
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started:  # Start the game when Space is pressed
                    game_started = True
                    start_game()
            elif event.key == pygame.K_UP and snake_direction != "down":
                snake_direction = "up"
            elif event.key == pygame.K_DOWN and snake_direction != "up":
                snake_direction = "down"
            elif event.key == pygame.K_LEFT and snake_direction != "right":
                snake_direction = "left"
            elif event.key == pygame.K_RIGHT and snake_direction != "left":
                snake_direction = "right"

    if game_started:
        # Move the snake
        if snake_direction == "up":
            new_head = (snake_pos[0][0], snake_pos[0][1] - snake_speed)
        elif snake_direction == "down":
            new_head = (snake_pos[0][0], snake_pos[0][1] + snake_speed)
        elif snake_direction == "left":
            new_head = (snake_pos[0][0] - snake_speed, snake_pos[0][1])
        elif snake_direction == "right":
            new_head = (snake_pos[0][0] + snake_speed, snake_pos[0][1])

        # Check for collision with the boundaries
        if new_head[0] < 0 or new_head[0] >= window_width or \
                new_head[1] < 0 or new_head[1] >= window_height:
            game_started = False

        # Check for collision with the snake's body
        if new_head in snake_pos[1:]:
            game_started = False

        # Check for collision with the food
        if is_close_to_food():
            score += 1
            food_spawned = False
            eating_sound.play()  # Play the sound effect

            # Grow the snake by inserting a new head position at the front
            snake_pos.insert(0, new_head)
        else:
            # Move the snake by removing the tail and inserting the new head position at the front
            snake_pos.pop()
            snake_pos.insert(0, new_head)

        # Spawn new food if necessary
        if not food_spawned:
            food_pos = (random.randint(0, (window_width - snake_size) // snake_size) * snake_size,
                        random.randint(0, (window_height - snake_size) // snake_size) * snake_size)
            food_spawned = True

        # Draw the background image
        screen.blit(background_img, (0, 0))

        # Draw the snake's body
        for pos in snake_pos[1:]:
            pygame.draw.rect(screen, GREEN, (pos[0], pos[1], snake_size, snake_size))

        # Rotate and draw the snake's head
        rotated_head = rotate_head(snake_head_img, snake_direction)
        screen.blit(rotated_head, (snake_pos[0][0], snake_pos[0][1]))

        # Draw the food
        pygame.draw.circle(screen, RED, (food_pos[0] + snake_size // 2, food_pos[1] + snake_size // 2), snake_size // 2)

        # Draw the volume buttons
        if mute:
            screen.blit(vol_off_img, (10, 10))
        else:
            screen.blit(vol_on_img, (10, 10))

        # Draw the score
        display_text("Score: " + str(score), font, WHITE, window_width // 2, 20)

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(30)
    else:
        # Draw the game over screen
        screen.blit(game_over_img, (0, 0))

        # Draw the final score
        display_text("Final Score: " + str(score), bold_font, BLACK, window_width // 2, window_height // 2)

        # Update the display
        pygame.display.flip()

# Quit the game
pygame.quit()
