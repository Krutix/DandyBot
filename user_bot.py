import random
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
    if t in a_star:
        a_star[t] = min(a_star[min_cell]+1, a_star[t])
        if a_star[t] == a_star[min_cell]+1:
            a_star_back[t] = min_cell
    elif not check('wall', t[0], t[1]):
        a_star[t] = a_star[min_cell]+1
        a_star_back[t] = min_cell

def script(check, x, y):
    if check('gold', x, y):
        return 'take'

    gold = set()
    depth = 1
    while len(gold) == 0:
        gold |= find_gold(check, x, y, depth)
        depth += 1

    gold = list(gold)
    gold.sort()

    a_star = {(x, y) : 0 }
    a_star_back = {}
    a_star_calculated = set()
    while True:
        key_min = lambda xy: potencial_len(xy, gold[0]) if not xy in a_star_calculated else 1024
        min_cell = min([*a_star], key=key_min)
        a_star_calculated |= {min_cell}

        check_and_append(check, a_star, a_star_back, (min_cell[0]-1, min_cell[1]), min_cell)
        check_and_append(check, a_star, a_star_back, (min_cell[0]+1, min_cell[1]), min_cell)
        check_and_append(check, a_star, a_star_back, (min_cell[0], min_cell[1]-1), min_cell)
        check_and_append(check, a_star, a_star_back, (min_cell[0], min_cell[1]+1), min_cell)

        if gold[0] in a_star:
            break

    back = gold[0]
    while a_star_back[back] != (x, y):
        back = a_star_back[back]

    if x - back[0] < 0:
        return 'right'
    if x - back[0] > 0:
        return 'left'
    if y - back[1] < 0:
        return 'down'
    if y - back[1] > 0:
        return 'up'

    return random.choice(['left', 'right', 'right', 'up', 'down'])


#def find_path(check, x, y, depth, back_move : str = '') -> int:
#    if depth < 0 or check('wall', x, y):
#        return None
#    if check('gold', x, y):
#        return ('take', 1)
#    move = []
#
#    r = find_path(check, x-1, y, depth-1, 'left') if back_move != 'right' else None
#    if None != r:
#        move.append(('left', r[1]+1))
#
#    r = find_path(check, x+1, y, depth-1, 'right') if back_move != 'left' else None
#    if None != r:
#        move.append(('right', r[1]+1))
#
#    r = find_path(check, x, y-1, depth-1, 'up') if back_move != 'down' else None
#    if None != r:
#        move.append(('up', r[1]+1))
#
#    r = find_path(check, x, y+1, depth-1, 'down') if back_move != 'up' else None
#    if None != r:
#        move.append(('down', r[1]+1))
#
#    if len(move) == 0:
#        return None
#    return min(move, key=lambda x: x[1])
#
#def script(check, x, y):
#    r = find_path(check, x, y, 12)
#    if None == r:
#        return random.choice(['left', 'right', 'right', 'up', 'down'])
#    else:
#        return r[0]
