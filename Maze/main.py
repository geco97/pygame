import pygame
import sys
import random
from collections import deque

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)  # Color for the flag
ROWS = SCREEN_HEIGHT // BLOCK_SIZE
COLS = SCREEN_WIDTH // BLOCK_SIZE

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

# Fonts
font = pygame.font.SysFont("Arial", 48, bold=True)
small_font = pygame.font.SysFont("Arial", 24)

def generate_maze(rows, cols):
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            maze[row][col] = 1 if random.random() > 0.3 else 0
    maze[1][1] = 1  # Starting position
    return maze

def get_random_goal(maze):
    while True:
        goal_x = random.randint(0, COLS - 1)
        goal_y = random.randint(0, ROWS - 1)
        if maze[goal_y][goal_x] == 1 and (goal_x != 1 or goal_y != 1):
            return goal_x, goal_y

def is_path_to_goal(maze, start_x, start_y, goal_x, goal_y):
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque([(start_x, start_y)])
    visited[start_y][start_x] = True
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        x, y = queue.popleft()
        if x == goal_x and y == goal_y:
            return True
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 1 and not visited[ny][nx]:
                visited[ny][nx] = True
                queue.append((nx, ny))
    return False

def draw_maze(maze):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            color = LIGHT_GRAY if maze[row][col] == 1 else DARK_GRAY
            pygame.draw.rect(screen, color, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            if maze[row][col] == 1:
                pygame.draw.rect(screen, WHITE, (col * BLOCK_SIZE + 2, row * BLOCK_SIZE + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))

def draw_player(x, y):
    pygame.draw.circle(screen, GREEN, 
                       (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2), 
                       BLOCK_SIZE // 2 - 4)
    pygame.draw.circle(screen, WHITE, 
                       (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2), 
                       BLOCK_SIZE // 2 - 6, 2)

def draw_goal(goal_x, goal_y):
    flag_pole_x = goal_x * BLOCK_SIZE + BLOCK_SIZE // 2
    flag_pole_y = goal_y * BLOCK_SIZE
    pygame.draw.line(screen, BLACK, (flag_pole_x, flag_pole_y), 
                     (flag_pole_x, flag_pole_y + BLOCK_SIZE - 5), 3)
    pygame.draw.polygon(screen, GOLD, [
        (flag_pole_x, flag_pole_y),
        (flag_pole_x + 10, flag_pole_y + 10),
        (flag_pole_x, flag_pole_y + 20)
    ])

def draw_coordinates(x, y):
    coordinates_text = small_font.render(f"X: {x}, Y: {y}", True, BLUE)
    screen.blit(coordinates_text, (10, 10))

def show_message(message):
    text = font.render(message, True, BLUE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def main():
    running = True
    while running:
        while True:
            maze = generate_maze(ROWS, COLS)
            player_x, player_y = 1, 1
            goal_x, goal_y = get_random_goal(maze)
            if is_path_to_goal(maze, player_x, player_y, goal_x, goal_y):
                break

        game_over = False
        clock = pygame.time.Clock()

        while not game_over:
            screen.fill(BLACK)
            draw_maze(maze)
            draw_player(player_x, player_y)
            draw_goal(goal_x, goal_y)
            draw_coordinates(player_x, player_y)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and player_y > 0 and maze[player_y - 1][player_x] == 1:
                player_y -= 1
            if keys[pygame.K_DOWN] and player_y < ROWS - 1 and maze[player_y + 1][player_x] == 1:
                player_y += 1
            if keys[pygame.K_LEFT] and player_x > 0 and maze[player_y][player_x - 1] == 1:
                player_x -= 1
            if keys[pygame.K_RIGHT] and player_x < COLS - 1 and maze[player_y][player_x + 1] == 1:
                player_x += 1

            if player_x == goal_x and player_y == goal_y:
                show_message("You Win!")
                pygame.time.wait(2000)
                game_over = True

            pygame.display.flip()
            clock.tick(30)

        while game_over:
            screen.fill(BLACK)
            show_message("Game Over! R to Restart, Q to Quit")
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_over = False
                        break
                    if event.key == pygame.K_q:
                        running = False
                        game_over = False

main()
