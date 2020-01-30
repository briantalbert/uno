import deck
import random
from os import system, name
from time import sleep

##GLOBALS#####
unoDeck = []
discardDeck = []
players = []
activeColor = ''
activeCard = ''
isReversed = False
##############

#####__CLASSES__#####
class Player():
    # defines the Player object
    def __init__(self, name, number):
        """
        initializes the Player object
        :param name: Just "Player #" maybe that could be more customizable
        :param number: Player's index, used for sorting
        """
        self.name = name
        self.hand = []
        self.number = number
        self.type = 'ai'  # human or computer

    # def printHand(self):
    #     """
    #     Prints all the cards in a player's deck.
    #     I wrote this and then realized that I
    #     never actually used it. Keeping it
    #     commented out just in case.
    #     :return: string of cards in hadn.
    #     """
    #     strList = []
    #     cards = ''
    #     s = ' | '
    #
    #     cards = s.join(self.hand)
    #     return cards

    def cardsInHand(self):
        return len(self.hand)

    def __lt__(self, other):
        if self.number < other.number:
            return True

    def __gt__(self, other):
        if self.number > other.number:
            return True

    def __eq__(self, other):
        return self.number == other.number

    def __repr__(self):
        return (f'{self.name}')

    def __str__(self):
        return (f'{self.name}')

class Card():
    def __init__(self, color, value):
        """
        Creates card object
        :param color: Color or blank (wilds)
        :param value: Number or action
        """
        colors = ['Red', 'Green', 'Yellow', 'Blue', '']
        actions = ['Wild', 'Wild Draw 4', 'Draw 2', 'Skip', 'Reverse']
        self.action = False
        self.color = color
        self.value = value
        self.colorvalue = colors.index(color)

        if self.value in actions:
            self.action = True

        if self.value in actions[0:2]:
            self.wild = True
        else:
            self.wild = False

    def __str__(self):
        if self.color != '':
            return (f'{self.color} {self.value}')
        else:
            return (f'{self.value}')

    def __lt__(self, other):
        if self.color == other.color:
            return self.value < other.value
        else:
            return self.color < other.color

    def __gt__(self, other):
        if self.color == other.color:
            return self.value > other.value
        else:
            return self.color > other.color

    def __eq__(self, other):
        return self.color == other.color and self.value == other.value

    def __repr__(self):
        if self.color != '':
            return (f'{self.color} {self.value}')
        else:
            return (f'{self.value}')

    def playableOn(self, other, activeColor):
        """
        Checks to see if one card is playable on another
        :param other: The other card
        :param activeColor: The active color
        :return: Boolean, True if self can be played on other
        """
        if self.wild:
            return True
        if self.color == other.color:
            return True
        if self.value == other.value:
            return True
        elif self.color == activeColor:
            return True
        else:
            return False


#####__METHODS__#####
def screen_clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def buildDeck():
    """
    Builds 2D list of cards
    :return: list in the form of [[color, value], [color, value],...]
    """
    colors = ['Red', 'Green', 'Yellow', 'Blue']
    values = ['0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9', 'Draw 2',
              'Draw 2', 'Skip', 'Skip', 'Reverse', 'Reverse']
    tempDeck = deck.buildDeck(colors, values)
    wilds = [['Wild', ''], ['Wild', ''], ['Wild', ''], ['Wild', ''], ['Wild Draw 4', ''], ['Wild Draw 4', ''],
             ['Wild Draw 4', ''], ['Wild Draw 4', '']]
    for card in wilds:
        tempDeck.append(card)
    random.shuffle(tempDeck)
    return addCards(tempDeck)


def addCards(tempDeck):
    """
    Turns list of cards into card objects
    :param tempDeck: deck list from buildDeck()
    :return: list of Card objects
    """
    global unoDeck
    for card in tempDeck:
        unoDeck.append(Card(card[1], card[0]))
    random.shuffle(unoDeck)
    return unoDeck


