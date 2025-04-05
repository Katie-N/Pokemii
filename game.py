import pygame
import random
from typing import List
from Types import pokemon_type_chart


class Game:
    """Manages the game state and logic."""

    def __init__(self):
        
        self.health = 100
        self.health2 = 100
        self.turn = 1
        self.max_health = 100
        self.harden_active = False
        self.empower_active = False
        self.experience = 0
        self.experience_needed = 100
        self.level = 1
        # New attribute: names
        self.player_name = "Jimmy"
        self.opponent_name = "Opponent"
        #Console log
        self.console_logs: List[str] = []
        self.show_console = False #changed to false
        self.player_type = "Fire"  # Example type
        self.opponent_type = random.choice(list(pokemon_type_chart.keys())) #added to choose a random type
        self.opponent_color = random.choice(pokemon_type_chart[self.opponent_type]["color"]) #added to choose a random color

    def opponent_turn(self):
        """Simulates the opponent's turn."""
        self.add_log(f"{self.opponent_name}'s turn")
        moves = {
            "Kick": lambda: self._apply_damage(5),
            "Heal": lambda: self._heal_opponent(10),
            "Stomp": lambda: self._apply_damage(10),
            "Scratch": lambda: self._apply_damage(20),
        }
        chosen_move = random.choice(list(moves.keys()))
        log = f"{self.opponent_name} used {chosen_move}!"
        self.add_log(log)
        moves[chosen_move]()
        self.end_turn()
        self.show_console = True #added to show the console after the turn

    def _apply_damage(self, damage):
        """Applies damage to the player."""
        damage_multiplier = 0.5 if self.harden_active else 1
        type_multiplier = self.calculate_type_effectiveness(self.opponent_type, self.player_type)
        self.health -= damage * damage_multiplier * type_multiplier
        if self.health <= 0 or self.health2 <= 0:
            self.check_win()

    def add_log(self, log: str):
        self.console_logs.append(log)
        if len(self.console_logs) > 5:  # Reduced to 5 for better fit
            self.console_logs.pop(0)

    def _heal_opponent(self, heal_amount):
        """Heals the opponent."""
        if self.health2 < self.max_health:
            self.health2 += heal_amount
        self.health2 = min(self.health2, self.max_health)  # Ensure health doesn't exceed max
        self.add_log(f"{self.opponent_name} healed itself!")

    def end_turn(self):
        """Ends the current turn and switches to the next."""
        self.add_log("Turn Ended")
        if self.health <= 0 or self.health2 <= 0:
            self.check_win()
        elif self.turn == 1:
            self.turn = 2
            self.opponent_turn()
        elif self.turn == 2:
            self.turn = 1
            self.harden_active = False

    def player_kick(self):
        """Handles the player's kick action."""
        damage_multiplier = 2 if self.empower_active else 1
        type_multiplier = self.calculate_type_effectiveness(self.player_type, self.opponent_type)
        self.health2 -= 25 * damage_multiplier * type_multiplier
        if self.health <= 0 or self.health2 <= 0:
            self.check_win()
        self.end_turn()
        self.empower_active = False

    def player_heal(self):
        """Handles the player's heal action."""
        if self.health < self.max_health:
            self.health += 20
        self.health = min(self.health, self.max_health)
        self.end_turn()

    def player_harden(self):
        """Handles the player's harden action."""
        self.harden_active = True
        self.end_turn()

    def player_empower(self):
        """Handles the player's empower action."""
        self.empower_active = True
        self.end_turn()

    def check_win(self):
        """Checks if the player has won and updates experience."""
        if self.health2 <= 0:
            self.experience += 50  # Increase experience on win
            self.check_level_up()
            self.add_log("You won!")
        else:
            self.add_log("You lost")
        self.reset_game()

    def check_level_up(self):
        """Checks if the player has leveled up."""
        while self.experience >= self.experience_needed:
            self.level += 1
            self.experience -= self.experience_needed
            self.experience_needed += 50  # Increase experience needed for next level
            self.add_log(f"Level Up! You are now level {self.level}!")

    def reset_game(self):
        """Resets the game state."""
        from actions import GameState, current_state
        self.health = 100
        self.health2 = 100
        self.turn = 1
        self.harden_active = False
        self.empower_active = False
        self.opponent_type = random.choice(list(pokemon_type_chart.keys())) #added to choose a random type
        self.opponent_color = random.choice(pokemon_type_chart[self.opponent_type]["color"]) #added to choose a random color
        current_state = GameState.MAIN_MENU

    def calculate_type_effectiveness(self, attacking_type, defending_type):
        """Calculates type effectiveness multiplier."""
        if defending_type in pokemon_type_chart[attacking_type]["weaknesses"]:
            return 2.0  # Super effective
        elif defending_type in pokemon_type_chart[attacking_type]["resistances"]:
            return 0.5  # Not very effective
        elif defending_type in pokemon_type_chart[attacking_type]["immunities"]:
            return 0.0  # No effect
        else:
            return 1.0  # Normal effectiveness
