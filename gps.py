import math

def distance((x1, y1), (x2, y2)):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return math.sqrt(dx**2 + dy**2)
