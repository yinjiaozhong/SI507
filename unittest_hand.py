import random
from cards import Card, Deck
import unittest
from hand import Hand


class TestHand(unittest.TestCase):
    # create the Hand with an initial set of cards
        '''a hand for playing card '''


    def test_initialize_hand(self):
        # Test that a hand is properly initialized
        c1 = Hand.Card()
        c2 = Hand.Card(1, 2)

        cardlist = [c1, c2]
        # create a hand
        h1 = Hand.Hand(cardlist)

        # test if card list is properly assigned
        self.assertEqual(h1.init_card, cardlist)
        # test if elements are instance of cards
        self.assertIsInstance(h1.init_card.pop(-1), HW_cards.Card)

        cards = [Card(0, 2), Card(1, 3)]
        hand = Hand(cards)
        self.assertEqual(len(hand.cards), 2)
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


    def test_add_card(self, card):
        # test add_card() method
        hand = Hand()
        card = Card(0,2)
        hand.add_card(card)
        self.assertIn(card, hand.cards)

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


    def test_remove_card(self, card):
        # test remove_card() method
        hand = Hand
        card = Card(0,2)
        hand.add_card(card)
        removed_card = hand.remove_card(card)
        self.assertEqual(removed_card, card)
        self.assertEqual(len(hand.cards),0)

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
        deck = Deck()
        hand = Hand()
        hand.draw(deck)
        self.asserEqual(len(hand.cards),1)

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


    def test_remove_pairs(self):
        # test remove_pairs() method
        cards =[Card(0,2),Card(1,2),Card(2,3),Card(3,3)]
        hand = Hand(cards)
        hand.remove_pairs()
        self.assertEqual(len(hand.cards),0)
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

if __name__ == "__main__":
    unittest.main()
