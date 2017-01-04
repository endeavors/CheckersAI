from util import board_size, Box, Player, GameState
from piece import Piece
import operator as op

#Fixed board size of 8 by 8
class Board:
    def __init__(self):
        self.board = None
        self.black_pieces = set()
        self.red_pieces = set()
        self.pos_list = None
        self.initBoard()

    def initBoard(self):
        self.board = []
        num_piece_rows = 3
        for r in range(board_size[0]):
            row_list = []
            for c in range(board_size[1]):
                #blacks
                if r < num_piece_rows:
                    if (r % 2 == 0 and c % 2 != 0) or (r % 2 != 0 and c % 2 == 0):
                        p = Piece((r,c),Player.B)
                        row_list.append(p)
                        self.red_pieces.add(p)
                    else:
                        row_list.append(None)

                elif r >= board_size[0] - num_piece_rows: #reds
                    if (r % 2 == 0 and c % 2 != 0) or (r % 2 != 0 and c % 2 == 0):
                        p = Piece((r,c),Player.A)
                        row_list.append(p)
                        self.black_pieces.add(p)
                    else:
                        row_list.append(None)
                else:
                    row_list.append(None)
            self.board.append(row_list)

    def __str__(self):
        l_margin_size = 5
        item_spacing = 5
        left_margin = " " * l_margin_size
        res_list = []

        #column numbers
        col_title = "".join(map(lambda x: "{:^{}}".format(x,item_spacing),
            range(board_size[1])))
        res_list += [left_margin, col_title,"\n"]

        col_len = len(col_title)
        #top border line
        hor_line = Box.HORIZONTAL * (item_spacing-1)
        res_list += [left_margin,Box.LEFT_TOP_CORNER, (hor_line + Box.DOWN_VERTICAL)
            * (board_size[1] - 1), hor_line, Box.RIGHT_TOP_CORNER, "\n"]


        for r, row in enumerate(self.board):
            last = r == (len(self.board) - 1)
            res_list += ["{:^{}}".format(r,l_margin_size), Box.VERTICAL]
            for piece in row:
                res_list += ["{:^{}}".format(str(piece) if piece else "",item_spacing-1),
                    Box.VERTICAL]
            res_list += ["\n", left_margin, Box.LEFT_BOTTOM_CORNER if last else
                Box.LEFT_SIDE_BORDER]

            for i in range(len(row)-1):
                    res_list += [hor_line, Box.UPPER_VERITCAL if last else Box.PLUS]

            res_list += [hor_line, Box.RIGHT_BOTTOM_CORNER if last else
                Box.RIGHT_SIDE_BORDER,"\n"]

        return "".join(res_list)

    def getRowSize(self):
        return len(self.board)

    def getColSize(self):
        return len(self.board[0])

    def move(self, from_pos, to_pos, player):
        ty,tx = to_pos
        fy,fx = from_pos

        if ty == ((fy - 1) if player == Player.A else (fy + 1)) and \
            (tx == (fx - 1) or tx == (fx + 1)):
            #idx is empty
            if not self.board[ty][tx]:
                self.movePieces(from_pos,to_pos,player)
                return 1
        else:
            jump_res, self.pos_list = self.getValidJumpToPos(from_pos,to_pos,player)

            if jump_res:
                for i,pos in enumerate(self.pos_list):
                    self.pos_list[i] = pos[::-1]
                #multiple jumps available, ask the user for their choice
                if len(self.pos_list) > 1:
                    return 0
                elif len(self.pos_list) == 1:
                    self.movePieces(from_pos,to_pos,player)
                    return 1

        return -1

    def movePieces(self,from_pos,to_pos,player,idx=None):
        ty,tx = to_pos
        fy,fx = from_pos
        self.board[ty][tx],self.board[fy][fx] = self.board[fy][fx],self.board[ty][tx]
        self.board[ty][tx].setPos((ty,tx))

        #capture pieces
        #Idx is not None when multiple jump paths are available
        if self.pos_list:
            p_list =  self.pos_list[idx-1] if idx else self.pos_list[0]
            cap_pieces = self.getCapturePieces(p_list)
            for cap_p in cap_pieces:
                self.capturePiece(cap_p)
            self.pos_list = None

    def getMultipleJumpPaths(self):
        if self.pos_list:
            return self.pos_list
        return None

    def getCapturePieces(self,p_list):
        res_list = []
        for i in range(len(p_list)-1):
            curr_pos = p_list[i]
            next_pos = p_list[i+1]
            #use midpoint formula
            y = (curr_pos[0] + next_pos[0])//2
            x = (curr_pos[1] + next_pos[1])//2
            res_list.append((y,x))
        return res_list

    def capturePiece(self,pos):
        piece = self.board[pos[0]][pos[1]]
        self.board[pos[0]][pos[1]] = None
        if piece in self.black_pieces:
            self.black_pieces.discard(piece)
        else:
            self.red_pieces.discard(piece)

    def takeJumpFromPath(self,from_pos,to_pos,player,idx):
        self.movePieces(from_pos,to_pos,player,idx)

    def getValidJumpToPos(self,from_pos,to_pos,player):
        def helper(from_pos,to_pos,player,orig_pos):
            fy, fx = from_pos
            ty, tx = to_pos
            pos_list = None
            if (from_pos == to_pos):
                return True, [[to_pos]]
            #We've skipped over the idx
            if player == Player.A:
                if (fx <= tx and fy <= ty) or (fx >= tx and fy <= ty):
                    return False, pos_list
            else:
                if (fx <= tx and fy >= ty) or (fx >= tx and fy >= ty):
                    return False, pos_list

            #last 2 items are for player B only
            #simulates this -> (fy-2,fx-2),(fy-2, fy+2),(fy+2, fy-2),(fy+2, fy+2)
            ops_list = [(op.sub,op.sub),(op.sub,op.add),(op.add,op.sub),(op.add,op.add)]
            if player == Player.B:
                ops_list = ops_list[::-1]

            #finds all possible routes to the end idx
            for i in range(2):
                op1,op2 = ops_list[i]
                new_from_pos = (op1(fy,2), op2(fx,2))
                if self.checkFromBounds(new_from_pos):
                    board_val = self.board[op1(fy,1)][op2(fx,1)]
                    if board_val and board_val.getPlayer() != \
                        self.board[orig_pos[0]][orig_pos[1]].getPlayer():
                        #must be empty for us to make a jump
                        if not self.board[new_from_pos[0]][new_from_pos[1]]:
                            res, tups = helper(new_from_pos,to_pos,player,orig_pos)
                            if res:
                                for p in tups: p.append(from_pos)
                                if not pos_list: pos_list = tups
                                else: pos_list = pos_list + tups

            return pos_list != None, pos_list
        return helper(from_pos,to_pos,player,from_pos)

    def checkPosBounds(self, from_pos, to_pos):
        if not from_pos or not to_pos: return False
        return self.checkFromBounds(from_pos) and self.checkToBounds(to_pos)

    def checkFromBounds(self, from_pos):
        if from_pos[0] >= 0 and from_pos[0] < self.getRowSize() and from_pos[1] >= 0 \
            and from_pos[1] < self.getColSize():
            return True
        return False

    def checkToBounds(self, to_pos):
        if to_pos[0] >= 0 and to_pos[0] < self.getRowSize() and to_pos[1] >= 0 \
            and to_pos[1] < self.getColSize():
            return True
        return False

    def isWon(self,player):
        A_legalmoves = self.isLegalMovesAvailable(Player.A)
        B_legalmoves = self.isLegalMovesAvailable(Player.B)
        if (len(self.red_pieces) == 0 and len(self.black_pieces) == 0) or \
            (not A_legalmoves and not B_legalmoves):
            return GameState.DRAW

        if player == Player.A:
            #any pieces left:
            if len(self.red_pieces) == 0 or not B_legalmoves:
                return GameState.WON
        elif player == Player.B:
            if len(self.black_pieces) == 0 or not A_legalmoves:
                return GameState.WON
        return GameState.CONTINUE

    def isLegalMovesAvailable(self, player):
        ops_list = [(op.sub,op.sub),(op.sub,op.add),(op.add,op.sub),(op.add,op.add)]
        if player == Player.B:
            ops_list = ops_list[::-1]

        for piece in self.getPlayerPieces(player):
            fy,fx = piece.getPos()
            #check consecutive diagonals
            for i in range(2):
                op1,op2 = ops_list[i]
                new_to_pos = (op1(fy,1), op2(fx,1))
                if self.checkToBounds(new_to_pos):
                    if not self.board[new_to_pos[0]][new_to_pos[1]]:
                        return True

            #check jump diagonals
            for i in range(2):
                op1,op2 = ops_list[i]
                new_to_pos = (op1(fy,2), op2(fx,2))
                if self.checkFromBounds(new_to_pos):
                    board_val = self.board[op1(fy,1)][op2(fx,1)]
                    if board_val and board_val.getPlayer() != self.board[fy][fx].getPlayer():
                        if not self.board[new_to_pos[0]][new_to_pos[1]]:
                            return True

        return False

    def getPlayerPieces(self,player):
        return self.black_pieces if player == Player.A else self.red_pieces

    def getBoardItem(self,pos):
        return self.board[pos[0]][pos[1]]
