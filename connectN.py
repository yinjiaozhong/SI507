from enum import Enum
from typing import Optional

# initialize setting
class Notation(Enum):
    """Enumeration for representing different types of notations in the game.

        Attributes:
            EMPTY (int): Represents an empty cell on the board.
            PLAYER1 (int): Represents a cell occupied by Player 1.
            PLAYER2 (int): Represents a cell occupied by Player 2.
        """
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 =2

class Player:
    """Represents a player in the game.

        Attributes:
            __playerName (str): The name of the player.
            __playerNotation (Notation): The notation (symbol) used by the player on the board.
            __curScore (int): The current score of the player.

        Args:
            playerName (str): The name of the player.
            playerNotation (Notation): The notation (symbol) used by the player.
            curScore (int): The initial score of the player.
        """
    # create the initial state of the objects
    def __init__(self, playerName: str, playerNotation: Notation, curScore: int) -> None:
        # initialize board attributions
        self.__playerName = playerName # private attribution
        self.__playerNotation = playerNotation
        self.__curScore = curScore

    def display(self) -> str:
        """Displays the player's details including name, notation, and current score."""
        return f"Player: {self.__playerName}, Score: {self.__curScore}, Notation: {self.__playerNotation}"


    def addScoreByOne(self) -> None:
        """Increments the player's score by one."""
        self.__curScore += 1

    def getScore(self) -> int:
        """Returns the current score of the player."""
        return self.__curScore

    def getName(self) -> str:
        """Returns the name of the player."""
        return self.__playerName

    def getNotation(self) -> Notation:
        """Returns the notation used by the player."""
        return self.__playerNotation

class Board:
    """Represents the game board.

    Attributes:
        __rowNum (int): Number of rows in the board.
        __colNum (int): Number of columns in the board.
        __grid (list): 2D list representing the game board.

    Args:
        rowNum (int): Number of rows in the board.
        colNum (int): Number of columns in the board.
    """

    def __init__(self, rowNum, colNum) -> None:
        # create a 2D list to save the game board
        self.__rowNum = rowNum
        self.__colNum = colNum
        self.__grid = [[Notation.EMPTY] * colNum for _ in range(rowNum)]

    def initGrid(self) -> None:
        """Initializes the game board with empty cells."""
        self.__grid = [[Notation.EMPTY] * self.__colNum for _ in range(self.__rowNum)]

    def getColNum(self) -> int:
        """Returns the number of columns in the board."""
        return self.__colNum

    def placeMark(self, colNum: int, mark: Notation) ->bool:
        """Attempts to place a mark on the board at the specified column.

        Args:
            colNum (int): The column number where the mark is to be placed.
            mark (Notation): The mark to be placed on the board.

        Returns:
            bool: True if the mark was successfully placed, False otherwise.
        """
        # create loop
        # check the range of colNum
        if not (0 <= colNum < self.__colNum):
            print("Error: Column number out of range.")
            return False

        # traverse reverse loop
        for row in range(self.__rowNum -1, -1, -1):
            if self.__grid[row][colNum] == Notation.EMPTY:
                self.__grid[row][colNum] = mark
                return True
        print("Error: Colum is full")
        return False

    def checkFull(self) -> bool:
        """Checks if the board is completely filled.

     Returns:
            bool: True if the board is full, False otherwise.
        """
        # check all cells are filled
        return all(cell != Notation.EMPTY for row in self.__grid for cell in row)


    def display(self) -> None:
        """Displays the current state of the board."""
        boardStr = ""
        for row in self.__grid:
            for cell in row:
                if cell == Notation.EMPTY:
                    boardStr += 'O'
                elif cell == Notation.PLAYER1:
                    boardStr += 'R'
                elif cell == Notation.PLAYER2:
                    boardStr += 'Y'
            boardStr += '\n'
        print("Current Board is")
        print(boardStr)

    # Private methods for internal use
    # check horizontal line
    def __checkWinHorizontal(self, target:int) -> Optional[Notation]:
        # traverse every row
        for row in range(self.__rowNum):
            # ensure it don't cross the range
            for col in range(self.__colNum - target +1):
                if all(self.__grid[row][col + i] == self.__grid[row][col] != Notation.EMPTY for i in range(target)):
                    return self.__grid[row][col]
        return None
    # check vertical line
    def __checkWinVertical(self, target:int) -> Optional[Notation]:
        for col in range(self.__colNum):
            for row in range(self.__rowNum - target +1):
                if all(self.__grid[row + i][col] == self.__grid[row][col] != Notation.EMPTY for i in range(target)):
                    return self.__grid[row][col]
        return None

    # check upper left to lower right
    def __checkWinOneDiag(self, target: int) -> Optional[Notation]:
        for row in range(self.__rowNum - target + 1):
            for col in range(self.__colNum - target + 1):
                if all(self.__grid[row + i][col + i]== self.__grid[row][col] != Notation.EMPTY for i in range(target)):
                    return self.__grid[row][col]
        return None

    # check unpper right to lower left
    def __checkWinAntiOneDiag(self, target: int) ->Optional[Notation]:
        for row in range(self.__rowNum - target + 1):
            for col in range(target - 1, self.__colNum):
                if all(self.__grid[row + i][col - i] == self.__grid[row][col] != Notation.EMPTY for i in range(target)):
                    return self.__grid[row][col]
        return None

    # check any line
    def __checkWinDiagonal(self, target: int) ->Optional[Notation]:
        for row in range(self.__rowNum - target +1):
            for col in range(self.__colNum - target +1):
                if all(self.__grid[row + i][col + 1] == self.__grid[row][col] != Notation.EMPTY for i in range(target)):
                    return self.__grid[row][col]
        return None

    def checkWin(self, target: int) -> Optional[Notation]:
        """Checks if there is a winning condition on the board.

        Args:
            target (int): The number of consecutive marks needed for a win.

        Returns:
            Notation or None: The notation of the winning player, or None if there is no winner.
        """
        # check if there is a line in horizontal direction
        win_horizontal = self.__checkWinHorizontal(target)
        if win_horizontal:
            return win_horizontal

        # check if there is a line in vertical direction
        win_vertical = self.__checkWinVertical(target)
        if win_vertical:
            return win_vertical

        # check if there is a line in diagonal direction
        win_diagonal = self.__checkWinOneDiag(target)
        if win_diagonal:
            return win_diagonal

        win_anti_diagonal = self.__checkWinAntiOneDiag(target)
        if win_anti_diagonal:
            return win_anti_diagonal

        # if there isn't any line
        return None

