import os
import csv

class SaveFileManager:
    def __init__(self, save_directory="saves"):
        self.save_directory = save_directory
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def get_save_files(self):
        """Returns a list of available save files (CSV files) in the save directory."""
        save_files = []
        for filename in os.listdir(self.save_directory):
            if filename.endswith(".csv"):
                save_files.append(filename)
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
        except Exception as e:
            print(f"Error loading save file: {e}")
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
        except Exception as e:
            print(f"Error saving data: {e}")

    # def choose_save_file(self):
    #     """Allows the user to choose a save file from the console."""
    #     save_files = self.get_save_files()

    #     if not save_files:
    #         new_data = [{"name": "Player 1", "score": 100}, {"name": "Player 2", "score": 150}]
    #         print("No save files found.")
    #         name = input("Name for new save:")
    #         self.save_data(f"{name}.csv", new_data)
    #         return self.get_save_files()[0]
    #     else:
    #         print("Available save files:")
    #         for i, filename in enumerate(save_files):
    #             print(f"{i + 1}. {filename}")
    #         while True:
    #             try:
    #                 choice = int(input("Enter the number of the save file to load: "))
    #                 if 1 <= choice <= len(save_files):
    #                     return save_files[choice - 1]
    #                 else:
    #                     print("Invalid choice. Please enter a number from the list.")
    #             except ValueError:
    #                 print("Invalid input. Please enter a number.")
