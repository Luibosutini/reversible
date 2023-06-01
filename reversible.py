import tkinter as tk
from tkinter import messagebox

# 定数
BOARD_SIZE = 8
EMPTY = 0
BLACK = 1
WHITE = 2

# ゲームの状態を表す変数
current_player = BLACK
game_board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
game_board[3][3] = game_board[4][4] = BLACK
game_board[3][4] = game_board[4][3] = WHITE

# プレイヤーがマスをクリックしたときの処理
def cell_click(row, col):
    global current_player, game_board
    
    # 既に石が置かれている場合は処理しない
    if game_board[row][col] != EMPTY:
        return
    

    # 石を挟む処理
    flipped = []
    for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        r, c = row, col
        flipped_direction = []
        r += drow
        c += dcol
        while r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and game_board[r][c] == opponent(current_player):
            flipped_direction.append((r, c))
            r += drow
            c += dcol
        if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and game_board[r][c] == current_player:
            flipped.extend(flipped_direction)
    
    # 石が挟めない場合はパスとする
    if len(flipped) == 0:
        if not can_place_stone(current_player):
            current_player = opponent(current_player)
        return
    
    # 石をひっくり返す
    for r, c in flipped:
        game_board[r][c] = current_player
    
    # 石を置く
    game_board[row][col] = current_player
    
    # マスの表示を更新する
    update_board()
    
    # 勝敗判定を行う
    if not can_place_stone(opponent(current_player)):
        if not can_place_stone(current_player):
            end_game()        
    
    # プレイヤーを切り替える
    current_player = opponent(current_player)
    
# 相手の色を返す関数
def opponent(player):
    if player == BLACK:
        return WHITE
    else:
        return BLACK

# 石を置けるかどうかを判定する関数
def can_place_stone(player):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if game_board[row][col] == EMPTY:
                for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    r, c = row, col
                    r += drow
                    c += dcol
                    if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and game_board[r][c] == opponent(player):
                        r += drow
                        c += dcol
                        while r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and game_board[r][c] == opponent(player):
                            r += drow
                            c += dcol
                        if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and game_board[r][c] == player:
                            return True

# ゲーム終了時の処理
def end_game():
    black_count = sum(row.count(BLACK) for row in game_board)
    white_count = sum(row.count(WHITE) for row in game_board)
    if black_count > white_count:
        winner = "黒"
    elif white_count > black_count:
        winner = "白"
    else:
        winner = "引き分け"
    messagebox.showinfo("終局", f"ゲーム終了\n勝者: {winner}\n黒: {black_count} 石\n白: {white_count} 石")
    reset_game()

# ゲームをリセットする関数
def reset_game():
    global current_player, game_board
    current_player = BLACK
    game_board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    game_board[3][3] = game_board[4][4] = BLACK
    game_board[3][4] = game_board[4][3] = WHITE
    update_board()
# マスの表示を更新する関数
def update_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if game_board[row][col] == BLACK:
                buttons[row][col].configure(text="●", bg="black", fg="white")
            elif game_board[row][col] == WHITE:
                buttons[row][col].configure(text="●", bg="white", fg="black")
            else:
                buttons[row][col].configure(text="", bg="green")

# メインウィンドウを作成
window = tk.Tk()
window.title("リバーシ")

# ボタンを作成
buttons = []
for row in range(BOARD_SIZE):
    button_row = []
    for col in range(BOARD_SIZE):
        button = tk.Button(window, text="", width=4, height=2, command=lambda r=row, c=col: cell_click(r, c))
        button.grid(row=row, column=col)
        button_row.append(button)
    buttons.append(button_row)

# ゲームをリセットするボタン
reset_button = tk.Button(window, text="リセット", command=reset_game)
reset_button.grid(row=BOARD_SIZE, columnspan=BOARD_SIZE)

# マスの表示を初期化
update_board()

# メインループを開始
window.mainloop()