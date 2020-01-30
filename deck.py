import random

def standardDeck():
    suits = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
    numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = buildDeck(suits, numbers)
    return deck

def buildDeck(suits, numbers):
    deck = []
    for i in suits:
        for j in numbers:
            deck.append([j, i])
    random.shuffle(deck)
    return deck
