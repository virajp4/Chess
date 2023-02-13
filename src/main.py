import pygame
import sys

from const import *
from chess_Pieces import *
from chess_Square import *
from chess_Board import *
from chess_Dragger import *

# THIS FILE IS THE MAIN FILE WHICH RUNS THE PROGRAM

class Main:
    
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        
    def mainloop(self):
        
        game = chess_Board(self.screen)
        dragger = chess_Dragger()
        
        while True:
            
            game.display_bg(self.screen) # DISPLAY CHESS BOARD
            game.display_pieces(self.screen, dragger.piece) # DISPLAY CHESS BOARD PIECES
            
            if dragger.dragging:
                dragger.update_icon(self.screen)
            
            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN: # WHEN PIECE IS CLICKED ON
                    
                    dragger.update_mouse_pos(event.pos)
                    
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if game.squares[clicked_row][clicked_col].has_piece():
                        dragging_piece = game.squares[clicked_row][clicked_col].piece
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(dragging_piece)
                    
                elif event.type == pygame.MOUSEMOTION: # WHEN PIECE IS DRAGGED
                    if dragger.dragging:
                        dragger.update_mouse_pos(event.pos)
                        game.display_bg(self.screen)
                        game.display_pieces(self.screen, dragging_piece)
                        dragger.update_icon(self.screen)
                
                elif event.type == pygame.MOUSEBUTTONUP: # WHEN PIECE IS RELEASED
                    dragger.undrag_piece(dragging_piece)
                    
                elif event.type == pygame.QUIT: # EXIT GAME
                    pygame.quit()
                    sys.exit()

            pygame.display.update() # UPDATE WHOLE DISPLAY


if __name__ == "__main__":
    main = Main()
    main.mainloop()