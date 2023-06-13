import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set the width and height of the game window
window_width = 1024
window_height = 1024
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Advanced Snake Game")

# Set the clock to control the game's frame rate
clock = pygame.time.Clock()

# Set the snake's initial position and movement direction
snake_pos = [(window_width // 2, (window_height // 2) + 50)]
snake_size = 20
snake_speed = 5
snake_direction = "right"

# Create the food at a random position
food_pos = (
    random.randint(0, (window_width - snake_size) // snake_size) * snake_size,
    random.randint(0, (window_height - snake_size - 50) // snake_size) * snake_size + 50,
)
food_spawned = True

def create_food():
    global random_fruit_img

    # Generate a random position for the food
    x = random.randint(0, (window_width - snake_size) // snake_size) * snake_size
    y = random.randint(0, (window_height - snake_size - game_bar_height) // snake_size) * snake_size + game_bar_height

    # Generate a new random fruit image if it's the same as the previous one
    while True:
        new_fruit_img = random.choice(fruit_images)
        if new_fruit_img != random_fruit_img:
            random_fruit_img = new_fruit_img
            break

    return x, y

# Set the initial score and level
score = 0
level = 0

# Load the font for displaying text
font = pygame.font.Font(None, 36)
bold_font = pygame.font.Font(None, 48)

# Load the image for the snake's head
snake_head_img = pygame.image.load("assets/graphic/snake_head.png")
snake_head_img = pygame.transform.scale(snake_head_img, (snake_size, snake_size))

# Load the background image
background_img = pygame.image.load("assets/graphic/background.png")
background_img = pygame.transform.scale(background_img, window_size)

# Load the sound effect for eating
eating_sound = pygame.mixer.Sound("assets/audio/eating_fx.mp3")

# Load the game over image
game_over_img = pygame.image.load("assets/graphic/game_over.png")
game_over_img = pygame.transform.scale(game_over_img, window_size)

# Load the intro screen
start_screen_img = pygame.image.load("assets/graphic/start_screen.png")
start_screen_img = pygame.transform.scale(start_screen_img, window_size)

# Load the play button image
play_btn_img = pygame.image.load("assets/graphic/play_btn.png")

fruit1_img = pygame.image.load("assets/graphic/apple.png")
fruit2_img = pygame.image.load("assets/graphic/pear.png")
fruit3_img = pygame.image.load("assets/graphic/watermelon.png")
fruit4_img = pygame.image.load("assets/graphic/strawberry.png")

fruit_images = [fruit1_img, fruit2_img, fruit3_img, fruit4_img]

# Load the random fruit image once at the beginning
random_fruit_img = random.choice(fruit_images)

# Define the height of the game bar
game_bar_height = 50

# Function to display text on the screen
def display_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

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

# Function to start the game
def start_game():
    global snake_pos, snake_direction, score, food_spawned, level
    snake_pos = [(window_width // 2, (window_height // 2) + game_bar_height)]
    snake_direction = "right"
    score = 0
    level = 1
    food_spawned = True

# Variables to control game state
game_started = False
game_over = False
previous_score = 0
required_score = 5

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:  # Restart the game when Space is pressed after game over
                    game_started = True
                    game_over = False
                    start_game()
                elif not game_started:  # Start the game when Space is pressed for the first time
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
        if not game_over:
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
            if (
                new_head[0] < 0
                or new_head[0] >= window_width
                or new_head[1] < game_bar_height
                or new_head[1] >= window_height
            ):
                game_over = True

            # Check for collision with the snake's body
            if new_head in snake_pos[1:]:
                game_over = True

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

            # Check if the required score for the next level is reached
            if score - previous_score >= required_score:
                previous_score = score
                level += 1
                snake_speed += 1

        # Clear the screen
        screen.fill(BLACK)

        # Draw the background image
        screen.blit(background_img, (0, 0))

        # Draw the snake
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, (pos[0], pos[1], snake_size, snake_size))

        # Draw the snake's head
        snake_head = rotate_head(snake_head_img, snake_direction)
        screen.blit(snake_head, (snake_pos[0][0], snake_pos[0][1]))

        # Draw the food
        if not food_spawned:
            # Create a random position for the food
            food_pos = create_food()

            # Load the random fruit image once at the beginning
            random_fruit_img = random.choice(fruit_images)

            food_spawned = True

        # Draw the food image
        screen.blit(random_fruit_img, (food_pos[0], food_pos[1]))


        # Draw the game bar
        pygame.draw.rect(screen, GRAY, (0, 0, window_width, game_bar_height))

        # Display game information
        display_text(f"Score: {score}", font, WHITE, 100, game_bar_height // 2)
        display_text(f"Level: {level}", font, WHITE, window_width // 2, game_bar_height // 2)


        # Update the display
        pygame.display.flip()

        # Control the game's frame rate
        clock.tick(30)
         
    else:
        # Display the start screen
        screen.blit(start_screen_img, (0, 0))
        screen.blit(play_btn_img, ((window_width - play_btn_img.get_width()) // 2, (window_height - play_btn_img.get_height()) // 2))


        # Check for button clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()

        if (
            (window_width - play_btn_img.get_width()) // 2 <= mouse_pos[0] <= (window_width + play_btn_img.get_width()) // 2
            and (window_height - play_btn_img.get_height()) // 2 <= mouse_pos[1] <= (window_height + play_btn_img.get_height()) // 2
        ):
            if mouse_clicked[0]:
                game_started = True
                start_game()

        if 10 <= mouse_pos[0] <= 10 + vol_on_img.get_width() and window_height - vol_on_img.get_height() - 10 <= mouse_pos[1] <= window_height - 10:
            if mouse_clicked[0]:
                sound_on = not sound_on
                if sound_on:
                    pygame.mixer.unpause()
                else:
                    pygame.mixer.pause()

        # Update the display
        pygame.display.flip()

        # Control the game's frame rate
        clock.tick(30)


# Exit the program
pygame.quit()
sys.exit()
