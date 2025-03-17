import pygame
import sys
import random
from button import Button

# Initialize Pygame
pygame.init()

# Game constants
WIDTH = 600
HEIGHT = 400
GRID_SIZE = 20
FPS = 7

# Visual settings
SNAKE_RADIUS = GRID_SIZE // 2
FOOD_RADIUS = GRID_SIZE // 2 - 2
SHINE_RADIUS = FOOD_RADIUS // 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)
GRID_COLOR = (40, 40, 40)
BUTTON_COLOR = (50, 120, 190)
BUTTON_HOVER_COLOR = (70, 140, 210)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()


def init_game():
    return [(WIDTH//2, HEIGHT//2)], (GRID_SIZE, 0), (
        random.randint(0, (WIDTH-GRID_SIZE)//GRID_SIZE) * GRID_SIZE,
        random.randint(0, (HEIGHT-GRID_SIZE)//GRID_SIZE) * GRID_SIZE
    ), 0


def show_menu():
    start_button = Button(WIDTH//2 - 100, HEIGHT//2 -
                          40, 200, 50, "Start Game")
    about_button = Button(WIDTH//2 - 100, HEIGHT//2 +
                          30, 200, 50, "About Game")

    while True:
        screen.fill(BLACK)
        title_font = pygame.font.SysFont(None, 72)
        title = title_font.render("Snake Game", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))

        start_button.draw(screen)
        about_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if start_button.handle_event(event):
                return "start"
            if about_button.handle_event(event):
                return "about"

        pygame.display.update()
        clock.tick(FPS)


def show_about():
    back_button = Button(WIDTH//2 - 100, HEIGHT - 80, 200, 50, "Back to Menu")
    about_text = [
        "Snake Game",
        "Control the snake using arrow keys.",
        "Eat the red food to grow longer.",
        "Avoid hitting walls and yourself.",
        "Try to achieve the highest score!",

    ]

    while True:
        screen.fill(BLACK)
        y = 80
        for i, line in enumerate(about_text):
            font_size = 48 if i == 0 else 32
            font = pygame.font.SysFont(None, font_size)
            text = font.render(line, True, WHITE if i > 0 else GREEN)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, y))
            y += 50

        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if back_button.handle_event(event):
                return "menu"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        pygame.display.update()
        clock.tick(FPS)


def show_game_over(score):
    play_again_button = Button(
        WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50, "Play Again")
    exit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 90, 200, 50, "Exit")

    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 48)
        text = font.render(f'Game Over! Score: {score}', True, RED)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))

        play_again_button.draw(screen)
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if play_again_button.handle_event(event):
                return "play_again"
            if exit_button.handle_event(event):
                return "quit"

        pygame.display.update()
        clock.tick(FPS)


def game_loop():
    snake, direction, food, score = init_game()
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_UP and direction != (0, GRID_SIZE):
                        direction = (0, -GRID_SIZE)
                    elif event.key == pygame.K_DOWN and direction != (0, -GRID_SIZE):
                        direction = (0, GRID_SIZE)
                    elif event.key == pygame.K_LEFT and direction != (GRID_SIZE, 0):
                        direction = (-GRID_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-GRID_SIZE, 0):
                        direction = (GRID_SIZE, 0)

        if paused:
            font = pygame.font.SysFont(None, 48)
            text = font.render('PAUSED', True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            pygame.display.update()
            continue

        # Move snake
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        # Check food consumption
        if snake[0] == food:
            score += 1
            food = (random.randint(0, (WIDTH-GRID_SIZE)//GRID_SIZE) * GRID_SIZE,
                    random.randint(0, (HEIGHT-GRID_SIZE)//GRID_SIZE) * GRID_SIZE)
        else:
            snake.pop()

        # Collision detection
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake[1:]):
            return "game_over", score

        # Clear screen
        screen.fill(BLACK)

        # Draw grid
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

        # Draw snake with gradient effect
        for i, segment in enumerate(snake):
            color = tuple(c1 + (c2 - c1) * (i / len(snake))
                          for c1, c2 in zip(LIGHT_GREEN, DARK_GREEN))
            x, y = segment[0] + SNAKE_RADIUS, segment[1] + SNAKE_RADIUS
            pygame.draw.circle(screen, color, (x, y), SNAKE_RADIUS)

        # Draw food (apple with shine)
        x, y = food[0] + FOOD_RADIUS + 2, food[1] + FOOD_RADIUS + 2
        pygame.draw.circle(screen, RED, (x, y), FOOD_RADIUS)
        # Add shine effect
        shine_pos = (x - FOOD_RADIUS//2, y - FOOD_RADIUS//2)
        pygame.draw.circle(screen, WHITE, shine_pos, SHINE_RADIUS)

        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

    return "quit", score


def main():
    while True:
        choice = show_menu()
        if choice == "quit":
            break
        elif choice == "about":
            if show_about() == "quit":
                break
        elif choice == "start":
            result, score = game_loop()
            if result == "quit":
                break
            elif result == "game_over":
                choice = show_game_over(score)
                if choice == "quit":
                    break
                elif choice != "play_again":
                    break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