class Game:
    """Represents the game logic and flow.

    Args:
        rowNum (int): Number of rows in the game board.
        colNum (int): Number of columns in the game board.
        connectN (int): Number of consecutive marks needed for a win.
        targetScore (int): The score a player needs to reach to win the game.
        playerName1 (str): Name of the first player.
        playerName2 (str): Name of the second player.
    """

    # initialize every attribution
    def __init__(self, rowNum: int, colNum: int, connectN: int, targetScore: int, playerName1: str, playerName2: str) -> None:
        # create a new board
        self.__board = Board(rowNum, colNum)
        # achieve the targetScore to win
        self.__connectN = connectN
        self.targetScore = targetScore
        self.__playerList = [Player(playerName1, Notation.PLAYER1, 0), Player(playerName2, Notation.PLAYER2, 0)]
        self.__curPlayer = self.__playerList[0]

    def __playBoard(self, curPlayer):
        """Handles the process of a player making a move on the board.

        Args:
            curPlayer (Player): The current player who is making the move.
        """
        print(f"{curPlayer.getName()}'s turn to play:")
        self.__board.display()
        while True:
            colNum = input("Enter the colum number to place your mark: ")
            try:
                # get number which is inputted by player
                colNum = int(colNum)
                if not (0 <= colNum < self.__board.getColNum()):
                    print("Error: Column number out of range.")
                    continue
                mark = curPlayer.getNotation()
                # check if column is full
                if not self.__board.placeMark(colNum, mark):
                    print("Error: Column is full.")
                    continue
                break
            except ValueError:
                print("Error: Invalid column number. Please enter a valid integer.")
        self.__board.display()

    def __changeTurn(self):
        """Switches the turn to the other player."""
        self.__curPlayer = self.__playerList[1] if self.__curPlayer == self.__playerList[0] else self.__playerList[0]


    def playRound(self):
        """Plays a single round of the game."""
        print("Starting a new round.")
        while True:
            self.__playBoard(self.__curPlayer)
            # check if player achieve the score of winning
            winner = self.__board.checkWin(self.__connectN)
            if winner:
                # add score
                winner = next(player for player in self.__playerList if player.getNotation() == winner)
                winner.addScoreByOne()
                print(f"Congratulation! {self.__curPlayer.getName()} wins!")
                break
            # check board is full
            elif self.__board.checkFull():
                print("Board is full. It's a tie!")
                break
            self.__changeTurn()
            #print(f"Game Over! {self.__curPlayer.getName()} wins!")

    def play(self):
        """Starts and manages the game play until a player wins."""
        while True:
            self.playRound()
            for player in self.__playerList:
                if player.getScore() >= self.targetScore:
                    print(f"Game Over! {player.getName()} wins!")
                    return


def main():
    """Main function to start the game."""
    game = Game(4, 4, 3, 2, 'P1', 'P2')
    game.play()

if __name__ == "__main__":
    main()