def generatePlayers():
    """
    Asks how many players
    """
    numplayers = 0
    while numplayers not in range(2, 8):
        numplayers = input('How many players? Enter 2-7 > ')
        if numplayers.isnumeric():
            numplayers = int(numplayers)
    createPlayers(numplayers)
    dealCards()


def createPlayers(num):
    """
    Creates specified number of Player objects
    :param num: number of players
    """
    global players
    for i in range(0, num):
        players.append(Player(f'Player {i + 1}', i))


def pickHuman():
    """
    Randomly pick a place in play order for the human player
    """
    global players

    ##__for testing only___##
    # humanPlayer = players[0]
    ##_____________________##

    humanPlayer = random.choice(players)
    humanPlayer.type = 'human'
    print(f'Let\'s play! You are {humanPlayer.name}!\n')


def setup():
    global unoDeck

    unoDeck = buildDeck()
    generatePlayers()
    pickHuman()


def dealCards():
    """
    Deals 7 cards to each player
    """
    global players
    global unoDeck

    random.shuffle(unoDeck)

    for player in players:
        for i in range(0, 7):
            player.hand.append(unoDeck.pop(0))
        player.hand.sort()


def firstCard():
    """
    Deals the first card to start the game. Fuck
    current Uno rules, everyone plays by shuffling
    action cards back into the deck so that's what
    we're doing here.
    """
    global unoDeck
    global discardDeck
    global activeCard

    activeCard = unoDeck[0]
    while activeCard.action:
        random.shuffle(unoDeck)
        activeCard = unoDeck[0]
    discardDeck.insert(0, unoDeck.pop(0))


def gameWon():
    """
    Checks to see if there are any empty hands
    :return: Boolean, True if there's an empty hand
    """
    global players
    
    fullDecks = 0
    for player in players:
        if player.hand:
            fullDecks += 1
    if fullDecks == len(players):
        return False
    else:
        return True


def fortestingonly():
    """
    Place a specific card on top of the deck for testing
    """
    global unoDeck
    unoDeck.insert(0, Card('Blue', 'Draw 2'))


def pickColor(player):
    """
    Used for picking color after playing a wild
    :param player: Player object
    :return: Color
    """
    global players
    global activeCard
    global activeColor
    global isReversed

    #print(f'{player.name} plays a {activeCard.value}!')
    colors = ['Red', 'Green', 'Yellow', 'Blue']
    coloridx = -1
    if player.type == 'human':
        for i in range(len(colors)):
            print(f'{i + 1}) {colors[i]}')
        while coloridx not in range(1, 5):
            coloridx = input('Enter your color selection (1-4)> ')
            if coloridx.isnumeric():
                coloridx = int(coloridx)
        colorchoice = colors[coloridx - 1]
        activeColor = colorchoice
    elif player.type == 'ai':
        playercolors = [x.color for x in player.hand]
        playercolors = [x for x in playercolors if x]
        colorchoice = max(set(playercolors), key=colors.count)
        activeColor = colorchoice
        print(f'{player.name} chooses {activeColor}!')

    if isReversed:
        nextPlayer = players[(players.index(player) - 1) % (len(players))]
    else:
        nextPlayer = players[(players.index(player) + 1) % (len(players))]
    return nextPlayer


def printBoard():
    """
    Prints the current board status: Number of cards in
    each player's hand, as well as top card of the
    discard deck (the active card).
    """
    global players
    global unoDeck
    global discardDeck
    global activeColor
    global activeCard
    global isReversed
    
    tempPlayers = players
    tempPlayers.sort()
    for p in tempPlayers:
        print(f'{p.name}: {p.cardsInHand()} cards in hand')
    activeCard = discardDeck[0]
    print(f'Current card on top of Discard Deck is {activeCard}.')
    if activeCard.wild == True:
        print(f'Active color is {activeColor}')
    if isReversed:
        print(f'**Play order is reversed!**\n')


