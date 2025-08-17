import time
from playwright.sync_api import sync_playwright

class SnakeGame:
    """브라우저 및 게임 환경과의 상호작용을 관리하는 클래스"""
    
    def __init__(self, url):
        self.url = url
        self.page = None
        self.browser = None
        self.playwright = None
        self.moves_made = 0

    def setup_browser(self):
        """브라우저 설정"""
        print("브라우저 시작...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.page.set_viewport_size({"width": 1200, "height": 800})

    def load_game(self):
        """게임 페이지 로드"""
        print(f"게임 페이지 로드: {self.url}")
        self.page.goto(self.url, wait_until="domcontentloaded")
        time.sleep(3)

    def inject_state_extractor(self):
        """게임 상태 추출을 위한 JavaScript 코드 주입"""
        print("상태 추출 코드 주입...")
        with open('state_extractor.js', 'r') as f:
            injection_script = f.read()
        self.page.add_init_script(injection_script)

    def get_game_state(self):
        """현재 게임 상태 추출"""
        try:
            state = self.page.evaluate("() => window.__get_game_state__ && window.__get_game_state__()")
            return state
        except Exception as e:
            print(f"게임 상태 추출 오류: {e}")
            return None

    def send_key(self, direction):
        """키 입력 전송"""
        try:
            self.page.keyboard.press(direction)
            self.moves_made += 1
        except Exception as e:
            print(f"키 입력 오류: {e}")

    def print_game_state(self, state, algorithm_name):
        """게임 상태 출력"""
        if not state:
            return
        print(f"[{algorithm_name.upper()}] 점수: {state['score']}, 뱀 길이: {len(state['snake'])}, 이동: {self.moves_made}회")

    def auto_play(self, solver):
        """자동 플레이 루프"""
        algorithm_name = solver.__class__.__name__.replace('Solver', '')
        print(f"\n{algorithm_name.upper()} 알고리즘으로 자동 플레이 시작!")
        print("게임을 수동으로 시작한 후, 봇이 자동으로 플레이합니다.")
        print("Ctrl+C를 눌러 중단할 수 있습니다.\n")
        
        frame_count = 0
        while True:
            try:
                state = self.get_game_state()
                if state:
                    if state['gameOver']:
                        print("게임 오버! 최종 점수: {}".format(state['score']))
                        # 재시작 로직 (필요시 추가)
                        try:
                            restart_btn = self.page.locator("#playAgainBtn")
                            if restart_btn.is_visible():
                                print("게임 재시작...")
                                restart_btn.click()
                                time.sleep(2)
                                self.moves_made = 0
                                continue
                        except Exception as e:
                            print(f"재시작 실패: {e}")
                            break # 재시작 실패 시 루프 종료

                    elif state['snake'] and not state['gameOver']:
                        if frame_count % 10 == 0:
                            self.print_game_state(state, algorithm_name)
                        
                        next_move = solver.solve(state)
                        
                        if next_move:
                            self.send_key(next_move)
                        else:
                            print("안전한 움직임을 찾을 수 없습니다!")
                
                time.sleep(0.05)
                frame_count += 1

            except KeyboardInterrupt:
                print("\n사용자에 의해 중단되었습니다.")
                break
            except Exception as e:
                print(f"오류 발생: {e}")
                time.sleep(1)

    def close(self):
        """리소스 정리"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
