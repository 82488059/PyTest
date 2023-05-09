import pygame
import random
import math
import time
import heapq

pygame.init()

# 定义界面大小
screen = pygame.display.set_mode((800, 600))

# 定义图形的大小
grid_size = 20
grid_width = screen.get_width() // grid_size
grid_height = screen.get_height() // grid_size

# 定义颜色
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# 随机生成障碍物
def random_obstacles(num):
    obstacles = set()
    while len(obstacles) < num:
        x = random.randint(0, grid_width - 1)
        y = random.randint(0, grid_height - 1)
        obstacles.add((x, y))
    return obstacles


# 计算两个节点间的距离
def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


# 计算每个点到目标的距离
def heuristic(a, b):
    return distance(a, b)


# A*算法搜索过程
def astar(start, goal, obstacles):
    closed_set = set()
    open_set = [(0, start)]
    came_from = {}

    g_score = {}  # 记录从起点到每个点的距离
    g_score[start] = 0
    f_score = {}  # 记录每个点的估价函数值
    f_score[start] = heuristic(start, goal)

    while len(open_set) > 0:
        # 获取距离目标最近的节点
        current = heapq.heappop(open_set)[1]

        # 如果当前节点是目标节点
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        # 加入闭合集合
        closed_set.add(current)

        # 遍历相邻节点
        for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = current[0] + x, current[1] + y

            # 如果邻居节点已经处理过了或者有障碍物
            if neighbor in closed_set or neighbor in obstacles:
                continue

            tentative_g_score = g_score[current] + distance(current, neighbor)
            if neighbor not in open_set or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in open_set:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # 将搜索过程图形缓存到内存中
        for node in closed_set:
            pygame.draw.rect(background, RED, (node[0] * grid_size, node[1] * grid_size, grid_size, grid_size))
        for node in open_set:
            pygame.draw.rect(background, GRAY, (node[1][0] * grid_size, node[1][1] * grid_size, grid_size, grid_size))

        # 绘制起点、终点和障碍物
        pygame.draw.rect(background, GREEN, (start[0] * grid_size, start[1] * grid_size, grid_size, grid_size))
        pygame.draw.rect(background, BLUE, (goal[0] * grid_size, goal[1] * grid_size, grid_size, grid_size))
        for obstacle in obstacles:
            pygame.draw.rect(background, BLACK, (obstacle[0] * grid_size, obstacle[1] * grid_size, grid_size, grid_size))

        # 标记搜索路径
        if current != start:
            pygame.draw.rect(background, GREEN, (current[0] * grid_size, current[1] * grid_size, grid_size, grid_size))

        # 更新屏幕显示
        screen.blit(background, (0, 0))
        pygame.display.update()

    return None


# 画网格线
def draw_grid():
    for x in range(0, screen.get_width(), grid_size):
        pygame.draw.line(background, BLACK, (x, 0), (x, screen.get_height()))
    for y in range(0, screen.get_height(), grid_size):
        pygame.draw.line(background, BLACK, (0, y), (screen.get_width(), y))


# 画路径
def draw_path(path):
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        pygame.draw.line(screen, GREEN,
                         (start[0] * grid_size + grid_size // 2, start[1] * grid_size + grid_size // 2),
                         (end[0] * grid_size + grid_size // 2, end[1] * grid_size + grid_size // 2), 5)
    pygame.draw.rect(screen, RED, (path[-1][0] * grid_size, path[-1][1] * grid_size, grid_size, grid_size))


# 随机生成起点和终点
start = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
goal = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))

obstacles = random_obstacles(150)  # 随机生成150个障碍物

background = pygame.Surface(screen.get_size())  # 构建背景
background.fill(WHITE)

draw_grid()  # 画网格线
pygame.draw.rect(background, GREEN, (start[0] * grid_size, start[1] * grid_size, grid_size, grid_size))  # 画起点
pygame.draw.rect(background, BLUE, (goal[0] * grid_size, goal[1] * grid_size, grid_size, grid_size))  # 画终点
for obstacle in obstacles:
    pygame.draw.rect(background, BLACK, (obstacle[0] * grid_size, obstacle[1] * grid_size, grid_size, grid_size))  # 画障碍物
draw_path(astar(start, goal, obstacles))  # 画路径

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background, (0, 0))  # 绘制背景
    pygame.display.update()
