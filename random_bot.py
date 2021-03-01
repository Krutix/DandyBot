import random

def find_path(check, x, y, depth, back_move : str = '') -> int:
    if depth < 0 or check('wall', x, y):
        return None
    if check('gold', x, y):
        return ('take', 1)
    move = []

    r = find_path(check, x-1, y, depth-1, 'left') if back_move != 'right' else None
    if None != r:
        move.append(('left', r[1]+1))

    r = find_path(check, x+1, y, depth-1, 'right') if back_move != 'left' else None
    if None != r:
        move.append(('right', r[1]+1))

    r = find_path(check, x, y-1, depth-1, 'up') if back_move != 'down' else None
    if None != r:
        move.append(('up', r[1]+1))

    r = find_path(check, x, y+1, depth-1, 'down') if back_move != 'up' else None
    if None != r:
        move.append(('down', r[1]+1))

    if len(move) == 0:
        return None
    return min(move, key=lambda x: x[1])

def script(check, x, y):
    r = find_path(check, x, y, 5)
    if None == r:
        return random.choice(['left', 'right', 'right', 'up', 'down'])
    else:
        return r[0]