def drawCards(player, num, canPlay):
    """
    Adds cards from draw deck to a player's hand for
    Draw 2, Draw 4, or drawing a single card when a
    player cannot go (or chooses to draw instead of
    play a card).
    :param player: current player
    :param num: number to draw (should only ever be 1, 2, or 4)
    :param canPlay: Boolean, True if player could play but chose to
                    draw anyway
    :return: the next player (could change if player who couldn't go
             draws an action card like skip or reverse)
    """
    global players
    global unoDeck
    global isReversed
    
    tempCards = []
    s = ', '

    if isReversed:
        nextPlayer = players[(players.index(player) - 1) % (len(players))]
    else:
        nextPlayer = players[(players.index(player) + 1) % (len(players))]
 
    if num > 1:
        for i in range(0, num):
            tempCards.append(f'{unoDeck[0].color} {unoDeck[0].value}')
            nextPlayer.hand.append(unoDeck.pop(0))
        if nextPlayer.type == 'human':
            print(f'{nextPlayer.name} draws: {s.join(tempCards)}!')
        return nextPlayer
    
    if num == 1:
        card = unoDeck.pop(0)
        if player.type == 'human':
            print(f'{player.name} draws: {card}!')
        if not canPlay and card.playableOn(activeCard, activeColor):
            nextPlayer = playCard(player, card)
        else:
            player.hand.append(card)
    try:
        nextPlayer
    except NameError:
        input('what the fuck')
    return nextPlayer


def printPlayableHand(player):
    """
    Checks which cards in a player's hand can be played
    on the current active card. If it's a human player,
    the hand is printed with a * indicating playable
    cards.

    :return: list of playable indices
    """
    global players
    global activeColor
    global activeCard

    s = ''
    numPlayable = 0
    playableCards = []
    if not activeCard.wild:
        activeColor = activeCard.color
    player.hand.sort()
    for i in range(0, len(player.hand)):
        card = player.hand[i]
        if card.playableOn(activeCard, activeColor):
            s = '*'
            numPlayable += 1
            playableCards.append(i)
        else:
            s = ''
        if player.type == 'human':
            print(f'{i + 1}) {card}{s}')
    if numPlayable > 0:
        if player.type == 'human':
            print(f'* indicates a playable card')
    else:
        if player.type == 'human':
            print(f'No playable cards! Draw one!')

    return playableCards


def performAction(player):
    """
    If an action card is played, performs that action
    :return: next player
    """
    global activeCard
    
    value = activeCard.value
    print(f'{player.name} played a {activeCard}!')
    if value == 'Skip':  # DONE
        nextPlayer = skip(player)
    elif value == 'Reverse':  # DONE
        nextPlayer = reverse(player)
    elif value == 'Draw 2':  # DONE
        nextPlayer = drawCards(player, 2, False)
    elif value == 'Wild Draw 4':  # DONE
        pickColor(player)
        nextPlayer = drawCards(player, 4, False)
    elif value == 'Wild':  # DONE
        nextPlayer = pickColor(player)

    return nextPlayer


def skip(player):
    global players
    global isReversed
    
    if isReversed:
        nextPlayer = players[(players.index(player) - 2) % (len(players))]
    else:
        nextPlayer = players[(players.index(player) + 2) % (len(players))]

    return nextPlayer


def reverse(player):
    """
    Reverses play order. If there are only 2 players, allows
    current player to go again.
    :param player:
    :return:
    """
    global players
    global isReversed

    if len(players) == 2:
        return player
    
    isReversed = not isReversed

    if isReversed:
        nextPlayer = players[(players.index(player) - 1) % (len(players))]
    else:
        nextPlayer = players[(players.index(player) + 1) % (len(players))]

    return nextPlayer


