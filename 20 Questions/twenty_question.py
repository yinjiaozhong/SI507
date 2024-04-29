class TwentyQuestions:
    def __init__(self):
        """
        Initialize the TwentyQuestions class with predefined small and medium trees.
        Sets the current tree to the small tree by default.
        """
        self.smallTree = (
            "Is it bigger than a breadbox?",
            ("an elephant", None, None),
            ("a mouse", None, None),
        )
        self.mediumTree = (
            "Is it bigger than a breadbox?",
            ("Is it gray?", ("an elephant", None, None), ("a tiger", None, None)),
            ("a mouse", None, None),
        )
        # Default tree
        self.currentTree = self.smallTree

    def inputChecker(self, userIn: str) -> bool:
        """
        Check if the user's input is an affirmative response.

        Parameters
        ----------
        userIn : str
            The input string from the user.

        Returns
        -------
        bool
            True if the input is an affirmative response ('y', 'yes', 'yup', 'sure'), else False.
        """
        affirmative_responses = ['yes', 'y', 'yup', 'sure']
        return userIn.lower() in affirmative_responses

    def checkIfLeaf(self, curNode: tuple) -> bool:
        """
        Determine if the given node is a leaf node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        bool
            True if the node is a leaf (both children are None), else False.
        """
        return curNode[1] is None and curNode[2] is None

    def simplePlay(self, curNode: tuple) -> bool:
        """
        Conduct a simple playthrough of the game using the current node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        bool
            True if the player successfully guesses the item, else False.
        """
        if self.checkIfLeaf(curNode):
            # If the current node is a leaf node, ask if the guess is correct
            guess = curNode[0]
            response = input(f"Is it {guess}? (yes/no): ")
            return self.inputChecker(response)
        else:
            # If not a leaf, ask question and proceed based on the user's response.
            question = curNode[0]
            response = input(f"{question} (yes/no): ")
            if self.inputChecker(response):
                return self.simplePlay(curNode[1])
            else:
                return self.simplePlay(curNode[2])

    def createNode(self, userQuestion: str, userAnswer: str, isCorrectForQues: bool, curNode: tuple) -> tuple:
        """
        Create a new node in the decision tree.

        Parameters
        ----------
        userQuestion : str
            The question to differentiate the new answer from the current node.
        userAnswer : str
            The answer provided by the user.
        isCorrectForQues : bool
            True if the userAnswer is the correct response to the userQuestion.
        curNode : tuple
            The current node in the decision tree at which the game has arrived.

        Returns
        -------
        tuple
            The new node created with the user's question and answer.
        """
        if isCorrectForQues:
            # If the answer is correct for the question, add it to the left child.
            return (userQuestion, (userAnswer, None, None), curNode)
        else:
            # If the answer is incorrect for the question, add it to the right child.
            return (userQuestion, curNode, (userAnswer, None, None))

    def playLeaf(self, curNode: tuple) -> tuple:
        """
        Handle gameplay when a leaf node is reached in the decision tree.

        Parameters
        ----------
        curNode : tuple
            The current leaf node in the decision tree.

        Returns
        -------
        tuple
            The updated node based on user input.
        """
        guess = curNode[0]
        response = input(f"Is it {guess}? (yes/no): ")
        if self.inputChecker(response):
            # If the guess is correct, print success message
            print("I got it!")
            return curNode
        else:
            # If the guess is incorrect, prompt for correct answer and create a new node.
            correctAnswer = input("I give up. What was it? ")
            newQuestion = input(f"Please give me a question that would distinguish {guess} from {correctAnswer}: ")
            answerForNewQuestion = input(f"What would be the answer for {correctAnswer}? (yes/no): ")
            return self.createNode(newQuestion, correctAnswer, self.inputChecker(answerForNewQuestion), curNode)



    def play(self, curNode: tuple) -> tuple:
        """
        Conduct gameplay starting from the given node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        tuple
            The updated tree after playing from the given node.
        """
        if self.checkIfLeaf(curNode):
            # If current node is a leaf, handle leaf gameplay.
            return self.playLeaf(curNode)
        else:
            # If current node is not a leaf, ask the question and proceed accordingly.
            question = curNode[0]
            response = input(f"{question} (yes/no): ")
            if self.inputChecker(response):
                # If yes, explore left subtree.
                newSubtree = self.play(curNode[1])
                return (question, newSubtree, curNode[2])
            else:
                # If no, explore right subtree.
                newSubtree = self.play(curNode[2])
                return (question, curNode[1], newSubtree)

        #def updated_tree(curNode, path, new):

    def playRound(self):
        """
        Execute a single round of the game, starting from the current state of the currentTree attribute.
        """
        print("Let's play Twenty Questions!")
        self.currentTree = self.play(self.currentTree)

    def saveTree(self, node, treeFile):
        """
        Recursively save the decision tree to a file.

        Parameters
        ----------
        node : tuple
            The current node in the decision tree.
        treeFile : _io.TextIOWrapper
            The file object where the tree is to be saved.
        """
        if node is None:
            treeFile.write('Leaf\n')
        if self.checkIfLeaf(node):
            # If leaf node, write node information.
            print(f"Leaf\n{node[0]}", file=treeFile)
        else:
            # If internal node, write node information and recursively save children.
            print(f"Internal node\n{node[0]}", file=treeFile)
            self.saveTree(node[1], treeFile)
            self.saveTree(node[2], treeFile)

    def saveGame(self, treeFileName):
        """
        Save the current state of the game's decision tree to a specified file. This method opens the file
        with the given filename and writes the structure of the current decision tree to it. The tree is saved
        in a txt format.

        The method uses the 'saveTree' function to perform the recursive traversal and writing of the tree
        structure. Each node of the tree is written to the file with its type ('Leaf' or 'Internal node')
        followed by its content (question or object name).

        Important: the format of the txt file should be exactly the same as the ones in our doc to pass the autograder.

        Parameters
        ----------
        treeFileName : str
            The name of the file where the current state of the decision tree will be saved. The file will be
            created or overwritten if it already exists.

        """
        with open(treeFileName, 'w') as treefile:
            self.saveTree(self.currentTree, treefile)

    def loadTree(self, treeFile):
        """
        Recursively read a binary decision tree from a file and reconstruct it.

        Parameters
        ----------
        treeFile : _io.TextIOWrapper
            An open file object to read the tree from.

        Returns
        -------
        tuple
            The reconstructed binary tree.
        """
        nodeType = treeFile.readline().strip()
        if not nodeType:
            return None
        content = treeFile.readline().strip()
        if nodeType == "Leaf":
            # If leaf node, return leaf.
            return (content, None, None)
        else:
            # If internal node, recursively load children.
            left = self.loadTree(treeFile)
            right = self.loadTree(treeFile)
            return (content, left, right)

    def loadGame(self, treeFileName):
        """
        Load the game state from a specified file and update the current decision tree. This method opens the
        file with the given filename and reconstructs the decision tree based on its contents.

        The method employs the 'loadTree' function to perform recursive reading of the tree structure from the
        file. Each node's type ('Leaf' or 'Internal node') and content (question or object name) are read and
        used to reconstruct the tree in memory. This restored tree becomes the new 'self.currentTree' of the game.

        Parameters
        ----------
        treeFileName : str
            The name of the file from which the game state will be loaded. The file should exist and contain a
            previously saved decision tree.

        """
        with open(treeFileName, 'r') as treeFile:
            self.currentTree = self.loadTree(treeFile)

    def printTree(self):
        self._printTree(tree = self.currentTree)

    def _printTree(self, tree, prefix='', bend='', answer=''):
        """Recursively print a 20 Questions tree in a human-friendly form.
        TREE is the tree (or subtree) to be printed.
        PREFIX holds characters to be prepended to each printed line.
        BEND is a character string used to print the "corner" of a tree branch.
        ANSWER is a string giving "Yes" or "No" for the current branch."""
        text, left, right = tree
        if left is None and right is None:
            print(f'{prefix}{bend}{answer}It is {text}')
        else:
            print(f'{prefix}{bend}{answer}{text}')
            if bend == '+-':
                prefix = prefix + '| '
            elif bend == '`-':
                prefix = prefix + '  '
            self._printTree(left, prefix, '+-', "Yes: ")
            self._printTree(right, prefix, '`-', "No:  ")

def main():
    """
    Main function for the Twenty Questions game.
    """
    tq = TwentyQuestions()
    print("Welcome to 20 Questions!")
    load = input("Would you like to load a tree from a file? (yes/no): ")
    if tq.inputChecker(load):
        filename = input("What's the name of the file? ")
    tq.loadGame(filename)
    print("Tree loaded successfully.")

if __name__ == '__main__':
    main()
