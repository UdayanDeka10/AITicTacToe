import sys
import pygame
import numpy as np
import random
import copy
from constants import *

#PYGAME SETUP
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill(BG_COLOR)

#CLASSES
class Board():
    def __init__(self) -> None:
        self.squares = np.zeros((ROWS, COLS))
        #[squares]
        self.empty_squares = self.squares
        self.marked_squares = 0
    
    def final_state(self, show = False):
        '''
            @return 0 if there is no win YET (not necessarily a draw)
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''
        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQ_SIZE + SQ_SIZE // 2, 20)
                    fPos = (col * SQ_SIZE + SQ_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
            
        #horiz wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQ_SIZE + SQ_SIZE // 2)
                    fPos = (WIDTH - 20, row * SQ_SIZE + SQ_SIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]
            
        #desc diag
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                    color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                    iPos = (20, 20)
                    fPos = (WIDTH - 20, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]
        
        #asc diag
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] !=0:
            if show:
                    color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                    iPos = (20, HEIGHT - 20)
                    fPos = (WIDTH - 20, 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]
        
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def empty_square(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))
        return empty_squares
    
    def is_full(self):
        return self.marked_squares == 9
    
    def is_empty(self):
        return self.marked_squares == 0
    
class AI():

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player
    
    def rnd(self, board):
        empty_sqrs = board.get_empty_squares()
        index = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[index]
    
    def minimax(self, board, maximizing):
        case = board.final_state()

        #base case: player 1 wins
        if case == 1:
            return 1, None #eval, move
        #base case: player 2 wins
        if case == 2:
            return -1, None
        #base case: draw
        elif board.is_full():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_squares()
            
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, True)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_squares()
            
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, False)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            
            return min_eval, best_move


    def eval(self, main_board):
        if self.level == 0:
            eval = 'random'
            move = self.rnd(main_board)
        else:
            #recursive backtracking
            eval, move = self.minimax(main_board, False)
            
        print(f'AI has chosen ro mark the square in pos {move} with an eval of: {eval}')
        return move

class Game:
    def __init__(self):
        self.board = Board()
        #which is next player to mark a square
        self.ai = AI()
        self.player = 2 # 1-cross 2-circle
        self.game_mode = 'AI' # or 'ai'
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        screen.fill(BG_COLOR)
        #vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQ_SIZE, 0), (SQ_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQ_SIZE, 0), (WIDTH - SQ_SIZE, HEIGHT), LINE_WIDTH)
        #horiz lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQ_SIZE), (WIDTH, SQ_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQ_SIZE), (WIDTH, HEIGHT - SQ_SIZE), LINE_WIDTH)
    
    def next_turn(self):
        self.player = self.player % 2 + 1
    
    def draw_fig(self, row, col):

        if self.player == 1:
            #desc line
            start_desc = (col * SQ_SIZE + OFFSET, row * SQ_SIZE + OFFSET)
            end_desc = (col * SQ_SIZE + SQ_SIZE - OFFSET, row * SQ_SIZE + SQ_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            #asc
            start_asc = (col * SQ_SIZE + OFFSET, row * SQ_SIZE + SQ_SIZE - OFFSET)
            end_asc = (col * SQ_SIZE + SQ_SIZE - OFFSET, row * SQ_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        else:

            CENTER = (col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, CENTER, RADIUS, CIRC_WIDTH)
    
    def change_game_mode(self):
        if self.game_mode == 'AI':
            self.game_mode = 'PVP'
        else:
            self.game_mode = 'AI'
    
    def reset(self):
        self.__init__()
    
    def is_over(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()


def main():
    #ogj

    game = Game()
    board = game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    game.change_game_mode()

                if event.key == pygame.K_0:
                    ai.level = 0

                if event.key == pygame.K_1:
                    ai.level = 1

                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                #row is y
                row = pos[1] // SQ_SIZE
                col = pos[0] // SQ_SIZE
                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)
            
                if game.is_over():
                    game.running = False

            if game.game_mode == 'AI' and game.player == ai.player and game.running:
                pygame.display.update()

                row, col = ai.eval(board)
                
                game.make_move(row, col)
                if game.is_over():
                    game.running = False
                
        pygame.display.update()

main()
