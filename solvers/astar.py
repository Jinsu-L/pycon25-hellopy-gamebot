import heapq
from collections import deque
from .base import Solver
from utils import manhattan_distance, flood_fill_area

class AStarSolver(Solver):
    """휴리스틱 a* 솔버"""

    def solve(self, game_state):
        snake = game_state['snake']
        snake_head = snake[0]
        food = game_state['food']

        # 1. 안전한 음식 경로 탐색
        if food:
            path_to_food = self._find_path_astar(game_state, snake_head, food, snake[1:])
            if path_to_food and self._is_path_safe(game_state, path_to_food):
                return path_to_food[0]

        # 2. 꼬리 추적 (생존 전략, 꼬리는 장애물에서 제외)
        path_to_tail = self._find_path_astar(game_state, snake_head, snake[-1], snake[1:-1])
        if path_to_tail:
            return path_to_tail[0]

        # 3. 최후의 수단: 가장 넓은 공간으로 이동
        return self._find_best_survival_move(game_state, snake_head)

    def _find_path_astar(self, game_state, start, goal, snake_body_obstacles):
        obstacles = { (segment['x'], segment['y']) for segment in snake_body_obstacles }
        node_counter = 0
        heap = [(manhattan_distance(start, goal), 0, node_counter, start, [])]
        visited = { (start['x'], start['y']) }

        while heap:
            f, g, _, current, path = heapq.heappop(heap)
            if current['x'] == goal['x'] and current['y'] == goal['y']:
                return path

            directions = [(0, -1, 'ArrowUp'), (0, 1, 'ArrowDown'), (-1, 0, 'ArrowLeft'), (1, 0, 'ArrowRight')]
            for dx, dy, direction in directions:
                next_pos = {'x': current['x'] + dx, 'y': current['y'] + dy}
                next_pos_tuple = (next_pos['x'], next_pos['y'])
                if self._is_valid_pos(game_state, next_pos) and next_pos_tuple not in obstacles and next_pos_tuple not in visited:
                    visited.add(next_pos_tuple)
                    new_g = g + 1
                    h = manhattan_distance(next_pos, goal)
                    new_f = new_g + h
                    node_counter += 1
                    heapq.heappush(heap, (new_f, new_g, node_counter, next_pos, path + [direction]))
        return None

    def _is_path_safe(self, game_state, path):
        future_snake = self._simulate_move_and_grow(game_state['snake'], path)
        if not future_snake or len(future_snake) < 2:
            return False
        
        # 미래의 뱀 머리에서 미래의 꼬리까지 BFS(너비 우선 탐색)를 수행하여 경로가 존재하는지 확인 -> 문제가 생겨도 한번은 돌 수 있는가?
        head = future_snake[0]
        tail = future_snake[-1]
       
        obstacles = { (segment['x'], segment['y']) for segment in future_snake[1:-1] }
        
        queue = deque([head])
        visited = { (head['x'], head['y']) }
        grid_width, grid_height = game_state['gridWidth'], game_state['gridHeight']

        while queue:
            current = queue.popleft()
            if current['x'] == tail['x'] and current['y'] == tail['y']:
                return True # 경로 찾음 -> 안전함
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in directions:
                next_pos = {'x': current['x'] + dx, 'y': current['y'] + dy}
                next_pos_tuple = (next_pos['x'], next_pos['y'])
                if self._is_valid_pos(game_state, next_pos) and next_pos_tuple not in obstacles and next_pos_tuple not in visited:
                    visited.add(next_pos_tuple)
                    queue.append(next_pos)
        return False # 경로 못 찾음 -> 함정임

    def _simulate_move_and_grow(self, snake, path):
        snake_copy = [dict(s) for s in snake]
        for move in path:
            head = snake_copy[0]
            directions = {'ArrowUp': (0, -1), 'ArrowDown': (0, 1), 'ArrowLeft': (-1, 0), 'ArrowRight': (1, 0)}
            dx, dy = directions[move]
            new_head = {'x': head['x'] + dx, 'y': head['y'] + dy}
            snake_copy.insert(0, new_head)
        return snake_copy[:len(snake) + 1]

    def _is_valid_pos(self, game_state, pos):
        return 0 <= pos['x'] < game_state['gridWidth'] and 0 <= pos['y'] < game_state['gridHeight']

    def _find_best_survival_move(self, game_state, snake_head):
        obstacles = { (s['x'], s['y']) for s in game_state['snake'][1:] }
        best_direction = 'ArrowUp'
        max_area = -1

        for dx, dy, direction in [(0, -1, 'ArrowUp'), (0, 1, 'ArrowDown'), (-1, 0, 'ArrowLeft'), (1, 0, 'ArrowRight')]:
            next_pos = {'x': snake_head['x'] + dx, 'y': snake_head['y'] + dy}
            if self._is_valid_pos(game_state, next_pos) and (next_pos['x'], next_pos['y']) not in obstacles:
                area = flood_fill_area(game_state, next_pos, obstacles)
                if area > max_area:
                    max_area = area
                    best_direction = direction
        return best_direction
