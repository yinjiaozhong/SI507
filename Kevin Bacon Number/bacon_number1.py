import random

random.seed(17)
from collections import deque


class BaconNumberCalculator:
    """
    A class to calculate the Kevin Bacon number in a network of actors.

    Parameters
    ----------
    fileName : str
        The name of the file containing the movie data.

    Attributes
    ----------
    adjList : dict
        Adjacency list representing the actor connections.

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

        return [-1, []]
    def calcAvgNumber(self, startActor, threshold):
        """
        Calculates the average Bacon number for a given actor until convergence.

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
# 测试代码
if __name__ == "__main__":
    calculator = BaconNumberCalculator("PopularCast.txt")

    print("Test1:")
    print(calculator.calcBaconNumber("Bacon, Kevin", "Kidman, Nicole"))
    print(calculator.calcBaconNumber("Bacon, Kevin", "Bacon, Kevin"))
    print(calculator.calcBaconNumber("Bacon, Kevin", "NonExistentActor"))
    print()

    print("Test2:")
    print(calculator.calcAvgNumber("Bacon, Kevin",0.1))
    print(calculator.calcAvgNumber("Kidman, Nicole", 0.1))
    print(calculator.calcAvgNumber("NonExistentActor", 0.1))