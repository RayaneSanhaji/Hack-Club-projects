import pygame
import random
import sys

# Initialize Pygame and Audio Mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2)

# Main Window Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classic Retro Arcade")

clock = pygame.time.Clock()

# Colors
BG_COLOR = (24, 28, 36)
PANEL_COLOR = (36, 42, 54)
TEXT_COLOR = (240, 244, 248)
ACCENT_COLOR = (79, 110, 242)
ACCENT_HOVER = (110, 138, 255)
BTN_COLOR = (52, 60, 78)
BTN_HOVER = (70, 80, 104)
RED = (235, 87, 87)
GREEN = (46, 204, 113)

# Global Settings
global_volume = 0.5


def play_beep(frequency=440, duration=100):
    """Generates and plays a synthetic sound effect scaling properly with volume."""
    if global_volume <= 0.01:
        return
    sample_rate = 22050
    num_samples = int(sample_rate * (duration / 1000.0))
    buffer = bytearray()

    amplitude = int(16000 * global_volume)

    for i in range(num_samples):
        wave_val = (
            amplitude
            if (i // int(sample_rate / frequency / 2)) % 2 == 0
            else -amplitude
        )
        low_byte = wave_val & 0xFF
        high_byte = (wave_val >> 8) & 0xFF
        buffer.append(low_byte)
        buffer.append(high_byte)

    try:
        sound = pygame.mixer.Sound(buffer=bytes(buffer))
        sound.set_volume(global_volume)
        sound.play()
    except Exception:
        pass


class Button:

    def __init__(
        self, x, y, w, h, text, color, hover_color, text_color, font_size=20
    ):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        current_color = self.hover_color if is_hover else self.color

        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(
            surface, (255, 255, 255), self.rect, width=2, border_radius=10
        )

        txt_surf = self.font.render(self.text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                play_beep(600, 80)
                return True
        return False


def select_mode_and_difficulty(game_name, has_2p_mode=True):
    """Sub-menu to choose difficulty and Mode (vs Bot / 2 Players)."""
    font_title = pygame.font.SysFont("Arial", 32, bold=True)
    font_sub = pygame.font.SysFont("Arial", 20)
    btn_back = Button(
        20, 20, 100, 40, "<- Back", RED, (255, 100, 100), TEXT_COLOR
    )

    mode = "vs_bot"
    difficulty = "Medium"

    btn_mode_bot = Button(
        220,
        190,
        170,
        40,
        "1 Player (vs Bot)",
        ACCENT_COLOR,
        ACCENT_HOVER,
        TEXT_COLOR,
        16,
    )
    btn_mode_2p = Button(
        410, 190, 170, 40, "2 Players", BTN_COLOR, BTN_HOVER, TEXT_COLOR, 16
    )

    btn_easy = Button(
        180, 320, 130, 40, "Easy", BTN_COLOR, BTN_HOVER, TEXT_COLOR
    )
    btn_med = Button(
        335, 320, 130, 40, "Medium", ACCENT_COLOR, ACCENT_HOVER, TEXT_COLOR
    )
    btn_hard = Button(
        490, 320, 130, 40, "Hard", BTN_COLOR, BTN_HOVER, TEXT_COLOR
    )

    btn_start = Button(
        WIDTH // 2 - 100,
        430,
        200,
        50,
        "Start Game",
        GREEN,
        (80, 220, 140),
        TEXT_COLOR,
    )

    while True:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_back.is_clicked(event):
                return None, None

            if has_2p_mode:
                if btn_mode_bot.is_clicked(event):
                    mode = "vs_bot"
                elif btn_mode_2p.is_clicked(event):
                    mode = "2p"

            if btn_easy.is_clicked(event):
                difficulty = "Easy"
            elif btn_med.is_clicked(event):
                difficulty = "Medium"
            elif btn_hard.is_clicked(event):
                difficulty = "Hard"

            if btn_start.is_clicked(event):
                return mode, difficulty

        if has_2p_mode:
            btn_mode_bot.color = (
                ACCENT_COLOR if mode == "vs_bot" else BTN_COLOR
            )
            btn_mode_2p.color = ACCENT_COLOR if mode == "2p" else BTN_COLOR

        btn_easy.color = ACCENT_COLOR if difficulty == "Easy" else BTN_COLOR
        btn_med.color = ACCENT_COLOR if difficulty == "Medium" else BTN_COLOR
        btn_hard.color = ACCENT_COLOR if difficulty == "Hard" else BTN_COLOR

        title = font_title.render(f"{game_name} - Setup", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 55))

        if has_2p_mode:
            lbl_mode = font_sub.render("Select Game Mode:", True, TEXT_COLOR)
            screen.blit(lbl_mode, (WIDTH // 2 - lbl_mode.get_width() // 2, 150))
            btn_mode_bot.draw(screen)
            btn_mode_2p.draw(screen)

        lbl_diff = font_sub.render("Select Difficulty:", True, TEXT_COLOR)
        screen.blit(lbl_diff, (WIDTH // 2 - lbl_diff.get_width() // 2, 275))

        btn_easy.draw(screen)
        btn_med.draw(screen)
        btn_hard.draw(screen)
        btn_start.draw(screen)
        btn_back.draw(screen)

        pygame.display.flip()
        clock.tick(60)


# ==========================================
# 1. ROCK - PAPER - SCISSORS
# ==========================================
def run_rps(mode, difficulty):
    font_title = pygame.font.SysFont("Arial", 32, bold=True)
    font_text = pygame.font.SysFont("Arial", 22)

    btn_rock = Button(
        150, 420, 150, 50, "Rock", BTN_COLOR, BTN_HOVER, TEXT_COLOR
    )
    btn_paper = Button(
        325, 420, 150, 50, "Paper", BTN_COLOR, BTN_HOVER, TEXT_COLOR
    )
    btn_scissors = Button(
        500, 420, 150, 50, "Scissors", BTN_COLOR, BTN_HOVER, TEXT_COLOR
    )
    btn_back = Button(
        20, 20, 100, 40, "<- Back", RED, (255, 100, 100), TEXT_COLOR
    )
    btn_restart = Button(
        WIDTH // 2 - 75,
        500,
        150,
        40,
        "Play Again",
        ACCENT_COLOR,
        ACCENT_HOVER,
        TEXT_COLOR,
    )

    p1_choice, p2_choice, result, turn = "", "", "", 1
    choices = ["Rock", "Paper", "Scissors"]

    running = True
    while running:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_back.is_clicked(event):
                return
            if btn_restart.is_clicked(event):
                p1_choice, p2_choice, result, turn = "", "", "", 1

            if not result:
                chosen = None
                if btn_rock.is_clicked(event):
                    chosen = "Rock"
                elif btn_paper.is_clicked(event):
                    chosen = "Paper"
                elif btn_scissors.is_clicked(event):
                    chosen = "Scissors"

                if chosen:
                    if mode == "vs_bot":
                        p1_choice = chosen
                        if difficulty == "Easy":
                            losing_map = {
                                "Rock": "Scissors",
                                "Paper": "Rock",
                                "Scissors": "Paper",
                            }
                            p2_choice = (
                                losing_map[p1_choice]
                                if random.random() < 0.6
                                else random.choice(choices)
                            )
                        elif difficulty == "Hard":
                            counter_map = {
                                "Rock": "Paper",
                                "Paper": "Scissors",
                                "Scissors": "Rock",
                            }
                            p2_choice = (
                                counter_map[p1_choice]
                                if random.random() < 0.6
                                else random.choice(choices)
                            )
                        else:
                            p2_choice = random.choice(choices)
                    else:
                        if turn == 1:
                            p1_choice = chosen
                            turn = 2
                        elif turn == 2:
                            p2_choice = chosen

                    if p1_choice and p2_choice:
                        if p1_choice == p2_choice:
                            result = "It's a Tie!"
                        elif (
                            (p1_choice == "Rock" and p2_choice == "Scissors")
                            or (p1_choice == "Paper" and p2_choice == "Rock")
                            or (
                                p1_choice == "Scissors"
                                and p2_choice == "Paper"
                            )
                        ):
                            result = (
                                "Player 1 Wins!"
                                if mode == "2p"
                                else "You Win!"
                            )
                        else:
                            result = (
                                "Player 2 Wins!"
                                if mode == "2p"
                                else "Computer Wins!"
                            )

        title = font_title.render(
            f"Rock Paper Scissors ({difficulty})", True, TEXT_COLOR
        )
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

        if result:
            p1_t = font_text.render(
                f"P1 Choice: {p1_choice}", True, TEXT_COLOR
            )
            p2_t = font_text.render(
                f"{'P2' if mode=='2p' else 'Bot'} Choice: {p2_choice}",
                True,
                TEXT_COLOR,
            )
            res_t = font_title.render(result, True, ACCENT_COLOR)
            screen.blit(p1_t, (WIDTH // 2 - p1_t.get_width() // 2, 180))
            screen.blit(p2_t, (WIDTH // 2 - p2_t.get_width() // 2, 220))
            screen.blit(res_t, (WIDTH // 2 - res_t.get_width() // 2, 290))
            btn_restart.draw(screen)
        else:
            prompt = (
                f"Player {turn}, choose your move:"
                if mode == "2p"
                else "Choose your move:"
            )
            inst = font_text.render(prompt, True, TEXT_COLOR)
            screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, 250))
            btn_rock.draw(screen)
            btn_paper.draw(screen)
            btn_scissors.draw(screen)

        btn_back.draw(screen)
        pygame.display.flip()
        clock.tick(60)


# ==========================================
# 2. TIC-TAC-TOE
# ==========================================
def run_ttt(mode, difficulty):
    font_title = pygame.font.SysFont("Arial", 36, bold=True)
    font_cell = pygame.font.SysFont("Arial", 60, bold=True)
    btn_back = Button(
        20, 20, 100, 40, "<- Back", RED, (255, 100, 100), TEXT_COLOR
    )
    btn_restart = Button(
        WIDTH // 2 - 75,
        520,
        150,
        40,
        "Play Again",
        ACCENT_COLOR,
        ACCENT_HOVER,
        TEXT_COLOR,
    )

    board = [["" for _ in range(3)] for _ in range(3)]
    turn = "X"
    winner = None

    def check_win():
        for r in range(3):
            if board[r][0] == board[r][1] == board[r][2] != "":
                return board[r][0]
        for c in range(3):
            if board[0][c] == board[1][c] == board[2][c] != "":
                return board[0][c]
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]
        if all(board[r][c] != "" for r in range(3) for c in range(3)):
            return "Tie"
        return None

    def bot_move():
        empty_cells = [
            (r, c)
            for r in range(3)
            for c in range(3)
            if board[r][c] == ""
        ]
        if not empty_cells:
            return
        if difficulty in ["Medium", "Hard"]:
            for symbol in ["O", "X"]:
                for r, c in empty_cells:
                    board[r][c] = symbol
                    if check_win() == symbol:
                        board[r][c] = "O"
                        return
                    board[r][c] = ""
        r, c = random.choice(empty_cells)
        board[r][c] = "O"

    running = True
    while running:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_back.is_clicked(event):
                return
            if btn_restart.is_clicked(event):
                board = [["" for _ in range(3)] for _ in range(3)]
                turn = "X"
                winner = None

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and not winner
            ):
                mx, my = event.pos
                if 250 <= mx <= 550 and 180 <= my <= 480:
                    c = (mx - 250) // 100
                    r = (my - 180) // 100
                    if board[r][c] == "":
                        board[r][c] = turn
                        play_beep(400, 100)
                        winner = check_win()

                        if not winner:
                            if mode == "vs_bot":
                                bot_move()
                                play_beep(300, 100)
                                winner = check_win()
                            else:
                                turn = "O" if turn == "X" else "X"

        title = font_title.render(f"Tic-Tac-Toe ({difficulty})", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

        for r in range(3):
            for c in range(3):
                rx = 250 + c * 100
                ry = 180 + r * 100
                pygame.draw.rect(
                    screen, PANEL_COLOR, (rx, ry, 96, 96), border_radius=8
                )
                if board[r][c] != "":
                    color = (
                        (90, 140, 255) if board[r][c] == "X" else (255, 120, 120)
                    )
                    txt = font_cell.render(board[r][c], True, color)
                    screen.blit(txt, txt.get_rect(center=(rx + 48, ry + 48)))

        if winner:
            if winner == "Tie":
                res_txt = font_title.render("It's a Tie!", True, TEXT_COLOR)
            else:
                res_txt = font_title.render(
                    f"Player {winner} Wins!", True, GREEN
                )
            screen.blit(res_txt, (WIDTH // 2 - res_txt.get_width() // 2, 485))
            btn_restart.draw(screen)

        btn_back.draw(screen)
        pygame.display.flip()
        clock.tick(60)


# ==========================================
# 3. SNAKE
# ==========================================
def run_snake(mode, difficulty):
    font_title = pygame.font.SysFont("Arial", 36, bold=True)
    font_score = pygame.font.SysFont("Arial", 22)
    btn_back = Button(
        20, 20, 100, 40, "<- Back", RED, (255, 100, 100), TEXT_COLOR
    )
    btn_restart = Button(
        WIDTH // 2 - 75,
        535,
        150,
        40,
        "Play Again",
        ACCENT_COLOR,
        ACCENT_HOVER,
        TEXT_COLOR,
    )

    speeds = {"Easy": 150, "Medium": 100, "Hard": 60}
    speed = speeds.get(difficulty, 100)

    def reset_snake_game():
        nonlocal snake, direction, next_direction, food, score, game_over
        snake = [{"x": 10, "y": 10}, {"x": 9, "y": 10}, {"x": 8, "y": 10}]
        direction = {"x": 1, "y": 0}
        next_direction = {"x": 1, "y": 0}
        food = {"x": random.randint(0, 19), "y": random.randint(0, 19)}
        score = 0
        game_over = False

    snake, direction, next_direction, food, score, game_over = (
        [],
        {},
        {},
        {},
        0,
        False,
    )
    reset_snake_game()

    MOVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE_EVENT, speed)

    running = True
    while running:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.time.set_timer(MOVE_EVENT, 0)
                pygame.quit()
                sys.exit()
            if btn_back.is_clicked(event):
                pygame.time.set_timer(MOVE_EVENT, 0)
                return
            if game_over and btn_restart.is_clicked(event):
                reset_snake_game()

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP and direction["y"] == 0:
                    next_direction = {"x": 0, "y": -1}
                elif event.key == pygame.K_DOWN and direction["y"] == 0:
                    next_direction = {"x": 0, "y": 1}
                elif event.key == pygame.K_LEFT and direction["x"] == 0:
                    next_direction = {"x": -1, "y": 0}
                elif event.key == pygame.K_RIGHT and direction["x"] == 0:
                    next_direction = {"x": 1, "y": 0}

            if event.type == MOVE_EVENT and not game_over:
                direction = next_direction
                new_head = {
                    "x": snake[0]["x"] + direction["x"],
                    "y": snake[0]["y"] + direction["y"],
                }

                if (
                    new_head["x"] < 0
                    or new_head["x"] >= 20
                    or new_head["y"] < 0
                    or new_head["y"] >= 20
                    or new_head in snake
                ):
                    game_over = True
                    play_beep(200, 300)
                else:
                    snake.insert(0, new_head)
                    if new_head["x"] == food["x"] and new_head["y"] == food["y"]:
                        score += 10
                        play_beep(800, 80)
                        food = {
                            "x": random.randint(0, 19),
                            "y": random.randint(0, 19),
                        }
                        while food in snake:
                            food = {
                                "x": random.randint(0, 19),
                                "y": random.randint(0, 19),
                            }
                    else:
                        snake.pop()

        title = font_title.render(f"Snake ({difficulty})", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
        s_txt = font_score.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(s_txt, (WIDTH // 2 - s_txt.get_width() // 2, 70))

        board_rect = pygame.Rect(200, 120, 400, 400)
        pygame.draw.rect(screen, PANEL_COLOR, board_rect, border_radius=10)

        fx = 200 + food["x"] * 20
        fy = 120 + food["y"] * 20
        pygame.draw.rect(screen, RED, (fx + 2, fy + 2, 16, 16), border_radius=4)

        for i, block in enumerate(snake):
            bx = 200 + block["x"] * 20
            by = 120 + block["y"] * 20
            color = GREEN if i == 0 else (70, 180, 120)
            pygame.draw.rect(
                screen, color, (bx + 1, by + 1, 18, 18), border_radius=4
            )

        if game_over:
            go_txt = font_title.render("GAME OVER", True, RED)
            screen.blit(go_txt, (WIDTH // 2 - go_txt.get_width() // 2, 280))
            btn_restart.draw(screen)

        btn_back.draw(screen)
        pygame.display.flip()
        clock.tick(60)


# ==========================================
# 4. MINESWEEPER
# ==========================================
def run_minesweeper(mode, difficulty):
    font_title = pygame.font.SysFont("Arial", 36, bold=True)
    font_cell = pygame.font.SysFont("Arial", 20, bold=True)
    btn_back = Button(
        20, 20, 100, 40, "<- Back", RED, (255, 100, 100), TEXT_COLOR
    )
    btn_restart = Button(
        WIDTH // 2 - 75,
        540,
        150,
        40,
        "Play Again",
        ACCENT_COLOR,
        ACCENT_HOVER,
        TEXT_COLOR,
    )

    configs = {
        "Easy": (8, 8, 6),
        "Medium": (8, 8, 10),
        "Hard": (10, 10, 18),
    }
    ROWS, COLS, MINES = configs.get(difficulty, (8, 8, 10))
    cell_size = 35 if ROWS == 10 else 40
    start_x = (WIDTH - COLS * cell_size) // 2
    start_y = 130

    def create_board():
        b = [
            [
                {
                    "mine": False,
                    "revealed": False,
                    "flagged": False,
                    "count": 0,
                }
                for _ in range(COLS)
            ]
            for _ in range(ROWS)
        ]
        placed = 0
        while placed < MINES:
            rx, ry = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
            if not b[rx][ry]["mine"]:
                b[rx][ry]["mine"] = True
                placed += 1
        for r in range(ROWS):
            for c in range(COLS):
                if b[r][c]["mine"]:
                    continue
                cnt = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if (
                            0 <= nr < ROWS
                            and 0 <= nc < COLS
                            and b[nr][nc]["mine"]
                        ):
                            cnt += 1
                b[r][c]["count"] = cnt
        return b

    board = create_board()
    game_over = False
    won = False

    def reveal(r, c):
        nonlocal game_over, won
        if (
            not (0 <= r < ROWS and 0 <= c < COLS)
            or board[r][c]["revealed"]
            or board[r][c]["flagged"]
        ):
            return
        board[r][c]["revealed"] = True
        if board[r][c]["mine"]:
            game_over = True
            play_beep(150, 400)
            return
        if board[r][c]["count"] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    reveal(r + dr, c + dc)

    def check_win():
        for r in range(ROWS):
            for c in range(COLS):
                if not board[r][c]["mine"] and not board[r][c]["revealed"]:
                    return False
        return True

    running = True
    while running:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_back.is_clicked(event):
                return
            if btn_restart.is_clicked(event):
                board = create_board()
                game_over = False
                won = False

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and not game_over
                and not won
            ):
                mx, my = event.pos
                if (
                    start_x <= mx < start_x + COLS * cell_size
                    and start_y <= my < start_y + ROWS * cell_size
                ):
                    c = (mx - start_x) // cell_size
                    r = (my - start_y) // cell_size
                    if event.button == 1:
                        if not board[r][c]["flagged"]:
                            play_beep(500, 50)
                            reveal(r, c)
                            if not game_over and check_win():
                                won = True
                    elif event.button == 3:
                        if not board[r][c]["revealed"]:
                            board[r][c]["flagged"] = not board[r][c]["flagged"]
                            play_beep(300, 50)

        title = font_title.render(
            f"Minesweeper ({difficulty})", True, TEXT_COLOR
        )
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        for r in range(ROWS):
            for c in range(COLS):
                cell = board[r][c]
                rx = start_x + c * cell_size
                ry = start_y + r * cell_size
                rect = pygame.Rect(rx, ry, cell_size - 2, cell_size - 2)

                if cell["revealed"]:
                    if cell["mine"]:
                        pygame.draw.rect(screen, RED, rect, border_radius=4)
                    else:
                        pygame.draw.rect(
                            screen, PANEL_COLOR, rect, border_radius=4
                        )
                        if cell["count"] > 0:
                            txt = font_cell.render(
                                str(cell["count"]), True, ACCENT_COLOR
                            )
                            screen.blit(txt, txt.get_rect(center=rect.center))
                else:
                    pygame.draw.rect(screen, BTN_COLOR, rect, border_radius=4)
                    if cell["flagged"]:
                        f_txt = font_cell.render("F", True, RED)
                        screen.blit(f_txt, f_txt.get_rect(center=rect.center))

        if game_over or won:
            msg = "You Win!" if won else "Explosion! Game Over"
            color = GREEN if won else RED
            res_txt = font_title.render(msg, True, color)
            screen.blit(res_txt, (WIDTH // 2 - res_txt.get_width() // 2, 490))
            btn_restart.draw(screen)

        btn_back.draw(screen)
        pygame.display.flip()
        clock.tick(60)


# ==========================================
# 5. PONG (NOUVEAU JEU)
# ==========================================
def run_pong(mode, difficulty):
    font_title = pygame.font.SysFont("Arial", 36, bold=True)
    font_score = pygame.font.SysFont("Arial", 28, bold=True)
    btn_back = Button(
        20, 20, 100, 40, "<- Back", RED, (255, 100, 100), TEXT_COLOR
    )
    btn_restart = Button(
        WIDTH // 2 - 75,
        520,
        150,
        40,
        "Play Again",
        ACCENT_COLOR,
        ACCENT_HOVER,
        TEXT_COLOR,
    )

    paddle_heights = {"Easy": 100, "Medium": 80, "Hard": 60}
    p_h = paddle_heights.get(difficulty, 80)
    p_w = 15

    p1_y = HEIGHT // 2 - p_h // 2
    p2_y = HEIGHT // 2 - p_h // 2
    p1_score = 0
    p2_score = 0

    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = 4 if difficulty == "Easy" else (6 if difficulty == "Medium" else 8)
    ball_speed_y = 3 if difficulty == "Easy" else (5 if difficulty == "Medium" else 7)
    if random.choice([True, False]):
        ball_speed_x *= -1

    game_over = False
    winner_text = ""

    running = True
    while running:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_back.is_clicked(event):
                return

        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if btn_restart.is_clicked(event):
                    p1_score, p2_score = 0, 0
                    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                    game_over = False

            screen.fill(BG_COLOR)
            title = font_title.render("PONG", True, TEXT_COLOR)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
            w_txt = font_title.render(winner_text, True, GREEN)
            screen.blit(w_txt, (WIDTH // 2 - w_txt.get_width() // 2, 250))
            btn_restart.draw(screen)
            btn_back.draw(screen)
            pygame.display.flip()
            clock.tick(60)
            continue

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and p1_y > 100:
            p1_y -= 6
        if keys[pygame.K_s] and p1_y < HEIGHT - p_h - 20:
            p1_y += 6

        if mode == "2p":
            if keys[pygame.K_UP] and p2_y > 100:
                p2_y -= 6
            if keys[pygame.K_DOWN] and p2_y < HEIGHT - p_h - 20:
                p2_y += 6
        else:
            # Bot AI based on difficulty
            bot_speed = 3 if difficulty == "Easy" else (5 if difficulty == "Medium" else 7)
            if p2_y + p_h // 2 < ball_y:
                p2_y += bot_speed
            elif p2_y + p_h // 2 > ball_y:
                p2_y -= bot_speed
            p2_y = max(100, min(HEIGHT - p_h - 20, p2_y))

        # Ball movement
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Wall collisions top/bottom
        if ball_y <= 100 or ball_y >= HEIGHT - 20:
            ball_speed_y *= -1
            play_beep(300, 50)

        # Paddle collisions
        p1_rect = pygame.Rect(40, p1_y, p_w, p_h)
        p2_rect = pygame.Rect(WIDTH - 55, p2_y, p_w, p_h)
        ball_rect = pygame.Rect(ball_x - 8, ball_y - 8, 16, 16)

        if ball_rect.colliderect(p1_rect) and ball_speed_x < 0:
            ball_speed_x *= -1
            play_beep(600, 80)
        elif ball_rect.colliderect(p2_rect) and ball_speed_x > 0:
            ball_speed_x *= -1
            play_beep(600, 80)

        # Scoring
        if ball_x < 0:
            p2_score += 1
            play_beep(150, 200)
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_speed_x *= -1
        elif ball_x > WIDTH:
            p1_score += 1
            play_beep(150, 200)
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_speed_x *= -1

        if p1_score >= 5 or p2_score >= 5:
            game_over = True
            winner_text = "Player 1 Wins!" if p1_score >= 5 else ("Player 2 Wins!" if mode == "2p" else "Computer Wins!")

        # Draw Pong arena
        title = font_title.render(f"Pong ({difficulty})", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        score_text = font_score.render(f"{p1_score}   -   {p2_score}", True, ACCENT_COLOR)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 65))

        pygame.draw.line(screen, PANEL_COLOR, (0, 100), (WIDTH, 100), 2)
        pygame.draw.rect(screen, ACCENT_COLOR, p1_rect, border_radius=4)
        pygame.draw.rect(screen, RED, p2_rect, border_radius=4)
        pygame.draw.circle(screen, TEXT_COLOR, (ball_x, ball_y), 8)

        btn_back.draw(screen)
        pygame.display.flip()
        clock.tick(60)


# ==========================================
# 6. MEMORY MATCH (NOUVEAU JEU)
# ==========================================
def run_memory(mode, difficulty):
    font_title = pygame.font.SysFont("Arial", 36, bold=True)
    font_card = pygame.font.SysFont("Arial", 28, bold=True)
    font_text = pygame.font.SysFont("Arial", 20)
    btn_back = Button(
        20, 20, 100, 40, "<- Back", RED, (255, 100, 100), TEXT_COLOR
    )
    btn_restart = Button(
        WIDTH // 2 - 75,
        540,
        150,
        40,
        "Play Again",
        ACCENT_COLOR,
        ACCENT_HOVER,
        TEXT_COLOR,
    )

    pairs_count = {"Easy": 4, "Medium": 8, "Hard": 12}.get(difficulty, 8)
    total_cards = pairs_count * 2
    cols = 4 if pairs_count <= 8 else 6
    rows = total_cards // cols

    symbols = list(range(1, pairs_count + 1)) * 2
    random.shuffle(symbols)

    cards = []
    card_w, card_h = 75, 75
    start_x = (WIDTH - (cols * (card_w + 10))) // 2
    start_y = 150

    for i, sym in enumerate(symbols):
        r = i // cols
        c = i % cols
        rx = start_x + c * (card_w + 10)
        ry = start_y + r * (card_h + 10)
        cards.append(
            {
                "rect": pygame.Rect(rx, ry, card_w, card_h),
                "symbol": sym,
                "revealed": False,
                "matched": False,
            }
        )

    first_selection = None
    can_click = True
    timer = 0
    moves = 0
    matched_pairs = 0

    running = True
    while running:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_back.is_clicked(event):
                return
            if matched_pairs == pairs_count and btn_restart.is_clicked(event):
                return run_memory(mode, difficulty)

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and can_click
                and matched_pairs < pairs_count
            ):
                mx, my = event.pos
                for card in cards:
                    if card["rect"].collidepoint(mx, my) and not card["revealed"] and not card["matched"]:
                        card["revealed"] = True
                        play_beep(500, 50)
                        if first_selection is None:
                            first_selection = card
                        else:
                            moves += 1
                            if first_selection["symbol"] == card["symbol"]:
                                first_selection["matched"] = True
                                card["matched"] = True
                                matched_pairs += 1
                                play_beep(800, 100)
                                first_selection = None
                            else:
                                can_click = False
                                timer = pygame.time.get_ticks()

        if not can_click and pygame.time.get_ticks() - timer > 700:
            for card in cards:
                if not card["matched"]:
                    card["revealed"] = False
            first_selection = None
            can_click = True

        title = font_title.render(f"Memory Match ({difficulty})", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
        m_txt = font_text.render(f"Moves: {moves} | Pairs: {matched_pairs}/{pairs_count}", True, TEXT_COLOR)
        screen.blit(m_txt, (WIDTH // 2 - m_txt.get_width() // 2, 70))

        for card in cards:
            if card["revealed"] or card["matched"]:
                pygame.draw.rect(screen, PANEL_COLOR, card["rect"], border_radius=8)
                pygame.draw.rect(screen, ACCENT_COLOR, card["rect"], width=2, border_radius=8)
                s_surf = font_card.render(str(card["symbol"]), True, TEXT_COLOR)
                screen.blit(s_surf, s_surf.get_rect(center=card["rect"].center))
            else:
                pygame.draw.rect(screen, BTN_COLOR, card["rect"], border_radius=8)
                pygame.draw.rect(screen, (255, 255, 255), card["rect"], width=2, border_radius=8)

        if matched_pairs == pairs_count:
            win_txt = font_title.render("You Won!", True, GREEN)
            screen.blit(win_txt, (WIDTH // 2 - win_txt.get_width() // 2, 480))
            btn_restart.draw(screen)

        btn_back.draw(screen)
        pygame.display.flip()
        clock.tick(60)


# ==========================================
# 7. SETTINGS
# ==========================================
def run_settings():
    global global_volume
    font_title = pygame.font.SysFont("Arial", 36, bold=True)
    font_text = pygame.font.SysFont("Arial", 22)

    btn_back = Button(
        20, 20, 100, 40, "<- Back", RED, (255, 100, 100), TEXT_COLOR
    )
    btn_minus = Button(
        WIDTH // 2 - 120, 260, 50, 50, "-", BTN_COLOR, BTN_HOVER, TEXT_COLOR
    )
    btn_plus = Button(
        WIDTH // 2 + 70, 260, 50, 50, "+", BTN_COLOR, BTN_HOVER, TEXT_COLOR
    )
    btn_test = Button(
        WIDTH // 2 - 75,
        350,
        150,
        40,
        "Test Sound",
        ACCENT_COLOR,
        ACCENT_HOVER,
        TEXT_COLOR,
    )

    running = True
    while running:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_back.is_clicked(event):
                return
            if btn_minus.is_clicked(event):
                global_volume = max(0.0, round(global_volume - 0.1, 1))
            if btn_plus.is_clicked(event):
                global_volume = min(1.0, round(global_volume + 0.1, 1))
            if btn_test.is_clicked(event):
                play_beep(550, 150)

        title = font_title.render("Settings", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        vol_label = font_text.render(
            f"Sound Volume: {int(global_volume * 100)} %", True, TEXT_COLOR
        )
        screen.blit(vol_label, (WIDTH // 2 - vol_label.get_width() // 2, 200))

        bar_rect = pygame.Rect(WIDTH // 2 - 60, 275, 120, 20)
        pygame.draw.rect(screen, PANEL_COLOR, bar_rect, border_radius=5)
        fill_width = int(120 * global_volume)
        fill_rect = pygame.Rect(WIDTH // 2 - 60, 275, fill_width, 20)
        pygame.draw.rect(screen, ACCENT_COLOR, fill_rect, border_radius=5)

        btn_minus.draw(screen)
        btn_plus.draw(screen)
        btn_test.draw(screen)
        btn_back.draw(screen)

        pygame.display.flip()
        clock.tick(60)


# ==========================================
# MAIN MENU
# ==========================================
def main_menu():
    font_title = pygame.font.SysFont("Arial", 38, bold=True)

    btn_rps = Button(
        WIDTH // 2 - 160, 130, 320, 42, "Rock - Paper - Scissors", BTN_COLOR, BTN_HOVER, TEXT_COLOR, 18
    )
    btn_ttt = Button(
        WIDTH // 2 - 160, 185, 320, 42, "Tic-Tac-Toe", BTN_COLOR, BTN_HOVER, TEXT_COLOR, 18
    )
    btn_snake = Button(
        WIDTH // 2 - 160, 240, 320, 42, "Snake", BTN_COLOR, BTN_HOVER, TEXT_COLOR, 18
    )
    btn_mine = Button(
        WIDTH // 2 - 160, 295, 320, 42, "Minesweeper", BTN_COLOR, BTN_HOVER, TEXT_COLOR, 18
    )
    btn_pong = Button(
        WIDTH // 2 - 160, 350, 320, 42, "Pong", BTN_COLOR, BTN_HOVER, TEXT_COLOR, 18
    )
    btn_memory = Button(
        WIDTH // 2 - 160, 405, 320, 42, "Memory Match", BTN_COLOR, BTN_HOVER, TEXT_COLOR, 18
    )
    btn_settings = Button(
        WIDTH // 2 - 160, 475, 320, 42, "Settings (Sound)", ACCENT_COLOR, ACCENT_HOVER, TEXT_COLOR, 18
    )

    while True:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if btn_rps.is_clicked(event):
                mode, diff = select_mode_and_difficulty("Rock Paper Scissors")
                if mode:
                    run_rps(mode, diff)
            elif btn_ttt.is_clicked(event):
                mode, diff = select_mode_and_difficulty("Tic-Tac-Toe")
                if mode:
                    run_ttt(mode, diff)
            elif btn_snake.is_clicked(event):
                _, diff = select_mode_and_difficulty("Snake", False)
                if diff:
                    run_snake("vs_bot", diff)
            elif btn_mine.is_clicked(event):
                _, diff = select_mode_and_difficulty("Minesweeper", False)
                if diff:
                    run_minesweeper("vs_bot", diff)
            elif btn_pong.is_clicked(event):
                mode, diff = select_mode_and_difficulty("Pong")
                if mode:
                    run_pong(mode, diff)
            elif btn_memory.is_clicked(event):
                _, diff = select_mode_and_difficulty("Memory Match", False)
                if diff:
                    run_memory("vs_bot", diff)
            elif btn_settings.is_clicked(event):
                run_settings()

        title = font_title.render("CLASSIC RETRO ARCADE", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 45))

        btn_rps.draw(screen)
        btn_ttt.draw(screen)
        btn_snake.draw(screen)
        btn_mine.draw(screen)
        btn_pong.draw(screen)
        btn_memory.draw(screen)
        btn_settings.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
