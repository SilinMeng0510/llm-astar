import math
from shapely.geometry import LineString

def filter_collision_path(start, ends, object):
    new = []
    for end in ends:
        if start[0] == end[0] and start[1] == end[1]:
            continue
        if not line_circle(start[0], start[1], end[0], end[1], object[0], object[1], object[2]):
            new.append(end)
    return new

# Function to check if a line intersects with a circle
def line_circle(x1, y1, x2, y2, cx, cy, r):
    inside1 = point_circle(x1, y1, cx, cy, r)
    inside2 = point_circle(x2, y2, cx, cy, r)
    if inside1 or inside2:
        return True

    distX = x1 - x2
    distY = y1 - y2
    len = math.sqrt(distX**2 + distY**2)
    dot = ((cx-x1) * (x2-x1) + (cy-y1) * (y2-y1)) / len**2

    closestX = x1 + dot * (x2 - x1)
    closestY = y1 + dot * (y2 - y1)

    on_segment = line_point(x1, y1, x2, y2, closestX, closestY)
    if not on_segment:
        return False

    distX = closestX - cx
    distY = closestY - cy
    distance = math.sqrt(distX**2 + distY**2)

    return distance <= r

# Function to check if a point is inside a circle
def point_circle(px, py, cx, cy, r):
    distX = px - cx
    distY = py - cy
    distance = math.sqrt(distX**2 + distY**2)
    return distance <= r

# Function to check if a point is on a line segment
def line_point(x1, y1, x2, y2, px, py):
    d1 = math.dist((px, py), (x1, y1))
    d2 = math.dist((px, py), (x2, y2))
    lineLen = math.dist((x1, y1), (x2, y2))
    buffer = 0.1
    return abs(d1 + d2 - lineLen) <= buffer


def is_lines_collision(line1, line2):
    line1 = LineString(line1)
    line2 = LineString(line2)
    return line1.intersects(line2)