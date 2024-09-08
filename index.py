import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Cài đặt kích thước cửa sổ
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")




# Định nghĩa các màu sắc sử dụng trong game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Kích thước của mỗi ô vuông trong lưới
block_size = 30

# Kích thước của lưới chơi (số ô)
grid_width = 10
grid_height = 20

# Tính toán vị trí của lưới chơi trên màn hình
grid_x = (width - grid_width * block_size) // 2
grid_y = height - grid_height * block_size - 20

# Định nghĩa các hình dạng Tetromino
# Mỗi hình dạng là một mảng 2D biểu diễn khối
shapes = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# Màu sắc tương ứng cho mỗi hình dạng
colors = [CYAN, YELLOW, MAGENTA, RED, GREEN, BLUE, ORANGE]

# Lớp Tetromino đại diện cho một khối đang rơi
class Tetromino:
    def __init__(self):
        self.shape = random.choice(shapes)
        self.color = colors[shapes.index(self.shape)]
        
        # Đặt khối ở giữa trên cùng của lưới
        self.x = grid_width // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move(self, dx, dy):
        # Di chuyển khối
        self.x += dx
        self.y += dy

    def rotate(self):
        # Xoay khối 90 độ theo chiều kim đồng hồ
        self.shape = list(zip(*self.shape[::-1]))

# Hàm vẽ lưới chơi
def draw_grid():
    for x in range(grid_width):
        for y in range(grid_height):
            pygame.draw.rect(screen, WHITE, (grid_x + x * block_size, grid_y + y * block_size, block_size, block_size), 1)

# Hàm vẽ Tetromino
def draw_tetromino(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetromino.color, (grid_x + (tetromino.x + x) * block_size, 
                                                           grid_y + (tetromino.y + y) * block_size, 
                                                           block_size, block_size))

# Hàm kiểm tra va chạm
def check_collision(tetromino, dx=0, dy=0):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                # Kiểm tra va chạm với biên và các khối đã cố định
                if (tetromino.x + x + dx < 0 or 
                    tetromino.x + x + dx >= grid_width or 
                    tetromino.y + y + dy >= grid_height or 
                    grid[tetromino.y + y + dy][tetromino.x + x + dx]):
                    return True
    return False

# Khởi tạo lưới chơi trống
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

# Tạo Tetromino đầu tiên
current_tetromino = Tetromino()

# Biến điều khiển game
clock = pygame.time.Clock()
# fall_time = 0
# fall_speed = 0.5  # Thời gian (giây) giữa mỗi lần rơi tự động

# Vòng lặp chính của game
running = True
while running:
    fall_time += clock.get_rawtime()
    clock.tick()

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Di chuyển sang trái nếu không va chạm
                if not check_collision(current_tetromino, dx=-1):
                    current_tetromino.move(-1, 0)
            if event.key == pygame.K_RIGHT:
                # Di chuyển sang phải nếu không va chạm
                if not check_collision(current_tetromino, dx=1):
                    current_tetromino.move(1, 0)
            if event.key == pygame.K_DOWN:
                # Di chuyển xuống nếu không va chạm
                if not check_collision(current_tetromino, dy=1):
                    current_tetromino.move(0, 1)
            if event.key == pygame.K_UP:
                # Xoay khối, nếu va chạm thì xoay lại
                current_tetromino.rotate()
                if check_collision(current_tetromino):
                    current_tetromino.rotate()
                    current_tetromino.rotate()
                    current_tetromino.rotate()

    # Di chuyển Tetromino xuống tự động
    if fall_time / 1000 > fall_speed:
        fall_time = 0
        if not check_collision(current_tetromino, dy=1):
            current_tetromino.move(0, 1)
        else:
            # Cố định Tetromino vào lưới
            for y, row in enumerate(current_tetromino.shape):
                for x, cell in enumerate(row):
                    if cell:
                        grid[current_tetromino.y + y][current_tetromino.x + x] = current_tetromino.color

            # Tạo Tetromino mới
            current_tetromino = Tetromino()

            # Kiểm tra game over
            if check_collision(current_tetromino):
                running = False

    # Xóa các hàng đã hoàn thành
    full_rows = [i for i, row in enumerate(grid) if all(row)]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [0 for _ in range(grid_width)])

    # Vẽ màn hình
    screen.fill(BLACK)
    draw_grid()
    draw_tetromino(current_tetromino)

    # Vẽ các khối đã cố định
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            if color:
                pygame.draw.rect(screen, color, (grid_x + x * block_size, grid_y + y * block_size, block_size, block_size))

    pygame.display.flip()

# Kết thúc Pygame
pygame.quit()