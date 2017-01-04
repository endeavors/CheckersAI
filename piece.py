from util import PieceState, Player

class Piece:
    def __init__(self,pos,player):
        self.pos = pos #it's a tuple
        self.player = player

    def __str__(self):
        if self.player == Player.A:
            return PieceState.BLACK
        else:
            return PieceState.RED

    def getPlayer(self):
        return self.player

    def getPos(self):
        return self.pos

    def setPos(self,pos):
        self.pos = pos
