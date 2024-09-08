import pygame
import random

pygame.init()
width = 1000
height = 650
screen = pygame.display.set_mode((width, height))
Clock  = pygame.time.Clock()
running = True



BLUE = (0,0,255)
NAVY = (0,0,128)
WHITE = (255,255,255)
LIME =  (0,255,0)
CYAN = (0,255,255)
OLIVE = (128,128,0)
TEAL = (0,128,128)
MAROON = (128,0,0)
RED = (255,0,0)
colors = [BLUE,NAVY,WHITE,LIME,CYAN,OLIVE,TEAL,MAROON,RED]

grid_width = 10
grid_height = 20

block_size = 30

grid_x = (width - grid_width * block_size)//2
grid_y = height - grid_height * block_size - 20

shapes = [
    [[1, 1, 1, 1]],
    [[1, 1],[1,1]],
    [[1,1,1],[0,1,0]],
    [[1,1,1],[1,0,0]],
    [[1,1,1],[0,0,1]],
    [[1,1,0],[0,1,1]],
    [[0,1,1],[1,1,0]]]

class block:
    def __init__(self):
        self.shape = random.choice(shapes)
        self.color = colors[shapes.index(self.shape)]
        self.x  = grid_width // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move(self,dx,dy):
        self.x += dx
        self.y += dy

        
    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

def draw_grid():
    for x in range(grid_width):
        for y in range(grid_height):
            pygame.draw.rect(screen, WHITE, (grid_x + x * block_size, grid_y + y * block_size, block_size, block_size),1)

def draw_tetromino(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetromino.color,(grid_x + (tetromino.x + x) * block_size, 
                                                          grid_y + (tetromino.y + y) * block_size,
                                                          block_size, block_size))




def check_collision(tetromino, dx=0,dy=0):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                if (tetromino.x + x + dx < 0 or
                    tetromino.x + x + dx >= grid_width or 
                    tetromino.y + y + dy >= grid_height or
                    grid[tetromino.y + y + dy][tetromino.x + x + dx]):
                    return True
    return False

grid = [
    [0 for _ in range(grid_width)] for _ in range(grid_height)
    ]

current_tetromino = block()

fall_time = 0
fall_speed = 0.5

while running:
    fall_time += Clock.get_rawtime()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("left")
                if not check_collision(current_tetromino, dx=-1):
                    current_tetromino.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                if not check_collision(current_tetromino, dx=1):
                    current_tetromino.move(1, 0)
            elif event.key == pygame.K_DOWN:
                if not check_collision(current_tetromino, dy=1):
                    current_tetromino.move(0, 1)
            elif event.key == pygame.K_UP:
                current_tetromino.rotate()
                if check_collision(current_tetromino):
                    current_tetromino.rotate()

    if fall_time / 1000 > fall_speed:
        fall_time = 0
        if not check_collision(current_tetromino, dy=1):
            current_tetromino.move(0, 1)
        else:
            for y, row in enumerate(current_tetromino, shape):
                for x, cell in enumerate(row):
                    if cell:
                        grid[current_tetromino.y + y][current_tetromino.x + x] = current_tetromino.color
        
        current_tetromino = Tetromino()

        if check_collision(current_tetromino):
            running = False
            
        
        
    screen.fill("black")
    draw_grid()
    draw_tetromino(current_tetromino)

    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            if color:
                pygame.draw.rect(screen, color, (grid_x + x * block_size, grid_y + y * block_size, block_size, block_size))
    pygame.display.flip()
    Clock.tick(120)
pygame.quit()