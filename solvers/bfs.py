from collections import deque
from .base import Solver
from utils import flood_fill_area

class BFSSolver(Solver):
    """BFS 알고리즘과 '가장 넓은 공간으로 이동' 생존 전략을 사용한 솔버"""
    
    def solve(self, game_state):
        """BFS로 음식까지의 최단 경로를 찾고, 없으면 가장 넓은 공간으로 이동합니다."""
        snake_head = game_state['snake'][0]
        food = game_state['food']
        obstacles = self._get_obstacles(game_state)
        
        # 1. 음식으로 가는 최단 경로 탐색
        path_to_food = self._find_path(game_state, snake_head, food, obstacles)
        if path_to_food:
            return path_to_food[0]
        
        # 2. 음식을 못 찾으면, 가장 넓은 공간으로 이동하여 생존
        return self._find_best_survival_move(game_state, snake_head, obstacles)

    def _find_path(self, game_state, start, goal, obstacles):
        """BFS 알고리즘으로 최단 경로를 찾습니다."""
        if not start or not goal:
            return None
        queue = deque([(start, [])])
        visited = { (start['x'], start['y']) }
        directions = [(0, -1, 'ArrowUp'), (0, 1, 'ArrowDown'), (-1, 0, 'ArrowLeft'), (1, 0, 'ArrowRight')]
        grid_width, grid_height = game_state['gridWidth'], game_state['gridHeight']

        while queue:
            current, path = queue.popleft()
            if current['x'] == goal['x'] and current['y'] == goal['y']:
                return path
            for dx, dy, direction in directions:
                next_x, next_y = current['x'] + dx, current['y'] + dy
                next_pos_tuple = (next_x, next_y)
                if not (0 <= next_x < grid_width and 0 <= next_y < grid_height) or next_pos_tuple in visited or next_pos_tuple in obstacles:
                    continue
                visited.add(next_pos_tuple)
                queue.append(({'x': next_x, 'y': next_y}, path + [direction]))
        return None

    def _get_obstacles(self, game_state):
        return { (segment['x'], segment['y']) for segment in game_state['snake'][1:] }

    def _find_best_survival_move(self, game_state, snake_head, obstacles):
        """4방향 중 가장 접근 가능한 공간이 넓은 방향을 찾습니다."""
        best_direction = 'ArrowUp' # 기본값
        max_area = -1

        directions = [(0, -1, 'ArrowUp'), (0, 1, 'ArrowDown'), (-1, 0, 'ArrowLeft'), (1, 0, 'ArrowRight')]
        
        for dx, dy, direction in directions:
            next_pos = {'x': snake_head['x'] + dx, 'y': snake_head['y'] + dy}
            area = flood_fill_area(game_state, next_pos, obstacles)
            if area > max_area:
                max_area = area
                best_direction = direction
        
        return best_direction