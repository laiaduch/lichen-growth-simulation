# This is an example of the Pong game to familiarize myself with the Pygame library.

import pygame
import sys

# Initialize Pygame
pygame.init()

# Window configuration
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Game")

# Color
black = (0, 0, 0)
white = (255, 255, 255)

# Player
player_width, player_height = 20, 100
player_x, player_y = 20, height // 2 - player_height // 2
player_speed = 5

# Opponent
opponent_width, opponent_height = 20, 100
opponent_x, opponent_y = width - 40, height // 2 - opponent_height // 2
opponent_speed = 5

# Ball
ball_size = 15
ball_x, ball_y = width // 2 - ball_size // 2, height // 2 - ball_size // 2
ball_speed_x, ball_speed_y = 7, 7

# Score
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

def draw_objects():
    win.fill(black)
    pygame.draw.rect(win, white, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(win, white, (opponent_x, opponent_y, opponent_width, opponent_height))
    pygame.draw.ellipse(win, white, (ball_x, ball_y, ball_size, ball_size))
    pygame.draw.aaline(win, white, (width // 2, 0), (width // 2, height))

def display_scores():
    player_text = font.render(str(player_score), True, white)
    opponent_text = font.render(str(opponent_score), True, white)
    win.blit(player_text, (width // 4, 20))
    win.blit(opponent_text, (3 * width // 4 - 20, 20))

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < height - player_height:
        player_y += player_speed

    # Movement logical for the opponent
    if opponent_y < ball_y and opponent_y < height - opponent_height:
        opponent_y += opponent_speed
    elif opponent_y > ball_y and opponent_y > 0:
        opponent_y -= opponent_speed

    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Bounce on the upper and lower edges
    if ball_y <= 0 or ball_y >= height - ball_size:
        ball_speed_y = -ball_speed_y

    # Bounce on the paddles
    if player_x + player_width >= ball_x >= player_x and player_y + player_height >= ball_y >= player_y:
        ball_speed_x = -ball_speed_x

    if opponent_x <= ball_x + ball_size <= opponent_x + opponent_width and opponent_y + opponent_height >= ball_y >= opponent_y:
        ball_speed_x = -ball_speed_x

    # Point for the opponent
    if ball_x <= 0:
        opponent_score += 1
        ball_x, ball_y = width // 2 - ball_size // 2, height // 2 - ball_size // 2

    # Point for the player
    if ball_x + ball_size >= width:
        player_score += 1
        ball_x, ball_y = width // 2 - ball_size // 2, height // 2 - ball_size // 2

    draw_objects()
    display_scores()

    pygame.display.flip()
    pygame.time.Clock().tick(30)
