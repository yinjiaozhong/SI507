from collections import deque
import random
random.seed(17)

class BaconNumberCalculator:
    """
    A class to calculate the Kevin Bacon number in a network of actors.

    Parameters
    ----------
    fileName : str
        The name of the file containing the movie data.

    Attributes
    ----------
    adjList : dict of dict/dict of list/ dict of tuple/etc...

    Methods
    -------
    generateAdjList(fileName)
        Constructs the adjacency list from the given file.
    
    calcBaconNumber(startActor, endActor)
        Calculates the Bacon number between two actors.
    
    calcAvgNumber(startActor, threshold)
        Calculates the average Bacon number for a given actor.
    """

    def __init__(self, fileName):
        """
        Constructs all the necessary attributes for the BaconNumberCalculator object.

        Parameters
        ----------
        fileName : str
            The name of the file containing the movie data.
        """
        self.adjList = {}
        self.generateAdjList(fileName)

    def generateAdjList(self, fileName):
        """
        Reads a file and builds an adjacency list representing actor connections.

        Parameters
        ----------
        fileName : str
            The name of the file to read the movie data from.
            You need to think about which encoding you should use,
	        To load the file.
        
        Attributes
        ----------
        adjList : dict of dict/dict of list/ dict of tuple/etc...
        The key of the adjList should be the original(unmodified) actor name
        in the inputted file. You should not and do not need to modify it.
        For example:
        Bacon, Kevin
        Kidman, Nicole
         

        Returns
        -------
        None
        """
        with open(fileName, 'r', encoding='ISO-8859-1') as f:
            for line in f:
                actors = line.strip().split('/')[1:]
                for i in range(len(actors)):
                    if actors[i] not in self.adjList:
                        self.adjList[actors[i]] = set()
                    self.adjList[actors[i]].update(actors[j] for j in range(len(actors)) if j != i)

    def calcBaconNumber(self, startActor, endActor):
        """
        Calculates the Bacon number (shortest path) between two actors.

        Parameters
        ----------
        startActor : str
            The name of the starting actor.
        endActor : str
            The name of the ending actor.

        Returns
        -------
        List[int, List[str]]
            A List containing the Bacon number and the path of connections.
            The second List should be in the following form.
            [startActor, moive1, actor1, moive2,actor1, movie3,endActor]

        Note
        -------
        1.A local variable visited:set() is needed, which aviod visiting the same
        actor more than once. 

        2.List should not be used to simulate the behavior of a queue.
        related reading:https://docs.python.org/3/tutorial/datastructures.html
        solution to is question is in the next line of the reason in the website

        3. It should return [-1, []], if one of the inputted actor is not
        in our graph.

        4.It should return [0, [start actor]], if the start actor is the end actor

        Hint
        -------
        What infomation you should store in the queue?
        Should it be the whole current path, or a single actor, or a tuple with 
        length of two?

        If the whole path, think about how many new list object you might create
        during the process. Notice, create a new list is not very time efficient.

        If a single actor, think about how to reconstruct the path from startActor
        to endActor. Will you need a dictionary to do so? 

        If a tuple, think about what information need to be in the tuple, and 
        how to reconstruct the path. Will you need a dictionary to do so? 

        BFS is a search algorithm that extends step by step, so if a point is traversed, 
        there is one and only one path to the point due to the visited set. 
        Each time, you enqueue an actor, 
        record the actor and movie before it in a dictionary.

        """

        if startActor not in self.adjList or endActor not in self.adjList:
            return [-1, []]

        if startActor == endActor:
            return [0, [startActor]]

        visited = {startActor}
        queue = deque([(startActor, [startActor])])
        while queue:
            actor, path = queue.popleft()
            for neighbor in self.adjList[actor]:
                if neighbor == endActor:
                    shortestPath = path + [endActor]
                    baconNumber = len(shortestPath) - 1
                    while len(shortestPath) < 2 * baconNumber + 1:
                        for i in range(1, len(shortestPath), 2):
                            if len(shortestPath) < 2 * baconNumber + 1:
                                for j in self.adjList[shortestPath[i - 1]]:
                                    if j != shortestPath[i] and j not in shortestPath:
                                        shortestPath.insert(i, j)
                                        break
                            else:
                                break
                    return [baconNumber, shortestPath]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return [-1, []]  # No path found


    def calcAvgNumber(self, startActor, threshold):
        """
        Calculates the average Bacon number for a given actor until convergence.

        The method iteratively selects a random actor and computes the Bacon number 
        from the startActor to this random actor. It updates and calculates the 
        average Bacon number. This process continues until the difference between 
        successive averages is less than the specified threshold, indicating convergence.

        pseudocode 
        ----------
        Initialize previousAvg to 0, curDiff to a large number (acting as infinity)
        Create a list of all possible actors from the adjacency list.
        Enter a while loop that continues as long as curDiff is greater than the threshold.
        a. Increment round count.
        b. Choose a random actor from the list of possible actors.
        c. Calculate the Bacon number (bNum) from startActor to the chosen actor.
        d. If bNum is valid (not -1 and not 0):
            addjust totalBNum and calculate the difference (curDiff) between the current and previous averages.
            Update previousAvg to the current average.
        e. If bNum is invalid, exclude it and adjust round count, undo the effect of this unsuccessful round.
        Return the previousAvg once the loop exits.

        Parameters
        ----------
        startActor : str
            The actor for whom the average Bacon number is to be calculated.
        threshold : float
            The convergence threshold for the average calculation.

        Returns
        -------
        float
            The converged average Bacon number for the startActor.
        """
        if startActor not in self.adjList:
            return -1

        visited = set()
        queue = deque([(startActor, 0)])
        totalBNum = 0
        count = 0

        while queue:
            actor, distance = queue.popleft()
            if actor not in visited:
                visited.add(actor)
                totalBNum += distance
                count += 1

                for neighbor in self.adjList[actor]:
                    if neighbor not in visited:
                        queue.append((neighbor, distance + 1))

        if count > 0:
            return totalBNum / count
        else:
            return -1

if __name__ == "__main__":
    calculator = BaconNumberCalculator("PopularCast.txt")

