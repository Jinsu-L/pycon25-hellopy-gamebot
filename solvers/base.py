from abc import ABC, abstractmethod

class Solver(ABC):
    """알고리즘 솔버의 기본 클래스"""
    
    @abstractmethod
    def solve(self, game_state):
        """주어진 게임 상태에 대해 다음 움직임을 결정합니다.

        Args:
            game_state (dict): 현재 게임 상태 (보드, 뱀, 음식 등).

        Returns:
            str: 다음 움직임 방향 ('ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight').
        """
        pass
