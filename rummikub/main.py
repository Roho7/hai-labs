import pygame
import os
import time
import random
import copy
from movechecker import *

WIDTH, HEIGHT = 1080, 750
MARGIN = WIDTH//10
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
YELLOW = (177, 138, 1)
WHITE = (255,255,255)

BLOCK_IMG_RAW = pygame.image.load(os.path.join("Assets", "block.png"))
BLOCK_HEIGHT = 50
BLOCK_WIDTH = 90
BLOCK_IMG = pygame.transform.scale(BLOCK_IMG_RAW, (BLOCK_HEIGHT, BLOCK_WIDTH))

BLOCK_ARRAY = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
BLOCK_COLORS = [RED, GREEN, BLACK, BLUE, YELLOW]


all_tiles = []
player_tiles = []
opponent_tiles = []
def deal_table():
    for o, n in enumerate(BLOCK_ARRAY):
        for j in BLOCK_COLORS:
            all_tiles.append([n, j, str(n)+str(j)+"a"])
            all_tiles.append([n, j, str(n)+str(j)+"b"])
    random.shuffle(all_tiles)

    for i in range(14):
        player_tiles.append(all_tiles[i])
        all_tiles.remove(all_tiles[i])
    
    for j in range(14):
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

    # def on_click(self, mouse_pos):
    #     print("button clicked")
    #     return self.rect.collidepoint(mouse_pos)
    


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
        if self.selected:
            pygame.draw.rect(WIN, WHITE, self.rect, 2)
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

