import random
from cards import Card

def log():
    global p_hand, up_card, active_suit
    print("Your hand:" , end='     ')
    for card in p_hand:
        print(card.short_name, end='  ')
    print("")
    print("UP card: %s        active suit: %s" % (up_card.short_name, active_suit))
    
def new_suit():
    global active_suit
    while not got_suit:
        got_suit = True
        suit = input("Pick a suit: ")
        if suit.upper() == 'D':
            active_suit = "Diamonds"
        elif suit.upper() == 'S':
            active_suit = 'Spades'
        elif suit.upper() == 'H':
            active_suit = 'Hearts'
        elif suit.upper() == 'C':
            active_suit = 'Clubs'
        else:
            print("Not a valid suit. try again.")
            got_suit = False
    print("You picked" , active_suit)
    
def init():
    global deck, p_hand, c_hand, up_card
    for suit_id in range(1, 5):
        for rank_id in range(1, 14):
            card = Card(suit_id, rank_id)
            if card.rank_id == 8:
                card.value = 50
            deck.append(card)
    for a in range(1, 6):
        p_card = random.choice(deck)
        p_hand.append(p_card)
        deck.remove(p_card)
        c_card = random.choice(deck)
        c_hand.append(c_card)
        deck.remove(c_card)
    up_card = random.choice(deck)
    deck.remove(up_card)

def player_turn():
    global deck, p_hand, up_card, active_suit, blocked

    response = input("Type a card name to play or 'Draw' to take a card: ")
    is_eight = False
    valid_play = False
    selected_card = None
    while not valid_play:
        selected_card = None
        if selected_card == None:
            if response.upper() == 'DRAW':
                valid_play = True
                if len(deck) > 0:
                    card = random.choice(deck)
                    p_hand.append(card)
                    deck.remove(card)
                    print("You draw", card.short_name)
                else:
                    print("There are no cards left in the deck")
                    blocked += 1
                return
            else:
                for card in p_hand:
                    if response.upper() == card.short_name:
                        selected_card = card
                if selected_card == None:
                    response = input("You don't have that card. Try again:")
                if selected_card == '8':
                    valid_play = True
                    is_eight = True
                elif selected_card.suit == active_suit:
                    valid_play = True
                elif selected_card.rank == up_card.rank:
                    valid_play = True
                if not valid_play:
                    response = input("That's not a legal play. Try again: ")
                else:
                    up_card = selected_card
                    p_hand.remove(selected_card)
                    if is_eight:
                        new_suit()

def computer_turn():
    global c_hand, deck, up_card, active_suit, blocked
    options= []
    out_card = False
    for card in c_hand:
        if card.rank == '8':
            c_hand.remove(card)
            up_card = card
            suit_totals = [0, 0, 0, 0]
            for card in c_hand:
                suit_totals[(card.suit_id-1)] += 1
            long_suit = 0
            for i in range(4):
                if suit_totals[long_suit] < suit_totals[i]:
                    long_suit = i
            if long_suit == 0: active_suit = 'Diamonds'
            elif long_suit == 1: active_suit = 'Hearts'
            elif long_suit == 2: active_suit = 'Spades'
            else: active_suit = 'Clubs'
            out_card = True
            print("  Computer played ", card.short_name)
            break
        if card.suit == active_suit:
            options.append(card)
        elif card.rank == up_card.rank:
            options.append(card)

    if not out_card:
        if len(options) > 0:
            best_play = options[0]
            for card in options:
                if card.value > best_play.value:
                    best_play = card
            c_hand.remove(best_play)
            up_card = best_play
            active_suit = up_card.suit
            print("  Computer played ", best_play.short_name)
        else:
            if len(deck) > 0:
                card = random.choice(deck)
                deck.remove(card)
                c_hand.append(card)
                print("  Computer drew a card")
            else:
                print("Computer is blocked")
                blocked += 1
    print("Computer has %i cards left" % (len(c_hand)))
        
deck = []
p_hand = []
c_hand = []
up_card = None
init()
active_suit = up_card.suit
done = False
p_total = c_total = 0
while not done:
    game_done = False
    while not game_done:
        log()
        blocked = 0
        player_turn()
        if len(p_hand) == 0:
            game_done = True
            print("You won!")
        if not game_done:
            computer_turn()
        if len(c_hand) == 0:
            game_done = True
            print("Computer won!")
        if blocked >= 2:
            game_done = True
            print("Both player blocked, GAME OVER")
    player_points = computer_points = 0
    for card in c_hand:
        player_points += card.value
    p_total += player_points
    for card in p_hand:
        computer_points += card.value
    c_total += computer_points
    print("You got %i points for computer's hand" % player_points)
    print("Computer got %i points for your hand" % computer_points)

    play_again = input("play again (Y/N)? ")
    if play_again.upper() == "Y":
        done = False
        print("\nSo far,you have %i points" % p_total)
        print("and the computer has %i points.\n" % c_total)
    else:
        done = True

print("\n Final Score:")
print("You: %i     Computer:%i" % (p_total, c_total))

