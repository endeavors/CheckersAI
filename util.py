from enum import Enum

class PieceState:
    RED = '🔴'
    BLACK = '⬤'

class Box:
    LEFT_TOP_CORNER = '┏'
    RIGHT_TOP_CORNER = '┓'
    LEFT_BOTTOM_CORNER = '┗'
    RIGHT_BOTTOM_CORNER = '┛'
    HORIZONTAL = '━'
    VERTICAL = '┃'
    DOWN_VERTICAL = '┳'
    UPPER_VERITCAL = '┻'
    PLUS = '╋'
    LEFT_SIDE_BORDER = '┣'
    RIGHT_SIDE_BORDER = '┫'

class Player(Enum):
    A = 1 #Black pieces
    B = 2 #Red pieces


class GameState(Enum):
    CONTINUE = 1
    WON = 2
    DRAW = 3

board_size = (8,8) #row by col
