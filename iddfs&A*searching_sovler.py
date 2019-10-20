from queue import PriorityQueue as PQ
import copy
import random
import math

def create_tile_puzzle(rows, cols):
    num_of_grid = rows*cols
    row, col = 0, 0
    board = [[0 for c in range(cols)]for r in range(rows)]
    if rows == 0 or cols == 0:
        return TilePuzzle(board)
    for i in range(num_of_grid):
        if not col == 0 and int(col % cols) == 0:
            row += 1
            col = 0
        board[row][col] = i+1
        col += 1
    board[rows-1][cols-1] = 0
    return TilePuzzle(board)


class TilePuzzle(object):
    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.f = 0
        self.move = []
        if not self.rows == 0 and not self.cols == 0 and self.board[self.rows-1][self.cols-1] == 0:
            self.empty_tile_loc = [self.rows-1, self.cols-1]
        else:
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.board[r][c] == 0:
                        self.empty_tile_loc = [r, c]

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        current_row, current_col = self.empty_tile_loc
        if direction == '':
            return True
        else:
            if direction.strip() == 'up' and current_row-1 >= 0:
                self.board[current_row][current_col] = self.board[current_row-1][current_col]
                self.board[current_row-1][current_col] = 0
                self.empty_tile_loc = [current_row-1, current_col]
                return True
            if direction.strip() == 'down' and current_row+1 < self.rows:
                self.board[current_row][current_col] = self.board[current_row+1][current_col]
                self.board[current_row+1][current_col] = 0
                self.empty_tile_loc = [current_row+1, current_col]
                return True
            if direction.strip() == 'left' and current_col-1 >= 0:
                self.board[current_row][current_col] = self.board[current_row][current_col-1]
                self.board[current_row][current_col-1] = 0
                self.empty_tile_loc = [current_row, current_col-1]
                return True
            if direction.strip() == 'right' and current_col+1 < self.cols:
                self.board[current_row][current_col] = self.board[current_row][current_col+1]
                self.board[current_row][current_col+1] = 0
                self.empty_tile_loc = [current_row, current_col+1]
                return True
        return False

    def scramble(self, num_moves):
        for i in range(num_moves):
            moves = random.choice(['up', 'down', 'left', 'right'])
            self.perform_move(moves)

    def is_solved(self):
        if self.board == create_tile_puzzle(self.rows, self.cols).board:
            return True
        return False

    def copy(self):
        board_copy = copy.deepcopy(self.board)
        return TilePuzzle(board_copy)

    def successors(self):
        choice = ['up   ', 'down ', 'left ', 'right']
        for move in choice:
            successor = self.copy()
            if successor.perform_move(move):
                yield (move.strip(), successor)

    # Required
    def find_solutions_iddfs(self):
        limit, moves = 0, []
        found = False
        while not found:
            for move in self.iddfs_helper(limit, moves):
                yield move
                found = True
            limit += 1

    def iddfs_helper(self, limit, moves):
        if self.is_solved() and limit == 0:
            yield moves
        elif limit > 0:
            for move, children_node in self.successors():
                yield from children_node.iddfs_helper(limit-1, moves+[move])

    # Required
    def find_solution_a_star(self):
        open_q = PQ()
        visited = set()
        index = 0
        self.f = self.find_manhattan_dis()
        open_q.put((self.f, index, self))
        while not open_q.empty():
            get_node = open_q.get()
            parent_node = get_node[2]
            if parent_node.is_solved():
                return parent_node.move
            for move, children_node in parent_node.successors():
                temp_node = tuple(tuple(element) for element in children_node.board)
                if temp_node not in visited:
                    index += 1
                    children_node.f = parent_node.f + children_node.find_manhattan_dis()
                    children_node.move = parent_node.move + [move]
                    visited.add(temp_node)
                    open_q.put((children_node.f, index, children_node))

    def find_manhattan_dis(self):
        board_compared = create_tile_puzzle(self.rows, self.cols)
        manhattan_dis = 0
        trace_dic = {}
        for r in range(self.rows):
            for c in range(self.cols):
                trace_dic[board_compared.board[r][c]] = [r, c]
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.board[r][c] == board_compared.board[r][c] and not self.board[r][c] == 0:
                    manhattan_dis += abs(r-trace_dic[self.board[r][c]][0]) + abs(c-trace_dic[self.board[r][c]][1])
        return manhattan_dis
