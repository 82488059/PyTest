import pygame

pygame.init()

# 窗口和游戏板块的大小
size = width, height = 600, 600
block_size = 50

screen = pygame.display.set_mode((800, 600))
# 颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# 游戏地图
map = [
    "wwwwwwwwww",
    "wt       w",
    "w   www  w",
    "w   wbw  w",
    "w   w    w",
    "w   www  w",
    "w        w",
    "wwwwwwwwww",
]

# 将地图转化为二维数组
game_map = []
for row in map:
    game_map.append(list(row))

# 初始化玩家和目标盒子的位置
player_pos = [1, 1]
box_pos = [3, 3]
target_pos = [3, 4]

# 将二维数组中的'w'转化为绘制墙壁所需的坐标
walls = []
for i in range(len(game_map)):
    for j in range(len(game_map[i])):
        if game_map[i][j] == 'w':
            walls.append(pygame.Rect(j * block_size, i * block_size, block_size, block_size))

# 绘制游戏对象
def draw():
    # 绘制背景
    screen.fill(white)
    # 绘制墙壁
    for wall in walls:
        pygame.draw.rect(screen, black, wall, 0)
    # 绘制目标盒子
    pygame.draw.rect(screen, green, (target_pos[1] * block_size, target_pos[0] * block_size, block_size, block_size), 0)
    # 绘制玩家
    pygame.draw.rect(screen, blue, (player_pos[1] * block_size, player_pos[0] * block_size, block_size, block_size), 0)
    # 绘制盒子
    pygame.draw.rect(screen, red, (box_pos[1] * block_size, box_pos[0] * block_size, block_size, block_size), 0)
    # 刷新屏幕
    pygame.display.update()

# 移动函数
def move_up():
    global player_pos, box_pos
    if game_map[player_pos[0] - 1][player_pos[1]] == ' ':
        player_pos[0] -= 1
    elif game_map[player_pos[0] - 1][player_pos[1]] == 'b':
        if game_map[box_pos[0] - 1][box_pos[1]] == ' ':
            player_pos[0] -= 1
            box_pos[0] -= 1
        elif game_map[box_pos[0] - 1][box_pos[1]] == 't':
            player_pos[0] -= 1
            box_pos[0] -= 1
            win()

def move_down():
    global player_pos, box_pos
    if game_map[player_pos[0] + 1][player_pos[1]] == ' ':
        player_pos[0] += 1
    elif game_map[player_pos[0] + 1][player_pos[1]] == 'b':
        if game_map[box_pos[0] + 1][box_pos[1]] == ' ':
            player_pos[0] += 1
            box_pos[0] += 1
        elif game_map[box_pos[0] + 1][box_pos[1]] == 't':
            player_pos[0] += 1
            box_pos[0] += 1
            win()

def move_left():
    global player_pos, box_pos
    if game_map[player_pos[0]][player_pos[1] - 1] == ' ':
        player_pos[1] -= 1
    elif game_map[player_pos[0]][player_pos[1] - 1] == 'b':
        if game_map[box_pos[0]][box_pos[1] - 1] == ' ':
            player_pos[1] -= 1
            box_pos[1] -= 1
        elif game_map[box_pos[0]][box_pos[1] - 1] == 't':
            player_pos[1] -= 1
            box_pos[1] -= 1
            win()

def move_right():
    global player_pos, box_pos
    if game_map[player_pos[0]][player_pos[1] + 1] == ' ':
        player_pos[1] += 1
    elif game_map[player_pos[0]][player_pos[1] + 1] == 'b':
        if game_map[box_pos[0]][box_pos[1] + 1] == ' ':
            player_pos[1] += 1
            box_pos[1] += 1
        elif game_map[box_pos[0]][box_pos[1] + 1] == 't':
            player_pos[1] += 1
            box_pos[1] += 1
            win()

# 获胜函数
def win():
    # 当所有盒子都在目标位置上时，游戏获胜
    for i in range(len(game_map)):
        for j in range(len(game_map[i])):
            if game_map[i][j] == 'b' and (i != target_pos[0] or j != target_pos[1]):
                return False
    print("You win!")
    pygame.quit()

# 创建窗口
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Push Box")

# 游戏循环
while True:
    # 处理游戏事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_up()
            elif event.key == pygame.K_DOWN:
                move_down()
            elif event.key == pygame.K_LEFT:
                move_left()
            elif event.key == pygame.K_RIGHT:
                move_right()

    # 绘制游戏对象
    draw()