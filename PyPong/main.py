import pygame
import pygame.freetype
import random
import sys
import math

pygame.init()
pygame.freetype.set_default_resolution(120)
programIcon = pygame.image.load("icon.png")
pygame.display.set_icon(programIcon)

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyPong")

# Player and ball attributes
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 100
PLAYER_COLOR_OPTIONS = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
player1_color, player2_color = None, None
ball_color = (255, 255, 255)
player_y, player2_y = SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2
player_x, player2_x = 0, SCREEN_WIDTH - PLAYER_WIDTH
player_speed, player2_speed = 0.8, 0.8
ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
BALL_SPEED = 1.3
ball_speed_x, ball_speed_y = 0, 0
BALL_RADIUS = 10

# Score-related stuff
player_score, player2_score = 0, 0
delay_after_goal, delay_duration = False, 2
VICTORY_THRESHOLD = 5
player1_victories, player2_victories = 0, 0
sequential_games_played = 0

# Fonts and stuff
victory_font = pygame.freetype.SysFont('lato-regular', 55, True)
font_start = pygame.freetype.SysFont('lato-regular', 40, True)  # Adjusted font size
first_line_text, _ = font_start.render("First to 5 wins!", (255, 255, 255))
first_line_rect = first_line_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
second_line_text, _ = font_start.render("Press SPACE to begin", (255, 255, 255))
second_line_rect = second_line_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Check if the welcome screen has been shown
welcome_screen_shown = False

def initialize_game():
    global running, ball_speed_x, ball_speed_y, welcome_screen_shown, sequential_games_played

    # Display welcome screen only if it hasn't been shown
    if not welcome_screen_shown:
        show_welcome_screen()
        pygame.time.wait(4000)
        welcome_screen_shown = True

    # Display color menu for Player 1
    draw_color_selection(1)
    pygame.display.flip()

    # Choose color for Player 1
    choose_color(1)

    # Display color menu for Player 2
    draw_color_selection(2)
    pygame.display.flip()

    # Choose color for Player 2
    choose_color(2)

    # Display start menu and get start signal
    screen.fill((0, 0, 0))
    screen.blit(first_line_text, first_line_rect)
    screen.blit(second_line_text, second_line_rect)
    pygame.display.flip()
    ball_speed_x, ball_speed_y = start_menu()

    # Increment sequential games counter
    sequential_games_played += 1

    # Set running to True to start the main game loop
    running = True

def show_welcome_screen():
    welcome_font = pygame.freetype.SysFont('lato-regular', 60, True)
    welcome_font2 = pygame.freetype.SysFont('lato-regular', 30, True)
    welcome_text, _ = welcome_font.render("Welcome to PyPong!", (255, 255, 255))
    welcome_text_rect = welcome_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    welcome_text2, _ = welcome_font2.render("A simple Pong game", (255, 255, 255))
    welcome_text2_rect = welcome_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(welcome_text, welcome_text_rect)
    screen.blit(welcome_text2, welcome_text2_rect)
    pygame.display.flip()
