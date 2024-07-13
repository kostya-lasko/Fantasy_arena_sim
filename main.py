import random
import time
from collections import defaultdict
from tabulate import tabulate


# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

class Character:
    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.health = random.randint(80, 120)
        self.max_health = self.health
        self.attack = random.randint(13, 20)
        self.defense = random.randint(0, 10)
        self.wins = 0
        self.special_ability_cooldown = 0
        self.rage_available = character_class == "Barbarian"
        self.dodge_chance = 0.05  # 5% base dodge chance
        self.apply_class_modifiers()
        self.range = self.set_range()

    def apply_class_modifiers(self):
        if self.character_class == "Fighter":
            self.attack += 5
            self.defense += 5
        elif self.character_class == "Mage":
            self.attack += 10
            self.health -= 10
            self.max_health -= 10
        elif self.character_class == "Ranger":
            self.attack += 5
            #self.defense += 2
            self.dodge_chance += 0.05  # Rangers have higher dodge chance
        elif self.character_class == "Barbarian":
            self.health += 30
            self.max_health += 30
            self.attack += 5
        elif self.character_class == "Rogue":
            self.attack += 7
            self.defense += 3
            self.dodge_chance += 0.1  # Rogues have the highest dodge chance
        elif self.character_class == "Cleric":
            self.health += 10
            self.max_health += 10
            self.defense += 7
        elif self.character_class == "Assassin":
            self.attack += 8
            self.health -= 5
            self.max_health -= 5
            self.dodge_chance += 0.07  # Assassins have high dodge chance

    def set_range(self):
        if self.character_class in ["Fighter", "Barbarian", "Rogue", "Assassin"]:
            return 1  # Melee range
        elif self.character_class in ["Mage", "Ranger"]:
            return 5  # Long range
        else:  # Cleric
            return 3  # Medium range

    def attack_opponent(self, opponent, distance):
        if distance <= self.range:
            if random.random() < opponent.dodge_chance:
                return 0, "dodged"
            damage = max(0, self.attack - opponent.defense)
            opponent.health -= damage
            return damage, "hit"
        else:
            return 0, "out of range"

    def use_special_ability(self, opponent, distance):
        if self.special_ability_cooldown > 0:
            return f"{self.name}'s special ability is on cooldown. {self.special_ability_cooldown} turns remaining."

        if self.character_class == "Fighter":
            if distance <= self.range:
                damage = self.attack * 1.5
                opponent.health -= damage
                self.special_ability_cooldown = 3
                return f"{self.name} uses Powerful Strike, dealing {RED}{damage}{RESET} damage!"
            else:
                return f"{self.name} is too far to use Powerful Strike."
        elif self.character_class == "Mage":
            damage = random.randint(15, 30)
            opponent.health -= damage
            self.special_ability_cooldown = 2
            return f"{self.name} casts Fireball, dealing fire {RED}{damage}{RESET} damage!"
        elif self.character_class == "Ranger":
            self.attack += 5
            self.special_ability_cooldown = 2
            return f"{self.name} uses Precise Aim, increasing attack by 5!"
        elif self.character_class == "Barbarian":
            self.attack += 5
            self.special_ability_cooldown = 5
            self.defense -= 2
            return f"{self.name} enters a Berserker Rage, increasing attack by 5, but decreasing their defence!"
        elif self.character_class == "Rogue":
            if distance <= self.range:
                damage = self.attack + 10
                opponent.health -= damage
                self.special_ability_cooldown = 2
                return f"{self.name} performs a Sneak Attack, dealing {RED}{damage}{RESET} damage!"
            else:
                return f"{self.name} is too far to use Sneak Attack."
        elif self.character_class == "Cleric":
            heal = random.randint(10, 25)
            self.health = min(self.max_health, self.health + heal)
            self.special_ability_cooldown = 3
            return f"{self.name} uses Heal, restoring {GREEN}{heal}{RESET} health!"
        elif self.character_class == "Assassin":
            if distance <= self.range:
                damage = self.attack * 2
                opponent.health -= damage
                self.special_ability_cooldown = 2
                return f"{self.name} uses Deadly Strike, dealing {RED}{damage}{RESET} damage!"
            else:
                return f"{self.name} is too far to use Deadly Strike."

