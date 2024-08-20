import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and font
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)  # Define the RED color properly

# Paddle and Ball settings
PADDLE_WIDTH = 10
PADDLE_HEIGHT = int(100 * 0.7)  # Reduce paddle height by 30%
BALL_RADIUS = 7
paddle_speed = int(7 * 1.25)  # Increase paddle speed by 25%
base_ball_speed = 7

# Initialize player paddles and ball
left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Game state variables
game_active = False
entering_name = False
selecting_speed = False
main_menu_active = True  # Start with the main menu
viewing_instructions = False
viewing_leaderboard = False
current_speed = 1
winner_name = ""
winner = None
left_hits, right_hits = 0, 0
left_score, right_score = 0, 0
max_hits = 5  # Number of goals in a row to win
max_score = 10  # Maximum score to win

# Leaderboard
leaderboards = {1: [], 2: [], 3: [], 4: [], 5: []}  # Separate leaderboards for each speed

# Timer
start_time = None
time_to_win = None

# Ball velocity
ball_dx, ball_dy = 0, 0  # Initialize velocities

# Clock
clock = pygame.time.Clock()

def reset_game_state():
    global left_hits, right_hits, left_score, right_score, game_active, entering_name, winner_name, winner, start_time
    left_hits, right_hits = 0, 0
    left_score, right_score = 0, 0
    game_active = False
    entering_name = False
    winner_name = ""
    winner = None
    start_time = None
    reset_ball(randomize_direction=True)

def handle_text_input(event, current_text):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            current_text = current_text[:-1]  # Remove last character
        elif event.key == pygame.K_RETURN:
            return current_text, True  # Indicate that text input is complete
        elif event.unicode.isprintable():
            current_text += event.unicode  # Add typed character
    return current_text, False

def draw_text_input(screen, text, font, rect):
    # Draw a background box for better visibility
    pygame.draw.rect(screen, DARK_GRAY, rect)
    # Render and display the text
    text_surface = font.render(text + '_', True, WHITE)
    screen.blit(text_surface, (rect.x + 5, rect.y + 5))
    pygame.display.update(rect)  # Only update the text area

def reset_ball(randomize_direction=True):
    global ball_dx, ball_dy
    ball.center = (WIDTH // 2, HEIGHT // 2)
    
    if randomize_direction:
        # Randomize the direction of the ball
        ball_dx = base_ball_speed if random.choice([True, False]) else -base_ball_speed
        ball_dy = base_ball_speed if random.choice([True, False]) else -base_ball_speed

def check_goal_conditions():
    global left_hits, right_hits, left_score, right_score, game_active, winner, time_to_win, start_time
    
    if ball.left <= 0:  # Right player scores
        right_score += 1
        right_hits += 1
        left_hits = 0
        reset_ball()
    elif ball.right >= WIDTH:  # Left player scores
        left_score += 1
        left_hits += 1
        right_hits = 0
        reset_ball()

    if left_hits >= max_hits or left_score >= max_score:
        game_active = False
        winner = 1
        time_to_win = time.time() - start_time
        show_end_game_screen(winner)
    elif right_hits >= max_hits or right_score >= max_score:
        game_active = False
        winner = 2
        time_to_win = time.time() - start_time
        show_end_game_screen(winner)

def show_end_game_screen(winner):
    global entering_name, winner_name
    screen.fill(BLACK)
    winner_text = font_large.render(f"Player {winner} Wins!", True, WHITE)
    winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(winner_text, winner_rect)
    
    prompt_text = font_small.render("Enter your name:", True, WHITE)
    prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(prompt_text, prompt_rect)
    
    # Background box for the name input
    name_box_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    pygame.draw.rect(screen, DARK_GRAY, name_box_rect)
    
    name_text = font_small.render(winner_name + "_", True, WHITE)
    name_rect = name_text.get_rect(center=name_box_rect.center)
    screen.blit(name_text, name_rect)
    
    pygame.display.flip()
    entering_name = True

def update_leaderboard(name, time_to_win, speed):
    leaderboards[speed].append((name, time_to_win))
    leaderboards[speed].sort(key=lambda x: x[1])  # Sort by time taken to win
    reset_game_state()  # Reset the game state after saving to leaderboard

def show_main_menu():
    screen.fill(BLACK)
    title_text = font_large.render("Pong Game", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)
    
    start_game_text = font_small.render("1. Start Game", True, WHITE)
    start_game_rect = start_game_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(start_game_text, start_game_rect)
    
    view_instructions_text = font_small.render("2. Instructions", True, WHITE)
    view_instructions_rect = view_instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(view_instructions_text, view_instructions_rect)
    
    view_leaderboard_text = font_small.render("3. View Leaderboard", True, WHITE)
    view_leaderboard_rect = view_leaderboard_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(view_leaderboard_text, view_leaderboard_rect)
    
    pygame.display.flip()

def show_instructions():
    screen.fill(BLACK)
    instructions_title_text = font_large.render("Instructions", True, WHITE)
    instructions_title_rect = instructions_title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(instructions_title_text, instructions_title_rect)
    
    instructions = [
        "Player 1: W (up) and S (down)",
        "Player 2: UP and DOWN arrow keys",
        "First to reach 10 points wins or 5 consecutive goals wins"
    ]
    
    for i, line in enumerate(instructions):
        instruction_text = font_small.render(line, True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 40))
        screen.blit(instruction_text, instruction_rect)
    
    return_text = font_small.render("Press ESC to return to main menu", True, RED)
    return_rect = return_text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    screen.blit(return_text, return_rect)
    
    pygame.display.flip()

