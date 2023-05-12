import pygame
import random

# 定义游戏界面常量
GRID_SIZE = 20
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
NUM_COLS = WINDOW_WIDTH // GRID_SIZE
NUM_ROWS = WINDOW_HEIGHT // GRID_SIZE

# 定义游戏状态变量和颜色
GAME_OVER = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCORE = 0

# 定义吃豆人的初始位置
PLAYER_POSITION = [NUM_COLS//2, NUM_ROWS//2]

# 定义豆子的分数
BEAN_SCORE = 10

# 定义障碍物列表和豆子列表
OBSTACLES = [(2, 2), (5, 5), (8, 8)]
BEANS = [(1, 1), (2, 3), (4, 4), (5, 7), (8, 6), (9, 3)]

# 初始化 Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("吃豆人游戏")
clock = pygame.time.Clock()

# 加载吃豆人和豆子的图像
PLAYER_IMAGE = pygame.image.load("player.png")
BEAN_IMAGE = pygame.image.load("bean.png")

def check_collision(player_position):
    global GAME_OVER, SCORE
    if player_position[0] < 0 or player_position[0] >= NUM_COLS:
        GAME_OVER = True
    elif player_position[1] < 0 or player_position[1] >= NUM_ROWS:
        GAME_OVER = True
    elif player_position in OBSTACLES:
        GAME_OVER = True
    elif player_position in BEANS:
        SCORE += BEAN_SCORE
        BEANS.remove(player_position)
    if len(BEANS) == 0:
        GAME_OVER = True
    return GAME_OVER

def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, WHITE, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, WHITE, (0, y), (WINDOW_WIDTH, y))

pygame.init()

# 创建游戏窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("吃豆人游戏")

# 设置游戏时钟
clock = pygame.time.Clock()

while not GAME_OVER:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_OVER = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER_POSITION[1] -= 1
            elif event.key == pygame.K_DOWN:
                PLAYER_POSITION[1] += 1
            elif event.key == pygame.K_LEFT:
                PLAYER_POSITION[0] -= 1
            elif event.key == pygame.K_RIGHT:
                PLAYER_POSITION[0] += 1
                
    # 检查碰撞
    if check_collision(PLAYER_POSITION):
        GAME_OVER = True
                
    # 绘制游戏界面
    window.fill(BLACK)
    
    # 绘制边界
    pygame.draw.rect(window, WHITE, (0, 0, WINDOW_WIDTH, GRID_SIZE))
    pygame.draw.rect(window, WHITE, (0, 0, GRID_SIZE, WINDOW_HEIGHT))
    pygame.draw.rect(window, WHITE, (0, WINDOW_HEIGHT - GRID_SIZE, WINDOW_WIDTH, GRID_SIZE))
    pygame.draw.rect(window, WHITE, (WINDOW_WIDTH - GRID_SIZE, 0, GRID_SIZE, WINDOW_HEIGHT))
    
    # 绘制障碍物和豆子
    for obstacle in OBSTACLES:
        pygame.draw.rect(window, WHITE, (obstacle[0]*GRID_SIZE, obstacle[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for bean in BEANS:
        window.blit(BEAN_IMAGE, (bean[0]*GRID_SIZE, bean[1]*GRID_SIZE))
       
    # 绘制吃豆人
    window.blit(PLAYER_IMAGE, (PLAYER_POSITION[0]*GRID_SIZE, PLAYER_POSITION[1]*GRID_SIZE))
    
    # 显示得分
    score_text = pygame.font.SysFont(None, 36).render("得分: {}".format(SCORE), True, WHITE)
    window.blit(score_text, (10, 10))
    
    # 更新屏幕
    pygame.display.update()
    
    # 控制帧率
    clock.tick(10)

# 游戏结束，退出 Pygame
pygame.quit()
