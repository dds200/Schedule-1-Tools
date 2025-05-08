import os
import json
import zipfile
import subprocess
import time
from rich.console import Console
console = Console()

people = [
    {"name": "You", "steam_id": 76561199372403302},
    {"name": "Tibi", "steam_id": 76561199102831024},
    {"name": "Bazavan", "steam_id": 76561199067577784}
]

def find_my_save_folder():
    local_low = os.path.join(os.getenv('LOCALAPPDATA').replace('Local', 'LocalLow'))
    saves_path = os.path.join(local_low, "TVGS", "Schedule I", "Saves")

    if not os.path.exists(saves_path):
        return None

    for folder in os.listdir(saves_path):
        if folder != "TempPlayer" and folder.isdigit():
            return os.path.join(saves_path, folder)

    return None


def pipe(thickness = 1):
    thickness = str(thickness)
    if thickness == "thick":
        print('━' * 20)
    else:
        print('─' * 20)

def zip_save_file(zip_path, zip_filename):
    zip_path = os.path.abspath(zip_path)
    all_files = []

    if os.path.isfile(zip_path):
        all_files = [zip_path]
    else:
        for foldername, subfolders, filenames in os.walk(zip_path):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                all_files.append(filepath)

    total_files = len(all_files)
    if total_files == 0:
        print("No files to compress.")
        return

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for idx, filepath in enumerate(all_files, 1):
            arcname = os.path.relpath(filepath, zip_path)
            zipf.write(filepath, arcname=arcname)

            # Dynamic progress output
            percent = (idx / total_files) * 100
            progress = f"Compressing: {percent:.2f}% ({idx}/{total_files})"
            print(f"\r{progress}", end='', flush=True)

    print(f"\n[+] Created ZIP file: {zip_filename}")


def appearing_text(text, delay=0.05):
    if delay == "slow":
        delay = 0.5
    elif delay == "medium":
        delay = 0.25
    elif delay == "fast":
        delay = 0.01
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_name_from_steam_id(steam_id):
    steam_id = str(steam_id)
    for person in people:
        if str(person["steam_id"]) == str(steam_id):
            return person["name"]
    return None

def get_steam_id_from_name(name):
    for person in people:
        if person["name"] == name:
            return str(person["steam_id"])
    return None


def exit_program(meessage):
    print(meessage)
    input("Press Enter to exit...")
    exit()

print(find_my_save_folder())

path = find_my_save_folder()
if not path:
    exit_program("Error: Save folder not found. Please check your installation of Schedule 1.")

folders =[]

console.print("Schedule 1 Save Tools", style = "bold")
pipe(thickness="thick")
mode = input("Select a mode (1: Host Changer, 2: Save Zipper): ")
if mode not in ["1", "2"]:
    exit_program("Invalid mode selected. Please choose 1 or 2.")
pipe()


