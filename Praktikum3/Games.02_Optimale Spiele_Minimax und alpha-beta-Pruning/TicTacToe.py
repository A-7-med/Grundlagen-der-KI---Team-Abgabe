
# Tic Tac Toe – Minimax und Alpha-Beta-Pruning


import math

# Board-Layout (Index):
# 0 1 2
# 3 4 5
# 6 7 8

USE_ORDERED_SUCCESSORS = True

def print_board(board):
    for i in range(0, 9, 3):
        def ch(x): return x if x else '.'
        print(ch(board[i]), ch(board[i+1]), ch(board[i+2]))
    print()

# Spielregeln

def winner(board):
    lines = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def terminal_test(board):
    return winner(board) is not None or all(board)

def utility(board):
    w = winner(board)
    if w == 'X': return 1
    if w == 'O': return -1
    return 0

# Nachfolger

def successors_left_to_right(board, player):
    moves = []
    for i in range(9):
        if board[i] == '':
            nb = board.copy()
            nb[i] = player
            moves.append((i, nb))
    return moves

def successors_ordered(board, player):
    order = [4, 0, 2, 6, 8, 1, 3, 5, 7]  # Mitte, Ecken, Kanten
    moves = []
    for i in order:
        if board[i] == '':
            nb = board.copy()
            nb[i] = player
            moves.append((i, nb))
    return moves

def successors(board, player):
    return successors_ordered(board, player) if USE_ORDERED_SUCCESSORS else successors_left_to_right(board, player)

# 1) Minimax

def max_value(board):
    if terminal_test(board): return utility(board)
    v = -math.inf
    for a, s in successors(board, 'X'):
        v = max(v, min_value(s))
    return v

def min_value(board):
    if terminal_test(board): return utility(board)
    v = math.inf
    for a, s in successors(board, 'O'):
        v = min(v, max_value(s))
    return v

def minimax(board):
    best_val = -math.inf
    best_action = None
    for a, s in successors(board, 'X'):
        v = min_value(s)
        if v > best_val:
            best_val, best_action = v, a
    return best_action, best_val

# 2) Alpha-Beta-Pruning (Vorlesungsstil)

def max_value_ab(board, alpha, beta):
    if terminal_test(board): return utility(board)
    v = -math.inf
    for a, s in successors(board, 'X'):
        v = max(v, min_value_ab(s, alpha, beta))
        if v >= beta: return v
        alpha = max(alpha, v)
    return v

def min_value_ab(board, alpha, beta):
    if terminal_test(board): return utility(board)
    v = math.inf
    for a, s in successors(board, 'O'):
        v = min(v, max_value_ab(s, alpha, beta))
        if v <= alpha: return v
        beta = min(beta, v)
    return v

def alphabeta(board):
    best_val = -math.inf
    best_action = None
    alpha, beta = -math.inf, math.inf
    for a, s in successors(board, 'X'):
        v = min_value_ab(s, alpha, beta)
        if v > best_val:
            best_val, best_action = v, a
        alpha = max(alpha, v)
    return best_action, best_val

# Zählvarianten für Aufgabe 3

def minimax_with_count(board):
    nodes = 0
    def MAX(b):
        nonlocal nodes
        nodes += 1
        if terminal_test(b): return utility(b)
        v = -math.inf
        for _, s in successors(b, 'X'):
            v = max(v, MIN(s))
        return v
    def MIN(b):
        nonlocal nodes
        nodes += 1
        if terminal_test(b): return utility(b)
        v = math.inf
        for _, s in successors(b, 'O'):
            v = min(v, MAX(s))
        return v
    best_val = -math.inf
    best_action = None
    for a, s in successors(board, 'X'):
        v = MIN(s)
        if v > best_val:
            best_val, best_action = v, a
    return best_action, best_val, nodes

def alphabeta_with_count(board):
    nodes = 0
    def MAX(b, alpha, beta):
        nonlocal nodes
        nodes += 1
        if terminal_test(b): return utility(b)
        v = -math.inf
        for _, s in successors(b, 'X'):
            v = max(v, MIN(s, alpha, beta))
            if v >= beta: return v
            alpha = max(alpha, v)
        return v
    def MIN(b, alpha, beta):
        nonlocal nodes
        nodes += 1
        if terminal_test(b): return utility(b)
        v = math.inf
        for _, s in successors(b, 'O'):
            v = min(v, MAX(s, alpha, beta))
            if v <= alpha: return v
            beta = min(beta, v)
        return v
    best_val = -math.inf
    best_action = None
    alpha, beta = -math.inf, math.inf
    for a, s in successors(board, 'X'):
        v = MIN(s, alpha, beta)
        if v > best_val:
            best_val, best_action = v, a
        alpha = max(alpha, v)
    return best_action, best_val, nodes

# Demo

if __name__ == "__main__":
    # leeres Brett
    board = [''] * 9
    print("Startzustand:")
    print_board(board)

    # 1) Minimax und 2) Alpha-Beta
    move, val = minimax(board)
    print("Minimax wählt Feld", move, "mit Bewertung", val)

    move_ab, val_ab = alphabeta(board)
    print("Alpha-Beta wählt Feld", move_ab, "mit Bewertung", val_ab)

    # 3) Knotenvergleich
    m_move, m_val, m_nodes = minimax_with_count(board)
    a_move, a_val, a_nodes = alphabeta_with_count(board)
    print("\nKnotenvergleich (Startzustand, USE_ORDERED_SUCCESSORS =", USE_ORDERED_SUCCESSORS, ")")
    print("Minimax:   move =", m_move, "value =", m_val, "nodes =", m_nodes)
    print("AlphaBeta: move =", a_move, "value =", a_val, "nodes =", a_nodes)

    # Beispielposition zum Test
    mid = [
        'X','O','X',
        '','O','',
        '','',''
    ]
    print("\nBeispielposition:")
    print_board(mid)

    m2_move, m2_val, m2_nodes = minimax_with_count(mid)
    a2_move, a2_val, a2_nodes = alphabeta_with_count(mid)
    print("Minimax:   move =", m2_move, "value =", m2_val, "nodes =", m2_nodes)
    print("AlphaBeta: move =", a2_move, "value =", a2_val, "nodes =", a2_nodes)