def create_character():
    name = input("Enter character name: ")
    
    classes = ["Fighter", "Mage", "Ranger", "Barbarian", "Rogue", "Cleric", "Assassin"]
    print("Available classes:")
    for i, class_name in enumerate(classes, 1):
        print(f"{i}. {class_name}")
    
    while True:
        choice = input("Choose a class (enter number or name): ")
        if choice.isdigit() and 1 <= int(choice) <= len(classes):
            character_class = classes[int(choice) - 1]
            break
        elif choice.capitalize() in classes:
            character_class = choice.capitalize()
            break
        else:
            print("Invalid choice. Please try again.")
    
    return Character(name, character_class)

def display_character_stats(character):
    print(f"\n{character.name} ({character.character_class}) Stats:")
    print(f"Health: {character.health}")
    print(f"Attack: {character.attack}")
    print(f"Defense: {character.defense}")
    print(f"Range: {character.range}")
    print(f"Dodge Chance: {character.dodge_chance * 100:.1f}%")

def battle(char1, char2, silent=False):
    if not silent:
        print("\n--- Pre-combat Stats ---")
        display_character_stats(char1)
        display_character_stats(char2)
        print(f"\n--- {char1.name} ({char1.character_class}) vs {char2.name} ({char2.character_class}) ---")
    
    turn = 0
    distance = 10  # Starting distance between characters
    special_ability_uses = 0

    while char1.health > 0 and char2.health > 0:
        turn += 1
        if not silent:
            print(f"\nRound {turn}")
            print(f"Distance between combatants: {distance}")

        attacker = char1 if turn % 2 != 0 else char2
        defender = char2 if turn % 2 != 0 else char1

        # Movement phase
        if distance > attacker.range:
            move = min(2, distance - attacker.range)
            distance -= move
            if not silent:
                print(f"{attacker.name} moves {move} units closer.")

        # Attack phase
        if random.random() < 0.2 and attacker.special_ability_cooldown == 0:
            if not silent:
                print(attacker.use_special_ability(defender, distance))
            special_ability_uses += 1
        else:
            damage, result = attacker.attack_opponent(defender, distance)
            if not silent:
                if result == "hit":
                    print(f"{attacker.name} deals {RED}{damage}{RESET} damage to {defender.name}")
                elif result == "dodged":
                    print(f"{defender.name} dodges {attacker.name}'s attack!")
                else:
                    print(f"{attacker.name} is out of range to attack.")

        if not silent:
            print(f"{char1.name}: {GREEN}{char1.health}{RESET} HP | {char2.name}: {GREEN}{char2.health}{RESET} HP")

        if defender.health <= 0:
            if defender.character_class == "Barbarian" and defender.rage_available:
                defender.rage_available = False
                defender.health = random.randint(10, 20)
                if not silent:
                    print(f"{defender.name} is filled with Rage and stands back up with {GREEN}{defender.health}{RESET} HP!")
            else:
                if not silent:
                    print(f"{attacker.name} wins!")
                attacker.wins += 1
                break

        # Reduce cooldowns
        char1.special_ability_cooldown = max(0, char1.special_ability_cooldown - 1)
        char2.special_ability_cooldown = max(0, char2.special_ability_cooldown - 1)
        
        if not silent:
            time.sleep(1)
            print()  # Empty line between rounds

    winner = attacker if defender.health <= 0 else defender
    loser = defender if defender.health <= 0 else attacker

    # Reset health and cooldowns for next battle
    char1.health = char1.max_health
    char2.health = char2.max_health
    char1.special_ability_cooldown = 0
    char2.special_ability_cooldown = 0
    char1.rage_available = char1.character_class == "Barbarian"
    char2.rage_available = char2.character_class == "Barbarian"

    return {
        "winner": winner.character_class,
        "loser": loser.character_class,
        "rounds": turn,
        "winner_health": winner.health,
        "special_ability_uses": special_ability_uses,
        "first_attacker": char1.character_class
    }

def test_specific_combination(class1, class2):
    print(f"Testing {class1} vs {class2}")
    for i in range(10):  # Run fewer iterations for quick testing
        char1 = Character("Player1", class1)
        char2 = Character("Player2", class2)
        battle_result = battle(char1, char2, silent=False)
        print(battle_result)

