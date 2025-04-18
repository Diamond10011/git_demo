import pygame
import random
import asyncio
import platform
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 600
HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# Snake class
class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1

    def get_head(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[2:]:
            return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize()

    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

snake = Snake()
food = Food()
running = True
game_over = False
start_time = time.time()
survival_time = 0

# Button properties
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
font = pygame.font.SysFont(None, 36)

def setup():
    global snake, food, running, game_over, start_time
    snake = Snake()
    food = Food()
    running = True
    game_over = False
    start_time = time.time()
    screen.fill(BLACK)

def draw_button():
    pygame.draw.rect(screen, GRAY, button_rect)
    text = font.render("Play Again", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

def update_loop():
    global running, snake, food, game_over, survival_time
    
    if game_over:
        # Handle game over screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    setup()  # Restart game
        return

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, 1):
                snake.direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                snake.direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                snake.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                snake.direction = (1, 0)

    # Update snake
    if not snake.update():
        survival_time = time.time() - start_time
        game_over = True

    # Check for food collision
    if snake.get_head() == food.position:
        snake.length += 1
        food.randomize()

    # Draw
    screen.fill(BLACK)
    if game_over:
        # Draw game over screen
        time_text = font.render(f"Time Survived: {survival_time:.1f} seconds", True, WHITE)
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(time_text, time_rect)
        draw_button()
    else:
        # Draw snake
        for pos in snake.positions:
            pygame.draw.rect(screen, GREEN, 
                           (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2))
        # Draw food
        pygame.draw.rect(screen, RED, 
                        (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2))
    
    pygame.display.flip()

async def main():
    setup()
    while running:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())