import pygame
import os
import time
import random

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rummikub")
pygame.font.init()

sysfont = pygame.font.get_default_font()
print('system font :', sysfont)
t0 = time.time()
font = pygame.font.SysFont(None, 48)

FPS = 60

BLACK = (64,64,64)
RED = (193,56, 13)
GREEN = (89,193,13)

BLOCK_IMG_RAW = pygame.image.load(os.path.join("Assets", "block.png"))
BLOCK_HEIGHT = 70
BLOCK_WIDTH = 110
BLOCK_IMG = pygame.transform.scale(BLOCK_IMG_RAW, (BLOCK_HEIGHT, BLOCK_WIDTH))

BLOCK_ARRAY = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
BLOCK_COLORS = [RED, GREEN, BLACK]


# DRAW BLOCKS
class Block:
    def __init__(self, x, y, number, color):
        self.rect = pygame.Rect(x, y, BLOCK_HEIGHT, BLOCK_WIDTH)
        self.number = number
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        WIN.blit(BLOCK_IMG, (self.x, self.y))
        NUMBER = font.render(str(self.number), True, (0, 0, 0))
        WIN.blit(NUMBER, (self.x + 30, self.y + 20))
        pygame.draw.circle(WIN, self.color, [self.x+40,self.y+80], 20, 20)

    def on_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


def draw_table():
    x = 100
    y = 100
    for i in range(14):
        n = random.choice(BLOCK_ARRAY)
        block = Block(x, y, n)
        block.draw()
        x += 50


# DRAW GAME WINDOW
def draw_window():
    WIN.fill((78, 48, 101))


def main():
    clock = pygame.time.Clock()
    run = True
    blocks = []

    for i in range(14):
        x = 0 + i * 70
        y = 500
        n = random.choice(BLOCK_ARRAY)
        c = random.choice(BLOCK_COLORS)
        blocks.append(Block(x, y, n, c))

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos
                    for block in blocks:
                        if block.on_click(mouse_pos):
                            print(f"Block {block.number} clicked!")

        draw_window()
        for block in blocks:
            block.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