def draw_color_selection(player_number):
    # Draw color selection screen for the given player
    screen.fill((0, 0, 0))
    font_color_choice = pygame.freetype.SysFont('lato-regular', 30, True)
    player_text, _ = font_color_choice.render(f"Player {player_number}: Choose your color", (255, 255, 255))
    text_position_y = SCREEN_HEIGHT // 2 - 90
    screen.blit(player_text, (SCREEN_WIDTH // 4 - 50, text_position_y))
    for i, color in enumerate(PLAYER_COLOR_OPTIONS):
        rect_position_y = SCREEN_HEIGHT // 2 - 30
        pygame.draw.rect(screen, color, (SCREEN_WIDTH // 4 + 20 + i * 100, rect_position_y, 100, 100), 0, 15)
def choose_color(player_number):
    global player1_color, player2_color
    while (player_number == 1 and player1_color is None) or (player_number == 2 and player2_color is None):
        for user_event in pygame.event.get():
            if user_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if user_event.type == pygame.MOUSEBUTTONDOWN:
                x, y = user_event.pos
                color_index = (x - SCREEN_WIDTH // 4 + 00) // 100
                rect_position_y = SCREEN_HEIGHT // 2 - 30
                if rect_position_y <= y <= rect_position_y + 100:
                    if player_number == 1:
                        player1_color = PLAYER_COLOR_OPTIONS[color_index]
                    elif player_number == 2:
                        player2_color = PLAYER_COLOR_OPTIONS[color_index]
            elif user_event.type == pygame.KEYDOWN and user_event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

def start_menu():
    while True:
        for user_event in pygame.event.get():
            if user_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif user_event.type == pygame.KEYDOWN and user_event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        check_keys = pygame.key.get_pressed()
        if check_keys[pygame.K_SPACE]:
            # Starts ball moving initially
            draw_game_elements()
            pygame.time.wait(2000)
            ball_speed_x_init = random.choice([-1, 1]) * BALL_SPEED
            ball_speed_y_init = random.uniform(-.2, .2) * BALL_SPEED
            break  # Exit the loop when SPACE is pressed
    return ball_speed_x_init, ball_speed_y_init
def check_exit_events():
    for user_event in pygame.event.get():
        if user_event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif user_event.type == pygame.KEYDOWN and user_event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
def clamp_player_position(y_position):
    # Ensure the player's position is within bounds
    if y_position < 42:
        return 42
    elif y_position > SCREEN_HEIGHT - PLAYER_HEIGHT:
        return SCREEN_HEIGHT - PLAYER_HEIGHT
    else:
        return y_position

def draw_game_elements():
    screen.fill((0, 0, 0))

    # Draw a solid line at y = 40
    pygame.draw.line(screen, (255, 255, 255), (0, 40), (SCREEN_WIDTH, 40), 2)

    # Draw players
    pygame.draw.rect(screen, player2_color, (player2_x, player2_y, PLAYER_WIDTH, PLAYER_HEIGHT), 0, 5)
    pygame.draw.rect(screen, player1_color, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT), 0, 5)

    # Draw player labels
    font_player_label = pygame.freetype.SysFont('lato-regular', 20, True)
    player1_label_text, _ = font_player_label.render(f"Player 1", player1_color)
    player2_label_text, _ = font_player_label.render(f"Player 2", player2_color)

    # Calculate the position for victories next to player names
    player1_label_rect = player1_label_text.get_rect(topleft=(10, 7))
    player2_label_rect = player2_label_text.get_rect(topright=(SCREEN_WIDTH - 10, 7))

    # Draw player labels
    screen.blit(player1_label_text, player1_label_rect.topleft)
    screen.blit(player2_label_text, player2_label_rect.topleft)

    # Draw victory balls next to player names
    for i in range(player1_victories):
        pygame.draw.circle(screen, player1_color, (player1_label_rect.right + i * (2 * BALL_RADIUS + 10) + 28, 22), BALL_RADIUS)

    for i in range(player2_victories):
        pygame.draw.circle(screen, player2_color, (player2_label_rect.left - (i + 1) * (2 * BALL_RADIUS + 10), 22), BALL_RADIUS)

    # Draw scores and centerline
    font = pygame.freetype.SysFont('lato-regular', 25, True)
    player1_score_text, _ = font.render(str(player_score), player1_color)
    player2_score_text, _ = font.render(str(player2_score), player2_color)
    player1_score_rect = player1_score_text.get_rect()
    player2_score_rect = player2_score_text.get_rect()
    centerline_x = SCREEN_WIDTH // 2
    player1_score_rect.topleft = (centerline_x - player1_score_rect.width - 10, 5)
    player2_score_rect.topleft = (centerline_x + 10, 5)
    screen.blit(player1_score_text, player1_score_rect)
    screen.blit(player2_score_text, player2_score_rect)

    # Draw centerline dashes
    dash_length = 10
    dash_gap = 5
    dash_y = 0
    while dash_y < SCREEN_HEIGHT:
        pygame.draw.line(screen, (255, 255, 255), (SCREEN_WIDTH // 2, dash_y), [SCREEN_WIDTH // 2, dash_y + dash_length])
        dash_y += dash_length + dash_gap

    # Draw ball
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), BALL_RADIUS)
    pygame.display.flip()

def move_players():
    global player_y, player2_y
    user_keys = pygame.key.get_pressed()

    # Player 2 movement (up and down arrow keys)
    if user_keys[pygame.K_UP] and player2_y > 0:
        player2_y -= player_speed
    if user_keys[pygame.K_DOWN] and player2_y < SCREEN_HEIGHT - PLAYER_HEIGHT:
        player2_y += player_speed

    # Player 1 movement (W and S keys)
    if user_keys[pygame.K_w] and player_y > 0:
        player_y -= player2_speed
    if user_keys[pygame.K_s] and player_y < SCREEN_HEIGHT - PLAYER_HEIGHT:
        player_y += player2_speed
def handle_collisions():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, player_x, player_y, player2_x, player2_y, ball_color, player1_color, player2_color

    # Collision with top wall
    if ball_y - BALL_RADIUS <= 40:
        ball_speed_y = abs(ball_speed_y)  # Reflect the ball downward

    # Collision with bottom wall
    elif ball_y + BALL_RADIUS >= SCREEN_HEIGHT:
        ball_speed_y = -abs(ball_speed_y)  # Reflect the ball upward

    # Collision with Player 1
    if (
        player_x <= ball_x + BALL_RADIUS - 20
        and player_x + PLAYER_WIDTH >= ball_x - BALL_RADIUS
        and player_y <= ball_y <= player_y + PLAYER_HEIGHT
    ):
        relative_intersect_y = (player_y + PLAYER_HEIGHT / 2) - ball_y
        normalized_intersect_y = relative_intersect_y / (PLAYER_HEIGHT / 2)

        # Varying ball angles by adding some randomness
        angle_variation = random.uniform(-math.pi / 14, math.pi / 14)
        angle = normalized_intersect_y * (2 * math.pi / 8) + angle_variation

        # Adjust ball speed based on the angle
        ball_speed_x = BALL_SPEED * math.cos(angle)
        ball_speed_y = BALL_SPEED * math.sin(angle)

        # Assigns a new color on collision
        ball_color = player1_color
    # Collision with Player 2
    elif (
        player2_x <= ball_x - BALL_RADIUS + 19
        and player2_x + PLAYER_WIDTH >= ball_x + BALL_RADIUS
        and player2_y <= ball_y <= player2_y + PLAYER_HEIGHT
    ):
        relative_intersect_y = (player2_y + PLAYER_HEIGHT / 2) - ball_y
        normalized_intersect_y = relative_intersect_y / (PLAYER_HEIGHT / 2)

        angle_variation = random.uniform(-math.pi / 10, math.pi / 10)
        angle = normalized_intersect_y * (2 * math.pi / 8) + angle_variation

        # Adjust ball speed based on the angle
        ball_speed_x = -BALL_SPEED * math.cos(angle)
        ball_speed_y = BALL_SPEED * math.sin(angle)

        # Assigns a new color on collision
        ball_color = player2_color

def handle_scoring_and_reset(player_score_param, player2_score_param):
    global ball_x, ball_y, ball_speed_x, ball_speed_y, player_y, player2_y, reset_time, ball_color

    # Handle scoring and ball + player reset
    if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= SCREEN_WIDTH:

        # Update scores
        if ball_speed_x < 0:
            player2_score_param += 1
        else:
            player_score_param += 1

        # Reset ball position and speed
        ball_color = (255, 255, 255)
        ball_x = SCREEN_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2
        ball_speed_x = 0
        ball_speed_y = 0
        reset_time = pygame.time.get_ticks()

        # Reset player positions
        player_y = SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2
        player2_y = SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2
    if ball_speed_x == 0:

        # Check if enough time has passed since the ball reset
        elapsed_time = pygame.time.get_ticks() - reset_time
        if elapsed_time >= 2000:

            # Set ball speed to start moving again
            ball_speed_x = random.choice([-1, 1]) * BALL_SPEED
            ball_speed_y = random.uniform(-.2, .2) * BALL_SPEED
    return player_score_param, player2_score_param

def display_victory_screen(winner_to_display):
    # Display victory screen
    font_victory = pygame.freetype.SysFont('lato-regular', 55, True)
    victory_text, _ = font_victory.render(f" {winner_to_display} wins!", (255, 255, 255))
    victory_text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 * 0.5))
    screen.blit(victory_text, victory_text_rect)
    pygame.display.flip()

def display_start_over_screen():
    # Display start-over screen
    screen.fill((0, 0, 0))
    font_menu = pygame.freetype.SysFont('lato-regular', 27, True)
    menu_text, _ = font_menu.render("Press N for a new game or Q to quit", (255, 255, 255))
    menu_text_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(menu_text, menu_text_rect)
    pygame.display.flip()
    
def handle_game_over():
    global running, player_score, player2_score, player1_color, player2_color, player1_victories, player2_victories
    winner = "Player 1" if player_score >= VICTORY_THRESHOLD else "Player 2"
    draw_game_elements()
    display_victory_screen(winner)
    pygame.time.wait(3000)

    # Check if it's the twelfth game
    if sequential_games_played % 12 == 0:
        # Reset victory counter after every twelfth game
        player1_victories = 0
        player2_victories = 0

    # Increment victories
    if winner == "Player 1":
        player1_victories += 1
    else:
        player2_victories += 1
    display_start_over_screen()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting_for_input = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    running = False
                    player_score = 0
                    player2_score = 0
                    player1_color = None
                    player2_color = None
                    initialize_game()
                    waiting_for_input = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    waiting_for_input = False

def main():
    global running, player_score, player2_score, player1_color, player2_color, player_y, player2_y, ball_x, ball_y

    # Initialize the game, pick colors, start menu
    initialize_game()

    while running:
        # Handle player exit with escape key or corner x
        check_exit_events()

        # Draws visual elements on screen
        draw_game_elements()

        # Allows movement of players with keys
        move_players()

        # Clamp player positions/prevent out of bounds
        player_y = clamp_player_position(player_y)
        player2_y = clamp_player_position(player2_y)

        # Move ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Handles collisions
        handle_collisions()

        # Updates score + resets players and ball
        player_score, player2_score = handle_scoring_and_reset(player_score, player2_score)

        # Handles game over
        if player_score >= VICTORY_THRESHOLD or player2_score >= VICTORY_THRESHOLD:
            handle_game_over()

# Main game loop
main()
