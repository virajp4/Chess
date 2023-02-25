from chess_Const import *

# THIS FILE CONTAINS THE CLASSES WHICH STORES EACH INDIVIDUAL SQUARE AND PIECE MOVES

class chess_Square:
    
    def __init__(self, row, col, piece=None):
        
        self.row = row
        self.col = col
        self.piece = piece
        self.isred = False
    
    def __eq__(self, other): # FUNC TO COMPARE 2 SQUARES
        return self.row == other.row and self.col == other.col
    
    def has_piece(self): # FUNC TO CHECK IF SQUARE HAS A PIECE
        return self.piece != None
    
    def isempty(self): # FUNC TO CHECK IF SQUARE IS EMPTY
        return not self.has_piece()
    
    def has_team_piece(self, color): # FUNC TO CHECK IF SQUARE HAS TEAM PIECE
        return self.has_piece() and self.piece.color == color
    
    def has_enemy_piece(self, color): # FUNC TO CHECK IF SQUARE HAS RIVAL
        return self.has_piece() and self.piece.color != color
    
    def isempty_or_enemy(self, color): # FUNC TO CHECK IF SQUARE IS EMPTY OR RIVAL
        return self.isempty() or self.has_enemy_piece(color)
    
    def is_first_enemy(self, row, col, row_inc=None, col_inc=None, color=None): # FUNC TO CHECK IF SQ IS THE FIRST ENEMY SQUARE IN LINE
        return chess_Square[row - row_inc][col - col_inc].isempty() and chess_Square[row][col].has_enemy_piece(color)
    
    @staticmethod
    def in_range(*args): # FUNC TO CALC IF MOVE SQUARE IS INSIDE THE BOARD
        for arg in args:
            if arg<0 or arg>7:
                return False
        return True
    
class chess_Move:
    
    def __init__(self, initial, final) -> None:
        self.initial = initial
        self.final = final
    
    def __eq__(self, other): # FUNC TO COMPARE 2 MOVES
        return self.initial == other.initial and self.final == other.final