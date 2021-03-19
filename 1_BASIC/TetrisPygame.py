# https://www.bilibili.com/video/BV13k4y1r7JE?from=search&seid=9751224032757141306
# https://youtu.be/zfvxp7PgQ6c?list=PLWKjhJtqVAbnqBxcdjVGgT3uVR10bzTEB
# Full Code: https://pastebin.com/embed_js/yaWTeF6y
# 在原作者基础上增加分数显示，音效

import pygame
import random

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

# pygame.font.init()
pygame.init()
# 添加游戏背景音乐
pygame.mixer.music.load('music.ogg')
#pygame.mixer.music.play(-1)  # -1参数值为单曲循环
# 添加音效，快速落地声，消除整行声，游戏结束声
sound_settle = pygame.mixer.Sound('settle.ogg')
sound_clear = pygame.mixer.Sound('clear.ogg')
sound_lose = pygame.mixer.Sound('lose.ogg')
sound_rotate = pygame.mixer.Sound('rotate.wav')
sound_shift = pygame.mixer.Sound('shift.wav')
# ---------------------------------------------------
# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per blo ck
block_size = 30

# 方块出现区域的左上原点的x,y坐标
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# scores 游戏得分
scores = 0

# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
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
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
                (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape

class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3


def draw_text_middle(text, size, color, surface):
    # font = pygame.font.SysFont('comicsans', size, bold=True)
    font = pygame.font.SysFont('SimHei', size, bold=True)    #SimHei可以显示中文

    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2),
                         top_left_y + play_height/2 - label.get_height()/2))


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    # 根据每个方块的旋转方向，其中一个形状
    format = shape.shape[shape.rotation % len(shape.shape)]
    # print(shape.shape)
    # print(format)
    for i, line in enumerate(format):
        # print(line)
        row = list(line)    # line 为形状的每一行，row将line.00..转化成列表形式['.', '0', '0', '.', '.']
        # print(row)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    # print(positions)    # [(7, 1), (6, 2), (7, 2), (8, 2)]
    # 将位置坐标的x坐标减2，y坐标减4，这样保证初始值在游戏框外，并且在中间
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    # print(positions)    # [(5, -3), (4, -2), (5, -2), (6, -2)]
    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(
        10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
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
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*30),
                         (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy),
                             (sx + j * 30, sy + play_height))  # vertical lines



def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one
    global scores
    inc = 0
    ind = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                    scores += inc
                except:
                    continue
    if inc > 0:
        sound_clear.play() 
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
        
         



def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface):
    surface.fill((0, 0, 0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
#    label = font.render('TETRIS', 1, (255, 255, 255))
    label = font.render('SCORES:'+str(scores), 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width /
                         2 - (label.get_width() / 2), 30))

    # rect(Surface, color, Rect, width=0)
    # 在 Surface  对象上绘制一个矩形。Rect 参数指定矩形的位置和尺寸。
    # width 参数指定边框的宽度，如果设置为 0 则表示填充该矩形。
    # 画出游戏格子中所有小方块，线宽0表示用颜色填充内部，填充颜色为grid[i][j]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    # draw grid and border
    # 画出游戏格子
    draw_grid(surface, 20, 10)
    # 画出游戏画面外框，宽度为5
    pygame.draw.rect(surface, (255, 100, 0), (top_left_x,
                                              top_left_y, play_width, play_height), 5)
    # 下面这行执行的话，下一个块的显示出现频闪
    # pygame.display.update()  


def main():
    global grid
     
    locked_positions = {}  # (x,y):(255,0,0) 记录累积的每个小方格的颜色，格式如：{(5, 16): (0, 255, 255), (5, 17): (0, 255, 255), (5, 18): (0, 255, 255), (5, 19): (0, 255, 255)}
    #grid 记录每个格子的颜色值(0,0,0),每行10组，共20行
    grid = create_grid(locked_positions)
    # print(grid)
    change_piece = False
    run = True
    current_piece = get_shape()    #返回一个随机的具体的对象
    # print(current_piece.shape)
    next_piece = get_shape()
    clock = pygame.time.Clock()
    
    fall_time = 0
    pygame.mixer.music.play(-1)  # -1参数值为单曲循环


    while run:
        fall_speed = 0.20   # 控制方块下降的速度0.2秒=200毫秒

        grid = create_grid(locked_positions)
        # print(grid)
        fall_time += clock.get_rawtime()    # 在上一个tick中使用的实际时间
        
        clock.tick()    # 更新时钟
        # PIECE FALLING CODE

        if fall_time/1000 >= fall_speed:    # 当时间大于设定的下降速度
            fall_time = 0
            current_piece.y += 1    # 让当前的方块的坐标y+1，就是下降一步
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sound_shift.play()
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    sound_shift.play()
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    sound_rotate.play()
                    current_piece.rotation = current_piece.rotation + \
                        1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - \
                            1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    sound_settle.play()
                    # print(convert_shape_format(current_piece))  # todo fix


        # 返回当前方块的各个小块的坐标值，如：[(5, -4), (5, -3), (5, -2), (5, -1)]
        # 初始值：各个小块的y坐标的最小值为-1
        shape_pos = convert_shape_format(current_piece)
        # print(current_piece.y)
        # print(shape_pos)
        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                # print(pos)
                print(p)
                locked_positions[p] = current_piece.color
            print(locked_positions)
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            clear_rows(grid, locked_positions)

        draw_window(win)

        draw_next_shape(next_piece, win)
        # print(grid)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False        
    pygame.mixer.music.stop()
    sound_lose.play()
    draw_text_middle("You Lost", 40, (0, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press any key to begin.', 48, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game
