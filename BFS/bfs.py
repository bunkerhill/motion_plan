import copy

import pygame
import sys

pygame.init()

# Game Constants
SCREENX = 500
SCREENY = 500
SCREEN = pygame.display.set_mode((SCREENX, SCREENY))
pygame.display.set_caption('Breadth-First-Search Path-Finding Algorithm')

# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

N_grid_x = 15
N_grid_y = 15

grid_x_dim = SCREENX // N_grid_x
grid_y_dim = SCREENY // N_grid_y

def drawGrid():

    grid_width = 2

    grids = []
    for i in range(N_grid_x):
        for j in range(N_grid_y):
            grids.append(pygame.Rect(i*grid_x_dim, j*grid_y_dim, grid_x_dim, grid_y_dim))
    for grid in grids:
        pygame.draw.rect(SCREEN, BLACK, grid, grid_width)
    rows = N_grid_y
    cols = N_grid_x
    search_graph = [[-1 for i in range(cols)] for j in range(rows)]
    return search_graph


def drawStart():
    i = 1
    j = 2
    start_grid = pygame.Rect(i*grid_x_dim, j*grid_y_dim, grid_x_dim, grid_y_dim)
    pygame.draw.rect(SCREEN, RED, start_grid)
    row_pos = j
    col_pos = i
    return [row_pos, col_pos]

def drawGoal():
    i = 6
    j = N_grid_y-1
    goal_grid = pygame.Rect(i*grid_x_dim, j*grid_y_dim, grid_x_dim, grid_y_dim)
    pygame.draw.rect(SCREEN, BLUE, goal_grid)
    row_pos = j
    col_pos = i
    return [row_pos, col_pos]


class BFS:
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.n_row = len(self.graph)
        self.n_col = len(self.graph[0])
        self.back_trace_row = [[-2 for i in range(self.n_col)] for j in range(self.n_row)]
        self.back_trace_col = [[-2 for i in range(self.n_col)] for j in range(self.n_row)]
        self.success = False
        self.path = []
        self.font = pygame.font.SysFont('Arial', 25)


    def findPath(self):
        queue = []
        queue.append(self.start)
        self.graph[self.start[0]][self.start[1]] = 0
        # mark as visited

        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        while queue:
            length = len(queue)
            for i in range(length):
                curr_node = queue.pop(0)
                if curr_node[0] == self.goal[0] and curr_node[1] == self.goal[1]:
                    self.success = True
                    return True
                else:
                    for dir in directions:
                        next_node = [curr_node[0]+dir[0], curr_node[1]+dir[1]]
                        if next_node[0] >= 0 and next_node[0] < self.n_row and next_node[1]>=0 and next_node[1] < self.n_col and self.graph[next_node[0]][next_node[1]] == -1:
                            queue.append(next_node)
                            self.graph[next_node[0]][next_node[1]] = self.graph[curr_node[0]][curr_node[1]]+1
                            self.back_trace_row[next_node[0]][next_node[1]] = -dir[0]
                            self.back_trace_col[next_node[0]][next_node[1]] = -dir[1]
        self.success = False
        return False

    def printStep(self):
        grid_x_dim = SCREENX // N_grid_x
        grid_y_dim = SCREENY // N_grid_y
        for i in range(self.n_row):
            for j in range(self.n_col):
                SCREEN.blit(self.font.render( str(self.graph[i][j]), True, BLACK), (j*grid_x_dim, i*grid_y_dim))
        # pygame.display.update()

    def drawPath(self):
        if self.success:
            curr_node = self.goal
            self.path.append(copy.deepcopy(curr_node))
            while not (curr_node[0]==self.start[0] and curr_node[1]==self.start[1]):
                x = curr_node[0] + self.back_trace_row[curr_node[0]][curr_node[1]]
                y = curr_node[1] + self.back_trace_col[curr_node[0]][curr_node[1]]
                curr_node[0] = x
                curr_node[1] = y
                self.path.append(copy.deepcopy(curr_node))
            for step in self.path:
                i = step[1]
                j = step[0]
                SCREEN.blit(self.font.render(str(self.graph[j][i]), True, GREEN), (i * grid_x_dim, j * grid_y_dim))









while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    SCREEN.fill(WHITE)
    search_graph = drawGrid()
    start_pos = drawStart()
    goal_pos = drawGoal()

    kbd = pygame.key.get_pressed()
    if kbd[pygame.K_SPACE]:
        bfs = BFS(search_graph, start_pos, goal_pos)
        success = bfs.findPath()
        print(success)
        bfs.printStep()
        bfs.drawPath()
        pygame.time.wait(300)
    pygame.display.update()
