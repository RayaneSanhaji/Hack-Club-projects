import random
import tkinter as tk
from tkinter import messagebox
class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Tic-Tac-Toe")
        self.root.geometry("400x500")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.scores = {"X": 0, "O": 0, "Nuls": 0}
        self.game_mode = "ai"  # 'ai' ou 'pvp'

        self.create_widgets()

    def create_widgets(self):
        # Titre
        title_label = tk.Label(
            self.root, 
            text="TIC-TAC-TOE", 
            font=("Arial", 22, "bold"), 
            bg="#1e1e2e", 
            fg="#cdd6f4"
        )
        title_label.pack(pady=10)

        # Scores
        self.score_label = tk.Label(
            self.root, 
            text="Joueur (X): 0 | IA/J2 (O): 0 | Nuls: 0", 
            font=("Arial", 11), 
            bg="#1e1e2e", 
            fg="#a6e3a1"
        )
        self.score_label.pack(pady=5)

        # Bouton de changement de mode
        mode_frame = tk.Frame(self.root, bg="#1e1e2e")
        mode_frame.pack(pady=5)

        self.mode_btn = tk.Button(
            mode_frame, 
            text="Mode : Contre l'IA (Imbattable)", 
            font=("Arial", 10, "bold"), 
            bg="#89b4fa", 
            fg="#11111b", 
            command=self.toggle_mode,
            relief="flat",
            padx=10,
            pady=5
        )
        self.mode_btn.pack()

        # Grille de jeu (9 boutons)
        self.grid_frame = tk.Frame(self.root, bg="#313244", bd=2, relief="solid")
        self.grid_frame.pack(pady=15)

        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.grid_frame, 
                text="", 
                font=("Arial", 24, "bold"), 
                width=4, 
                height=2, 
                bg="#45475a", 
                fg="#cdd6f4",
                activebackground="#585b70",
                activeforeground="#cdd6f4",
                relief="flat",
                command=lambda idx=i: self.make_move(idx)
            )
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.buttons.append(btn)

        # Bouton Réinitialiser
        control_frame = tk.Frame(self.root, bg="#1e1e2e")
        control_frame.pack(pady=10)

        reset_btn = tk.Button(
            control_frame, 
            text="Nouvelle Partie", 
            font=("Arial", 11, "bold"), 
            bg="#f38ba8", 
            fg="#11111b", 
            command=self.reset_board,
            relief="flat",
            padx=15,
            pady=8
        )
        reset_btn.pack()

    def toggle_mode(self):
        if self.game_mode == "ai":
            self.game_mode = "pvp"
            self.mode_btn.config(text="Mode : Joueur vs Joueur", bg="#fab387")
        else:
            self.game_mode = "ai"
            self.mode_btn.config(text="Mode : Contre l'IA (Imbattable)", bg="#89b4fa")
        self.reset_board()

    def make_move(self, idx):
        if self.board[idx] == " ":
            self.board[idx] = self.current_player
            self.buttons[idx].config(
                text=self.current_player, 
                fg="#89b4fa" if self.current_player == "X" else "#f38ba8"
            )

            if self.check_winner(self.current_player):
                messagebox.showinfo("Fin de partie", f"Le joueur {self.current_player} a gagné !")
                self.scores[self.current_player] += 1
                self.update_score_label()
                self.reset_board()
                return

            if self.is_full():
                messagebox.showinfo("Fin de partie", "Match nul !")
                self.scores["Nuls"] += 1
                self.update_score_label()
                self.reset_board()
                return

            # Alternance des joueurs
            self.current_player = "O" if self.current_player == "X" else "X"

            # Tour de l'IA si activé
            if self.game_mode == "ai" and self.current_player == "O":
                self.root.after(300, self.ai_move)

    def ai_move(self):
        move = self.minimax_decision()
        if move is not None:
            self.board[move] = "O"
            self.buttons[move].config(text="O", fg="#f38ba8")

            if self.check_winner("O"):
                messagebox.showinfo("Fin de partie", "L'IA a gagné !")
                self.scores["O"] += 1
                self.update_score_label()
                self.reset_board()
                return

            if self.is_full():
                messagebox.showinfo("Fin de partie", "Match nul !")
                self.scores["Nuls"] += 1
                self.update_score_label()
                self.reset_board()
                return

            self.current_player = "X"

    def check_winner(self, letter):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        return any(all(self.board[i] == letter for i in combo) for combo in wins)

    def is_full(self):
        return " " not in self.board

    def reset_board(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        for btn in self.buttons:
            btn.config(text="")

    def update_score_label(self):
        self.score_label.config(
            text=f"Joueur (X): {self.scores['X']} | IA/J2 (O): {self.scores['O']} | Nuls: {self.scores['Nuls']}"
        )

    # Algorithme Minimax pour l'IA imbattable
    def minimax_decision(self):
        best_score = -float('inf')
        best_move = None
        for move in range(9):
            if self.board[move] == " ":
                self.board[move] = "O"
                score = self.minimax(0, False)
                self.board[move] = " "
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_move

    def minimax(self, depth, is_maximizing):
        if self.check_winner("O"):
            return 10 - depth
        if self.check_winner("X"):
            return depth - 10
        if self.is_full():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for move in range(9):
                if self.board[move] == " ":
                    self.board[move] = "O"
                    score = self.minimax(depth + 1, False)
                    self.board[move] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in range(9):
                if self.board[move] == " ":
                    self.board[move] = "X"
                    score = self.minimax(depth + 1, True)
                    self.board[move] = " "
                    best_score = min(score, best_score)
            return best_score

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
