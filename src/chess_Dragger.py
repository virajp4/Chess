import pygame

from chess_Const import *
from chess_Square import *
from chess_Board import *

# THIS FILE CONTAINS THE CLASS RESPONSIBLE FOR DRAGGING PIECES

class chess_Dragger():
    
    def __init__(self):
        
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row, self.initial_col = 0, 0
    
    def update_icon(self, surface): # FUNC TO UPDATE DRAGGING PIECE LOCATION ALONG WITH MOUSE POS
        
        self.piece.set_texture(size=128)
        
        texture = self.piece.texture
        img = pygame.image.load(texture)
        
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        
        surface.blit(img, self.piece.texture_rect)
               
    def update_mouse_pos(self, pos): # FUNC TO UPDATE MOUSE POS
        self.mouseX, self.mouseY = pos
        
    def save_initial(self, pos): # FUNC TO SAVE INITIAL POSITION OF PIECE BEFORE DRAGGING
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE
        
    def drag_piece(self, piece): # FUNC TO DRAG PIECE
        self.piece = piece
        self.dragging = True
        
    def undrag_piece(self, piece): # FUNC TO UNDRAG PIECE
        self.piece = None
        self.dragging = False
        