import os
import json
import zipfile
import subprocess
import time
import sys
import shutil
from datetime import datetime
from tkinter import Tk, filedialog

from art import text2art
import subprocess

def header(text, font = "slant"):
    subprocess.run("cls", shell=True)
    print(text2art(text, font=font))  # try "block", "random", or "speed"
    print("━" * 60)




subprocess.run("cls", shell=True)
subprocess.run("mode con: cols=120 lines=40", shell=True)

settings_file = "settings.json"




def save_settings():
    with open(settings_file, "w", encoding = "utf-8") as f:
        players_json = ",\n        ".join(
            [json.dumps(player, separators=(", ", ": ")) for player in settings["players"]]
        )
        default_players_json = ",\n        ".join(
            [json.dumps(player, separators=(", ", ": ")) for player in settings["default_players"]]
        )
        f.write("{\n")
        f.write('    "players": [\n')
        f.write(f"        {players_json}\n")
        f.write("    ],\n")
        f.write('    "default_players": [\n')
        f.write(f"        {default_players_json}\n")
        f.write("    ],\n")
        f.write(f'    "zip_destination": {json.dumps(settings["zip_destination"])},\n')
        f.write(f'    "unzip_default_path": {json.dumps(settings["unzip_default_path"])},\n')
        f.write(f'    "auto_host_switch": {json.dumps(settings["auto_host_switch"])}\n')
        f.write("}\n")


if os.path.exists(settings_file):
    with open(settings_file, "r", encoding="utf-8") as f:
        settings = json.load(f)
else:
    settings = {
        "players": [
            {"name": "Maniac", "steam_id": 76561199372403302, "hidden": False},
            {"name": "Tibi", "steam_id": 76561199102831024, "hidden": False},
            {"name": "Baz", "steam_id": 76561199067577784, "hidden": False},
            {"name": "Nigga", "steam_id": 76561199447152889, "hidden": False},
            {"name": "G", "steam_id": 76561199404747355, "hidden": False},
            {"name": "Mathew", "steam_id": 76561198369717437, "hidden": False},
            {"name": "Ticu", "steam_id": 76561199367611432, "hidden": False}
        ],
        "default_players": [
            {"name": "Maniac", "steam_id": 76561199372403302, "hidden": False},
            {"name": "Tibi", "steam_id": 76561199102831024, "hidden": False},
            {"name": "Baz", "steam_id": 76561199067577784, "hidden": False},
            {"name": "Nigga", "steam_id": 76561199447152889, "hidden": False},
            {"name": "G", "steam_id": 76561199404747355, "hidden": False},
            {"name": "Mathew", "steam_id": 76561198369717437, "hidden": False},
            {"name": "Ticu", "steam_id": 76561199367611432, "hidden": False}
        ],

        "zip_destination": None,
        "unzip_default_path" : None,
        "auto_host_switch": True

    }
    save_settings()

def reload_settings():
    global settings
    with open(settings_file, "r", encoding="utf-8") as f:
        settings = json.load(f)


def restart_script():
    print("Restarting to apply changes...")
    time.sleep(1)
    python = sys.executable
    script = os.path.abspath(__file__)
    subprocess.Popen([python, script], shell=False)
    sys.exit()


def find_my_save_folder():
    local = os.getenv('LOCALAPPDATA')
    if not local:
        pause_and_return("Could not find LOCALAPPDATA environment variable. This script must be run on Windows with a valid user profile.")

    local_low = os.path.join(local.replace('Local', 'LocalLow'))
    saves_path = os.path.join(local_low, "TVGS", "Schedule I", "Saves")
    if not os.path.exists(saves_path):
        return None

    for folder in os.listdir(saves_path):
        if folder != "TempPlayer" and folder.isdigit():
            return os.path.join(saves_path, folder)
    return None


def find_my_steam_id():
    save_folder = find_my_save_folder()
    if save_folder:
        return os.path.basename(save_folder)
    return None


path = find_my_save_folder()
who_dis_steam_id = find_my_steam_id()

#print("[DEBUG] Detected Steam ID:", who_dis_steam_id)


