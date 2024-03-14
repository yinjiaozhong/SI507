# create the Hand with an initial set of cards
from cards import Card
class Hand:
    '''a hand for playing card '''


    def __init__(self, init_cards=None):
        self.cards = card if init_cards else []

            '''

            init the hand instance

            Parameters
            -------------------
            init_cards: a list of card instance
            the instance should be created using the card class in card.py


            Attributes
            -------------------
            cards: list
            use the init_cards to create self.cards
            a list of cards instance, indicating the cards in the hand


            '''



    def add_card(self, card):
        # check if the card is already in the hand
        if card not in self.cards:
            self.cards.append(card)
        '''
        
        add a card to hand
        silently fails if the card is already in the hand
        assuming there is only one deck with 52 cards (except jokers)
        two different cards instance with the same rank and suit are 
        regarded as one card
        
        for example:
            card1 = Card(suit=0,rank=2)
            card2 = Card(suit=0,rank=2)
            card1 and card2 are regarded as the same card

        Parameters
        -------------------
        card: card instance
        a card to add

        Returns
        -------
        None

        '''



    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            raise ValueError("Card not found in hand")
        '''

        remove a card from the hand

        Parameters
        -------------------
        card: card instance
        a card to remove

        Returns
        -------
        the removed card instance, or None if the card was not in the Hand

        '''



    def draw(self, deck):
        draw_card = deck.deal_card()
        self.add_card(draw_card)
        return draw_card

        '''

        draw a card from a deck and add it to the hand
        side effect: the deck will be depleted by one card

        Parameters
        -------------------
        deck: deck instance
        a deck from which to draw
        
        Returns
        -------
        None

        '''

    
    def remove_pairs(self):
        # get a dictionary to count the occurrentences of eacn rank
        rank_counts = {}
        for card in self.cards:
            rank = card.rank
            rank_counts[rank] = rank_counts.get(rank, 0) + 1

        # remove pairs if the cards with the same rank
        for rank, count in rank_counts.items():
            if count >= 2:
                self.cards = [card for card in self.cards if card.rank != rank]
        '''

        remove all the pairs in the hand
        this method is for extra credit 2
        
        Parameters
        -------------------
        None
        
        Returns
        -------
        None

        '''
