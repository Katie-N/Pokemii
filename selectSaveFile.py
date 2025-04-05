from save_file_manager import SaveFileManager

# Create a SaveFileManager instance
save_manager = SaveFileManager()

# Choose a save file
selected_file = save_manager.choose_save_file()

if selected_file:
    print(f"You selected: {selected_file}")
    # Load the data
    data = save_manager.load_save_file(selected_file)
    if data:
        print("Loaded data:")
        for row in data:
            print(row)
    else:
        print("Failed to load data.")
    
else:
    print("No save file selected.")
