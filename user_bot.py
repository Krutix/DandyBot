﻿import random
import random_bot

def find_gold(check, x, y, depth) -> [(int, int)]:
    gold = set()
    for i in range(depth * 2 + 1):
        if check('gold', x - depth + i, y - depth):
            gold |= {(x - depth + i, y - depth)}
        if check('gold', x - depth + i, y + depth):
            gold |= {(x - depth + i, y + depth)}
        if check('gold', x - depth, y - depth + i):
            gold |= {(x - depth, y - depth + i)}
        if check('gold', x + depth, y - depth + i):
            gold |= {(x + depth, y - depth + i)}
    return gold

def potencial_len(xy, t): return abs(xy[0] - t[0]) + abs(xy[1] - t[1])

def check_and_append(check, a_star, a_star_back, t, min_cell):
    addition = 1
    if t in a_star:
        if a_star[t] > a_star[min_cell]+addition:
            a_star[t] = a_star[min_cell]+addition
            a_star_back[t] = min_cell
    elif not check('wall', t[0], t[1]):
        a_star[t] = a_star[min_cell]+addition
        a_star_back[t] = min_cell

def find_path(check, start, find) -> ((int, int), int):
    a_star = {start : 0}
    a_star_back = {}
    a_star_calculated = set()
    while True:
        key_min = lambda xy: a_star[xy] + potencial_len(xy, find) if not xy in a_star_calculated else 99999999
        min_cell = min([*a_star], key=key_min)
        a_star_calculated |= {min_cell}

        check_and_append(check, a_star, a_star_back, (min_cell[0]-1, min_cell[1]), min_cell)
        check_and_append(check, a_star, a_star_back, (min_cell[0]+1, min_cell[1]), min_cell)
        check_and_append(check, a_star, a_star_back, (min_cell[0], min_cell[1]-1), min_cell)
        check_and_append(check, a_star, a_star_back, (min_cell[0], min_cell[1]+1), min_cell)

        if find in a_star:
            break

    back = find
    while a_star_back[back] != start:
        back = a_star_back[back]
    return (back, a_star[find])

def script(check, x, y):
    if check('gold', x, y):
        return 'take'

    gold = set()
    depth = 1
    while len(gold) == 0:
        gold |= find_gold(check, x, y, depth)
        depth += 1
    for _ in range(4):
        gold |= find_gold(check, x, y, depth)
        depth += 1

    gold = list(gold)
    gold.sort(key=lambda xy: potencial_len((x, y), xy))

    a_star_gold = []

    for g in gold:
        a_star_gold.append(find_path(check, (x, y), g))

    a_star_gold.sort(key=lambda xy_l: xy_l[1])

    if x - a_star_gold[0][0][0] < 0:
        return 'right'
    if x - a_star_gold[0][0][0] > 0:
        return 'left'
    if y - a_star_gold[0][0][1] < 0:
        return 'down'
    if y - a_star_gold[0][0][1] > 0:
        return 'up'

    return random.choice(['left', 'right', 'right', 'up', 'down'])
