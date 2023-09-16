from Towers import *
import random


min_weight = None
max_weight = None


def generate_random_towers(max_weight):
    current_weight = 0
    selected_towers = []

    selectable_towers = [frozenset(tower.items()) for tower in SELECTABLE_WEIGHTED_TOWERS]

    # Keep track of towers that have been used to prevent duplicates
    used_towers = set()

    max_iterations = 30  # Set a limit on the number of iterations
    iteration_count = 0

    with open("settings.txt", 'r') as file:
        settings_text = file.read()

        # Check if "include farm = True" is present in the settings text
        include_farm = "include farm = True" in settings_text
        use_true_random = "use true random = True" in settings_text

    # Calculate the random tower count based on conditions
    if use_true_random:
        random_tower_count = random.randint(1, 5)
    else:
        random_tower_count = 5

    if not include_farm:
        random_tower_count = min(random_tower_count, 4)

    while len(selected_towers) < random_tower_count and iteration_count < max_iterations:
        available_towers = [tower for tower in selectable_towers if tower not in used_towers]

        if not available_towers:
            break

        selected_frozenset = random.choice(available_towers)
        tower = dict(selected_frozenset)
        tower_weight = list(tower.values())[0]

        if current_weight + int(tower_weight) <= max_weight:
            selected_towers.append(tower)
            current_weight += tower_weight
            used_towers.add(selected_frozenset)

        iteration_count += 1

    return selected_towers

def edit_tower_entry(entry_number):
    # Get the tower you want to add
    tower_to_add = VARIABLE_WEIGHTED_TOWERS[entry_number]
    tower_name = list(tower_to_add.keys())[0]

    for tower in SELECTABLE_WEIGHTED_TOWERS:
        if list(tower.keys())[0] == tower_name:
            SELECTABLE_WEIGHTED_TOWERS.remove(tower)
            # print(f"'{tower_name}' has been removed.")
            # print(SELECTABLE_WEIGHTED_TOWERS)
            return  # Exit the function if it already exists

    SELECTABLE_WEIGHTED_TOWERS.append(tower_to_add)
    # print(f"'{tower_name}' has been appended.")
    # print(SELECTABLE_WEIGHTED_TOWERS)
