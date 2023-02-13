from const import *

# THIS FILE CONTAINS THE CLASS WHICH STORES EACH INDIVIDUAL SQUARE

class chess_Square:
    
    def __init__(self, row, col, piece=None):
        
        self.row = row
        self.col = col
        self.piece = piece
        
    def has_piece(self): # FUNC TO CHECK IF SQUARE HAS A PIECE
        return self.piece != None
    
    def isempty(self): # FUNC TO CHECK IF SQUARE IS EMPTY
        return not self.has_piece()
    
    def has_team_piece(self, color): # FUNC TO CHECK IF SQUARE HAS TEAM PIECE
        return self.has_piece() and self.piece.color == color
    
    def has_rival_piece(self, color): # FUNC TO CHECK IF SQUARE HAS RIVAL
        return self.has_piece() and self.piece.color != color
    
    def isempty_or_rival(self, color): # FUNC TO CHECK IF SQUARE IS EMPTY OR RIVAL
        return self.isempty() or self.has_rival_piece(color)
    
    @staticmethod
    def in_range(*args): # FUNC TO CALC MOVES INSIDE THE BOARD
        for arg in args:
            if arg<0 or arg>7:
                return False
        return True
    
    