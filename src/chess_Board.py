import pygame

from const import *
from chess_Square import *
from chess_Pieces import *
from chess_Dragger import *

# THIS FILE CONTAINS THE CLASS THAT DEALS WITH EVERYTHING ON BOARD

class chess_Board:
    
    def __init__(self, screen):
        
        self.screen = screen
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        self.display_bg(self.screen) # DISPLAY CHESS BOARD
        self.dragger = chess_Dragger()
        self.create_empty_squares() # CREATE EMPTY SQUARES
        self.create_pieces() # CREATE CHESS BOARD PIECES

    def create_empty_squares(self): # FUNC TO CREATE SQUARES AS OBJECT OF CH_SQ CLASS TO STORE VALUES
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = chess_Square(row,col)

    def create_pieces(self): # FUNC TO CREATE COLOR PIECES
        self.create_color_pieces(color = 'white')
        self.create_color_pieces(color = 'black')

    def create_color_pieces(self, color): # FUNC TO CREATE ALL PIECES
        
        # ROW SELECTOR
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
        
        # PAWNS
        for col in range(COLS):
            self.squares[row_pawn][col] = chess_Square(row_pawn, col, Pawn(color))
            
        # KNIGHTS
        self.squares[row_other][1] = chess_Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = chess_Square(row_other, 6, Knight(color))
        
        # BISHOPS
        self.squares[row_other][2] = chess_Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = chess_Square(row_other, 5, Bishop(color))
        
        # ROOKS
        self.squares[row_other][0] = chess_Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = chess_Square(row_other, 7, Rook(color))
        
        # QUEEN
        self.squares[row_other][3] = chess_Square(row_other, 3, Queen(color))
        
        # KING
        self.squares[row_other][4] = chess_Square(row_other, 4, King(color))

    def display_bg(self, screen): # FUNC TO DISPLAY THE CHESS BOARD
        
        for row in range(ROWS):
            for col in range(COLS):
                color = (234,235,200) if (row + col) % 2 == 0 else (119,154,88)
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(screen, color, rect)

    def display_pieces(self, screen, dragging_piece=None): # FUNC TO DISPLAY CHESS PIECES
        
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece(): # CHECK IF SQ IS EMPTY
                    
                    piece =  self.squares[row][col].piece
                    
                    if piece is not dragging_piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        screen.blit(img, piece.texture_rect)
                        
    def calc_moves(self, piece, row, col): #FUNC TO CALC VALID MOVES FOR CLICKED PIECE
        
        def create_moves(row,col,possible_move_row,possible_move_col): # CREATE VALID MOVES FOR A PIECE
            
            initial = chess_Square(row,col) # INITIAL POS
            final = chess_Square(possible_move_row,possible_move_col) # FINAL POS
            
            move = chess_Move(initial,final) # CREATE OBJ OF MOVE CLASS
            piece.add_move(move) # ADD MOVE TO MOVES LIST OF THAT PIECE
        
        def knight_moves(): # CALC VALID MOVES FOR KNIGHT
            possible_moves = [
                (row-2, col+1),
                (row-2, col-1),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col+2),
                (row-1, col+2),
                (row+1, col-2),
                (row-1, col-2),
            ]
            
            for pos_move in possible_moves:
                possible_move_row, possible_move_col = pos_move
                
                if chess_Square.in_range(possible_move_row,possible_move_col): # CHECK IF SQUARE IS IN BOARD
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color): # CHECK IF SQ IS EMPTY OR ENEMY
                        
                        create_moves(row,col,possible_move_row,possible_move_col)
        
        def pawn_moves(): # CALC VALID MOVES FOR PAWN
            
            steps = 1 if piece.moved else 2
            
            # VERTICAL MOVES
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            
            for possible_move_row in range(start, end, piece.dir):
                
                if chess_Square.in_range(possible_move_row) and self.squares[possible_move_row][col].isempty(): # CHECK IF MOVES ARE VALID   
                    
                    create_moves(row,col,possible_move_row,col)
                    
                else: break
                
            # DIAGONAL MOVES
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            
            for possible_move_col in possible_move_cols:
                if chess_Square.in_range(possible_move_col) and self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                    
                    create_moves(row,col,possible_move_row,possible_move_col)
                    
        def straightline_moves(increment):
            
            if self.squares[row][col].piece.name == 'king':
                for inc in increment:
                    row_inc, col_inc = inc
                    possible_move_row = row + row_inc
                    possible_move_col = col + col_inc
                    
                    if chess_Square.in_range(possible_move_row,possible_move_col) and self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        create_moves(row, col, possible_move_row, possible_move_col)
            
            else:
                for inc in increment:
                    row_inc, col_inc = inc
                    possible_move_row = row + row_inc
                    possible_move_col = col + col_inc
                    
                    while chess_Square.in_range(possible_move_row,possible_move_col):
                        
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            create_moves(row, col, possible_move_row, possible_move_col)
                            possible_move_row += row_inc
                            possible_move_col += col_inc
                        
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            create_moves(row, col, possible_move_row, possible_move_col)
                            break
                        
                        else: break
        
        if piece.name == "pawn": # PAWN MOVES
            pawn_moves()
        
        elif piece.name == 'knight': # KNIGHT MOVES
            knight_moves()
        
        elif piece.name == "bishop": # BISHOP MOVES
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1)
            ])
        
        elif piece.name == "rook": # ROOK MOVES
            straightline_moves([
                (-1, 0),
                (0, -1),
                (1, 0),
                (0, 1)
            ])
        
        elif piece.name == "queen": # QUEEN MOVES
            straightline_moves([
                (-1, 0),
                (0, -1),
                (1, 0),
                (0, 1),
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1)
            ])
        
        elif piece.name == "king":
            straightline_moves([
                (-1, 0),
                (0, -1),
                (1, 0),
                (0, 1),
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1)
            ])

    def display_moves(self, screen, dragger, dragging_piece=None): #FUNC TO DISPLAY VALID MOVES FOR CLICKED PIECE
        
        if dragger.dragging:
            
            for move in dragging_piece.moves:
                
                color = "#C86464" if (move.final.row + move.final.col) % 2 ==0 else "#C84646"
                
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(screen, color, rect)