import random
import time



class Card:
    def __init__(self, num, card=None):
        self.num = num
        self.number = False
        if card is not None:
            self.card = card
            self.number = True

    def returnValue(self):
        return int(self.num)
    
    def returnCard(self):
        return str(self.card) if self.number else str(self.num)
        
class Deck:
    def __init__(self, decks):
        self.cards = {
            'ace': Card(11, "A"),
            'two': Card(2),
            'three': Card(3),
            'four': Card(4),
            'five': Card(5),
            'six': Card(6),
            'seven': Card(7),
            'eight': Card(8),
            'nine': Card(9),
            'ten': Card(10),
            'jack': Card(10, "K"),
            'queen': Card(10, "Q"),
            'king': Card(10, "J")
        }

        self.card_list = list(self.cards.values())
        
        self.suits = {
            'clubs': list(self.card_list),
            'spades': list(self.card_list),
            'diamonds': list(self.card_list),
            'hearts': list(self.card_list)
        }
        
        self.fullDeck = list(self.suits.values())
        self.cardNumbers = decks * 4

        for i in range(decks-1):
            self.fullDeck.extend(self.fullDeck)

    def draw(self):
        value = 0
        while value < 1:
            suit_count = len(self.fullDeck)
            suit = int(suit_count * random.random())
            number = int(len(self.fullDeck[suit]) * random.random())
            value = self.fullDeck[suit].pop(number)
            return value
        
    def shuffle(self):
        if len(self.fullDeck) <= self.cardNumbers/2:
            print("\nShuffling deck...")
            time.sleep(2)
            for suit in self.suits:
                self.suits[suit] = list(self.card_list)
            self.fullDeck = list(self.suits.values())
            print("Deck shuffled!\n")

class Hand:
    def __init__(self, cards=None):
        self.cards = cards if cards else []
        self.is_busted = False
        self.is_done = False
        self.is_blackjack = False
        self.has_been_split = False
        self.is_surrendered = False
    
    def add_card(self, card):
        self.cards.append(card)
    
    def get_cards(self):
        return self.cards
    
    def get_card_values(self):
        return [card.returnCard() for card in self.cards]
        
    def can_split(self):
        return (len(self.cards) == 2 and 
                self.cards[0].returnValue() == self.cards[1].returnValue() and
                not self.has_been_split)
    
    def mark_as_split(self):
        self.has_been_split = True
        
    def split(self):
        if not self.can_split():
            return None
            
        card1 = self.cards[0]
        card2 = self.cards[1]
        
        return card1, card2
        
