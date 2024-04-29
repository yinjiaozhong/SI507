
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
        self.playlist.append(media)
        if self.currentMediaNode is None:
            self.currentMediaNode = self.playlist.dummyHead.next


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
        if index < 0 or index >= self.playlist.getSize():
            return False
        current = self.playlist.dummyHead.next
        prev = self.playlist.dummyHead
        current_index = 0
        while current_index < index and current is not None:
            prev = current
            current = current.next
            current_index += 1
        
        if current is None or current == self.playlist.dummyTail:
            return False
        
        if current == self.currentMediaNode:
            self.currentMediaNode = current.next

            if self._isNodeUnbound(self.currentMediaNode):
                self.currentMediaNode = None
                
        if prev is None:
            self.playlist.dummyHead.next = current.next
        else:
            prev.next = current.next
            current.next.prev = prev
        self.playlist.size -= 1
        return True
        

    def next(self) -> bool:
        """
        Moves currentMediaNode to the next media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the next media, False otherwise.
        """
        if self.currentMediaNode is not None and self.currentMediaNode.next != self.playlist.dummyTail:
            self.currentMediaNode = self.currentMediaNode.next
            return True
        return False
        

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
        if self.currentMediaNode is not None and self.currentMediaNode.prev != self.playlist.dummyHead:
            self.currentMediaNode = self.currentMediaNode.prev
            return True
        return False


    def resetCurrentMediaNode(self) -> bool:
        """
        Resets the current media to the first media in the playlist,
        if the playlist contains at least one media.

        Returns
        -------
        bool
            True if the current media was successfully reset, False otherwise.
        """
        if self.playlist.getSize() > 0:
            self.currentMediaNode = self.playlist.dummyHead.next
            return True
        return False
        

    def play(self):
        """
        Plays the current media in the playlist. 
        Call the play method of the media instance.
        Remeber currentMediaNode is a node not a media, but its data is the actual
        media. If the currentMediaNode is None or its data is None, 
        print "The current media is empty.". 
        """
        if self.currentMediaNode is not None and self.currentMediaNode.data is not None:
            self.currentMediaNode.data.play()
            #print("The current media is empty.")
        else:
            print("The current media is empty.")
            #self.currentMediaNode.data.play()

    def playForward(self):
        """
        Plays all the media in the playlist from front to the end,
        by iterating the linked list.  
        Remeber each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print "Playlist is empty.". 
        """
        if self.playlist.getSize() == 0:
            print("Playlist is empty.")
            return
        current = self.playlist.dummyHead.next
        while current != self.playlist.dummyTail:
            if current.data is not None:
                current.data.play()
            current = current.next
        

    def playBackward(self):
        """
        Plays all the media in the playlist from the back to front,
        by iterating the linked list.  
        Remeber each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print this string "Playlist is empty.". 
        """
        if self.playlist.getSize() == 0:
            print("Playlist is empty.")
        else:
            current = self.playlist.dummyTail.prev
            while current != self.playlist.dummyHead:
                if current.data is not None:
                    current.data.play()
                current = current.prev
        

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
        Remember to use the dictionary get method.

        Parameters
        ----------
        fileName : str
            The name of the JSON file to load media from.
        """
        with open(fileName, 'r') as file:
            data = json.load(file)

        for item in data:
            title = item.get('trackName', item.get('collectionName','No Title'))
            artist = item.get('artistName', 'No Title')
            releaseDate = item.get('releaseDate','No releaseDate')
            track = item.get('wrapperType', None)
            if 'track' in track:
                kind = item.get('kind')
                if 'song' in kind:
                    genre = item.get('primaryGenreName')
                    duration = item.get('trackTimeMillis')
                    url = item.get('trackViewUrl', item.get('collectionViewUrl', 'No URL'))
                    album = item.get('collectionName', 'No Album')
                    media = Track(title, artist, releaseDate, url, album, genre, duration)
                elif 'movie' in kind:
                    url = item.get('trackViewUrl', item.get('collectionViewUrl', 'No URL'))
                    rating = item.get('contentAdvisoryRating')
                    movieLength = item.get('trackTimeMillis')
                    media = Movie(title, artist, releaseDate, url, rating, movieLength)
                else:
                    url = item.get('trackViewUrl', item.get('collectionViewUrl', 'No URL'))
                    media = Media(title, artist, releaseDate, url)
            else:
                url = item.get('trackViewUrl', item.get('collectionViewUrl', 'No URL'))
                media = Media(title, artist, releaseDate, url)
            self.addMedia(media)




    def _isNodeUnbound(self, node):
        return node.prev is None or node.next is None


if __name__ == "__main__":
    player = Player()
    player.loadFromJson("insert_data.json")
    player.playForward()
    print(player.playlist.getSize())
    print(player.removeMedia(5))
    print(player.removeMedia(4))
    print(player.removeMedia(3))
    print(player.playlist.getSize())
    print(player.removeMedia(42))
    print(player.playlist.getSize())
    