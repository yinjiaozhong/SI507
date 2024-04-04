
from media import Media, Track, Movie
from linked_list import LinkedList
import json

class Player:
    """
    A media player class that manages a playlist of media.

    This class utilizes a doubly linked list (LinkedList) to store and manage media in a playlist.
    It provides methods for adding, removing, playing, and navigating through media.

    Attributes
    ----------
    playlist : LinkedList
        A doubly linked list that stores the media in the playlist.
    currentMediaNode : Node or None
        The current media being played, represented as a node in the linked list.
    """

    def __init__(self):
        """
        Initializes the Player with an empty playlist and None as currentMediaNode.
        """
        self.playlist = LinkedList()
        self.currentMediaNode = None
        

    def addMedia(self, media):
        """
        Adds a media to the end of the playlist.
        Set the currentMediaNode to the first node in the playlist, 
        if currentMediaNode is None. 

        Parameters
        ----------
        media : Media | Track | Movie 
            The media to add to the playlist.
        """
        if self.currentMediaNode is None:
            self.currentMediaNode = self.playlist.dummyHead.next
        self.playlist.append(media)

    def removeMedia(self, index) -> bool:
        """
        Removes a media from the playlist based on its index.
        You can assume the only invalid input is invalid index.
        Set the currentMediaNode to its next, if currentMediaNode is removed,
        and remeber using _isNodeUnbound(self.currentMediaNode) to check if a link is broken.

        Parameters
        ----------
        index : int
            The index of the media to remove.

        Returns
        -------
        bool
            True if the media was successfully removed, False otherwise.
        """
        if self.playlist.deleteAtIndex(index):
            if self.currentMediaNode == self.playlist.getNodeAtIndex(index):
                self.currentMediaNode = self.currentMediaNode.next
            return True
        return False
        

    def next(self) -> bool:
        """
        Moves currentMediaNode to the next media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the next media, False otherwise.
        """
        if self.currentMediaNode is None or self.currentMediaNode == self.playlist.dummyTail:
            return False
        self.currentMediaNode = self.currentMediaNode.next
        return True
        

    def prev(self) -> bool:
        """
        Moves currentMediaNode to the previous media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the previous media, False otherwise.
        """

        # If there is no current media node or the current media node is at the beginning of the playlist
        # We cannot move to the previous media, so return False
        if self.currentMediaNode is None or self.currentMediaNode == self.playlist.dummyHead.next:
            return False
        # Return True to indicate successful navigation to the previous media
        self.currentMediaNode = self.currentMediaNode.prev
        return True
        

    def resetCurrentMediaNode(self) -> bool:
        """
        Resets the current media to the first media in the playlist,
        if the playlist contains at least one media.

        Returns
        -------
        bool
            True if the current media was successfully reset, False otherwise.
        """
        if not self.playlist.getSize():
            return False
        self.currentMediaNode = self.playlist.dummyHead.next
        return True
        

    def play(self):
        """
        Plays the current media in the playlist. 
        Call the play method of the media instance.
        Remeber currentMediaNode is a node not a media, but its data is the actual
        media. If the currentMediaNode is None or its data is None, 
        print "The current media is empty.". 
        """
        if self.currentMediaNode is None or self.currentMediaNode.data is None:
            print("The current media is empty.")
        else:
            self.currentMediaNode.data.play()

    def playForward(self):
        """
        Plays all the media in the playlist from front to the end,
        by iterating the linked list.  
        Remeber each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print "Playlist is empty.". 
        """
        if not self.playlist.getSize():
            print("Playlist is empty.")
        else:
            current_node = self.playlist.dummyHead.next
            while current_node != self.playlist.dummyTail:
                print(current_node.data.info())
                current_node = current_node.next
        

    def playBackward(self):
        """
        Plays all the media in the playlist from the back to front,
        by iterating the linked list.  
        Remeber each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print this string "Playlist is empty.". 
        """
        if not self.playlist.getSize():
            print("Playlist is empty.")
        else:
            current_node = self.playlist.dummyTail.prev
            while current_node != self.playlist.dummyHead:
                print(current_node.data.info())
                current_node = current_node.prev
        

    def loadFromJson(self, fileName):
        """
        Loads media from a JSON file and adds them to the playlist.
        The order should be the same as the provided json file. 
        You could assume the filename is always valid
        Notice, for each given json object, 
        you should create instance of the correct instance type, (movie,track,media).
        You need to observe the provided json and figure how to do it.
        You could assume if a json object is not track or movie,
        it has to be a media.
        Pay attention the name of the key in each json object. 
        Set the currentMediaNode to the first media in the playlist, 
        if there is at least one media in the playlist.
        Remeber to use the dictionary get method. 

        Parameters
        ----------
        filename : str
            The name of the JSON file to load media from.
        """
        with open(fileName, 'r') as file:
            data = json.load(file)
            for item in data:
                if item.get('kind') == 'song':
                    new_media = Track(item.get('trackName', 'Unknown'), item.get('artistName', 'Unknown'))
                elif item.get('kind') == 'feature-movie':
                    new_media = Movie(item.get('trackName', 'Unknown'), item.get('artistName', 'Unknown'))
                else:
                    new_media = Media(item.get('trackName', 'Unknown'), item.get('artistName', 'Unknown'))
                self.addMedia(new_media)
