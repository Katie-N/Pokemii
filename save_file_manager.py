import os
import csv
import globalSettings

class SaveFileManager:
    def __init__(self, save_directory="saves", save_file="Players.csv"):
        self.save_directory = save_directory
        self.save_file = save_file
        self.save_filepath = os.path.join(self.save_directory, self.save_file)
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        if not os.path.exists(self.save_filepath):
            self.__create_empty_save_file__()

    def __create_empty_save_file__(self):
        """Creates an empty save file with headers if it doesn't exist."""
        with open(self.save_filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Id","Name", "Score", "Health", "Team Member 1", "Team Member 2", "Team Member 3"])  # Add headers
            print("wrote empty new save file")

    def get_save_file_ids(self):
        """Returns a list of available save names from the save file."""
        save_ids = []
        print("get_save_file")
        try:
            with open(self.save_filepath, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    save_ids.append(row["Id"])
        except Exception as e:
            print(f"Error reading save file: {e}")
        print(save_ids)
        return save_ids

    def load_save_file(self, save_id):
        """Loads data from a specified save name."""
        try:
            with open(self.save_filepath, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Id"] == save_id:
                        print(row)
                        return row
        except Exception as e:
            print(f"Error loading save file: {e}")
        return None

    # Function to update the player.csv file with the latest data
    # Call this function after the player levels up, loses health, imports a mii, etc. 
    def save_data(self, save_id, data):
        """Saves data to a specified save name."""
        try:
            existing_data = []
            save_found = False
            with open(self.save_filepath, 'r', newline='') as file:
                reader = csv.DictReader(file)
                existing_data = list(reader)
                for row in existing_data:
                    if row["Id"] == save_id:
                        row.update(data)
                        save_found = True
                        break
            if not save_found:
                data["Id"] = save_id
                existing_data.append(data)

            with open(self.save_filepath, 'w', newline='') as file:
                if existing_data:
                    writer = csv.DictWriter(file, fieldnames=existing_data[0].keys())
                    writer.writeheader()
                    writer.writerows(existing_data)
        except Exception as e:
            print(f"Error saving data: {e}")

    def new_player(self, name=""):
        # Get existing save IDs and find the next unused number
        existing_ids = self.get_save_file_ids()
        used_ids = set()

        for save_id in existing_ids:
            try:
                used_ids.add(int(save_id))
            except ValueError:
                pass  # Skip any non-integer IDs

        # Find the smallest unused integer ID starting from 1
        next_id = 1
        while next_id in used_ids:
            next_id += 1

        # Use the new ID
        new_id = str(next_id)

        new_data = {
            "Id": new_id,
            "Name": name,
            "Score": "0",
            "Health": "100",
            "Team Member 1": "",
            "Team Member 2": "",
            "Team Member 3": ""
        }

        self.save_data(new_id, new_data)
        print(f"Created new player save with Id '{new_id}'")
        return new_id  # In case you want to use it after creation
    def login_user(self, saveId, saveData = None):
        if (saveData):
            globalSettings.saveData = saveData
            print("printing from if", globalSettings.saveData)
        
        else:
            globalSettings.saveData = self.load_save_file(saveId)
            print(globalSettings.saveData)


# SAVING LOGIC
# --- Save File Manager ---
save_manager = SaveFileManager()