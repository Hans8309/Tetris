import tkinter as tk
import random
from tkinter import messagebox

# ---------------------------------------------------
# 引入pygame模块，只是为了添加音效
import pygame
# 初始化
pygame.init()
# 添加游戏背景音乐
pygame.mixer.music.load('music.ogg')
pygame.mixer.music.play(-1)  # -1参数值为单曲循环
# 添加音效，快速落地声，消除整行声，游戏结束声
sound_settle = pygame.mixer.Sound('settle.ogg')
sound_clear = pygame.mixer.Sound('clear.ogg')
sound_lose = pygame.mixer.Sound('lose.ogg')
# ---------------------------------------------------

cell_size = 30  # 每个小方块的边长大小，单位为像素
C = 12    # 游戏界面宽度，单位为方块数量
R = 20    # 游戏界面的高度，单位为方块数量
height = R * cell_size    # 游戏界面宽度，单位为像素jkjk
width = C * cell_size    # 游戏界面的高度，单位为像素

# 定义各种形状
# 每个形状的中心坐标为(0,0)
SHAPES = {
    "O": [(-1, -1), (0, -1), (-1, 0), (0, 0)],
    "S": [(-1, 0), (0, 0), (0, -1), (1, -1)],
    "T": [(-1, 0), (0, 0), (0, -1), (1, 0)],
    "I": [(0, 1), (0, 0), (0, -1), (0, -2)],
    "L": [(-1, 0), (0, 0), (-1, -1), (-1, -2)],
    "J": [(-1, 0), (0, 0), (0, -1), (0, -2)],
    "Z": [(-1, -1), (0, -1), (0, 0), (1, 0)],
}

# 定义各种形状的颜色
SHAPESCOLOR = {
    "O": "blue",
    "S": "red",
    "T": "yellow",
    "I": "green",
    "L": "purple",
    "J": "orange",
    "Z": "Cyan",
}


def draw_cell_by_cr(canvas, c, r, color="#000000"):
    """
    :param canvas: 画板，用于绘制一个方块的Canvas对象
    :param c: 方块所在列
    :param r: 方块所在行
    :param color: 方块颜色，默认为#CCCCCC，轻灰色
    :return:
    """
    x0 = c * cell_size
    y0 = r * cell_size
    x1 = c * cell_size + cell_size
    y1 = r * cell_size + cell_size
    canvas.create_rectangle(x0, y0, x1, y1, fill=color,
                            outline="#000000", width=1)
    # canvas.create_rectangle(x0+5, y0+5, x1-5, y1-5, fill=color,
                            # outline="#000000", width=2)

# 绘制面板上的每一个格子


def draw_board(canvas, block_list):
    for ri in range(R):
        for ci in range(C):
            cell_type = block_list[ri][ci]
            if cell_type:
                draw_cell_by_cr(canvas, ci, ri, SHAPESCOLOR[cell_type])
            else:
                draw_cell_by_cr(canvas, ci, ri)


def draw_cells(canvas, c, r, cell_list, color="#000000"):
    """
    绘制指定形状指定颜色的俄罗斯方块
    :param canvas: 画板
    :param r: 该形状设定的原点所在的行
    :param c: 该形状设定的原点所在的列
    :param cell_list: 该形状各个方格相对自身所处位置
    :param color: 该形状颜色
    :return:
    """
    for cell in cell_list:
        cell_c, cell_r = cell
        ci = cell_c + c
        ri = cell_r + r
        # 判断该位置方格在画板内部(画板外部的方格不再绘制)
        if 0 <= c < C and 0 <= r < R:
            draw_cell_by_cr(canvas, ci, ri, color)


win = tk.Tk()
# canvas = tk.Canvas(win, width=width, height=height)
canvas = tk.Canvas(win, width=600, height=height)
canvas.pack()

# 把窗体显示在屏幕的中间
winPositionX = (win.winfo_screenwidth()-width)/2
winPositionY = (win.winfo_screenheight()-height)/2
win.geometry("+%d+%d" % (winPositionX, winPositionY))

score = 0
win.title("SCORES: %s" % score)  # 标题中展示分数

# 这个block_list全局变量存储每个格子的状态
block_list = []
for i in range(R):
    i_row = ['' for j in range(C)]
    block_list.append(i_row)

draw_board(canvas, block_list)


# 当一个形状移动后，重新绘制面板
def draw_block_move(canvas, block, direction=[0, 0]):
    """
    绘制向指定方向移动后的俄罗斯方块
    :param canvas: 画板
    :param block: 俄罗斯方块对象
    :param direction: 俄罗斯方块移动方向
    :return:
    """
    shape_type = block['kind']
    c, r = block['cr']
    cell_list = block['cell_list']

    # 移动前，先清除原有位置绘制的俄罗斯方块,也就是用背景色绘制原有的俄罗斯方块
    draw_cells(canvas, c, r, cell_list)

    dc, dr = direction
    new_c, new_r = c+dc, r+dr
    block['cr'] = [new_c, new_r]
    # 在新位置绘制新的俄罗斯方块就好
    draw_cells(canvas, new_c, new_r, cell_list, SHAPESCOLOR[shape_type])