def run_balance_test():
    classes = ["Fighter", "Mage", "Ranger", "Barbarian", "Rogue", "Cleric", "Assassin"]
    results = defaultdict(lambda: defaultdict(lambda: {
        "wins": 0,
        "total_rounds": 0,
        "total_winner_health": 0,
        "special_ability_uses": 0,
        "first_attacker_wins": 0
    }))

    total_battles = len(classes) * (len(classes) - 1) * 1000
    battles_completed = 0
    start_time = time.time()
    timeout = 300  # 5 minutes timeout

    try:
        for class1 in classes:
            for class2 in classes:
                if class1 != class2:
                    print(f"Testing {class1} vs {class2}")
                    for i in range(1000):
                        if time.time() - start_time > timeout:
                            raise TimeoutError("Balance test took too long to complete")
                        
                        char1 = Character("Player1", class1)
                        char2 = Character("Player2", class2)
                        battle_result = battle(char1, char2, silent=True)

                        results[class1][class2]["wins"] += 1 if battle_result["winner"] == class1 else 0
                        results[class1][class2]["total_rounds"] += battle_result["rounds"]
                        results[class1][class2]["total_winner_health"] += battle_result["winner_health"]
                        results[class1][class2]["special_ability_uses"] += battle_result["special_ability_uses"]
                        results[class1][class2]["first_attacker_wins"] += 1 if battle_result["winner"] == battle_result["first_attacker"] else 0

                        battles_completed += 1
                        if battles_completed % 100 == 0:
                            elapsed_time = time.time() - start_time
                            estimated_total_time = (elapsed_time / battles_completed) * total_battles
                            remaining_time = estimated_total_time - elapsed_time
                            print(f"Progress: {battles_completed}/{total_battles} battles completed")
                            print(f"Estimated time remaining: {remaining_time:.2f} seconds")

    except TimeoutError as e:
        print(f"Warning: {str(e)}")
        print(f"Completed {battles_completed} out of {total_battles} planned battles")

    total_time = time.time() - start_time
    print(f"Total time taken: {total_time:.2f} seconds")

    return results

def display_summary_table(results):
    classes = list(results.keys())
    table = []
    headers = ["Class"] + classes

    for class1 in classes:
        row = [class1]
        for class2 in classes:
            if class1 == class2:
                row.append("-")
            else:
                wins = results[class1][class2]["wins"]
                percentage = (wins / 1000) * 100
                row.append(f"{wins} ({percentage:.2f}%)")
        table.append(row)

    print("\n--- Win Summary Table ---")
    print(tabulate(table, headers=headers, tablefmt="grid"))

    print("\n--- Win Summary Table ---")
    print(tabulate(table, headers=headers, tablefmt="grid"))

def display_balance_results(results):
    classes = list(results.keys())
    
    print("\n--- Balance Test Results ---")
    
    for class1 in classes:
        print(f"\n{class1} Results:")
        for class2 in classes:
            if class1 != class2:
                matchup_results = results[class1][class2]
                win_percentage = (matchup_results["wins"] / 1000) * 100
                avg_rounds = matchup_results["total_rounds"] / 1000
                avg_winner_health = matchup_results["total_winner_health"] / 1000
                special_ability_percentage = (matchup_results["special_ability_uses"] / 1000) * 100
                first_attacker_win_percentage = (matchup_results["first_attacker_wins"] / 1000) * 100
                
                print(f"  vs {class2}:")
                print(f"    Win Rate: {win_percentage:.2f}%")
                print(f"    Avg. Rounds: {avg_rounds:.2f}")
                print(f"    Avg. Winner Health: {avg_winner_health:.2f}")
                print(f"    Special Ability Use: {special_ability_percentage:.2f}%")
                print(f"    First Attacker Win Rate: {first_attacker_win_percentage:.2f}%")

def main():
    mode = input("Enter the number of players (or 'test' for balance mode): ")
    
    if mode.lower() == 'test':
        print("Running balance test...")
        results = run_balance_test()
        display_balance_results(results)
        display_summary_table(results)
    else:
        try:
            num_players = int(mode)
            characters = [create_character() for _ in range(num_players)]

            for i in range(len(characters)):
                for j in range(i+1, len(characters)):
                    battle(characters[i], characters[j])

            winner = max(characters, key=lambda x: x.wins)
            print(f"\nThe overall winner is {winner.name} ({winner.character_class}) with {winner.wins} wins!")
        except ValueError:
            print("Invalid input. Please enter a number or 'test'.")

if __name__ == "__main__":
    main()