def takeTurn(player):
    """
    Allows player to choose a card to play
    :return: next player
    """
    global players
    global discardDeck
    global activeCard

    cardChoice = -1

    if player.type == 'human':
        playableCards = printPlayableHand(player)
        playableCards.append('d')
        if playableCards:
            while cardChoice not in playableCards:
                cardChoice = input(f'Enter your choice, or D to draw a card! >')
                if cardChoice.isnumeric():
                    cardChoice = (int(cardChoice) - 1)
            if cardChoice == 'd' and len(playableCards) > 1:
                nextPlayer = drawCards(player, 1, True)
            elif cardChoice == 'd' and len(playableCards) == 1:
                nextPlayer = drawCards(player, 1, False)
            else:
                activeCard = player.hand.pop(cardChoice)
                nextPlayer = playCard(player, activeCard)
        else:
            nextPlayer = drawCards(player, 1, False)
    elif player.type == 'ai':
        if pickCard(player) == 'none':
            print(f'{player.name} is unable to play and draws a card!')
            nextPlayer = drawCards(player, 1, False)
        else:
            nextPlayer = playCard(player, activeCard)

    return nextPlayer


def playCard(player, card):
    """
    Plays the chosen card. If it's not an action card, just
    adds it to the discard deck. Otherwise, preforms the action

    :return: next player
    """
    global players
    global discardDeck
    global activeCard

    discardDeck.insert(0, card)
    activeCard = card

    if card.action:
        nextPlayer = performAction(player)
    else:
        if isReversed:
            nextPlayer = players[(players.index(player) - 1) % (len(players))]
        else:
            nextPlayer = players[(players.index(player) + 1) % (len(players))]
    if not card.action:
        activeColor = card.color
        print(f'{player.name} plays {card}')

    return nextPlayer


def pickCard(player):
    """
    Just used for AI players, basic AI for picking a card
    depending on how many cards other players have.

    :return: Doesn't return anything unless there are no cards
             to play.
    """
    global activeCard
    global players
    global activeColor

    playableCards = printPlayableHand(player)
    scores = [0 for i in playableCards]

    if isReversed:
        nextPlayer = players[(players.index(player) - 1) % (len(players))]
        nextNextPlayer = players[(players.index(player) - 2) % (len(players))]
    else:
        nextPlayer = players[(players.index(player) + 1) % (len(players))]
        nextNextPlayer = players[(players.index(player) + 2) % (len(players))]

    if not playableCards:
        return 'none'
    for i in range(len(playableCards)):
        card = player.hand[playableCards[i]]
        if not card.action:
            scores[i] += 1
        if card.value == 'Skip' or card.value == 'Reverse':
            if len(players) > 2 and nextNextPlayer.cardsInHand() < 3:
                scores[i] -= 2
            if len(players) == 2:
                scores[i] += 3
            else:
                scores[i] += 2
        if card.value == 'Draw 2':
            if nextPlayer.cardsInHand() < 3:
                scores[i] += 3
            else:
                scores[i] += 2
        if card.value == 'Wild Draw 4':
            scores[i] += 3
            if nextPlayer.cardsInHand() > 6:
                scores[i] -= 1
            if nextPlayer.cardsInHand() < 3:
                scores[i] += 2
        if card.value == 'Wild':
            if nextPlayer.cardsInHand() < 3:
                scores[i] += 2
            else:
                scores[i] += 1
    activeCard = player.hand.pop(playableCards[scores.index(max(scores))])


def game():
    """
    Main game loop.
    """
    global unoDeck
    global discardDeck
    global players
    global activeCard
    global isReversed

    turn = 0

    setup()

    currentPlayer = players[0]

    firstCard()
    print(f'First card is {activeCard}')
    if activeCard.action:
        currentPlayer = performAction(currentPlayer)
    currentPlayer = players[0]
    printBoard()
    isReversed = False
    while not gameWon():
        turn += 1
        if turn > 1:
            printBoard()
        print(f'Turn #{turn}\n')
        print(f'{currentPlayer.name} is taking their turn!')
        name = currentPlayer.name
        currentPlayer = takeTurn(currentPlayer)
        if gameWon():
            break
        print(f'Next player is {currentPlayer.name}!')
        input('Press enter to continue.')
        screen_clear()

def main():
    global players
    
    screen_clear()
    game()
    print(f'Game over!')
    
    for player in players:
        if player.cardsInHand() == 0:
            print(f'{player.name} wins!')
            
if __name__ == "__main__":
    main()

