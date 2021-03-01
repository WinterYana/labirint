import pygame
import sys
import random

number_of_cells = 20
pygame.init()
screen_size = HEIGHT, WIDTH = 576, 576
screen = pygame.display.set_mode(screen_size)
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)
FPS = 60


def start_screen():
    fon = pygame.image.load('data/fon.png')
    screen.blit(fon, (24, 24))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def generate_field():
    matrix = [['#' for _ in range(11)] for _ in range(11)]
    start_x = random.randint(0, 11 // 2 - 1) * 2
    start_y = 0
    stack = [(start_x, start_y)]
    while len(stack) > 0:
        x, y = stack.pop(-1)
        neightbors = []
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx = x + dx
            ny = y + dy
            if nx < 0 or nx >= 11:
                continue
            if ny < 0 or ny >= 11:
                continue
            if matrix[y + dy // 2][x + dx // 2] == '#' and matrix[y + dy][x + dx] == '#':
                neightbors.append((dx, dy))
        if len(neightbors) > 0:
            dx, dy = random.choice(neightbors)
            stack.append((x, y))
            stack.append((x + dx, y + dy))
            matrix[y + dy // 2][x + dx // 2] = '.'
            matrix[y + dy][x + dx] = '.'
    return matrix, (start_x, start_y), (random.randint(0, 11 // 2 - 1) * 2, 10)


def new_level():
    return []


class Level:
    def __init__(self, screen):
        self.screen = screen
        self.matrix, self.character_coords, self.exit_coords = generate_field()
        self.time = 0

    def update(self):
        background_objects = pygame.sprite.Group()
        player = pygame.sprite.Group()

        for y in range(11):
            for x in range(11):
                coords = (x, y)
                element = self.matrix[y][x]
                if coords == self.character_coords:
                    Objects(coords, '@', player)
                    Objects(coords, '.', background_objects)
                elif coords == self.exit_coords:
                    Objects(coords, 'r', background_objects)
                else:
                    Objects(coords, element, background_objects)

        f = pygame.font.SysFont('serif', 16)
        text = f.render(f'Таймер: {str(self.time)}', False, (0, 180, 0))
        self.screen.blit(text, (0, 0))
        background_objects.draw(self.screen)
        player.draw(self.screen)

    def move(self, coords_of_move):
        new_coords = (self.character_coords[0] + coords_of_move[0],
                      self.character_coords[1] + coords_of_move[1])
        if self.next_cell(new_coords):
            self.character_coords = new_coords

    def next_cell(self, coords):
        if not (0 <= coords[0] < 11) or not (0 <= coords[1] < 11) or self.matrix[coords[1]][coords[0]] == '#':
            return False
        return True

    def is_it_over(self):
        if self.character_coords == self.exit_coords:
            return True
        return False

    def timer(self, time):
        self.time = time


class Objects(pygame.sprite.Sprite):
    def __init__(self, coord, element, group):
        super().__init__()
        sprites = {'.': pygame.transform.scale(pygame.image.load('data/grass.png'), (48, 48)),
                   '#': pygame.transform.scale(pygame.image.load('data/ground.png'), (48, 48)),
                   '@': pygame.transform.scale(pygame.image.load('data/cat.png'), (48, 48)),
                   'r': pygame.transform.scale(pygame.image.load('data/red.png'), (48, 48))}
        self.image = sprites[element]
        self.rect = self.image.get_rect(topleft=(coord[0] * 48 + 24, coord[1] * 48 + 24))
        group.add(self)


level = Level(screen)
time = 0
start_screen()
level.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                level.move([1, 0])
            elif event.key == pygame.K_LEFT:
                level.move([-1, 0])
            elif event.key == pygame.K_UP:
                level.move([0, -1])
            elif event.key == pygame.K_DOWN:
                level.move([0, 1])
            if level.is_it_over():
                level = Level(screen)
                time = 0
                level.update()
        elif event.type == pygame.USEREVENT:
            time += 1
    level.timer(time)
    screen.fill((0, 0, 0))
    level.update()
    pygame.display.update()