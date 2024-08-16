def get_card_value(card):
    """Convert card input to its numerical value."""
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)

def get_hand_value(cards):
    """Calculate the value of a hand."""
    value = sum(get_card_value(card) for card in cards)
    # Adjust for Aces
    num_aces = cards.count('A')
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def is_soft_hand(cards):
    """Determine if a hand is soft (contains an Ace counted as 11)."""
    return 'A' in cards and get_hand_value(cards) <= 21

def basic_strategy(player_cards, dealer_upcard):
    """Provide advice based on basic strategy."""
    player_value = get_hand_value(player_cards)
    dealer_value = get_card_value(dealer_upcard)

    if player_value > 21:
        return "You've busted!"
    elif player_value == 21:
        return "Congratulations! You have Blackjack!"

    # Check for splits
    if len(player_cards) == 2 and player_cards[0] == player_cards[1]:
        if player_cards[0] in ['A', '8']:
            return "Split"
        elif player_cards[0] in ['2', '3', '7'] and dealer_value in range(2, 8):
            return "Split"
        elif player_cards[0] == '6' and dealer_value in range(2, 7):
            return "Split"
        elif player_cards[0] == '9' and dealer_value in [2, 3, 4, 5, 6, 8, 9]:
            return "Split"
        elif player_cards[0] in ['5', '10']:
            return "Do not split"

    # Check for hard hands
    if not is_soft_hand(player_cards):
        if player_value in range(5, 9):
            return "Hit"
        elif player_value == 9 and dealer_value in range(3, 7):
            return "Double Down"
        elif player_value == 10 and dealer_value in range(2, 10):
            return "Double Down"
        elif player_value == 11 and dealer_value in range(2, 11):
            return "Double Down"
        elif player_value in range(12, 17) and dealer_value in range(7, 12):
            return "Hit"
        elif player_value in range(12, 17) and dealer_value in range(2, 7):
            return "Stand"
        elif player_value >= 17:
            return "Stand"

    # Check for soft hands
    if is_soft_hand(player_cards):
        if player_value in range(13, 18) and dealer_value in [5, 6]:
            return "Double Down"
        elif player_value in range(13, 18):
            return "Hit"
        elif player_value == 18 and dealer_value in [2, 7, 8]:
            return "Stand"
        elif player_value == 18:
            return "Hit"
        elif player_value >= 19:
            return "Stand"

    # Check for surrender
    if player_value == 16 and dealer_value in [9, 10, 11]:
        return "Surrender"
    elif player_value == 15 and dealer_value == 10:
        return "Surrender"

    return "Stand"

def is_valid_card(card):
    """Check if the entered card is valid."""
    return card.isdigit() and 2 <= int(card) <= 10 or card in ['A', 'J', 'Q', 'K']

def get_player_cards():
    """Prompt the player to enter valid cards."""
    while True:
        player_input = input("Enter your two cards (e.g., '2 8'): ").split()
        if len(player_input) == 2 and all(is_valid_card(card) for card in player_input):
            return player_input
        else:
            print("Invalid input. Please enter two valid cards (2-10, J, Q, K, A).")

def get_dealer_upcard():
    """Prompt the player to enter a valid dealer upcard."""
    while True:
        dealer_upcard = input("Enter the dealer's upcard: ")
        if is_valid_card(dealer_upcard):
            return dealer_upcard
        else:
            print("Invalid input. Please enter a valid card (2-10, J, Q, K, A).")

def main():
    while True:
        player_cards = get_player_cards()
        dealer_upcard = get_dealer_upcard()

        advice = basic_strategy(player_cards, dealer_upcard)
        print(f"Advice: {advice}")

        if advice == "Hit":
            while True:
                new_card = input("Enter the new card you received: ")
                if is_valid_card(new_card):
                    player_cards.append(new_card)
                    advice = basic_strategy(player_cards, dealer_upcard)
                    print(f"Advice: {advice}")
                    if advice != "Hit":
                        break
                else:
                    print("Invalid input. Please enter a valid card (2-10, J, Q, K, A).")

        continue_playing = input("Do you want to play another hand? (yes/no): ").lower()
        if continue_playing != 'yes':
            break

if __name__ == "__main__":
    main()
