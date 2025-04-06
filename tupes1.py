pokemon_type_chart = {
    "Normal": {
        "weaknesses": ["Fighting"],
        "resistances": [],
        "immunities": [],
        "color" :["white"],
    },
    "Fire": {
        "weaknesses": ["Water"],
        "resistances": ["Fire", "Grass", "Ice", "Bug", "", "Fairy"],
        "immunities": [],
        "color" :["orange"],
    },
    "Water": {
        "weaknesses": ["Grass", "Electric"],
        "resistances": ["Fire", "Water", "Ice"],
        "immunities": [],
        "color" :["dark blue"],
    },
    "Grass": {
        "weaknesses": ["Fire", "Ice", "Poison", "Bug"],
        "resistances": ["Water", "Grass", "Electric", ],
        "immunities": [],
        "color" :["green"],
    },
    "Electric": {
        "weaknesses": [],
        "resistances": ["Electric"],
        "immunities": [],
        "color" :["yellow"],
    },
    "Ice": {
        "weaknesses": ["Fire", "Fighting"],
        "resistances": ["Ice"],
        "immunities": [],
        "color" :["light blue"],
    },
    "Fighting": {
        "weaknesses": ["Fairy"],
        "resistances": ["Bug", "Dark"],
        "immunities": [],
        "color" :["red"],
    },
    "Poison": {
        "weaknesses": [],
        "resistances": ["Grass", "Fighting", "Poison", "Bug", "Fairy"],
        "immunities": [],
        "color" :["purple"],
    },
    
    "Bug": {
        "weaknesses": ["Fire"],
        "resistances": ["Grass", "Fighting"],
        "immunities": [],
        "color" :["lime"],
    },
    
    "Dark": {
        "weaknesses": ["Fighting", "Bug", "Fairy"],
        "resistances": ["Dark"],
        "immunities": [],
        "color" :["black"],
    },
    "Fairy": {
        "weaknesses": ["Poison"],
        "resistances": ["Fighting", "Bug", "Dark"],
        "immunities": [],
        "color" :["pink"],
    },
}

# Example usage:
# To get the weaknesses of the Fire type:
#fire_weaknesses = pokemon_type_chart["Fire"]["weaknesses"]
#print(f"Fire type weaknesses: {fire_weaknesses}")

# To check if Water is a weakness of :
#if "Water" in pokemon_type_chart["weaknesses"]:
#    print("Water is a weakness of .")