def show_leaderboard(selected_speed):
    screen.fill(BLACK)
    title_text = font_large.render(f"Leaderboard (Speed {selected_speed})", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)
    
    leaderboard = leaderboards[selected_speed]
    for i, (name, time_to_win) in enumerate(leaderboard):
        entry_text = font_small.render(f"{i + 1}. {name} - {time_to_win:.2f} seconds", True, WHITE)
        entry_rect = entry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 40))
        screen.blit(entry_text, entry_rect)
    
    clear_text = font_small.render("Press C to clear leaderboard", True, RED)
    clear_rect = clear_text.get_rect(center=(WIDTH // 2, HEIGHT - 80))
    screen.blit(clear_text, clear_rect)
    
    return_text = font_small.render("Press ESC to return to main menu", True, RED)
    return_rect = return_text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    screen.blit(return_text, return_rect)
    
    pygame.display.flip()

def countdown():
    screen.fill(BLACK)
    for i in range(3, 0, -1):
        countdown_text = font_large.render(str(i), True, WHITE)
        countdown_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.fill(BLACK)
        screen.blit(countdown_text, countdown_rect)
        pygame.display.flip()
        time.sleep(1)
    go_text = font_large.render("GO!", True, WHITE)
    go_rect = go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill(BLACK)
    screen.blit(go_text, go_rect)
    pygame.display.flip()
    time.sleep(1)

def select_speed():
    global selecting_speed, current_speed, ball_speed
    selecting_speed = True
    screen.fill(BLACK)
    speed_text = font_large.render("Select Game Speed (1-5)", True, WHITE)
    speed_rect = speed_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(speed_text, speed_rect)
    
    for i in range(1, 6):
        speed_option_text = font_small.render(f"{i}. Speed Level {i}", True, WHITE)
        speed_option_rect = speed_option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100 + i * 50))
        screen.blit(speed_option_text, speed_option_rect)
    
    pygame.display.flip()
    
    speed_selected = False
    while not speed_selected:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    current_speed = event.key - pygame.K_0
                    ball_speed = base_ball_speed * (1 + (current_speed - 1) * 0.15)
                    selecting_speed = False
                    speed_selected = True
                    print(f"Selected speed level {current_speed}, ball speed: {ball_speed}")  # Debugging output
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if entering_name:
            winner_name, complete = handle_text_input(event, winner_name)
            if complete:
                update_leaderboard(winner_name, time_to_win, current_speed)
                entering_name = False
                main_menu_active = True
            draw_text_input(screen, winner_name, font_small, pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50))

        if main_menu_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    reset_game_state()  # Reset game state when starting a new game
                    print("Starting speed selection...")  # Debugging output
                    select_speed()  # Ask for speed before starting the game
                    countdown()  # Show countdown before starting the game
                    reset_ball(randomize_direction=True)
                    game_active = True
                    main_menu_active = False
                    start_time = time.time()  # Start the timer
                    print("Game started...")  # Debugging output
                elif event.key == pygame.K_2:
                    viewing_instructions = True
                    main_menu_active = False
                elif event.key == pygame.K_3:
                    viewing_leaderboard = True
                    main_menu_active = False

        if viewing_instructions or viewing_leaderboard:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu_active = True
                    viewing_instructions = False
                    viewing_leaderboard = False
                elif viewing_leaderboard and pygame.K_1 <= event.key <= pygame.K_5:
                    show_leaderboard(event.key - pygame.K_0)  # Show leaderboard for selected speed level
                elif viewing_leaderboard and event.key == pygame.K_c:
                    leaderboards[current_speed].clear()

    if game_active:
        check_goal_conditions()

        ball.x += ball_dx
        ball.y += ball_dy

        # Ball collision with top/bottom walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        # Ball collision with paddles
        if ball.colliderect(left_paddle):
            ball_dx *= -1
        elif ball.colliderect(right_paddle):
            ball_dx *= -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += paddle_speed

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Display hits and scores
        left_hits_text = font_small.render(f"Hits in a row: {left_hits}", True, WHITE)
        screen.blit(left_hits_text, (WIDTH // 4 - 50, 20))
        right_hits_text = font_small.render(f"Hits in a row: {right_hits}", True, WHITE)
        screen.blit(right_hits_text, (WIDTH * 3 // 4 - 50, 20))
        left_score_text = font_small.render(f"Score: {left_score}", True, WHITE)
        screen.blit(left_score_text, (WIDTH // 4 - 50, 60))
        right_score_text = font_small.render(f"Score: {right_score}", True, WHITE)
        screen.blit(right_score_text, (WIDTH * 3 // 4 - 50, 60))

        pygame.display.flip()

    if main_menu_active:
        show_main_menu()

    if viewing_instructions:
        show_instructions()

    if viewing_leaderboard:
        show_leaderboard(current_speed)

    clock.tick(60)