local_low = os.path.join(os.getenv('LOCALAPPDATA').replace('Local', 'LocalLow'))
saves_path = os.path.join(local_low, "TVGS", "Schedule I", "Saves")
for folder in os.listdir(saves_path):
    if folder != "TempPlayer" and folder.isdigit():
        who_dis_steam_id = folder

#print("Steam ID:", who_dis_steam_id)


people = []
found_myself = False

for person in settings["players"]:
    if person.get("hidden") is True:
        continue  # skip hidden players

    steam_id_str = str(person["steam_id"])
    if steam_id_str == who_dis_steam_id:
        people.append({"name": "You", "steam_id": steam_id_str})
        found_myself = True
    else:
        people.append({"name": person["name"], "steam_id": steam_id_str})

# Add unknown user if not already listed
if not found_myself and who_dis_steam_id:
    people.append({"name": "You", "steam_id": who_dis_steam_id})

"""
print("Final visible people:")
for p in people:
    print("-", p)
"""




from datetime import datetime

def zip_save_file(zip_path, zip_filename):
    zip_path = os.path.abspath(zip_path)
    base_name, ext = os.path.splitext(zip_filename)

    if os.path.exists(zip_filename):
        print(f"[!] ZIP file '{zip_filename}' already exists.")
        print("Options:")
        print("1. Overwrite")
        print("2. Automatically rename (SaveGame_1.zip → SaveGame_1 (1).zip)")
        print("3. Cancel")
        choice = input("Your choice [1/2/3]: ").strip()

        if choice == "1":
            os.remove(zip_filename)
        elif choice == "2":
            counter = 1
            original = zip_filename
            while os.path.exists(zip_filename):
                zip_filename = f"{base_name} ({counter}){ext}"
                counter += 1
            print(f"New filename: {zip_filename}")
        else:
            print("Canceled.")
            return


    all_files = []
    for foldername, subfolders, filenames in os.walk(zip_path):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            all_files.append(filepath)

    total_files = len(all_files)
    if total_files == 0:
        print("No files to compress.")
        return

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        now = datetime.now().timetuple()[:6]

        for idx, filepath in enumerate(all_files, 1):
            arcname = os.path.relpath(filepath, zip_path)

            with open(filepath, "rb") as f:
                data = f.read()

            info = zipfile.ZipInfo(arcname)
            info.date_time = now
            info.compress_type = zipfile.ZIP_DEFLATED

            zipf.writestr(info, data)

            percent = (idx / total_files) * 100
            progress = f"Compressing: {percent:.2f}% ({idx}/{total_files})"
            print(f"\r{progress}", end='', flush=True)

    print(f"\n[+] Created ZIP file: {zip_filename}")





def faster_zip_save_file(source_folder, output_zip_path):
    base = os.path.splitext(output_zip_path)[0]  # Remove .zip extension if present
    try:
        shutil.make_archive(base, 'zip', root_dir=source_folder)
        print(f"[+] Created ZIP file: {output_zip_path}")
    except Exception as e:
        print(f"[!] Error creating ZIP: {e}")


def appearing_text(text, delay=0.01):
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

def pipe(thickness = 1):
    appearing_text('━━━━━━' * 10, delay=0.01)

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


def pause_and_return(message):
    print(message)
    input("Press Enter to return to the main menu...")

def list_save_folders(base_path):
    return [
        name for name in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, name))
    ]


if not path:
    pause_and_return("Error: Save folder not found. Please check your installation of Schedule 1.")

folders =[]

print('━' * 60)
header("Schedule 1 Tools")


sys.stdout.flush()
#Are draci programu si tre sa pun asta ca altfel o ia razna dupa settings



