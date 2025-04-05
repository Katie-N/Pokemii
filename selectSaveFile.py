from save_file_manager import SaveFileManager
save_manager = SaveFileManager()

def getSaveData(filename):
    if not filename or (filename not in save_manager.get_save_files()):
        print("Invalid filename")
        return -1
    # Create a SaveFileManager instance

    data = save_manager.load_save_file(filename)
    return data
    # if data:
    #     print(f"You selected: {selected_file}")
    #     # Load the data
    #     data = save_manager.load_save_file(selected_file)
    #     if data:
    #         print("Loaded data:")
    #         for row in data:
    #             print(row)
    #     else:
    #         print("Failed to load data.")
        
    # else:
    #     print("No save file selected.")
