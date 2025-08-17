from collections import deque

def manhattan_distance(pos1, pos2):
    """맨하탄 거리 계산"""
    return abs(pos1['x'] - pos2['x']) + abs(pos1['y'] - pos2['y'])

def flood_fill_area(game_state, start_pos, obstacles):
    """Flood Fill로 특정 지점에서부터 접근 가능한 영역의 크기를 계산합니다."""
    grid_width = game_state['gridWidth']
    grid_height = game_state['gridHeight']

    if not (0 <= start_pos['x'] < grid_width and 0 <= start_pos['y'] < grid_height):
        return 0
    if (start_pos['x'], start_pos['y']) in obstacles:
        return 0
    
    q = deque([start_pos])
    visited = { (start_pos['x'], start_pos['y']) }
    count = 0
    while q:
        pos = q.popleft()
        count += 1
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            next_pos = {'x': pos['x'] + dx, 'y': pos['y'] + dy}
            next_pos_tuple = (next_pos['x'], next_pos['y'])

            if (0 <= next_pos['x'] < grid_width and 0 <= next_pos['y'] < grid_height and
                next_pos_tuple not in obstacles and next_pos_tuple not in visited):
                visited.add(next_pos_tuple)
                q.append(next_pos)
    return count