# DISPLAY MESSAGES 
class Messages():
    def __init__(self, msg):
        self.msg = msg
    
    def error(self):
        MSG = error_font.render(self.msg, True, WHITE)
        text_rect = MSG.get_rect(center=(WIDTH//2, HEIGHT//2))
        WIN.blit(MSG,text_rect)
        pygame.display.flip()
        pygame.time.delay(int(1 * 1000))
    
    def normal(self):
        MSG = font.render(self.msg, True, WHITE)
        text_rect = MSG.get_rect(center=(WIDTH//2, HEIGHT//6))
        WIN.blit(MSG,text_rect)
        pygame.display.flip()
        pygame.time.delay(int(1 * 1000))
    

class Opponent():
    def __init__(self, turn_count):
        self.blocks = opponent_tiles
        self.chosen_blocks = []
        self.move = 0
        self.return_list = []
    
    def sort_tiles(self):
        n = len(self.blocks)

        for i in range(n):
            for j in range(0, n - i - 1):
                if self.blocks[j][0] < self.blocks[j + 1][0]:
                    self.blocks[j], self.blocks[j + 1] = self.blocks[j + 1], self.blocks[j]
        return self.blocks

    def deal_tiles(self):
        self.chosen_blocks.clear()
        self.sort_tiles()
        max_sum = float('-inf')
        print("opponent is thinking")
        add_blocks = False
        for i in range(len(self.blocks)-2):
            if self.blocks[i][0] - 1 == self.blocks[i + 1][0] and self.blocks[i + 1][0] - 1 == self.blocks[i + 2][0] and str(self.blocks[i][1]) == str(self.blocks[i + 1][1]) and str(self.blocks[i + 1][1]) == str(self.blocks[i + 2][1]):
                add_blocks = True
            elif self.blocks[i][0] == self.blocks[i + 2][0] and self.blocks[i][0] == self.blocks[i + 1][0] and self.blocks[i + 1][0] == self.blocks[i + 2][0]:
                add_blocks = True
            else:
                add_blocks = False

            if add_blocks == True:
                current_sum = self.blocks[i][0] + self.blocks[i+1][0] + self.blocks[i+2][0]
                if current_sum > max_sum:
                    max_sum = current_sum
                    if max_sum < 30 and self.move == 0:
                        self.blocks.append(all_tiles[0])
                        all_tiles.remove(all_tiles[0])
                        self.chosen_blocks.clear()
                        print("drew cards")
                        Messages("Opponent drew tiles").normal()
                        return []
                    else:
                        self.chosen_blocks.append(self.blocks[i+2])
                        self.chosen_blocks.append(self.blocks[i+1])
                        self.chosen_blocks.append(self.blocks[i])
                        global opponent_tiles 
                        opponent_tiles = [block for block in opponent_tiles if block[2] not in [chosen_block[2] for chosen_block in self.chosen_blocks]]
                        self.move += 1
                        print("opponent played", self.blocks)
                        return self.chosen_blocks
            else:
                self.blocks.append(all_tiles[0])
                all_tiles.remove(all_tiles[0])
                self.chosen_blocks.clear()
                print("drew cards")
                Messages("Opponent drew tiles").normal()
                return []



# APPEND TILES TO RENDER ARRAYS
def add_tiles_to_display(logic_list, display_list, y_value, nested):
    inc = 0
    y_inner = 0
    if not nested:
        for i in range(len(logic_list)):
            x = MARGIN + i * 50
            y = y_value
            n, c = logic_list[i][0], logic_list[i][1]
            key = logic_list[i][2]
            display_list.append(Block(x, y, key, n, c))
    else:
        for b, j in enumerate(logic_list):
            if b%3 == 0 and b != 0:
                inc += 200
                y_inner = 0
            for i in range(len(j)):
                x = MARGIN + i * 50 + inc
                y = y_inner
                n, c = j[i][0], j[i][1]
                key = j[i][2]
                display_list.append(Block(x, y, key, n, c))
            y_inner += 100


button = Button(0, 200, 100, 50, RED, "Draw", WHITE)
play_button = Button(WIDTH-100, 200, 100, 50, RED, "Play", WHITE)
mod_button = Button(WIDTH-100, 300, 100, 50, RED, "Mod", WHITE)

def check_tiles(chosen_blocks, block_sum):
    allowed = True # Start with True
    for i in range(len(chosen_blocks)-1):
        current_block = chosen_blocks[i]
        next_block = chosen_blocks[i+1]
        block_sum += next_block[0]
        if not ((current_block[0] + 1 == next_block[0] and str(current_block[1]) == str(next_block[1])) or 
        (current_block[0] == next_block[0] and len([block[1] for block in chosen_blocks if str(block[1]) == str(current_block[1])]) == 1)):
            allowed = False
            print("illegal tile found", [block[1] for block in chosen_blocks if str(block[1]) == str(current_block[1])])
            break  # Break the loop as soon as a non-matching pair is found
    return allowed, block_sum


def add_tiles_to_main_board(chosen_blocks, main_game_board, chosen_blocks_d, turn_count):
    allowed = False
    # block_sum = 0

    # if chosen_blocks is not None:
    block_sum = chosen_blocks[0][0]
    allowed, block_sum = check_tiles(chosen_blocks, block_sum)
        
    if block_sum < 30 and turn_count < 1:
        allowed = False

    if allowed == True:
        main_game_board.extend([copy.deepcopy(chosen_blocks)])
        chosen_blocks.clear()
        chosen_blocks_d.clear()
        if turn_count%2 == 0:
            Messages("NICE MOVE!").error()
        else:
            Messages("OPPONENT PLAYED").error()
        pygame.display.update()
        print("allowed")
    else:
        if turn_count%2 == 0:
            Messages("WRONG MOVE!").error()
    return allowed

def modify_board(chosen_blocks, selected_list, main_game_board):
    # print(chosen_blocks)
    selected_list.extend(chosen_blocks)
    selected_list.sort(key=lambda x:x[0])
    print("selected list",selected_list)
    for i, block_list in enumerate(main_game_board):
        for block in block_list:
            if any(block[2] == new_block[2] for new_block in selected_list):
                main_game_board.pop(i)
                print("removed from main board", main_game_board)
                return selected_list

    return []


    # selected_list.sort(selected_list[1])



def main():
    clock = pygame.time.Clock()
    run = True
    pool_draw_counter = 0
    turn_count = 0
    deck_blocks_d = []
    chosen_blocks = []
    chosen_blocks_d = []
    main_game_board = []
    main_game_board_d = []
    selected_board_blocks = []

    add_tiles_to_display(player_tiles, deck_blocks_d, 500, False)

    while run:
        clock.tick(FPS)
        draw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos

# ========== DRAW BUTTON ============
                    if button.is_clicked(mouse_pos):
                        # drawing from pool
                        pool_draw_counter +=1
                        turn_count += 1
                        player_tiles.append(all_tiles[0])
                        deck_blocks_d.append(Block(MARGIN + 50 * pool_draw_counter, 610, all_tiles[0][2], all_tiles[0][0], all_tiles[0][1]))
                        all_tiles.remove(all_tiles[0])
                        # opponent move
                        opponent_blocks = Opponent(turn_count).deal_tiles()
                        if opponent_blocks:
                            if add_tiles_to_main_board(opponent_blocks, main_game_board, chosen_blocks_d, turn_count):
                                add_tiles_to_display(main_game_board, main_game_board_d, 0, True) 
                        turn_count += 1
                        print(turn_count)

# =========== PLAY BUTTON ===========
                    if play_button.is_clicked(mouse_pos):
                        if add_tiles_to_main_board(chosen_blocks, main_game_board, chosen_blocks_d, turn_count):
                            add_tiles_to_display(main_game_board, main_game_board_d, 0, True)  
                            turn_count += 1
                            opponent_blocks = Opponent(turn_count).deal_tiles()
                            if opponent_blocks:
                                print("opponent isn't empty", opponent_blocks)
                                if add_tiles_to_main_board(opponent_blocks, main_game_board, chosen_blocks_d, turn_count):
                                    add_tiles_to_display(main_game_board, main_game_board_d, 0, True)
                        turn_count += 1
                        print("MAIN BOARD", main_game_board)

# =========== BLOCK CLICKS ============
                    for block in deck_blocks_d + chosen_blocks_d:
                        if block.on_click(mouse_pos):
                            if block.key in [b.key for b in deck_blocks_d]: # if block is present in deck_blocks_d array 
                                chosen_blocks.extend([player_tile for player_tile in player_tiles if player_tile[2] == block.key]) # add to the main board
                                deck_blocks_d = [b for b in deck_blocks_d if b.key != block.key]
                                chosen_blocks_d.append(block)
                                # print(chosen_blocks)
                            elif block.key in [p.key for p in chosen_blocks_d]: # if block is on the board
                                to_remove = [player_tile for player_tile in chosen_blocks if player_tile[2] == block.key]
                                for element in to_remove:
                                    chosen_blocks.remove(element) # remove from main board list
                                chosen_blocks_d = [p for p in chosen_blocks_d if p.key != block.key]
                                deck_blocks_d.append(block)
                                # print(chosen_blocks)
                                block.reset_position()

# ========== MAIN BOARD CLICK ===================
                    for block in main_game_board_d:
                        if block.on_click(mouse_pos):
                            for block_data_list in main_game_board:
                                if any(block_data[2] == block.key for block_data in block_data_list):
                                    selected_board_blocks = block_data_list
                                    break
                            print("you clicked this", (selected_board_blocks))

# ========== MOD BUTTON CLICK ===================
                    if mod_button.is_clicked(mouse_pos):
                        new_mod_blocks = []
                        new_mod_blocks = modify_board(chosen_blocks, selected_board_blocks, main_game_board)
                        if new_mod_blocks != []:
                            if add_tiles_to_main_board(new_mod_blocks, main_game_board, chosen_blocks_d, turn_count):
                                add_tiles_to_display(main_game_board, main_game_board_d, 0, True)
                                turn_count += 1
                                opponent_blocks = Opponent(turn_count).deal_tiles()
                                if opponent_blocks:
                                    print("opponent isn't empty", opponent_blocks)
                                    if add_tiles_to_main_board(opponent_blocks, main_game_board, chosen_blocks_d, turn_count):
                                        add_tiles_to_display(main_game_board, main_game_board_d, 0, True)


        # RENDER OTHER ELEMENTS
        # draw_window()
        button.draw()
        play_button.draw()
        mod_button.draw()
        for block in deck_blocks_d:
            block.draw()
        for block in main_game_board_d:
            block.draw()
        for i, block in enumerate(chosen_blocks_d):
            if i >= 4:
                x = MARGIN + i * WIDTH//10 + 40
            else:
                x = MARGIN + i * WIDTH//10
            y = 350
            block.play(x, y)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
