import globalSettings
import save_file_manager
import random
from enum import Enum
# --- Game States ---
class GameState(Enum):
    """Enumeration for different game states."""
    MENU = 0
    CREDITS = 1
    GAME_MENU = 2
    OPTIONS = 3

# --- Game Class ---
class Game:
    """Manages the game state and logic."""

    def __init__(self):
        self.opponentHealth = 100
        self.opponentMaxHealth = 100
        self.gameOver = False
        self.turn = 1
        self.harden_active = False
        self.empower_active = False

        self.experience_needed = 100 + (globalSettings.saveData["Level"] - 1) * 50  # Calculate experience needed for the current level

    def opponent_turn(self):
        """Simulates the opponent's turn."""
        moves = {
            "Kick": lambda: self._apply_damage(5),
            "Heal": lambda: self._heal_opponent(10),
            "Stomp": lambda: self._apply_damage(10),
            "Scratch": lambda: self._apply_damage(20),
        }
        chosen_move = random.choice(list(moves.keys()))
        print(f"Opponent used {chosen_move}!")
        moves[chosen_move]()
        self.end_turn()

    def _apply_damage(self, damage):
        """Applies damage to the player."""
        damage_multiplier = 0.5 if self.harden_active else 1
        globalSettings.saveData["Current Health"] -= damage * damage_multiplier
        if globalSettings.saveData["Current Health"] <= 0 or self.opponentHealth <= 0:
            self.check_win()

    def _heal_opponent(self, heal_amount):
        """Heals the opponent."""
        if self.opponentHealth < globalSettings.saveData["Max Health"]:
            self.opponentHealth += heal_amount
        self.opponentHealth = min(self.opponentHealth, globalSettings.saveData["Max Health"])  # Ensure health doesn't exceed max
        print("Opponent healed itself!")

    def end_turn(self):
        """Ends the current turn and switches to the next."""
        # Only execute the turn if the game is not over.
        # This fixed the bug where the game would end, everything would be reset, but the queued end_turn() calls would execute. 
        if self.gameOver == False:
            print("Turn Ended")

            if globalSettings.saveData["Current Health"] <= 0 or self.opponentHealth <= 0:
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
        self.opponentHealth -= 25 * damage_multiplier
        if globalSettings.saveData["Current Health"] <= 0 or self.opponentHealth <= 0:
            self.check_win()
        self.end_turn()
        self.empower_active = False

    def player_heal(self):
        """Handles the player's heal action."""
        if globalSettings.saveData["Current Health"] < globalSettings.saveData["Max Health"]:
            globalSettings.saveData["Current Health"] += 20
        # Don't let the player heal over max health
        globalSettings.saveData["Current Health"] = min(globalSettings.saveData["Current Health"], globalSettings.saveData["Max Health"])
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
        if self.opponentHealth <= 0:
            globalSettings.saveData["Experience"] += 50  # Increase experience on win
            self.check_level_up()
            print("You win!")
            # After a win the game should always end before the next turn. 
            self.gameOver = True

        elif globalSettings.saveData["Current Health"] <= 0:
            print("You lose!")
            # After a lose the game should always end before the next turn. 
            self.gameOver = True
        print("RESETTING")
        self.reset_game()

    def check_level_up(self):
        """Checks if the player has leveled up."""
        while globalSettings.saveData["Experience"] >= self.experience_needed:
            globalSettings.saveData["Level"] += 1
            globalSettings.saveData["Experience"] -= self.experience_needed
            self.experience_needed += 50  # Increase experience needed for next level
            print(f"Level Up! You are now level {globalSettings.saveData['Level']}!")

    def reset_game(self):
        """Resets the game state."""
        globalSettings.saveData["Current Health"] = globalSettings.saveData["Max Health"]
        save_file_manager.save_manager.save_progress()  # Save progress to the save file
        self.opponentHealth = 100
        self.turn = 1
        self.harden_active = False
        self.empower_active = False
        globalSettings.current_state = GameState.MENU
