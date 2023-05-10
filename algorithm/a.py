import random
import pygame

WIDTH = 40  # 迷宫宽度
HEIGHT = 20  # 迷宫高度
LAYERS = 5  # 迷宫层数

# 初始化迷宫地图
maze_map = [[[1 for _ in range(WIDTH)] for _ in range(HEIGHT)] for _ in range(LAYERS)]


def generate_maze(layer, x, y):
    # 标记当前位置为已经访问过
    maze_map[layer][x][y] = 0
    
    # 随机打乱四个方向的顺序
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(directions)
    
    # 挨个尝试四个方向
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT:
            continue  # 越界了，不能走
        if maze_map[layer][nx][ny] == 0:
            continue  # 已经访问过了，不能走

        # 打通两个格子之间的墙壁
        if dx == 1:
            maze_map[layer][x][y] &= 0b1110  # 当前格子右边的墙壁
            maze_map[layer][nx][ny] &= 0b1101  # 新的格子左边的墙壁
        elif dx == -1:
            maze_map[layer][x][y] &= 0b1101  # 当前格子左边的墙壁
            maze_map[layer][nx][ny] &= 0b1110  # 新的格子右边的墙壁
        elif dy == 1:
            maze_map[layer][x][y] &= 0b1011  # 当前格子下边的墙壁
            maze_map[layer][nx][ny] &= 0b1110  # 新的格子上边的墙壁
        elif dy == -1:
            maze_map[layer][x][y] &= 0b1110  # 当前格子上边的墙壁
            maze_map[layer][nx][ny] &= 0b1011  # 新的格子下边的墙壁

        generate_maze(layer, nx, ny)  # 递归访问新的格子


# 生成多层迷宫
for layer in range(LAYERS):
    # 随机选择一个起点
    start_x, start_y = random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)

    # 生成迷宫
    generate_maze(layer, start_x, start_y)


# 初始化Pygame窗口
BLOCK_SIZE = 20  # 方格尺寸
WIN_WIDTH = WIDTH * BLOCK_SIZE
WIN_HEIGHT = HEIGHT * BLOCK_SIZE

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT * LAYERS))

# 配置颜色和字体
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36
FONT = pygame.font.SysFont(None, FONT_SIZE)

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 清空屏幕
    screen.fill(WHITE)

    # 绘制迷宫
    for layer in range(LAYERS):
        for row in range(HEIGHT):
            for col in range(WIDTH):
                x = col * BLOCK_SIZE
                y = row * BLOCK_SIZE + layer * WIN_HEIGHT
                if maze_map[layer][col][row] & 0b1000:  # 上边的墙壁
                    pygame.draw.line(screen, BLACK, (x, y), (x+BLOCK_SIZE, y), 2)
                if maze_map[layer][col][row] & 0b0100:  # 下边的墙壁
                    pygame.draw.line(screen, BLACK, (x, y+BLOCK_SIZE), (x+BLOCK_SIZE, y+BLOCK_SIZE), 2)
                if maze_map[layer][col][row] & 0b0010:  # 右边的墙壁
                    pygame.draw.line(screen, BLACK, (x+BLOCK_SIZE, y), (x+BLOCK_SIZE, y+BLOCK_SIZE), 2)
                if maze_map[layer][col][row] & 0b0001:  # 左边的墙壁
                    pygame.draw.line(screen, BLACK, (x, y), (x, y+BLOCK_SIZE), 2)

    # 显示层数
    for layer in range(LAYERS):
        layer_text = FONT.render(f"Layer {layer+1}", True, BLACK)
        screen.blit(layer_text, (10, layer*WIN_HEIGHT))

    # 刷新界面
    pygame.display.flip()

# 退出程序
pygame.quit()