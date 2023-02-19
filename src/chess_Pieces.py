import os

# THIS FILE CONTAINS ALL THE PIECE ICONS (TEXTURES) AND THE PIECE DATA

class Piece:
    
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        
        value_sign = 1 if color == 'white' else -1
        self.dir = 1 if color == 'black' else -1
        
        self.name = name
        self.color = color
        self.value = value * value_sign
        
        self.moves = []
        self.last_move = None
        self.moved = False
        
        self.texture = texture
        self.texture_rect = texture_rect
        
        self.set_texture()
        
    def set_texture(self, size=80): # FUNC TO JOIN IMAGE WITH CORRESPONDING PIECE
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')
        
    def add_move(self, move): # FUNC TO STORE VALID MOVES OF A PIECE
        self.moves.append(move)
    
    def clear_moves(self): # CLEAR MOVES OF A PIECE
        self.moves = []
        
class Pawn(Piece):
    
    def __init__(self, color):
        super().__init__('pawn', color, 1.0)

class Knight(Piece):
    
    def __init__(self, color):
        super().__init__('knight', color, 3.0)
        
class Bishop(Piece):
    
    def __init__(self, color):
        super().__init__('bishop', color, 3.001)
        
class Rook(Piece):
    
    def __init__(self, color):
        super().__init__('rook', color, 5.0)
        
class Queen(Piece):
    
    def __init__(self, color):
        super().__init__('queen', color, 9.0)
        
class King(Piece):
    
    def __init__(self, color):
        self.right_rook = None
        self.left_rook = None
        super().__init__('king', color, 10000.0)
