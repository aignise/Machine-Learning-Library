import sqlite3

"""
SETTING UP DATABASE
"""
db_link = sqlite3.connect("tictactoe.db")
cursor = db_link.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS game_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    move_order INTEGER NOT NULL,
    board_state TEXT NOT NULL,
    move_made TEXT NOT NULL,
    immediate_reward INTEGER NOT NULL,
    final_reward INTEGER NOT NULL,
    win_percentage REAL DEFAULT 0.0
    )
''')

db_link.commit()
db_link.close()

def get_next_game_id():
    conn = sqlite3.connect('tictactoe.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(game_id) FROM game_data")
    max_game_id = cursor.fetchone()[0]
    conn.close()
    return (max_game_id or 0) + 1

def board_to_string():
    return "".join("".join(row) for row in board)

def store_move(game_id, move_order, board_state, move_made, immediate_reward, final_reward):
    conn = sqlite3.connect('tictactoe.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO game_data (game_id, move_order, board_state, move_made, immediate_reward, final_reward)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (game_id, move_order, board_state, move_made, immediate_reward, final_reward))
    conn.commit()
    conn.close()

board = [["", "", ""], ["", "", ""], ["", "", ""]]
winner = None

def game_board():
    print("   A   B   C")
    row_num = 1
    for row in board:
        print(row_num, row)
        row_num += 1
    print("")

def make_move(player):
    global board, move_order, winner
    valid_move = False
    immediate_reward = 0

    while not valid_move:
        try:
            row = int(input("Row (1-3): ")) - 1
            if row not in [0, 1, 2]:
                print("Row should be between 1 and 3.")
                continue

            col_map = {"A": 0, "B": 1, "C": 2}
            col = col_map[input("Column (A-C): ").upper()]

            if board[row][col]:
                print("Cell already occupied. Try a different one.")
            else:
                valid_move = True
                board[row][col] = 'X' if player == 1 else 'O'
                move_order += 1

                check_win()
                if winner:
                    if winner == 'X':
                        immediate_reward = 1
                    elif winner == 'O':
                        immediate_reward = -1

                store_move(game_id, move_order, board_to_string(), f"{row},{col}", immediate_reward, 0)

        except (ValueError, KeyError):
            print("Invalid input. Please provide valid row (1-3) and column (A-C).")

def check_win():
    global winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0]:
            winner = board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i]:
            winner = board[0][i]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
        winner = board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        winner = board[0][2]

    if winner:
        print(f"Winner is {winner}")

def play_game():
    global move_order, game_id
    move_order = 0
    game_id = get_next_game_id()
    player = 1
    while not winner and any("" in row for row in board):  
        game_board()
        print(f"Player {player}'s turn")
        make_move(player)
        player = 3 - player  

    final_reward = 0
    if winner == 'X':
        final_reward = 1
    elif winner == 'O':
        final_reward = -1

    conn = sqlite3.connect('tictactoe.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE game_data SET final_reward = ? WHERE game_id = ?", (final_reward, game_id))
    conn.commit()
    conn.close()

    # Fetch all moves made in this game
    conn = sqlite3.connect('tictactoe.db')
    cursor = conn.cursor()
    cursor.execute("SELECT board_state, move_made FROM game_data WHERE game_id = ?", (game_id,))
    moves = cursor.fetchall()
    conn.close()

    for move in moves:
        board_state, action = move
        update_win_percentage(board_state, action)

    if not winner:
        print("It's a draw!")
    else:
        game_board()

def update_win_percentage(board_state, action):
    conn = sqlite3.connect('tictactoe.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT final_reward FROM game_data WHERE board_state = ? AND move_made = ?", (board_state, action))
    outcomes = cursor.fetchall()
    
    wins = sum(1 for outcome in outcomes if outcome[0] == 1)
    total_games = len(outcomes)
    win_percentage = (wins / total_games) * 100
    
    cursor.execute("UPDATE game_data SET win_percentage = ? WHERE board_state = ? AND move_made = ?", (win_percentage, board_state, action))
    
    conn.commit()
    conn.close()

play_game()
