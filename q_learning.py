import random
import sqlite3

# Set up the database
def setup_database():
    conn = sqlite3.connect("tictactoe_agent.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS q_values (
                        state TEXT NOT NULL,
                        action TEXT NOT NULL,
                        value REAL NOT NULL,
                        PRIMARY KEY (state, action)
                    )''')
    conn.commit()
    conn.close()

setup_database()

# Q-learning parameters
alpha = 0.1
gamma = 0.9
epsilon = 0.2

# Initialize Q-table
Q = {}

# Initialize the board
board = [[' ' for _ in range(3)] for _ in range(3)]

def board_to_string(board):
    return ''.join([''.join(row) for row in board])

def available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    if ' ' not in board_to_string(board):
        return 'Draw'
    return None

def get_q_value(state, action):
    if state not in Q:
        Q[state] = {}
    if action not in Q[state]:
        Q[state][action] = 0
    return Q[state][action]

def choose_action(state, available_actions):
    if random.uniform(0, 1) < epsilon:
        return random.choice(available_actions)
    q_values = [get_q_value(state, action) for action in available_actions]
    max_q_value = max(q_values)
    return available_actions[q_values.index(max_q_value)]

def play_game():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'

    while winner(board) is None:
        if current_player == 'X':
            i, j = agent_move(board)
        else:
            print_board(board)
            i, j = human_move(board)
        board[i][j] = current_player
        current_player = 'O' if current_player == 'X' else 'X'

    print_board(board)
    result = winner(board)
    if result == 'Draw':
        print("It's a draw!")
    else:
        print(f"Player {result} wins!")

def print_board(board):
    for i, row in enumerate(board):
        print(' | '.join(row))
        if i < 2:  # Only print the separator if it's not the last row
            print('- ' * 5)

def human_move(board):
    while True:
        move = input("Enter your move (row col): ").split()
        if len(move) != 2:
            print("Invalid input. Enter row and column separated by space.")
            continue
        i, j = int(move[0])-1, int(move[1])-1
        if 0 <= i < 3 and 0 <= j < 3 and board[i][j] == ' ':
            return i, j
        else:
            print("Invalid move. Try again.")

def agent_move(board):
    state = board_to_string(board)
    action = choose_action(state, available_moves(board))
    next_board = [row.copy() for row in board]
    next_board[action[0]][action[1]] = 'X'
    reward = 0
    next_state = board_to_string(next_board)
    if winner(next_board) == 'X':
        reward = 1
    elif winner(next_board) == 'O':
        reward = -1
    elif winner(next_board) == 'Draw':
        reward = 0.5
    else:
        reward = -0.01  # Small negative reward for each move
        next_max_q_value = max([get_q_value(next_state, next_action) for next_action in available_moves(next_board)], default=0)
        reward += gamma * next_max_q_value

    Q[state][action] = get_q_value(state, action) + alpha * (reward - get_q_value(state, action))
    save_q_value(state, action, Q[state][action])
    return action

def decrease_epsilon():
    global epsilon
    epsilon *= 0.995  # Decrease epsilon by 0.5% each time

def load_all_q_values():
    global Q
    conn = sqlite3.connect("tictactoe_agent.db")
    cursor = conn.cursor()
    cursor.execute("SELECT state, action, value FROM q_values")
    for state, action, value in cursor.fetchall():
        if state not in Q:
            Q[state] = {}
        Q[state][eval(action)] = value
    conn.close()

def save_q_value(state, action, value):
    conn = sqlite3.connect("tictactoe_agent.db")
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO q_values (state, action, value) VALUES (?, ?, ?)", (state, str(action), value))
    conn.commit()
    conn.close()


def save_all_q_values():
    conn = sqlite3.connect("tictactoe_agent.db")
    cursor = conn.cursor()
    for state, actions in Q.items():
        for action, value in actions.items():
            cursor.execute("REPLACE INTO q_values (state, action, value) VALUES (?, ?, ?)", (state, str(action), value))
    conn.commit()
    conn.close()

load_all_q_values()
for _ in range(100):  # Play 100 games
    play_game()
    decrease_epsilon()
    if _ % 10 == 0:  # Save Q-values to the database every 10 games
        save_all_q_values()
save_all_q_values()  # Save Q-values at the end
