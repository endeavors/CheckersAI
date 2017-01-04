from util import GameState, Player
from board import Board
import re

class Checkers:
    def __init__(self):
        self.board = Board()
        self.player_a = None
        self.player_b = None

    #pass in a from_pos/to_pos tuple
    def move(self,from_pos,to_pos,player):
        #must be in bounds and you should only move your piece.
        validMove = self.board.checkPosBounds(from_pos, to_pos) and \
            self.board.getBoardItem(from_pos) in self.board.getPlayerPieces(player) \
            and from_pos != to_pos

        if validMove:
            resMove = self.board.move(from_pos,to_pos,player)
            #multiple jump paths available
            if resMove == 0:
                jump_ans = self.selectJump(self.board.getMultipleJumpPaths())
                self.board.takeJumpFromPath(from_pos,to_pos,player,jump_ans)

        if not validMove or resMove == -1:
            print("Not a valid move!")
            return False
        return True

    def selectJump(self,pos_list):
        print("Multiple jumps paths are available. Please select one:")
        for i,p in enumerate(pos_list):
            print("{}) {}".format(i+1, str(p)))
        sel_jump = input("=> ").strip()
        while not sel_jump.isdigit() or int(sel_jump) < 0 or int(sel_jump) > \
            len(pos_list):
            print('Please enter an integer from the choices above.')
            sel_jump = input("=> ").strip()
        return int(sel_jump)

    def printBoard(self):
        print(str(self.board))

    def getUserMove(self,player):
        player_str = self.player_a if player == Player.A else self.player_b
        from_pos = to_pos = None
        while True:
            try:
                move = input("{}{}: ".format("Enter your move ",player_str))
                move_list = move.split()
                if len(move_list) != 2:
                    print("Please enter a valid position like this: '50 41'")
                from_pos, to_pos = map(lambda x: x.strip(),move_list)

                if len(from_pos) != 2 or len(to_pos) != 2 or \
                    not from_pos.isdigit() or not to_pos.isdigit():
                    print("Please enter a valid position like this: '50 41'")

                m_from = re.search("(\d)(\d)", from_pos)
                m_to = re.search("(\d)(\d)", to_pos)
                if m_from and m_to:
                    from_pos = (int(m_from.group(1)), int(m_from.group(2)))
                    to_pos = (int(m_to.group(1)), int(m_to.group(2)))
                    break
            except Exception:
                pass
        return from_pos, to_pos

    def playGame(self,player_name):
        self.player_a = player_name[0]
        self.player_b = player_name[1]
        curr_player = Player.A
        neg_player = Player.B
        curr_gamestate = GameState.CONTINUE
        self.printBoard()
        while curr_gamestate == GameState.CONTINUE:
            #make sure you get a valid move
            move_res = self.performMove(curr_player)
            while not move_res:
                move_res = self.performMove(curr_player)
            curr_gamestate = self.board.isWon(curr_player)
            neg_player, curr_player = curr_player, neg_player
            self.printBoard()
        self.declareWinner(curr_gamestate,neg_player)

    def performMove(self,curr_player):
        #Player A always goes first
        f_pos, t_pos = self.getUserMove(curr_player)
        return self.move(f_pos, t_pos, curr_player)

    def declareWinner(self,gamestate,winplayer):
        if gamestate == GameState.DRAW:
            print("GAME IS DRAW!!!")
        elif gamestate == GameState.WON:
            player_str = self.player_a if winplayer == Player.A else self.player_b
            print("{} WON!!!".format(player_str))
