import unittest
# Import necessary classes from cards
from cards import Card, Deck
# Import the Hand class to be tested
from hand_starter import Hand

class TestHand(unittest.TestCase):
    def test_initialize_hand(self):
        # Test that a hand is initialized properly
        # Create a hand with some initial cards
        hand = Hand([Card(0, 2), Card(1, 3)])
        # Assert that the hand contains the correct number of cards
        self.assertEqual(len(hand.cards), 2)

    def test_add_and_remove_card(self):
        # Test that add_card() and remove_card()
        hand = Hand()
        card = Card(0, 2)
        # Add a card to the hand
        hand.add_card(card)
        # Assert that the card was added successfully
        self.assertIn(card, hand.cards)
        # Remove the card from the hand
        removed_card = hand.remove_card(card)
        # Assert that the removed card is the same as the one added
        self.assertEqual(removed_card, card)
        # Assert that the hand is now empty
        self.assertEqual(len(hand.cards), 0)

    def test_draw(self):
        # Test that draw() works
        deck = Deck()
        hand = Hand()
        # Draw a card from the deck
        hand.draw(deck)
        # Assert that the hand contains the drawn card
        self.assertEqual(len(hand.cards), 1)

    def test_remove_pairs(self):
        # Test the remove_pairs() method
        hand = Hand([Card(0, 2), Card(1, 2), Card(2, 3), Card(3, 3)])  # Two pairs
        hand.remove_pairs()
        # Assert that pairs are removed correctly
        self.assertEqual(len(hand.cards), 0)  # All pairs should be removed

if __name__ == "__main__":
    unittest.main()
