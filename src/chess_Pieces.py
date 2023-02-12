import os

# THIS FILE CONTAINS ALL THE PIECE ICONS (TEXTURES) AND THE PIECE DATA

class Piece:
    
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        
        value_sign = 1 if color == 'white' else -1
        
        self.name = name
        self.color = color
        self.value = value * value_sign
        
        self.moves = []
        self.moved = False
        
        self.texture = texture
        self.texture_rect = texture_rect
        
        self.set_texture()
        
    def set_texture(self, size=80):
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')
        
class Pawn(Piece):
    
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
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
        super().__init__('king', color, 10000.0)