while True:
    subprocess.run("cls", shell=True)
    header("Schedule 1 Tools")
    print("Select a mode:")
    print("1. Host Changer")
    print("2. Save Exporter")
    print("3. Save Importer")
    print("4. Save Swapper")
    print("5. Save Renamer")
    print("6. Save Deleter")
    print("0. Settings")
    print("Press Enter to exit")
    print('━' * 60)
    mode = input("Mode: ").strip()

    if mode == "":
        print("Exiting program...")
        break

    if mode not in ["1", "2", "3", "4", "5", "6", "0"]:
        input("Invalid mode selected. Press Enter to continue...")
        continue

    # Here you'd call the appropriate mode logic
    if mode == "1":
        try:
            subprocess.run("cls", shell=True)
            header("Host Changer")
            folders = []
            folders = list_save_folders(path)
            if (len(folders) == 0):
                pause_and_return("No saves found")
            #This looks for all the folders in the path specified and adds them to the folders list
            time.sleep(0.3)
            appearing_text("Which save do you want to change?", delay=0.01)
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
            
                print(str(folder_selection+1) + ".", folders[folder_selection].replace("_", " "), "-", organisation_name)
                time.sleep(0.1)
            #This lists all the save folders in the path and the name of the save inside the folder


            print("-------------------")
            selected_save = input("Select a save: ")

            try:
                selected_save = int(selected_save)
                if selected_save < 1 or selected_save > len(folders):
                    pause_and_return("Invalid save selection.")
                else:
                    #print("You selected save:", folders[selected_save - 1].replace("_", " "))
                    pass
            except ValueError:
                pause_and_return("Invalid input. Please enter a number.")

            # This is the part where the user selects the save they want to the the host from.

            appearing_text('━━━━━━' * 10, delay=0.01)

            appearing_text("Players:", delay=0.01)
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
                pause_and_return("Can't change host, no players found in save file.")

            for person in people:
                if str(person["steam_id"]) in ids_in_save_file:
                    continue
                if len(host_in_save_file) > 1:
                    appearing_text(f"- {person['name']} (Potential Host)", delay=0.01)
                else:
                    appearing_text(f"- {person['name']} (Host)", delay=0.01)


            appearing_text('━━━━━━' * 10, delay=0.01)
            appearing_text("Who do you want the new host to be?", delay=0.01)

            for player in range(len(players_in_save_file)):
                player_index = (str(player + 1) + ".", players_in_save_file[player])
                appearing_text(player_index, delay=0.01)
                time.sleep(0.15)
            print("--------------------")

            player_selected = input("Select a player: ")

            try:
                player_selected = int(player_selected)
                if player_selected > len(players_in_save_file) or player_selected < 1:
                    pause_and_return("Invalid selection.")
            except ValueError:
                pause_and_return("Invalid input. Please enter a number.")

            players_in_save_file = []
            for steam_id in ids_in_save_file:
                for person in people:
                    if str(person["steam_id"]) == steam_id:
                        players_in_save_file.append(str(person["steam_id"]))
                        break

            # Confirm who was selected
            new_host_steam_id = players_in_save_file[player_selected - 1]
            #print("You selected:", get_name_from_steam_id(new_host_steam_id))

            # Find current host
            old_host_steam_id = None
            for person in people:
                if str(person["steam_id"]) not in ids_in_save_file:
                    old_host_steam_id = str(person["steam_id"])
                    break

            potential_hosts = [
                str(person["steam_id"])
                for person in people
                if str(person["steam_id"]) not in ids_in_save_file
            ]

            if len(potential_hosts) == 0:
                pause_and_return("Error: Could not determine current host.")

            elif len(potential_hosts) == 1:
                old_host_steam_id = potential_hosts[0]

            else:
                appearing_text('━━━━━━' * 10, delay=0.01)
                appearing_text("Multiple potential hosts found:", delay=0.01)
                for index, sid in enumerate(potential_hosts):
                    name = get_name_from_steam_id(sid)
                    name = name if name else "Unknown"
                    multiple_host_index = (f"{index + 1}. {name}")
                    appearing_text(multiple_host_index, delay=0.01)
                    time.sleep(0.1)
                print("-------------------")
                try:
                    selected = int(input("Select the host you want to switch to a player: "))
                    if selected < 1 or selected > len(potential_hosts):
                        pause_and_return("Invalid selection.")
                    old_host_steam_id = potential_hosts[selected - 1]
                except ValueError:
                    pause_and_return("Invalid input. Please enter a number.")

            

            # Paths
            old_host_folder = os.path.join(selected_save, "Player_0")
            renamed_old_host_folder = os.path.join(selected_save, f"Player_{old_host_steam_id}")
            new_host_folder = os.path.join(selected_save, f"Player_{new_host_steam_id}")
            renamed_new_host_folder = os.path.join(selected_save, "Player_0")

            try:
                os.rename(old_host_folder, renamed_old_host_folder)
                appearing_text('━━━━━━' * 10, delay=0.01)
                message = f"Switched {get_name_from_steam_id(old_host_steam_id)} to a player (Host -> Player)"
                appearing_text(message, delay=0.01)
                os.rename(new_host_folder, renamed_new_host_folder)
                message = f"Made {get_name_from_steam_id(new_host_steam_id)} the new host (Player -> Host)"
                appearing_text(message, delay=0.01)
                pause_and_return("Host switch complete.")
            except FileExistsError:
                pause_and_return("Error: Target folder already exists. Clean up before proceeding.")
            except FileNotFoundError:
                pause_and_return("Error: One of the folders wasn't found.")
            except Exception as e:
                pause_and_return(f"An unexpected error occurred: {e}")
        except Exception as e:
            pause_and_return(f"[!] Error in Host Changer: {e}")
            pass
    elif mode == "2":
        try:
            subprocess.run("cls", shell=True)
            header("Save Exporter")
            if not settings.get("zip_destination"):
                print("Select folder where zipped saves will be stored...")
                root = Tk()
                root.withdraw()
                zip_path = filedialog.askdirectory(title="Choose ZIP Destination Folder")
                if not zip_path:
                    pause_and_return("No folder selected. Returning to menu.")
                    continue
                settings["zip_destination"] = zip_path
                save_settings()
                print(f"Save files will be zipped to {zip_path}")
            
            appearing_text("Select a save to zip:", delay=0.01)
            time.sleep(0.3)
            folders = []
            folders = list_save_folders(path)
            
            if (len(folders) == 0):
                pause_and_return("No saves found")
                continue

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
            
                print(str(folder_selection+1) + ".", folders[folder_selection].replace("_", " "), "-", organisation_name)
                time.sleep(0.1)
            #This lists all the save folders in the path and the name of the save inside the folder


            print("-------------------")
            selected_save = input("Select a save: ")

            try:
                selected_save = int(selected_save)
                if selected_save < 1 or selected_save > len(folders):
                    pause_and_return("Invalid save selection.")
                else:
                    pass
            except ValueError:
                pause_and_return("Invalid input. Please enter a number.")
            
            appearing_text('━━━━━━' * 10, delay=0.01)
            zip_path = os.path.abspath(settings["zip_destination"])
            source_folder = os.path.join(path, folders[selected_save - 1])
            output_zip_path = os.path.join(zip_path, f"{folders[selected_save - 1]}.zip")
            # Create sender_info.txt to store who exported the save
            sender_steam_id = who_dis_steam_id  # this is already detected earlier
            sender_info_path = os.path.join(source_folder, "sender_info.txt")
            with open(sender_info_path, "w", encoding="utf-8") as f:
                f.write(sender_steam_id)
            start = time.time()
            zip_save_file(source_folder, output_zip_path)
            end = time.time()
            pause_and_return(f"Zipped to: {zip_path} in {round(end - start, 2)} seconds")
            # Clean up the file after zipping
            if os.path.exists(sender_info_path):
                os.remove(sender_info_path)
            pass
        except Exception as e:
            pause_and_return(f"[!] Error in Save Exporter: {e}")
    
    elif mode == "3":
        try: 
            header("Save Importer")

            # Ask for default unzip path if not already set
            if not settings.get("unzip_default_path"):
                print("Select default unzip location (where ZIP save files are):")
                print("")
                root = Tk()
                root.withdraw()
                unzip_path = filedialog.askdirectory(title="Choose default unzip folder")
                if not unzip_path:
                    pause_and_return("No folder selected. Returning to menu.")
                    continue
                settings["unzip_default_path"] = unzip_path
                save_settings()
                print(f"Unzipped files will be loaded from {unzip_path}")
            else:
                unzip_path = settings["unzip_default_path"]

            # Ask user to select the ZIP file
            root = Tk()
            root.withdraw()
            unzip_file = filedialog.askopenfilename(
                initialdir=unzip_path,
                title="Select ZIP Save File",
                filetypes=[("ZIP files", "*.zip")]
            )
            if not unzip_file:
                pause_and_return("No file selected. Exiting.")

            # Ask user for which slot
            appearing_text("What save slot should this be? (e.g., 1, 2, 3):")
            print("--------------------")
            try:
                slot = int(input("Save slot #: ").strip())
                if slot < 1:
                    pause_and_return("Invalid slot number.")
            except ValueError:
                pause_and_return("Invalid input.")

            pipe()

            target_folder_name = f"SaveGame_{slot}"
            target_path = os.path.join(path, target_folder_name)

            # Handle existing folder
            if os.path.exists(target_path):
                print(f"SaveGame {slot} already exists.")
                print("----------------------")
                print("1. Overwrite")
                print("2. Choose next available slot")
                print("3. Cancel")
                print("----------------------")
                choice = input("Choose an option: ").strip()
                pipe()

                if choice == "1":
                    shutil.rmtree(target_path)
                elif choice == "2":
                    while os.path.exists(os.path.join(path, f"SaveGame_{slot}")):
                        slot += 1
                    print(f"Using next available slot: SaveGame_{slot}")
                    target_path = os.path.join(path, f"SaveGame_{slot}")
                else:
                    pause_and_return("Operation cancelled.")

            # Extract the zip
            try:
                with zipfile.ZipFile(unzip_file, 'r') as zip_ref:
                    zip_ref.extractall(target_path)
                print(f"Successfully imported Save Game {slot}")
            except Exception as e:
                pause_and_return(f"Error extracting ZIP: {e}")

            # Host switch logic
            sender_info_path = os.path.join(target_path, "sender_info.txt")
            if os.path.exists(sender_info_path):
                try:
                    with open(sender_info_path, "r", encoding="utf-8") as f:
                        sender_steam_id = f.read().strip()

                    if not sender_steam_id.isdigit():
                        print("Invalid sender Steam ID format in sender_info.txt.")
                    else:
                        local_folder = os.path.join(target_path, f"Player_{who_dis_steam_id}")
                        sender_folder = os.path.join(target_path, f"Player_{sender_steam_id}")
                        host_folder = os.path.join(target_path, "Player_0")

                        if not os.path.exists(local_folder):
                            print("You're already the host. Host switch not needed.")
                        elif not os.path.exists(sender_folder):
                            print("Sender player folder not found. Host switch not performed.")
                        else:
                            if not settings.get("auto_host_switch", False):
                                pipe()
                                appearing_text("This save was sent by another player.", delay=0.01)
                                appearing_text("Do you want to make yourself the host and demote them to a player?", delay=0.01)
                                pipe()
                                choice = input("Type 'yes' to switch host: ").strip().lower()
                                if choice != "yes":
                                    print("Host switch skipped.")
                                else:
                                    switch_host = True
                            else:
                                print("[Auto Mode] Automatically switching host based on settings...")
                                time.sleep(0.5)
                                switch_host = True

                            if switch_host:
                                temp_folder = os.path.join(target_path, "__temp_host_swap__")
                                if os.path.exists(host_folder):
                                    os.rename(host_folder, temp_folder)
                                else:
                                    os.mkdir(temp_folder)

                                os.rename(local_folder, host_folder)
                                os.rename(sender_folder, f"Player_{sender_steam_id}")
                                if os.path.exists(temp_folder):
                                    shutil.rmtree(temp_folder)
                                print("Host successfully switched. You are now the host.")

                except Exception as e:
                    print(f"Error processing host switch: {e}")
            else:
                print("No sender info found. Host switch skipped.")

            # Final clean pause
            pause_and_return("Import complete. Press Enter to return to the main menu...")

        except Exception as e:
            pause_and_return(f"[!] Error in Save Importer: {e}")







    elif mode == "4":
        try:

            header("Save Swapper")

            save_folders = [
                f for f in os.listdir(path)
                if f.startswith("SaveGame_") and os.path.isdir(os.path.join(path, f))
            ]

            if len(save_folders) < 2:
                pause_and_return("Not enough saves to swap.")

            appearing_text("Available Saves:", delay=0.01)

            save_info = []
            for folder in sorted(save_folders):
                save_path = os.path.join(path, folder)
                org_name = "Unknown"
                game_json = os.path.join(save_path, "Game.json")
                try:
                    with open(game_json, "r") as f:
                        data = json.load(f)
                        org_name = data.get("OrganisationName", "Unknown")
                except (FileNotFoundError, json.JSONDecodeError):
                    org_name = "Unknown"
                save_info.append((folder, org_name))

            for idx, (folder, org_name) in enumerate(save_info, 1):
                print(f"{idx}. {folder} - {org_name}")
                time.sleep(0.05)

            print("--------------------")
            try:
                a = int(input("Select the first save to swap: "))
                b = int(input("Select the second save to swap to: "))

                if a == b:
                    pause_and_return("Selected the same save twice. No action taken.")
                if a < 1 or b < 1 or a > len(save_info) or b > len(save_info):
                    pause_and_return("Invalid selection.")

                save_a = save_info[a - 1][0]
                save_b = save_info[b - 1][0]

                full_a = os.path.join(path, save_a)
                full_b = os.path.join(path, save_b)
                temp_name = os.path.join(path, "__temp_swap_folder__")

                # Swap folders
                os.rename(full_a, temp_name)
                os.rename(full_b, full_a)
                os.rename(temp_name, full_b)

                pipe()
                pause_and_return(f"Swapped {save_a} <--> {save_b}")
            except ValueError:
                pause_and_return("Invalid input. Please enter valid numbers.")
            except Exception as e:
                pause_and_return(f"An error occurred: {e}")
                pass
        except Exception as e:
            pause_and_return(f"[!] Error in Save Exporter: {e}")

    elif mode == "5":
        try:
            header("Save Renamer")
            appearing_text("Select a save game to rename (will edit only it's display name):", delay=0.01)
            time.sleep(0.3)
            folders = list_save_folders(path)
            
            if len(folders) == 0:
                pause_and_return("No saves found")
                continue

            for i, folder in enumerate(folders):
                save_path = os.path.join(path, folder)
                org_name = "Unknown"
                game_json = os.path.join(save_path, "Game.json")
                try:
                    with open(game_json, "r") as f:
                        data = json.load(f)
                        org_name = data.get("OrganisationName", "Unknown")
                except:
                    org_name = "Unknown save"
                print(f"{i+1}. {folder.replace('_', ' ')} - {org_name}")
                time.sleep(0.1)

            print("-------------------")
            selected_save = input("Select a save: ")

            try:
                selected_save = int(selected_save)
                if selected_save < 1 or selected_save > len(folders):
                    pause_and_return("Invalid save selection.")
            except ValueError:
                pause_and_return("Invalid input. Please enter a number.")

            selected_folder = folders[selected_save - 1]
            game_json_path = os.path.join(path, selected_folder, "Game.json")

            if not os.path.exists(game_json_path):
                pause_and_return("Error: Game.json not found in the selected save.")

            # Load the existing JSON
            with open(game_json_path, "r", encoding="utf-8") as f:
                try:
                    game_data = json.load(f)
                except json.JSONDecodeError:
                    pause_and_return("Error: Could not parse Game.json.")

            current_name = game_data.get("OrganisationName", "Unknown")
            print(f"Current name: {current_name}")
            new_name = input("Enter new name: ").strip()
            if not new_name:
                pause_and_return("No name entered. Operation cancelled.")

            game_data["OrganisationName"] = new_name

            # Write it back
            with open(game_json_path, "w", encoding="utf-8") as f:
                json.dump(game_data, f, indent=4)

            pause_and_return(f"Updated the game in {selected_folder} to '{new_name}'")

        except Exception as e:
            pause_and_return(f"[!] Error in Save Renamer: {e}")

    elif mode == "6":
        try:
            header("Save Deleter")
            appearing_text("Select a save game to delete:", delay=0.01)
            time.sleep(0.3)

            folders = list_save_folders(path)  # ✅ FIXED: Initialize folders

            if len(folders) == 0:
                pause_and_return("No saves found")
                continue

            for i, folder in enumerate(folders):
                save_path = os.path.join(path, folder)
                org_name = "Unknown"
                game_json = os.path.join(save_path, "Game.json")
                try:
                    with open(game_json, "r") as f:
                        data = json.load(f)
                        org_name = data.get("OrganisationName", "Unknown")
                except:
                    org_name = "Unknown save"
                print(f"{i+1}. {folder.replace('_', ' ')} - {org_name}")
                time.sleep(0.1)

            print("-------------------")
            selected_save = input("Select a save: ")

            try:
                selected_save = int(selected_save)
                if selected_save < 1 or selected_save > len(folders):
                    pause_and_return("Invalid save selection.")
            except ValueError:
                pause_and_return("Invalid input. Please enter a number.")

            selected_folder = folders[selected_save - 1]
            full_path = os.path.join(path, selected_folder)

            # Confirm deletion
            appearing_text('━━━━━━' * 10, delay=0.01)
            appearing_text(f"Are you sure you want to delete '{selected_folder}'?", delay=0.01)
            appearing_text("This action cannot be undone.", delay=0.01)
            appearing_text('━━━━━━' * 10, delay=0.01)

            confirm = input("Type 'yes' to confirm: ").strip().lower()
            if confirm != "yes":
                pause_and_return("Deletion cancelled.")

            shutil.rmtree(full_path)
            pause_and_return(f"Deleted '{selected_folder}' successfully.")
        except Exception as e:
            pause_and_return(f"[!] Error in Save Deleter: {e}")


    elif mode == "0":
        try:
            while True:
                subprocess.run("cls", shell=True)
                header("Settings")
                print("What settings do you want to change?")
                print("")
                print("1. Change the name of a person")
                
                print("2. Add a new person")
                
                print("3. Change the zip destination")
                
                print("4. Change the unzip default destination")
                
                print("5. Toggle people visibility")
                
                print("6. Remove a person")
                
                print("7. Reset player names")
                
                print("8. Toggle Auto Host Switch")
                
                print("Press Enter to go back")
                print("----------------")
                selected_setting = input("Select a setting: ")
                appearing_text('━━━━━━' * 10, delay=0.01)

                if selected_setting == "1":
                    header("Name Changer")
                    print("Select a person to change their name:")
                    print("")
                    for player in range(len(settings["players"])):
                        player_index = (str(player + 1) + ".", (settings["players"])[player]["name"])
                        appearing_text(player_index, delay=0.01)
                        time.sleep(0.1)
                    print("--------------------")
                    selected_person = input("Select a person: ")
                    try:
                        selected_person = int(selected_person)
                        if selected_person > len(settings["players"]) or selected_person < 1:
                            pause_and_return("Invalid selection.")
                        else:
                            new_name = input("Enter the new name: ")
                            settings["players"][selected_person - 1]["name"] = new_name
                            save_settings()

                            
                    except ValueError:
                        pause_and_return("Invalid input. Please enter a number.")


                elif selected_setting == "2":
                    header("Add New Person")
                    new_name = input("Enter the name of the new person: ")
                    print("")
                    new_steam_id = input("Enter the Steam ID of the new person: ")
                    settings["players"].append({"name": new_name, "steam_id": new_steam_id, "hidden": False})
                    settings["default_players"].append({"name": new_name, "steam_id": new_steam_id})
                    save_settings()
                    print(f"Added {new_name} with Steam ID {new_steam_id}")

                
                elif selected_setting == "3":
                    header("Change ZIP Destination")
                    print("Select folder where zipped saves will be stored...")
                    print("")
                    root = Tk()
                    root.withdraw()
                    zip_path = filedialog.askdirectory(title="Choose ZIP Destination Folder")
                    if not zip_path:
                        print("No folder selected. Returning to menu.")
                        pause_and_return("No folder selected. Returning to menu.")
                        continue
                    settings["zip_destination"] = zip_path
                    save_settings()
                    print(f"Save files will be zipped to {zip_path}")

                elif selected_setting == "4":
                    header("Unzip Path")
                    print("Select folder where unzipped saves will be stored...")
                    print("")
                    root = Tk()
                    root.withdraw()
                    unzip_path = filedialog.askdirectory(title="Choose Unzip Destination Folder")
                    if not unzip_path:
                        print("No folder selected. Returning to menu.")
                        pause_and_return("No folder selected. Returning to menu.")
                        continue
                    settings["unzip_default_path"] = unzip_path
                    save_settings()
                    print(f"Unzipped files will be stored in {unzip_path}")

                elif selected_setting == "5":
                    first_time = True
                    while True:
                        subprocess.run("cls", shell=True)
                        header("Toggle Visibility")
                        if first_time:
                            appearing_text("Toggle the visibility of players (HIDDEN/VISIBLE).", delay=0.01)
                            appearing_text("Press Enter without typing anything to go back.\n", delay=0.01)
                            first_time = False
                        else:
                            print("Toggle the visibility of players (HIDDEN/VISIBLE).")
                            print("Press Enter without typing anything to go back.\n")

                        for index, player in enumerate(settings["players"]):
                            status = "HIDDEN" if player.get("hidden") else "VISIBLE"
                            print(f"{index + 1}. {player['name']} [{status}]")

                        print("--------------------")
                        selected_index = input("Toggle person #: ").strip()

                        if selected_index == "":
                            break

                        try:
                            selected_index = int(selected_index) - 1
                            if selected_index < 0 or selected_index >= len(settings["players"]):
                                input("Invalid number. Press Enter to continue...")
                                continue

                            settings["players"][selected_index]["hidden"] = not settings["players"][selected_index].get("hidden", False)
                            save_settings()

                        except ValueError:
                            input("Invalid input. Press Enter to continue...")
                
                elif selected_setting == "6":
                    subprocess.run("cls", shell=True)
                    header("Remove people")
                    appearing_text("Select a person to remove:", delay=0.01)
                    for i, player in enumerate(settings["players"]):
                        print(f"{i+1}. {player['name']} (Steam ID: {player['steam_id']})")
                    print("--------------------")
                    try:
                        selected_remove = int(input("Enter the number of the person to remove: "))
                        if 1 <= selected_remove <= len(settings["players"]):
                            removed = settings["players"].pop(selected_remove - 1)
                            save_settings()
                            print(f"Removed {removed['name']} (Steam ID: {removed['steam_id']})")
                        else:
                            pause_and_return("Invalid selection.")
                    except ValueError:
                        pause_and_return("Invalid input. Please enter a number.")

                elif selected_setting == "7":
                    header("Reset Player Names")
                    print("This will reset all player names to their default values.")
                    confirmation = input("Are you sure? (y/n): ")
                    if confirmation.lower() != "y":
                        pause_and_return("Operation cancelled.")
                    else:
                        for default in settings.get("default_players", []):
                            for player in settings["players"]:
                                if str(player["steam_id"]) == str(default["steam_id"]):
                                    player["name"] = default["name"]
                    save_settings()
                    print("All names have been reset to default.")
                
                elif selected_setting == "8":
                    header("Auto Host Switch")
                    current = settings.get("auto_host_switch", False)
                    status = "ENABLED" if current else "DISABLED"
                    appearing_text(f"Auto-switching host on import is currently: {status}", delay=0.01)
                    print("")
                    appearing_text("Would you like to change it?", delay=0.01)
                    print("1. Enable (automatically make yourself the host on import)")
                    print("2. Disable (ask every time before switching host)")
                    print("Press Enter to cancel")
                    print("--------------------")

                    choice = input("Your choice: ").strip()

                    if choice == "1":
                        settings["auto_host_switch"] = True
                        save_settings()
                        pause_and_return("Auto host switch on import has been ENABLED.")
                    elif choice == "2":
                        settings["auto_host_switch"] = False
                        save_settings()
                        pause_and_return("Auto host switch on import has been DISABLED.")
                    else:
                        pause_and_return("No changes made.")

                
                elif selected_setting == "":
                    restart_script()
                    break
        except Exception as e:
            pause_and_return(f"[!] Error in Settings Menu: {e}")