# 记录存储整个面板中格子的状态
def save_block_to_list(block):
    shape_type = block['kind']
    cc, cr = block['cr']
    cell_list = block['cell_list']

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc
        r = cell_r + cr
        # block_list 在对应位置记下其类型
        block_list[r][c] = shape_type


# 左右移动形状
def horizontal_move_block(event):
    """
    左右水平移动俄罗斯方块
    """
    direction = [0, 0]
    if event.keysym == 'Left':
        direction = [-1, 0]
    elif event.keysym == 'Right':
        direction = [1, 0]
    else:
        return

    global current_block
    if current_block is not None and check_move(current_block, direction):
        draw_block_move(canvas, current_block, direction)


def generate_new_block():
    # 随机生成新的俄罗斯方块

    kind = random.choice(list(SHAPES.keys()))
    # 对应横纵坐标，以左上角为原点，水平向右为x轴正方向，
    # 竖直向下为y轴正方向，x对应横坐标，y对应纵坐标
    cr = [C // 2, 0]
    new_block = {
        'kind': kind,  # 对应俄罗斯方块的类型
        'cell_list': SHAPES[kind],
        'cr': cr
    }

    return new_block


def check_move(block, direction=[0, 0]):
    """
        判断俄罗斯方块是否可以朝制定方向移动
        :param block: 俄罗斯方块对象
        :param direction: 俄罗斯方块移动方向
        :return: boolean 是否可以朝制定方向移动
        """
    cc, cr = block['cr']
    cell_list = block['cell_list']

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc + direction[0]
        r = cell_r + cr + direction[1]
        # 判断该位置是否超出左右边界，以及下边界
        # 一般不判断上边界，因为俄罗斯方块生成的时候，可能有一部分在上边界之上还没有出来
        if c < 0 or c >= C or r >= R:
            return False

        # 必须要判断r不小于0才行，具体原因你可以不加这个判断，试试会出现什么效果
        if r >= 0 and block_list[r][c]:
            return False
    return True


# 检测整行是否全部填满各种形状
def check_row_complete(row):
    for cell in row:
        if cell == '':
            return False
    return True


# 检测是不是有整行被填满，可以消除
def check_and_clear():
    has_complete_row = False
    for ri in range(len(block_list)):
        if check_row_complete(block_list[ri]):
            has_complete_row = True
            # 当前行可消除
            if ri > 0:
                for cur_ri in range(ri, 0, -1):
                    block_list[cur_ri] = block_list[cur_ri-1][:]
                block_list[0] = ['' for j in range(C)]
            else:
                block_list[ri] = ['' for j in range(C)]
            global score
            score += 10
            sound_clear.play()

    if has_complete_row:
        draw_board(canvas, block_list)

        win.title("SCORES: %s" % score)


# 旋转当前形状
def rotate_block(event):
    global current_block
    if current_block is None:
        return

    cell_list = current_block['cell_list']
    rotate_list = []
    for cell in cell_list:
        cell_c, cell_r = cell
        rotate_cell = [cell_r, -cell_c]
        rotate_list.append(rotate_cell)

    block_after_rotate = {
        'kind': current_block['kind'],  # 对应俄罗斯方块的类型
        'cell_list': rotate_list,
        'cr': current_block['cr']
    }

    if check_move(block_after_rotate):
        cc, cr = current_block['cr']
        draw_cells(canvas, cc, cr, current_block['cell_list'])
        draw_cells(canvas, cc, cr, rotate_list,
                   SHAPESCOLOR[current_block['kind']])
        current_block = block_after_rotate


# 快速降落当前形状
def land(event):
    global current_block
    if current_block is None:
        return

    cell_list = current_block['cell_list']
    cc, cr = current_block['cr']
    min_height = R
    for cell in cell_list:
        cell_c, cell_r = cell
        c, r = cell_c + cc, cell_r + cr
        if block_list[r][c]:
            return
        h = 0
        for ri in range(r+1, R):
            if block_list[ri][c]:
                break
            else:
                h += 1
        if h < min_height:
            min_height = h

    down = [0, min_height]
    if check_move(current_block, down):
        draw_block_move(canvas, current_block, down)
        sound_settle.play()


# 控制游戏速度，形状自动降落的时间间隔
FPS = 200
# ---------------------------------


def game_loop():
    win.update()
    global current_block
    if current_block is None:
        new_block = generate_new_block()
        # 新生成的俄罗斯方块需要先在生成位置绘制出来
        draw_block_move(canvas, new_block)
        current_block = new_block
        if not check_move(current_block, [0, 0]):
            sound_lose.play()
            messagebox.showinfo("Game Over!", "Your Score is %s" % score)
            win.destroy()
            return
    else:
        if check_move(current_block, [0, 1]):
            draw_block_move(canvas, current_block, [0, 1])
        else:
            # 无法移动，记入 block_list 中
            save_block_to_list(current_block)
            current_block = None
            check_and_clear()

    # import time
    # print(time.ctime())
    win.after(FPS, game_loop)


canvas.focus_set()  # 聚焦到canvas画板对象上
canvas.bind("<KeyPress-Left>", horizontal_move_block)
canvas.bind("<KeyPress-Right>", horizontal_move_block)
canvas.bind("<KeyPress-Up>", rotate_block)
# canvas.bind("<KeyPress-Down>", land)
canvas.bind("<KeyPress-space>", land)

current_block = None

game_loop()
win.mainloop()
