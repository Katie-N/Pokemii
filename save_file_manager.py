import os
import csv

class SaveFileManager:
    def __init__(self, save_directory="saves"):
        self.save_directory = save_directory
        try:
            if not os.path.exists(self.save_directory):
                os.makedirs(self.save_directory)
        except OSError as e:
            print(f"Error creating save directory: {e}")

    def get_save_files(self):
        """Returns a list of available save files (CSV files) in the save directory."""
        save_files = []
        try:
            for filename in os.listdir(self.save_directory):
                if filename.endswith(".csv"):
                    save_files.append(filename)
        except FileNotFoundError:
            print(f"Save directory not found: {self.save_directory}")
        except OSError as e:
            print(f"Error accessing save directory: {e}")
        return save_files

    def load_save_file(self, filename):
        """Loads data from a specified save file."""
        filepath = os.path.join(self.save_directory, filename)
        if not os.path.exists(filepath):
            print(f"Error: Save file '{filename}' not found.")
            return None

        try:
            with open(filepath, 'r', newline='') as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]
                return data
        except FileNotFoundError:
            print(f"Error: Save file '{filename}' not found.")
            return None
        except csv.Error as e:
            print(f"Error reading CSV file '{filename}': {e}")
            return None
        except Exception as e:
            print(f"Error loading save file '{filename}': {e}")
            return None

    def save_data(self, filename, data):
        """Saves data to a specified save file."""
        filepath = os.path.join(self.save_directory, filename)
        try:
            with open(filepath, 'w', newline='') as file:
                if data and isinstance(data[0], dict):
                    writer = csv.DictWriter(file, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    writer = csv.writer(file)
                    writer.writerows(data)
        except TypeError as e:
            print(f"Error: Data is not in the correct format: {e}")
        except csv.Error as e:
            print(f"Error writing to CSV file '{filename}': {e}")
        except Exception as e:
            print(f"Error saving data to '{filename}': {e}")

# SAVING LOGIC
# --- Save File Manager ---
save_manager = SaveFileManager()

def selectSave(filename):
    if not filename or (filename not in save_manager.get_save_files()):
        print("Invalid filename")
        return -1
    data = save_manager.load_save_file(filename)
    if data is not None:
        print(f"You selected: {filename}\nWhich has the data: {data}")
    else:
        print(f"Failed to load data from {filename}")

def create_new_save():
    new_data = [{"name": "Player 1", "score": 100}, {"name": "Player 2", "score": 150}]
    try:
        name = input("Name for new save:")
        save_manager.save_data(f"{name}.csv", new_data)
        print(f"Created new save file: {name}.csv")
    except Exception as e:
        print(f"Error creating new save: {e}")
