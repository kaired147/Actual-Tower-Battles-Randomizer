from Randomizer import *
from tkinter import *
import atexit

bgcolor = "#f8f8e7"
FONT = "TrajanPro"
max_weight = 100

def default_settings():
    # Read the current contents of settings.txt
    with open("settings.txt", 'r') as file:
        settings_lines = file.readlines()

    # Check if "use true random" and "include farm" lines are present
    has_use_true_random = any(line.strip() == "use true random = False" for line in settings_lines)
    has_include_farm = any(line.strip() == "include farm = False" for line in settings_lines)

    # Write the lines if they are missing
    if not has_use_true_random:
        settings_lines.append("use true random = False\n")
    if not has_include_farm:
        settings_lines.append("include farm = False\n")

    # Write the updated contents back to settings.txt
    with open("settings.txt", 'w') as file:
        file.writelines(settings_lines)


def update_weight():
    global max_weight

    current_setting = current_difficulty_setting.get()

    # Read the current contents of settings.txt
    with open("settings.txt", 'r') as file:
        settings_lines = file.readlines()

    # Find and store the "Include Farm" line if it's present
    include_farm_line = None
    for i, line in enumerate(settings_lines):
        if line.strip().startswith("include farm ="):
            include_farm_line = settings_lines.pop(i)
            break

    # Define the lines you want to write
    lines_to_write = []

    if current_setting == 1:
        max_weight = 999
        lines_to_write.append("use true random = False")
    elif current_setting == 2:
        max_weight = 72
        lines_to_write.append("use true random = False")
    elif current_setting == 3:
        max_weight = 36
        lines_to_write.append("use true random = False")
    elif current_setting == 4:
        max_weight = 999
        lines_to_write.append("use true random = True")

    # Replace existing lines if they are present
    with open("settings.txt", 'w') as file:
        for line in settings_lines:
            if not line.strip().startswith("use true random ="):
                file.write(line)
        for line in lines_to_write:
            file.write(line + '\n')
        if include_farm_line:
            file.write(include_farm_line)


def farm_status():
    print("Farm checkbox clicked")
    if farm_state.get():
        # If the checkbox is checked, include "Farm" and set the setting to True
        SELECTABLE_WEIGHTED_TOWERS.append({"Farm": 25})

        # Read the current contents of settings.txt
        with open("settings.txt", 'r') as file:
            settings_lines = file.readlines()

        # Replace "include farm = False" with "include farm = True" if it's present
        with open("settings.txt", 'w') as file:
            for line in settings_lines:
                if not line.strip().startswith("include farm ="):
                    file.write(line)
            file.write("include farm = True\n")
    else:
        # If the checkbox is unchecked, remove "Farm" and set the setting to False
        for tower in SELECTABLE_WEIGHTED_TOWERS:
            if "Farm" in tower:
                SELECTABLE_WEIGHTED_TOWERS.remove(tower)

        # Read the current contents of settings.txt
        with open("settings.txt", 'r') as file:
            settings_lines = file.readlines()

        # Replace "include farm = True" with "include farm = False" if it's present
        with open("settings.txt", 'w') as file:
            for line in settings_lines:
                if not line.strip().startswith("include farm ="):
                    file.write(line)
            file.write("include farm = False\n")


def clear_settings_file():
    with open("settings.txt", 'w') as file:
        file.truncate(0)

def generate_and_display():
    current_selection = generate_random_towers(max_weight)
    tower_names = [list(tower.keys())[0] for tower in current_selection]
    towers_text = ", ".join(tower_names)
    towers_label.config(text="Your Towers are: " + towers_text)

#----------------------------------UI---------------------------------------#
default_settings()

window = Tk()
window.title("Tower Battles Randomizer")
window.minsize(width=650, height=950)
window.config(padx=25, bg=bgcolor)


canvas_border = Canvas(width=600, height=200, highlightthickness=0)
tb_border_img = PhotoImage(file="TowerBattles.png")
canvas_border.create_image(425, 100, image=tb_border_img)
canvas_border.place(x=0, y=0)

randomizer_title_text = Label(text="Tower Battles Randomizer!", font=(FONT, 30, "bold"), bg=bgcolor)
randomizer_title_text.place(x=50, y=150)


# DIFFICULTY SETTINGS

difficulty_title_text = Label(text="Choose a Difficulty:", font=(FONT, 15, "bold"), bg=bgcolor)
difficulty_title_text.place(x=0, y=250)

current_difficulty_setting = IntVar()
easy_difficulty = Radiobutton(text="Easy", value=1, variable=current_difficulty_setting, command=update_weight)
med_difficulty = Radiobutton(text="Medium", value=2, variable=current_difficulty_setting, command=update_weight)
hard_difficulty = Radiobutton(text="Hard", value=3, variable=current_difficulty_setting, command=update_weight)
random_difficulty = Radiobutton(text="True Random", value=4, variable=current_difficulty_setting, command=update_weight)
farm_state = BooleanVar()
farm_check = Checkbutton(text="Include Farm", variable=farm_state, command=farm_status)

