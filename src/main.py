import pygame
import sys

from const import *
from chess_Pieces import *
from chess_Square import *
from chess_Board import *
from chess_Dragger import *

# THIS FILE IS THE MAIN FILE WHICH RUNS THE PROGRAM
## TO DO :- CHECKS, CHECKMATE, EN PASSANT, AUDIO, ICON CLARITY


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
            game.display_last_move(self.screen) # DISPLAY PREVIOUS MOVE
            game.display_moves(self.screen, dragger, dragger.piece) # DISPLAY VALID MOVES
            game.display_hovered(self.screen)
            game.display_pieces(self.screen, dragger.piece) # DISPLAY CHESS BOARD PIECES
            
            if dragger.dragging:
                dragger.update_icon(self.screen) # CHANGE SIZE OF DRAGGING PIECE
                
            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN: # WHEN PIECE IS CLICKED ON
                    
                    dragger.update_mouse_pos(event.pos)
                    
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if game.squares[clicked_row][clicked_col].has_piece():
                        
                        dragging_piece = game.squares[clicked_row][clicked_col].piece
                        
                        if dragging_piece.color == game.next_player:
                        
                            # CALC VALID MOVES AND DRAG
                            game.calc_moves(dragging_piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(dragging_piece)
                            
                            # DISPLAY
                            game.display_bg(self.screen)
                            game.display_last_move(self.screen)
                            game.display_moves(self.screen, dragger, dragger.piece)
                            game.display_pieces(self.screen, dragging_piece)
                            
                elif event.type == pygame.MOUSEMOTION: # WHEN PIECE IS DRAGGED
                    
                    hovering_row = event.pos[1] // SQSIZE
                    hovering_col = event.pos[0] // SQSIZE
                    game.set_hover(hovering_row, hovering_col)
                    
                    if dragger.dragging:
                        
                        dragger.update_mouse_pos(event.pos)
                        
                        # DISPLAY
                        game.display_bg(self.screen)
                        game.display_last_move(self.screen)
                        game.display_moves(self.screen, dragger, dragger.piece)
                        game.display_hovered(self.screen)
                        game.display_pieces(self.screen, dragging_piece)
                        dragger.update_icon(self.screen)
                
                elif event.type == pygame.MOUSEBUTTONUP: # WHEN PIECE IS RELEASED
                    
                    if dragger.dragging:
                        
                        dragger.update_mouse_pos(event.pos)
                        
                        released_row = dragger.mouseY // SQSIZE 
                        released_col = dragger.mouseX // SQSIZE
                        
                        initial = chess_Square(dragger.initial_row, dragger.initial_col)
                        final = chess_Square(released_row,released_col)
                        
                        move = chess_Move(initial, final)
                        
                        if move in dragging_piece.moves: # CHECK IF MOVE TO BE DONE IS PRESENT IN VALID MOVES
                            
                            game.move_piece(dragging_piece, move)
                            
                            game.display_bg(self.screen)
                            game.display_last_move(self.screen)
                            game.display_pieces(self.screen)
                        
                    
                        dragger.undrag_piece(dragging_piece)
                
                elif event.type == pygame.KEYDOWN: # WHEN KEY PRESS IS DONE
                    
                    if event.key == pygame.K_t:
                        game.change_theme(self.screen)
                    
                    if event.key == pygame.K_r:
                        game.reset()
                        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        game = chess_Board(self.screen)
                        dragger = chess_Dragger()
                
                elif event.type == pygame.QUIT: # EXIT GAME
                    pygame.quit()
                    sys.exit()

            pygame.display.update() # UPDATE WHOLE DISPLAY


if __name__ == "__main__":
    main = Main()
    main.mainloop()