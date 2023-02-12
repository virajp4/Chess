import pygame
import sys

from const import *
from chess_Pieces import *
from chess_Square import *
from chess_Board import *

# THIS FILE IS THE MAIN FILE WHICH RUNS THE PROGRAM

class Main:
    
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        
    def mainloop(self):
        
        while True:
            
            game = chess_Board(self.screen)
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT: # EXIT GAME
                    pygame.quit()
                    sys.exit()

            pygame.display.update() # UPDATE WHOLE DISPLAY


if __name__ == "__main__":
    main = Main()
    main.mainloop()