class BlackJack:
    def __init__(self, decks, starting):
        self.oneDeck = Deck(decks)
        self.userTotal = int(starting)
        self.starting = int(starting)
        self.MAX_SPLITS = 3

    def get_valid_bet(self):
        while True:
            print(f"\nCurrent Amount: ${self.getUserTotal()}")
            try:
                self.bet = int(input(f"How much would you like to bet this hand? $"))
                if 0 < self.bet <= self.userTotal:
                    return self.bet
                else:
                    print("\nYou cannot bet more than your total.")
            except ValueError:
                print("\nPlease enter a valid number.")

    def calculate_hand_value(self, cards):
        total = 0
        aces = 0
        for card in cards:
            if card.returnCard() == "A":
                aces += 1
                total += 11 
            else:
                total += card.returnValue()
                
        while total > 21 and aces > 0:
            total -= 10  
            aces -= 1
        
        return total, aces
    
    def win(self, multiplier=1.0):
        self.userTotal += int(self.bet * multiplier)
    
    def lose(self):
        self.userTotal -= self.bet
        
    def push(self):
        pass
        
    def deal(self):
        nextGame = True
        while nextGame:
            dealerCard1 = self.oneDeck.draw()
            dealerCard2 = self.oneDeck.draw()
            dealerHand = [dealerCard1, dealerCard2]
            dealerShownHand = [dealerCard1.returnCard(), dealerCard2.returnCard()]
            dealerValue = self.calculate_hand_value(dealerHand)
            
            userCard1 = self.oneDeck.draw()
            userCard2 = self.oneDeck.draw()
            
            self.hands = [Hand([userCard1, userCard2])]
            self.split_count = 0
            
            self.oneDeck.shuffle()
            self.bet = self.get_valid_bet()
            
            initialValue, _ = self.calculate_hand_value(self.hands[0].get_cards())
            if initialValue == 21 and len(self.hands[0].get_cards()) == 2:
                print(f"\nYou have {self.hands[0].get_card_values()}\nBLACKJACK!!!")
                time.sleep(2)
                self.hands[0].is_blackjack = True
                self.hands[0].is_done = True
            
            print(f"\nDealer shows: {dealerShownHand[0]}")
            
            if dealerShownHand[0] == "A" and not self.hands[0].is_blackjack:
                self.offer_insurance(dealerHand)
            
            current_hand_idx = 0
            while current_hand_idx < len(self.hands):
                hand = self.hands[current_hand_idx]
                
                if hand.is_done:
                    current_hand_idx += 1
                    continue
                
                self.play_hand(hand, current_hand_idx, dealerHand)
                
                current_hand_idx += 1
            
            for idx, hand in enumerate(self.hands):
                print(f"\nHand {idx+1}: {hand.get_card_values()}")
                hand_value = self.calculate_hand_value(hand.get_cards())
                print(f"Hand Value: {hand_value[0]}")
                if hand.is_busted:
                    print("BUST!")
            
            print("\nDealer shows")
            time.sleep(2)
            print(f"Dealer's hand: {dealerShownHand}")
            
            all_busted = all(hand.is_busted for hand in self.hands)
            any_blackjack = any(hand.is_blackjack for hand in self.hands)
            
            if not all_busted and not any_blackjack:
                dealerValue, remaining_aces = self.calculate_hand_value(dealerHand)
                is_soft = remaining_aces > 0 and dealerValue <= 21
                
                while dealerValue < 17:
                    newCard = self.oneDeck.draw()
                    dealerHand.append(newCard)
                    dealerShownHand.append(newCard.returnCard())
                    dealerValue, remaining_aces = self.calculate_hand_value(dealerHand)
                    is_soft = remaining_aces > 0 and dealerValue <= 21
                    time.sleep(2)
                    print(f"Dealer's hand: {dealerShownHand}")
                
                time.sleep(2)
                if dealerValue > 21:
                    print("Dealer BUSTS!")
                else:
                    print(f"Dealer stands with {dealerValue}")
            else:
                print(f"Dealer's hand: {dealerShownHand}")
            
            time.sleep(2)
            print()
            for idx, hand in enumerate(self.hands):
                hand_value, _ = self.calculate_hand_value(hand.get_cards())
                
                if hand.is_busted:
                    print(f"Hand {idx+1}: You bust. You lose.")
                    self.lose()
                    
                elif hand.is_blackjack:
                    dealer_blackjack = len(dealerHand) == 2 and dealerValue == 21
                    
                    if dealer_blackjack:
                        print(f"Hand {idx+1}: Both have Blackjack. Push.")
                        self.push()
                    else:
                        print(f"Hand {idx+1}: BLACKJACK! You win 3:2.")
                        self.win(1.5)
                        
                elif dealerValue > 21:
                    print(f"Hand {idx+1}: Dealer busts. You win!")
                    self.win()
                    
                elif dealerValue == hand_value:
                    print(f"Hand {idx+1}: Push. Bet returned.")
                    self.push()
                    
                elif dealerValue > hand_value:
                    print(f"Hand {idx+1}: Dealer wins.")
                    self.lose()
                    
                else:
                    print(f"Hand {idx+1}: You win!")
                    self.win()
            
            time.sleep(2)
            print() 
            if self.userTotal <= 0:
                print("You're out of money!")
                break
                
            nextHand = "0"
            while not (nextHand == "1" or nextHand == "2"):
                nextHand = input("Enter 1 for next hand\nEnter 2 to cash out\nEnter 3 to see total\n")
                if nextHand == "2":
                    nextGame = False
                elif nextHand == "1":
                    nextGame = True
                elif nextHand == "3":
                    print(f"\nYour total is: ${self.userTotal}\n")
                    time.sleep(2)
                else:
                    print("Please enter 1, 2, or 3")
                    
    def offer_insurance(self, dealer_hand):
        if self.userTotal >= self.bet / 2:
            print("\nDealer is showing an Ace. Would you like insurance?")
            print("Insurance costs half your bet and pays 2:1 if dealer has blackjack.")
            while True:
                answer = input("Take insurance? (y/n): ").lower()
                if answer == 'y' or answer == 'yes':
                    insurance_bet = self.bet / 2
                    print(f"You bet ${insurance_bet} on insurance.")
                    
                    dealer_value, _ = self.calculate_hand_value(dealer_hand)
                    dealer_has_blackjack = dealer_value == 21 and len(dealer_hand) == 2
                    
                    if dealer_has_blackjack:
                        print("Dealer has blackjack! Insurance pays 2:1.")
                        self.userTotal += insurance_bet * 2
                    else:
                        print("Dealer does not have blackjack. Insurance bet lost.")
                        self.userTotal -= insurance_bet
                    return
                elif answer == 'n' or answer == 'no':
                    print("No insurance taken.")
                    return
                else:
                    print("Please enter y or n.")
        else:
            print("\nDealer is showing an Ace, but you don't have enough money for insurance.")
    
    def play_hand(self, hand, hand_idx, dealer_hand):
        first_action = True
        
        while not hand.is_done:
            hand_value, aces = self.calculate_hand_value(hand.get_cards())
            is_soft = aces > 0 and hand_value <= 21
            
            if hand_value > 21:
                hand.is_busted = True
                hand.is_done = True
                break
                
            print(f"\nHand {hand_idx+1}: {hand.get_card_values()}")
            print(f"Hand value: {hand_value}{' (soft)' if is_soft else ''}")
            
            dealer_value, _ = self.calculate_hand_value(dealer_hand)
            if dealer_value == 21 and len(dealer_hand) == 2:
                print("Dealer has Blackjack!")
                hand.is_done = True
                break
            
            print("Choose an option:")
            print("  1. Hit")
            print("  2. Stand")
            
            can_double = len(hand.get_cards()) == 2 and self.bet <= self.userTotal/2 and first_action
            if can_double:
                print("  3. Double")
                
            can_split = hand.can_split() and self.split_count < self.MAX_SPLITS and first_action
            if can_split:
                print("  4. Split")
                
            can_surrender = first_action and not hand.has_been_split and len(self.hands) == 1
            if can_surrender:
                print("  5. Surrender")
                
            answer = input("What will you do? ")
            
            if answer == "1":
                additional = self.oneDeck.draw()
                hand.add_card(additional)
                print(f"You drew: {additional.returnCard()}")
                first_action = False
                
            elif answer == "2":
                hand.is_done = True
                
            elif answer == "3" and can_double:
                self.bet *= 2
                additional = self.oneDeck.draw()
                hand.add_card(additional)
                print(f"You doubled down and drew: {additional.returnCard()}")
                print(f"Bet is now ${self.bet}")
                time.sleep(2)
                
                hand_value, _ = self.calculate_hand_value(hand.get_cards())
                if hand_value > 21:
                    hand.is_busted = True
                
                hand.is_done = True
                
            elif answer == "4" and can_split:
                card1, card2 = hand.split()
                
                new_hand1 = Hand([card1, self.oneDeck.draw()])
                new_hand2 = Hand([card2, self.oneDeck.draw()])
                
                new_hand1.mark_as_split()
                new_hand2.mark_as_split()
                
                self.hands[hand_idx] = new_hand1
                
                self.hands.append(new_hand2)
                
                self.split_count += 1
                
                print(f"Hand split! Now playing hand {hand_idx+1}.")
                
                hand = new_hand1
                
            elif answer == "5" and can_surrender:
                print("You surrender. Half your bet is returned.")
                self.userTotal -= self.bet / 2
                hand.is_done = True
                hand.is_surrendered = True
                
            else:
                print("Invalid input, try again")
        
    def getUserTotal(self):
        return str(self.userTotal)
        
    def getGains(self):
        return self.userTotal - self.starting
        
print("\nWelcome to Jonathan's Blackjack!")
while True:
    try:
        startingvalue = int(input("How much would you like to buy in for? $"))
        break
    except ValueError:
        print("\nPlease enter a valid number.")
            
game = BlackJack(1, startingvalue)
game.deal()
print()
if game.getGains() < 0:
    print(f"Sorry to say you have lost ${abs(game.getGains())}\n")
else:
    print(f"Congratulations, you have won ${game.getGains()}")
