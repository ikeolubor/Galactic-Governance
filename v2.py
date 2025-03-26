import random

def display_menu(coins, year, available_cards, picked_cards, events):
    print("\n" + "*" * 50)
    print(f"** GALACTIC GOVERNANCE - YEAR {year} **")
    print("*" * 50)
    print(f"Coins: {coins}")
    
    print("\nEvents This Year:")
    if events:
        for event in events:
            print(f"- {event}")
    else:
        print("No major events this year.")

    print("\nAvailable Cards:")
    for idx, card in enumerate(available_cards, 1):
        print(f"{idx}. {card['name']} - Cost: {card['cost']} coins")
        print(f"   -> {card['description']}")
    
    print("\nPicked Cards for this Year:")
    if picked_cards:
        for idx, card in enumerate(picked_cards, 1):
            print(f"{idx}. {card['name']} - Cost: {card['cost']} coins")
    else:
        print("None")
    
    print("\nEnter the number of a card to pick it,")
    print("or type 'r' to remove a card from your selection,")
    print("or '0' to confirm and end your turn (must pick at least one card).")

def get_player_choice(available_cards, coins, year):
    picked_cards = []
    
    while True:
        display_menu(coins, year, available_cards, picked_cards, [])
        choice = input("Your choice: ").strip().lower()
        
        if choice == '0':
            if not picked_cards:
                print("\nYou must pick at least one card before proceeding!")
                continue
            break
        
        elif choice == 'r':
            if not picked_cards:
                print("\nNo cards to remove!")
                continue
            for idx, card in enumerate(picked_cards, 1):
                print(f"{idx}. {card['name']} - Cost: {card['cost']} coins")
            try:
                remove_index = int(input("Enter the number of the card to remove: ")) - 1
                if 0 <= remove_index < len(picked_cards):
                    removed_card = picked_cards.pop(remove_index)
                    coins += removed_card['cost']
                    available_cards.append(removed_card)
                    print(f"\nRemoved {removed_card['name']}. {removed_card['cost']} coins refunded.")
                else:
                    print("\nInvalid card number for removal.")
            except ValueError:
                print("\nInvalid input.")
            continue
        
        else:
            try:
                card_index = int(choice) - 1
                if 0 <= card_index < len(available_cards):
                    selected_card = available_cards[card_index]
                    if selected_card['cost'] <= coins:
                        picked_cards.append(selected_card)
                        coins -= selected_card['cost']
                        available_cards.pop(card_index)
                        print(f"\nYou picked: {selected_card['name']}. Remaining coins: {coins}")
                    else:
                        print("\nInsufficient coins for that card.")
                else:
                    print("\nInvalid card number.")
            except ValueError:
                print("\nInvalid input.")
    
    return picked_cards, coins, available_cards

def check_events(year, picked_cards, coins):
    events = []
    
    # Convert picked cards list into a set for quick lookup
    picked_card_names = {card["name"] for card in picked_cards}

    if year == 2 and "Base Defense" not in picked_card_names:
        events.append("You got raided! -2000 coins lost")
        coins -= 2000

    if year == 3:
        if "Mining Drone Upgrade" not in picked_card_names:
            events.append("Your Mining Drones broke due to lack of upgrades!")
            for card in picked_cards:
                if card["name"] == "Mining Drone":
                    card["profit"] = 0  # Disable mining drones

        if "Access Control" not in picked_card_names:
            events.append("Security Breach! -4000 coins lost")
            coins -= 4000

        if "Risk Assessment" not in picked_card_names:
            events.append("Major cyber attack! -4000 coins lost")
            coins -= 4000

        if "Battery Upgrade" not in picked_card_names:
            events.append("Power failure! -2000 coins lost")
            coins -= 2000

    return events, coins

def show_year_summary(year_profit, coins, events):
    print("\n" + "=" * 50)
    print("Year Summary")
    print("=" * 50)
    
    print("\n--- Year Outcome ---")
    print(f"Profit earned: {year_profit} coins")
    print(f"Total coins now: {coins}")
    
    print("\nEvents:")
    if events:
        for event in events:
            print(f"- {event}")
    else:
        print("No major incidents this year.")
    
    input("\nPress Enter to proceed to the next year...")

def game_loop():
    coins = 10000
    current_year = 1

    base_available_cards_full = [
        {"name": "Mining Drone", "cost": 750, "profit": 2000, "description": "Boosts resource extraction from asteroids."},  # Half price Year 1
        {"name": "Mining Drone", "cost": 750, "profit": 2000, "description": "Boosts resource extraction from asteroids."},
        {"name": "Mining Drone", "cost": 750, "profit": 2000, "description": "Boosts resource extraction from asteroids."},
        {"name": "Mining Drone", "cost": 750, "profit": 2000, "description": "Boosts resource extraction from asteroids."},
        {"name": "Mining Drone Upgrade", "cost": 2000, "profit": 0, "description": "Enhances efficiency of mining drones."},
        {"name": "Research Lab", "cost": 2500, "profit": 0, "description": "Unlocks new technologies and innovations."},
        {"name": "Risk Assessment", "cost": 1000, "profit": 0, "description": "Identifies potential security vulnerabilities."},
        {"name": "Hydroponic Farm", "cost": 2000, "profit": 0, "description": "Provides sustainable food supply."},
        {"name": "Storage Upgrade", "cost": 1800, "profit": 0, "description": "Expands storage for critical resources."},
        {"name": "Base Defense", "cost": 3000, "profit": 0, "description": "Improves defenses against external threats."},
        {"name": "Battery Upgrade", "cost": 1700, "profit": 0, "description": "Enhances energy storage and resilience."},
        {"name": "Access Control", "cost": 2000, "profit": 0, "description": "Enhances Access Control System."}
    ]

    available_cards = base_available_cards_full.copy()

    while current_year <= 4:
        picked_cards, coins, available_cards = get_player_choice(available_cards, coins, current_year)
        year_profit = sum(card['profit'] for card in picked_cards)
        coins += year_profit
        
        events, coins = check_events(current_year, picked_cards, coins)

        show_year_summary(year_profit, coins, events)

        current_year += 1

    print("\n" + "=" * 50)
    print("Game Over!")
    print(f"Final coin balance: {coins}")
    print("=" * 50)

def start_game():
    input("Press Enter to Start the Game...")
    game_loop()

if __name__ == '__main__':
    start_game()
