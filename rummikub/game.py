import pygame
import sys

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
FPS = 60
FONT = pygame.font.Font(None, 36)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Display")

# Define function to render numbers at the bottom
def render_numbers(numbers):
    for i, number in enumerate(numbers):
        text = FONT.render(str(number), True, WHITE)
        x = i * (WIDTH // 5)
        y = HEIGHT - text.get_height()
        screen.blit(text, (x, y))

# Main game loop
clock = pygame.time.Clock()

numbers_at_bottom = [1, 2, 3, 4, 5]
selected_numbers = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            clicked_number = x // (WIDTH // 5) + 1

            if clicked_number in numbers_at_bottom:
                numbers_at_bottom.remove(clicked_number)
                selected_numbers.append(clicked_number)

    screen.fill(BLACK)

    # Render numbers at the bottom
    render_numbers(numbers_at_bottom)

    # Render selected numbers at the top
    for i, number in enumerate(selected_numbers):
        text = FONT.render(str(number), True, WHITE)
        x = i * (WIDTH // 5)
        y = 0
        screen.blit(text, (x, y))

    pygame.display.flip()
    clock.tick(FPS)
