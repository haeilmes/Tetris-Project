import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main
from pygame import surface

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.init()
pygame.font.init()
pygame.mixer.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

game_display = pygame.display.set_mode((s_width, s_height))

background_image = pygame.image.load('media/tetrisbg.png')

# SHAPE FORMATS

S = [['......',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def music():
    pygame.mixer.music.load('media\Tetris.mp3')
    pygame.mixer.music.play(-1)

def menu_music():
    pygame.mixer.music.load('media\menumusic.mp3')
    pygame.mixer.music.play(-1)


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText


def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("media\TETRIS.TTF", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))

def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

def previous_score(pscore):
    with open('lastscore.txt', 'w') as f:
        f.write(str(pscore))

def update_score(nscore):
    score = max_score()

    with open('highscore.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def show_last_score():
    with open('lastscore.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

def max_score():
    with open('highscore.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score


def draw_next_shape(shape, surface):
    font = pygame.font.Font('media\gamefont.ttf', 30)
    label = font.render("Next Shape", 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 ((sx + j * block_size), (sy + i * block_size), block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 25))


def draw_window(surface, grid, score=0, last_score=0, pscore=0):
    font = pygame.font.Font('media\gamefont.ttf', 80)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(background_image, [-1,0])
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 15))


    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 255, 255), (top_left_x + 1, top_left_y, play_width, play_height), 4)

    font = pygame.font.Font('media\gamefont.ttf', 30)
    label = font.render("score:" + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    pygame.draw.rect(surface, (255, 255, 255), (sx + 1, sy - 28, 138, 188), 0)
    pygame.draw.rect(surface, (0, 0, 0), (sx + 5, sy - 25, 130, 182), 0)

    surface.blit(label, (sx + 10, sy + 130))

    font = pygame.font.Font('media\gamefont.ttf', 30)
    label = font.render("High Score:" + str(last_score), 1, (255, 255, 255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    pygame.draw.rect(surface, (255, 255, 255), (sx - 20, sy + 125, 215, 74), 0)
    pygame.draw.rect(surface, (0, 0, 0), (sx - 17, sy + 128, 208, 68), 0)

    surface.blit(label, (sx - 15, sy + 130))

    font = pygame.font.Font('media\gamefont.ttf', 30)
    label = font.render("Previous Score:" + str(pscore), 1, (255, 255, 255))

    surface.blit(label, (sx - 15, sy + 160))

    draw_grid(surface, grid)

def draw_menu_window(surface):
    sx = play_width/2
    sy = play_height/2
    surface.blit(background_image, [-1,0])
    pygame.draw.rect(surface, (255, 255, 255), (sx+167, sy-3, 166, 116), 0)
    pygame.draw.rect(surface, (0, 0, 0), (sx+172, sy+2, 156, 106), 0)

def main(win):
    last_score = max_score()
    pscore = show_last_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    falling = False
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.3
    level_time = 0
    score = 0
    music()
    while run:

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.03

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                main_menu(win)
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_SPACE:
                    falling = True
                    while falling:
                        current_piece.y += 1
                        if not (valid_space(current_piece, grid)):
                            falling = False
                            current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    main_menu(win)

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, last_score, pscore)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "GAME OVER", 80, (255, 0, 0))
            pygame.display.update()
            pygame.time.delay(3000)
            update_score(score)
            previous_score(score)
            main_menu(win)
            run = False


def main_menu(win):
    run = True
    selected = "start"
    draw_menu_window(win)
    menu_music()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        main(win)
                    if selected == "quit":
                        pygame.quit()

        title = text_format("TETRIS", 'media\gamefont.ttf', 50, (255, 255, 255))
        if selected == "start":
            text_start = text_format("START", 'media\gamefont.ttf', 45, (255, 255, 255))
        else:
            text_start = text_format("START", 'media\gamefont.ttf', 45, (128, 128, 128))
        if selected == "quit":
            text_quit = text_format("QUIT", 'media\gamefont.ttf', 45, (255, 255, 255))
        else:
            text_quit = text_format("QUIT", 'media\gamefont.ttf', 45, (128, 128, 128))

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        game_display.blit(title, (s_width / 2 - (title_rect[2] / 2), 80))
        game_display.blit(text_start, (s_width / 2 - (start_rect[2] / 2), 300))
        game_display.blit(text_quit, (s_width / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()


win = pygame.display.set_mode((s_width, s_height))

pygame.display.set_caption("Tetris")
main_menu(win)
