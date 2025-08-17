#!/usr/bin/env python3
"""
PY-SON Snake Game Bot

알고리즘을 선택하여 스네이크 게임을 자동으로 플레이합니다.
"""

from game import SnakeGame
from solvers.bfs import BFSSolver
from solvers.astar import AStarSolver

def main():
    """메인 실행 함수"""
    print("PY-SON Snake Game Bot")
    print("="*40)
    
    # DFS가 제거되었으므로, 키를 '1', '2'로 재조정합니다.
    solvers = {
        '1': ('BFS', BFSSolver),
        '2': ('A*', AStarSolver),
    }
    
    print("사용 가능한 알고리즘:")
    for key, (name, _) in solvers.items():
        print(f"{key}. {name}")

    # 사용자 선택
    choice = ''
    while choice not in solvers:
        try:
            # 선택 옵션을 (1-2)로 변경합니다.
            choice = input("\n알고리즘을 선택하세요 (1-2): ").strip()
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            return

    # 선택된 솔버 인스턴스 생성
    solver_name, solver_class = solvers[choice]
    solver = solver_class()
    
    # 게임 URL 설정
    url = "https://hello-py.com/game/play?email="
    game = SnakeGame(url)
    
    try:
        # 게임 설정 및 로드
        game.setup_browser()
        game.inject_state_extractor()
        game.load_game()
        
        print("게임 페이지 로드 완료!")
        print(f"\n사용법 ({solver_name.upper()} 모드):")
        print("1. 브라우저에서 '게임 시작' 버튼을 클릭하세요")
        print(f"2. 게임이 시작되면 봇이 자동으로 {solver_name.upper()} 알고리즘으로 플레이합니다")
        
        # 자동 플레이 시작
        game.auto_play(solver)
        
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        print("게임을 종료합니다.")
        game.close()

if __name__ == "__main__":
    main()