if mode == "1":
    subprocess.run("cls", shell=True)
    appearing_text("Schedule 1 Host Changer")
    appearing_text('━' * 20, delay=0.01)
    only_folder = [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]
    for folder in only_folder:
        folders.append(folder)
    
    if (len(folders) == 0):
        exit_program("No saves found in the specified path.")
    #This looks for all the folders in the path specified and adds them to the folders list

    appearing_text("Which save do you want to change?", delay=0.025)
    time.sleep(0.3)
    print("")
    for folder_selection in range(len(folders)):
        save_folder_path = os.path.join(path, folders[folder_selection])
        organisation_name = "Unknown"
        # This tries to read the "game.json" file inside the folder to get the save name
        save_folder_path_game_json = os.path.join(save_folder_path, "Game.json")
        try :
            with open(save_folder_path_game_json, "r") as f:
                data = json.load(f)
                organisation_name = data.get("OrganisationName", "Unknown")
        except (FileNotFoundError, json.JSONDecodeError):
            organisation_name = "Unknown save"
        except Exception as e:
            print(f"Error reading {save_folder_path_game_json}: {e}")
            organisation_name = "Unknown save"
    
        line = (str(folder_selection+1) + ". ", folders[folder_selection].replace("_", " "), " - ", organisation_name)
        #this store the folder name and the save game name to later be printed out nicely
        appearing_text(line, delay=0.05)
        time.sleep(0.1)
    #This lists all the save folders in the path and the name of the save inside the folder


    appearing_text('━' * 20, delay=0.01)
    selected_save = input("Select a save: ")

    try:
        selected_save = int(selected_save)
        if selected_save < 1 or selected_save > len(folders):
            exit_program("Invalid save selection.")
        else:
            print("You selected save:", folders[selected_save - 1].replace("_", " "))
    except ValueError:
        exit_program("Invalid input. Please enter a number.")

    # This is the part where the user selects the save they want to the the host from.


    print("-------------------")


    print("Players:")
    selected_save = os.path.join(path, folders[selected_save - 1], "Players")
    #This is the path to the selected save folder, where the players are located
    ids_in_save_file = [
        fname.replace("Player_", "")
        for fname in os.listdir(selected_save)
    ]
    #This cleans the ids in the save file, removing the "Player_" part of the name 
    host_in_save_file = [str(person["steam_id"]) for person in people]
    players_in_save_file = []


    for player_steam_id in ids_in_save_file:
        for person in people:
            did_i_find_this_steam_id = False
            if str(person["steam_id"]) == player_steam_id:
                players_in_save_file.append(person["name"])
                host_in_save_file.remove(str(person["steam_id"]))
                print("-", person["name"])
                did_i_find_this_steam_id = True
                break
        if not did_i_find_this_steam_id and player_steam_id != "0":
            print("- Unknown player with Steam ID:", player_steam_id)

    if len(players_in_save_file) == 0:
        exit_program("Can't change host, no players found in save file.")

    for person in people:
        if str(person["steam_id"]) in ids_in_save_file:
            continue
        print("-", person["name"], "(Host)")

    print("-------------------")
    print("Who do you want the new host to be?")

    for player in range(len(players_in_save_file)):
        print(str(player + 1) + ".", players_in_save_file[player])
    print("-------------------")

    player_selected = input("Select a player: ")

    try:
        player_selected = int(player_selected)
        if player_selected > len(players_in_save_file) or player_selected < 1:
            exit_program("Invalid selection.")
    except ValueError:
        exit_program("Invalid input. Please enter a number.")

    # Convert player names back to steam IDs (fix: store IDs not names)
    # So instead of storing names, we rebuild the list as steam IDs
    players_in_save_file = []
    for steam_id in ids_in_save_file:
        for person in people:
            if str(person["steam_id"]) == steam_id:
                players_in_save_file.append(str(person["steam_id"]))
                break

    # Confirm who was selected
    new_host_steam_id = players_in_save_file[player_selected - 1]
    print("You selected:", get_name_from_steam_id(new_host_steam_id))

    # Find current host
    old_host_steam_id = None
    for person in people:
        if str(person["steam_id"]) not in ids_in_save_file:
            old_host_steam_id = str(person["steam_id"])
            break

    if not old_host_steam_id:
        exit_program("Error: Could not determine current host.")

    # Paths
    old_host_folder = os.path.join(selected_save, "Player_0")
    renamed_old_host_folder = os.path.join(selected_save, f"Player_{old_host_steam_id}")
    new_host_folder = os.path.join(selected_save, f"Player_{new_host_steam_id}")
    renamed_new_host_folder = os.path.join(selected_save, "Player_0")

    try:
        os.rename(old_host_folder, renamed_old_host_folder)
        print("Switched", get_name_from_steam_id(old_host_steam_id), "to a player (Host -> Player)")
        os.rename(new_host_folder, renamed_new_host_folder)
        print("Made", get_name_from_steam_id(new_host_steam_id), "the new host (Player -> Host)")
    except FileExistsError:
        exit_program("Error: Target folder already exists. Clean up before proceeding.")
    except FileNotFoundError:
        exit_program("Error: One of the folders wasn't found.")
    except Exception as e:
        exit_program(f"An unexpected error occurred: {e}")

elif mode == "2":
    print("Schedule 1 save zipper")
    pipe()


print("-------------------")
print("Done")
input("Press Enter to exit...")
  