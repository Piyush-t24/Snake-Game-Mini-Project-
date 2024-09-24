# Importing libraries
import pygame
import time
import random

# Initialising pygame
pygame.init()

# Sound effects
eat_sound = pygame.mixer.Sound('eat.mp3')
game_over_sound = pygame.mixer.Sound('gameover.mp3')
bonus_sound = pygame.mixer.Sound('bonus.mp3')

# Speed and window size
window_x = 720
window_y = 480

# Defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
purple = pygame.Color(128, 0, 128)  # Color for bonus fruit

# Initialise game window
pygame.display.set_caption('Piyush Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# Difficulty settings
difficulty = "Medium"
snake_speed = 15

# Snake default position and body
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# Fruit and bonus fruit positions
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]
bonus_fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                        random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True
bonus_fruit_spawn = False  # Bonus fruit initially not spawned

# Teleport portal positions
teleport_1 = [random.randrange(1, (window_x // 10)) * 10,
              random.randrange(1, (window_y // 10)) * 10]
teleport_2 = [random.randrange(1, (window_x // 10)) * 10,
              random.randrange(1, (window_y // 10)) * 10]

# Default direction
direction = 'RIGHT'
change_to = direction

# Initial score and high score
score = 0
high_score = 0

# Load high score from file (if exists)
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

# Snake color selection
snake_color = green
mouth_color = red

# Timer and move limit
move_limit = 100
time_limit = 100  # in seconds
start_ticks = pygame.time.get_ticks()  # starter tick
moves = 0

# Display score function
def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f'Score : {score} | High Score : {high_score} | Moves Left: {move_limit - moves}', True, color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (window_x / 2, 15)
    game_window.blit(score_surface, score_rect)

# Game over function
def game_over():
    global high_score

    # Update high score if needed
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))

    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render(f'Your Score is : {score}', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    pygame.mixer.Sound.play(game_over_sound)
    time.sleep(2)
    pygame.quit()
    quit()

# Function to change snake color
def change_snake_color():
    global snake_color
    if snake_color == green:
        snake_color = blue
    elif snake_color == blue:
        snake_color = yellow
    else:
        snake_color = green

# Function to change mouth color
def change_mouth_color():
    global mouth_color
    if mouth_color == red:
        mouth_color = green
    elif mouth_color == green:
        mouth_color = blue
    else:
        mouth_color = red

# Function to draw the snake with a mouth
def draw_snake():
    # Draw the snake body
    for pos in snake_body:
        pygame.draw.rect(game_window, snake_color, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw the mouth at the top center of the snake head
    mouth_width = 10
    mouth_height = 15
    mouth_x = snake_position[0] + 5  # Center the mouth on the x-axis
    mouth_y = snake_position[1] - mouth_height  # Position it above the snake head

    pygame.draw.polygon(game_window, mouth_color, [
        (mouth_x - mouth_width // 2, mouth_y + mouth_height),
        (mouth_x + mouth_width // 2, mouth_y + mouth_height),
        (mouth_x, mouth_y)
    ])

# Main Function
while True:
    # Handle timer
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
    if seconds >= time_limit:
        game_over()

    # Handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            if event.key == pygame.K_c:  # Press 'C' to change snake color
                change_snake_color()
            if event.key == pygame.K_d:  # Press 'D' to change mouth color
                change_mouth_color()

    # Ensuring the snake cannot move in the opposite direction instantly
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism and fruit collision
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        moves += 1  # Count moves when eating fruit
        snake_speed += 1  # Increase speed after eating
        pygame.mixer.Sound.play(eat_sound)
        fruit_spawn = False
    else:
        snake_body.pop()

    # Bonus fruit mechanism (appears every 50 points)
    if score > 0 and score % 50 == 0 and not bonus_fruit_spawn:
        bonus_fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                                random.randrange(1, (window_y // 10)) * 10]
        bonus_fruit_spawn = True

    if bonus_fruit_spawn and snake_position[0] == bonus_fruit_position[0] and snake_position[1] == bonus_fruit_position[1]:
        score += 50  # Bonus fruit gives more points
        pygame.mixer.Sound.play(bonus_sound)
        bonus_fruit_spawn = False

    # Spawning new fruit
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True

    # Filling background
    game_window.fill(black)

    # Drawing snake
    draw_snake()

    # Drawing fruit and bonus fruit
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
    if bonus_fruit_spawn:
        pygame.draw.rect(game_window, purple, pygame.Rect(bonus_fruit_position[0], bonus_fruit_position[1], 10, 10))

    # Teleportation mechanism
    if snake_position == teleport_1:
        snake_position = teleport_2[:]
    elif snake_position == teleport_2:
        snake_position = teleport_1[:]

    # Draw teleportation portals
    pygame.draw.rect(game_window, blue, pygame.Rect(teleport_1[0], teleport_1[1], 10, 10))
    pygame.draw.rect(game_window, blue, pygame.Rect(teleport_2[0], teleport_2[1], 10, 10))

    # Game over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x - 10 or snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # Update screen and show score
    show_score(white, 'times new roman', 20)
    pygame.display.update()

    # Control game speed
    fps.tick(snake_speed)
