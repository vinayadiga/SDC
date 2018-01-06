import pdb
from helpers import normalize, blur

def initialize_beliefs(grid):
    height = len(grid)
    width = len(grid[0])
    area = height * width
    belief_per_cell = 1.0 / area
    beliefs = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(belief_per_cell)
        beliefs.append(row)
    return beliefs

def sense(color, grid, beliefs, p_hit, p_miss):
    new_beliefs = [None] * len(beliefs)
    for i in range(len(beliefs)):
        new_beliefs[i] = [None] * len(beliefs[0])
    for i in range(len(beliefs)):
        for j in range(len(beliefs[i])):
            hit = (color == grid[i][j])
            new_beliefs[i][j] = (beliefs[i][j] * (hit * p_hit + (1-hit) * p_miss))    
    sum_beliefs = sum([sum(i) for i in new_beliefs])
    for i in range(len(beliefs)):
        for j in range(len(beliefs[i])):
            new_beliefs[i][j] = new_beliefs[i][j] / sum_beliefs
    return new_beliefs

def move(dy, dx, beliefs, blurring):
    height = len(beliefs)
    width = len(beliefs[0])
    #new_G = [[0.0 for i in range(height)] for j in range(width)]
    new_G = [None] * height
    for i in range(height):
        new_G[i] = [None] * width
    for i, row in enumerate(beliefs):
        for j, cell in enumerate(row):
            new_i = (i + dy ) % (height)
            new_j = (j + dx ) % (width)
            # pdb.set_trace()
            new_G[int(new_i)][int(new_j)] = cell
    return blur(new_G, blurring)