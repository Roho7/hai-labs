import pygame
import os
import time
import random
from movechecker import *

WIDTH, HEIGHT = 1080, 800
MARGIN = 50
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rummikub")
pygame.font.init()

sysfont = pygame.font.get_default_font()
print('system font :', sysfont)
t0 = time.time()
font = pygame.font.SysFont(None, 32)
error_font = pygame.font.SysFont(None, 100)

FPS = 60

BLACK = (64,64,64)
RED = (193,56, 13)
GREEN = (89,193,13)
BLUE = (10,50,200)
WHITE = (255,255,255)

BLOCK_IMG_RAW = pygame.image.load(os.path.join("Assets", "block.png"))
BLOCK_HEIGHT = 50
BLOCK_WIDTH = 90
BLOCK_IMG = pygame.transform.scale(BLOCK_IMG_RAW, (BLOCK_HEIGHT, BLOCK_WIDTH))

BLOCK_ARRAY = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
BLOCK_COLORS = [RED, GREEN, BLACK, BLUE]


all_tiles = []
player_tiles = []
opponent_tiles = []
def deal_table():
    for i in range(len(BLOCK_ARRAY)):
        for j in BLOCK_COLORS:
            all_tiles.append([i, j, str(i)+str(j)+"a"])
            all_tiles.append([i, j, str(i)+str(j)+"b"])
    random.shuffle(all_tiles)

    for i in range(14):
        player_tiles.append(all_tiles[i])
        all_tiles.remove(all_tiles[i])
    
    for i in range(14,28):
        opponent_tiles.append(all_tiles[i])
        all_tiles.remove(all_tiles[i])


deal_table()

class Button:
    def __init__(self, x, y, width, height, color, text, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        pygame.draw.rect(WIN, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        WIN.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def on_click(self, mouse_pos):
        print("button clicked")
        return self.rect.collidepoint(mouse_pos)
    


# DRAW BLOCKS
class Block:
    def __init__(self, x, y, key, number, color):
        self.rect = pygame.Rect(x, y, BLOCK_HEIGHT, BLOCK_WIDTH)
        self.key = key
        self.number = number
        self.x = x
        self.y = y
        self.original_x = x  # Store the original x position
        self.original_y = y
        self.color = color
        self.selected = False  # Added selected attribute

    def draw(self):
        WIN.blit(BLOCK_IMG, (self.x, self.y))
        NUMBER = font.render(str(self.number), True, self.color)
        text_rect = NUMBER.get_rect(center=self.rect.center)
        WIN.blit(NUMBER, text_rect)

    def play(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
        WIN.blit(BLOCK_IMG, (x, y))
        NUMBER = font.render(str(self.number), True, self.color)
        text_rect = NUMBER.get_rect(center=self.rect.center)
        WIN.blit(NUMBER, text_rect)
        # pygame.draw.circle(WIN, self.color, [x+40,y+80], 20, 20)

    def on_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.selected = not self.selected  # Toggle the selected attribute
            return True
        return False
    
    def reset_position(self):
        self.x = self.original_x
        self.y = self.original_y
        self.rect.topleft = (self.x, self.y)
            

# DRAW GAME WINDOW
def draw_window():
    WIN.fill((78, 48, 101))

class Error():
    def __init__(self, msg):
        self.msg = msg
    
    def draw(self):
        MSG = error_font.render(self.msg, True, WHITE)
        text_rect = MSG.get_rect(center=(WIDTH//2, HEIGHT//2))
        WIN.blit(MSG,text_rect)
        pygame.display.flip()
        pygame.time.delay(int(1 * 1000))

# APPEND TILES TO RENDER ARRAYS
def add_tiles_to_display(display_list):
    for i in range(len(player_tiles)):
        x = MARGIN + i * 50
        y = 500
        n, c = player_tiles[i][0], player_tiles[i][1]
        key = player_tiles[i][2]
        display_list.append(Block(x, y, key, n, c))

button = Button(0, 200, 100, 50, RED, "Draw", WHITE)
play_button = Button(WIDTH-100, 200, 100, 50, RED, "Play", WHITE)

def add_tiles_to_main_board(chosen_blocks, main_game_board):
    allowed = True
    block_sum = chosen_blocks[0][0]
    for i in range(len(chosen_blocks)-1):
        current_block = chosen_blocks[i]
        next_block = chosen_blocks[i+1]
        block_sum += next_block[0]
        if current_block[0] + 1 != next_block[0] and current_block[0] != next_block[0]:
            allowed = False
        else:
            print("linear")
    if block_sum < 30:
        allowed = False
    if allowed == True:
        main_game_board.extend([chosen_blocks])
        Error("NICE MOVE!").draw()
        print("allowed", main_game_board)
    else:
        print("illegal", block_sum)
        Error("WRONG MOVE!").draw()


def main():
    clock = pygame.time.Clock()
    run = True
    pool_draw_counter = 0
    deck_blocks_d = []
    chosen_blocks = []
    chosen_blocks_d = []
    main_game_board = []
    
    add_tiles_to_display(deck_blocks_d)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos
                    if button.is_clicked(mouse_pos):
                        pool_draw_counter +=1
                        player_tiles.append(all_tiles[0])
                        deck_blocks_d.append(Block(MARGIN + 50 * pool_draw_counter, 620, all_tiles[0][2], all_tiles[0][0], all_tiles[0][1]))
                        all_tiles.remove(all_tiles[0])
                        # print("chosen_blocks_d", chosen_blocks_d)
                        # print("deck_blocks_d", deck_blocks_d)
                        # print("all tiles", all_tiles)
                    if play_button.is_clicked(mouse_pos):
                        add_tiles_to_main_board(chosen_blocks, main_game_board)
                    for block in deck_blocks_d + chosen_blocks_d:
                        if block.on_click(mouse_pos):
                            if block.key in [b.key for b in deck_blocks_d]: # if block is present in deck_blocks_d array 
                                chosen_blocks.extend([player_tile for player_tile in player_tiles if player_tile[2] == block.key]) # add to the main board
                                deck_blocks_d = [b for b in deck_blocks_d if b.key != block.key]
                                # deck_blocks_d.remove(block) # remove from deck
                                chosen_blocks_d.append(block)
                                print(chosen_blocks)
                            elif block.key in [p.key for p in chosen_blocks_d]: # if block is on the board
                                to_remove = [player_tile for player_tile in chosen_blocks if player_tile[2] == block.key]
                                for element in to_remove:
                                    chosen_blocks.remove(element) # remove from main board list
                                # chosen_blocks_d.remove(block) # remove from the board display
                                chosen_blocks_d = [p for p in chosen_blocks_d if p.key != block.key]
                                deck_blocks_d.append(block)
                                print(chosen_blocks)
                                block.reset_position()

        # RENDER OTHER ELEMENTS
        draw_window()
        button.draw()
        play_button.draw()
        for block in deck_blocks_d:
            block.draw()
        for i, block in enumerate(chosen_blocks_d):
            if i >= 4:
                x = i * WIDTH//10 + 40
            else:
                x = i * WIDTH//10
            y = 300
            block.play(x, y)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
