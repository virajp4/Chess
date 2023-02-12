import pygame

from const import *
from chess_Square import *
from chess_Pieces import *
from chess_Dragger import *

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
                        
    def calc_moves(self, piece, row, col):
        
        def knight_moves():
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
                       
        if piece.name == "pawn":
            pass
        
        elif piece.name == "knight":
            knight_moves()
        
        elif piece.name == "bishop":
            pass
        
        elif piece.name == "rook":
            pass
        
        elif piece.name == "queen":
            pass
        
        elif piece.name == "king":
            pass