easy_difficulty.place(x=0, y=300)
med_difficulty.place(x=110, y=300)
hard_difficulty.place(x=240, y=300)
random_difficulty.place(x=350, y=300)
farm_check.place(x=500, y=300)


# TROPHY TOWERS

trophy_title = Label(text="Trophy Towers:", font=(FONT, 15, "bold"), bg=bgcolor)
trophy_title.place(x=0, y=350)

golden_scout_state = IntVar()
golden_scout_button = Checkbutton(text="Golden Scout", variable=golden_scout_state, command=lambda: edit_tower_entry(0))
golden_scout_button.place(x=0, y=400)

golden_commando_state = IntVar()
golden_commando_button = Checkbutton(text="Golden Commando", variable=golden_commando_state, command=lambda: edit_tower_entry(1))
golden_commando_button.place(x=0, y=450)


# April Fools Towers

fools_title = Label(text="April Fools:", font=(FONT, 15, "bold"), bg=bgcolor)
fools_title.place(x=220, y=350)

resting_soldier_state = IntVar()
resting_soldier_button = Checkbutton(text="Resting Soldier", variable=resting_soldier_state, command=lambda: edit_tower_entry(14))
resting_soldier_button.place(x=220, y=400)

monkey_state = IntVar()
monkey_button = Checkbutton(text="Monkey", variable=monkey_state, command=lambda: edit_tower_entry(15))
monkey_button.place(x=220, y=450)

poopi_state = IntVar()
poopi_button = Checkbutton(text="poopi", variable=poopi_state, command=lambda: edit_tower_entry(16))
poopi_button.place(x=220, y=500)


# SPECIAL TOWERS

special_title = Label(text="Special Towers:", font=(FONT, 15, "bold"), bg=bgcolor)
special_title.place(x=420, y=350)

red_scout_state = IntVar()
red_scout_button = Checkbutton(text="Red Scout", variable=red_scout_state, command=lambda: edit_tower_entry(11))
red_scout_button.place(x=420, y=400)

red_sniper_state = IntVar()
red_sniper_button = Checkbutton(text="Sniper but red", variable=red_sniper_state, command=lambda: edit_tower_entry(12))
red_sniper_button.place(x=420, y=450)

huntsman_state = IntVar()
huntsman_button = Checkbutton(text="Huntsman", variable=huntsman_state, command=lambda: edit_tower_entry(13))
huntsman_button.place(x=420, y=500)


# EVENT TOWERS

event_title = Label(text="Event Towers:", font=(FONT, 15, "bold"), bg=bgcolor)
event_title.place(x=0, y=550)

scarecrow_state = IntVar()
scarecrow_button = Checkbutton(text="Scarecrow", variable=scarecrow_state, command=lambda: edit_tower_entry(2))
scarecrow_button.place(x=0, y=600)

elf_state = IntVar()
elf_button = Checkbutton(text="Elf", variable=elf_state, command=lambda: edit_tower_entry(3))
elf_button.place(x=0, y=650)

hallowboomer_state = IntVar()
hallowboomer_button = Checkbutton(text="Hallowboomer", variable=hallowboomer_state, command=lambda: edit_tower_entry(4))
hallowboomer_button.place(x=0, y=700)

sleeter_state = IntVar()
sleeter_button = Checkbutton(text="Sleeter", variable=sleeter_state, command=lambda: edit_tower_entry(5))
sleeter_button.place(x=150, y=600)

graveyard_state = IntVar()
graveyard_button = Checkbutton(text="Graveyard", variable=graveyard_state, command=lambda: edit_tower_entry(6))
graveyard_button.place(x=150, y=650)

harpoon_hunter_state = IntVar()
harpoon_hunter_button = Checkbutton(text="Harpoon Hunter",variable=harpoon_hunter_state, command=lambda: edit_tower_entry(7))
harpoon_hunter_button.place(x=150, y=700)

tweeter_state = IntVar()
tweeter_button = Checkbutton(text="Tweeter", variable=tweeter_state, command=lambda: edit_tower_entry(8))
tweeter_button.place(x=300, y=600)

snowballer_state = IntVar()
snowballer_button = Checkbutton(text="Snowballer", variable=snowballer_state, command=lambda: edit_tower_entry(9))
snowballer_button.place(x=300, y=650)

patrioteer_state = IntVar()
patrioteer_button = Checkbutton(text="Patrioteer", variable=patrioteer_state, command=lambda: edit_tower_entry(10))
patrioteer_button.place(x=300, y=700)

# Randomize Button and label

randomize_button = Button(text="Randomize!", font=(FONT, 15, "bold"), command=generate_and_display)
randomize_button.place(x=225, y=775)

towers_label = Label(text="", font=(FONT, 13, "bold"), bg=bgcolor)
towers_label.place(x=0, y=850)

#----------------------------------TEST---------------------------------------#
# random_towers = generate_random_towers(max_weight)
# for tower in random_towers:
#     print(list(tower.keys())[0])

atexit.register(clear_settings_file)
window.mainloop()
