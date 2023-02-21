import pygame
import copy as cp

from const import *
from chess_Square import *
from chess_Pieces import *
from chess_Dragger import *

# THIS FILE CONTAINS THE CLASS THAT DEALS WITH EVERYTHING ON BOARD

class chess_Board:
    
    def __init__(self, screen):
        
        self.screen = screen
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.colors = [ ( (234, 235, 200),(119, 154, 88) ), 
                        ( (235, 209, 166),(165, 117, 80) ) ]
        self.color_test = 0
        self.cur_color = self.colors[self.color_test]
        
        self.last_moved_move = None
        self.last_moved_piece = None
        self.next_player = 'white'
        self.hovered_sqr = None
        self.king_loc = [[7,4],[0,4]]
        
        self.dragger = chess_Dragger()
        
        self.display_bg(self.screen) # DISPLAY CHESS BOARD
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
                color = self.cur_color[0] if (row + col) % 2 == 0 else self.cur_color[1]
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
        
        def create_moves(row,col,possible_move_row,possible_move_col,piece): # CREATE VALID MOVES FOR A PIECE
            
            initial = chess_Square(row,col) # INITIAL POS
            final_piece = self.squares[possible_move_row][possible_move_col].piece
            final = chess_Square(possible_move_row,possible_move_col,final_piece) # FINAL POS
            
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
                        
                        create_moves(row,col,possible_move_row,possible_move_col,piece)
            
        def pawn_moves(): # CALC VALID MOVES FOR PAWN
            
            steps = 1 if piece.moved else 2
            
            # VERTICAL MOVES
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            
            for possible_move_row in range(start, end, piece.dir):
                
                if chess_Square.in_range(possible_move_row) and self.squares[possible_move_row][col].isempty(): # CHECK IF MOVES ARE VALID   
                    
                    create_moves(row,col,possible_move_row,col,piece)
                    
                else: break
                
            # DIAGONAL MOVES
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            
            for possible_move_col in possible_move_cols:
                if chess_Square.in_range(possible_move_col) and self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                    
                    create_moves(row,col,possible_move_row,possible_move_col,piece)
            
            # EN PASSANT MOVES
            if isinstance(self.last_moved_piece, Pawn) and self.last_moved_piece.enpass:
                if self.last_moved_move.final.row == row:
                    side = self.last_moved_move.final.col - col
                    create_moves(row, col, row+piece.dir, col+side, piece)
                    piece.did_enpass = True
                   
        def king_moves(increment): # CALC VALID KING MOVES
            
            for inc in increment: # NORMAL KING MOVES
                    row_inc, col_inc = inc
                    possible_move_row = row + row_inc
                    possible_move_col = col + col_inc
                    
                    if chess_Square.in_range(possible_move_row,possible_move_col) and self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        create_moves(row, col, possible_move_row, possible_move_col,piece)
                    
            if not piece.moved: # CASTLING KING MOVES
                
                # SHORT CASTLE
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5,7):
                            if self.squares[row][c].has_piece():
                                break
                            if c == 5:
                                piece.right_rook = right_rook
                                create_moves(row,7,row,5,right_rook)
                                create_moves(row,col,row,6,piece)
                                
                # LONG CASTLE
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1,4):
                            if self.squares[row][c].has_piece():
                                break
                            if c == 3:
                                piece.left_rook = left_rook
                                create_moves(row,0,row,3,left_rook)
                                create_moves(row,col,row,2,piece)
                                     
        def straightline_moves(increment): # STRAIGHT AND DIAG MOVES
            
            for inc in increment:
                row_inc, col_inc = inc
                possible_move_row = row + row_inc
                possible_move_col = col + col_inc
                
                while chess_Square.in_range(possible_move_row,possible_move_col):
                    
                    if self.squares[possible_move_row][possible_move_col].isempty():
                        create_moves(row, col, possible_move_row, possible_move_col,piece)
                        possible_move_row += row_inc
                        possible_move_col += col_inc
                    
                    elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        create_moves(row, col, possible_move_row, possible_move_col,piece)
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
        
        elif piece.name == "king": # KING MOVES
            king_moves([
                (-1, 0),
                (0, -1),
                (1, 0),
                (0, 1),
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1)
            ])

    def castling(self, initial, final): # CHECK IF CASTLING IS POSSIBLE
            return abs(initial.col - final.col) == 2
    
    def check_promotion(self, piece, final): # PROMOTE PAWN TO QUEEN
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
    
    def gives_check(self, enemy, row, col): # CHECK IF ENEMY PIECE ATTACK KING
        
        self.calc_moves(enemy, row, col)
        
        for moves in enemy.moves:
            if isinstance(moves.final.piece, King):
                enemy.moves = []
                return True
        enemy.moves = []
        return False
    
    def after_move_check(self, piece): # FUNC TO CHECK IF MOVE IS LEGAL
        
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_enemy_piece(piece.color):
                    enemy = self.squares[row][col].piece
                    if self.gives_check(enemy, row, col):
                        return True
        return False
    
    def display_moves(self, screen, dragger, dragging_piece=None): # FUNC TO DISPLAY VALID MOVES FOR CLICKED PIECE
        
        if dragger.dragging:
            
            for move in dragging_piece.moves:

                    if self.is_illegal_move(dragging_piece, move):
                        dragging_piece.moves.remove(move)
                        
                    else:
                        color = "#C86464" if (move.final.row + move.final.col) % 2 == 0 else "#C84646"
                        
                        rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                        
                        pygame.draw.rect(screen, color, rect)
    
    def is_illegal_move(self, piece, move): # FUNC TO CHECK IF PIECE MOVE IS ILLEGAL
        
        initial = move.initial
        final = move.final
        
        self.squares[initial.row][initial.col].piece = None
        otherpiece = self.squares[final.row][final.col].piece
        self.squares[final.row][final.col].piece = piece
        
        if self.after_move_check(piece):
            self.squares[final.row][final.col].piece = otherpiece
            self.squares[initial.row][initial.col].piece = piece
            return True
        else:
            self.squares[final.row][final.col].piece = otherpiece
            self.squares[initial.row][initial.col].piece = piece
            return False
    
    def remove_illegal_moves(self, piece=None):
            
        for move in piece.moves:
            if self.is_illegal_move(piece, move):
                piece.moves.remove(move)
    
    def move_piece(self, piece, move): # FUNC TO MOVE PIECE
        
        initial = move.initial
        final = move.final
        
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        if isinstance(piece, Pawn): # FOR PAWN PROMOTION TO QUEEN
            self.check_promotion(piece, final)
            
            if abs(final.row - initial.row) == 2:
                piece.enpass = True
            
            if piece.did_enpass:
                rowdiff = self.last_moved_move.final.row - final.row
                self.squares[final.row+rowdiff][final.col].piece = None
            
        if isinstance(self.last_moved_piece, Pawn): # FOR ENPASSANT
            self.last_moved_piece.enpass = False
            self.last_moved_piece.did_enpass = False
            
        if isinstance(piece, King): # FOR CASTLING AND CHANGING ROOK POSITION
            if self.castling(initial,final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff<0) else piece.right_rook
                self.move_piece(rook, rook.moves[-1])
            if piece.color == 'white':
                self.king_loc[0] = [final.row,final.col]
            else:
                self.king_loc[1] = [final.row,final.col]
                
        if not self.after_move_check(piece): # CHECK IF MOVE IS LEGAL
            piece.moved = True
            piece.clear_moves()
            self.next_turn()
            self.last_moved_move = move
            self.last_moved_piece = piece
            piece.last_move = move
            self.check_for_mate(self.screen, piece)
     
    def undo_move(self, piece, move): # UNDO A MOVE
        initial = move.initial
        final = move.final
        self.squares[final.row][final.col].piece = None
        self.squares[initial.row][initial.col].piece = piece
        
    def next_turn(self): # FUNC TO DECIDE NEXT PLAYER TURN
        self.next_player = 'white' if self.next_player == 'black' else 'black'
    
    def display_last_move(self, screen): # FUNC TO DISPLAY LAST MOVE
        
        if self.last_moved_move:
            
            initial = self.last_moved_move.initial
            final = self.last_moved_move.final
            
            for pos in [initial, final]:
                
                color = (244,247,116) if (pos.row + pos.col) % 2 == 0 else (172,195,51)
                
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(screen, color, rect)
                
    def display_hovered(self, screen): # FUNC TO DISPLAY MOUSE LOCATION
        
        if self.hovered_sqr:
            
            color = (180,180,180)
            
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            
            pygame.draw.rect(screen, color, rect, width=4)
    
    def check_for_mate(self, screen, piece): # FUNC TO CHECK FOR CHECKMATE
        pass
    
    def set_hover(self, row, col): # TO SET HOVER SQUARE
        self.hovered_sqr = self.squares[row][col]

    def reset(self): # RESET BOARD
        self.__init__(self.screen)

    def change_theme(self, screen): # CHANGE THEME
        
        self.color_test += 1
        self.cur_color =  self.colors[0] if self.color_test % 2 == 0 else self.colors[1]
        self.display_bg(screen)