def area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    width = abs(p2[0] - p1[0]) + 1
    height = abs(p2[1] - p1[1]) + 1
    return width * height

def first_solution(filename: str) -> int:
    points = []
    max_col = 0
    max_ln = 0
    with open(filename) as file:
        for line in file:
            points.append(tuple([int(point) for point in line.strip().split(',')]))
            max_col = max(max_col, points[-1][0])
            max_ln = max(max_ln, points[-1][1])

    largest = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            largest = max(largest, area(points[i], points[j]))

    return largest

def point_in_polygon(x, y, polygon): # ray-casting algorithm
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

def is_on_boundary(x, y, polygon):
    n = len(polygon)
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        if p1[0] == p2[0] == x:
            if min(p1[1], p2[1]) <= y <= max(p1[1], p2[1]):
                return True
        elif p1[1] == p2[1] == y:
            if min(p1[0], p2[0]) <= x <= max(p1[0], p2[0]):
                return True
    return False

def is_rectangle_valid(min_x, max_x, min_y, max_y, polygon):
    corners = [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]
    
    for corner in corners:
        if corner in polygon:
            continue
        if is_on_boundary(corner[0], corner[1], polygon):
            continue
        if not point_in_polygon(corner[0], corner[1], polygon):
            return False
            
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2
    
    if is_on_boundary(mid_x, mid_y, polygon):
        return True
        
    if not point_in_polygon(mid_x, mid_y, polygon):
        return False
    
    return True

def intersects_interior(min_x, max_x, min_y, max_y, polygon):
    n = len(polygon)
    for k in range(n):
        p1 = polygon[k]
        p2 = polygon[(k + 1) % n]
        
        if p1[0] == p2[0]: # Vertical edge
            px = p1[0]
            py_min, py_max = min(p1[1], p2[1]), max(p1[1], p2[1])
            
            if min_x < px < max_x:
                if max(min_y, py_min) < min(max_y, py_max):
                    return True
                    
        else: # Horizontal edge
            py = p1[1]
            px_min, px_max = min(p1[0], p2[0]), max(p1[0], p2[0])
            
            if min_y < py < max_y:
                if max(min_x, px_min) < min(max_x, px_max):
                    return True
    return False

def second_solution(filename: str) -> int:
    points = []
    with open(filename) as file:
        for line in file:
            points.append(tuple([int(point) for point in line.strip().split(',')]))

    polygon = points
    largest = 0
    n = len(points)
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            
            if not is_rectangle_valid(min_x, max_x, min_y, max_y, polygon):
                continue
            
            if intersects_interior(min_x, max_x, min_y, max_y, polygon):
                continue
            
            current_area = area(points[i], points[j])
            if current_area > largest:
                largest = current_area
    
    return largest

if __name__ == '__main__':
    print(first_solution('input1.txt'))
    print(second_solution('input1.txt'))