# SCHEDULE 1 SAVE TOOLS 

[![Download](https://img.shields.io/badge/Download-Now-brightgreen?style=plastic)](https://github.com/dds200/Schedule-1-Tools/releases/download/v1.0.0/Schedule-1-Tools.exe)

A command-line utility for managing save files in the game "Schedule I".
Designed for enhanced control over host switching, save exporting/importing, and personalization.

Created by: dds_200

## REQUIREMENTS
• Windows 10 or 11
• No installation needed if you use the EXE version (all dependencies are bundled)
• If running the Python script directly:
    - Python 3.8+
    - Run: pip install art

## USAGE

Run the tool using:
    Schedule-1-Tools.exe

Select a mode using the number shown in the main menu.

## MODES EXPLAINED


1. Host Changer
   - Purpose: Change who is the host (Player_0) in a save file.
   - Usage: Select the save, then choose the player to become the new host.
     The current host will be demoted to a regular player.

2. Save Exporter
   - Purpose: Zip a save game folder for sending/sharing.
   - Usage: Select the save to export. The tool will zip it and include your Steam ID in a file named `sender_info.txt`.
     This allows the receiver to detect you were the original host.

3. Save Importer
   - Purpose: Import a zipped save file.
   - Usage: Select a ZIP file and choose a save slot. If the zip contains `sender_info.txt`, you’ll be asked if you want to make yourself the host (or it will do so automatically if the setting is enabled).

4. Save Swapper
   - Purpose: Swap positions between two save files.
   - Usage: Select two different saves (e.g., SaveGame_2 and SaveGame_5), and their folders will be swapped.

5. Save Renamer
   - Purpose: Rename the visible name of a save in the game's menu.
   - Usage: Select the save and enter a new display name. This changes the "OrganisationName" field in `Game.json`.

6. Save Deleter
   - Purpose: Delete a save file permanently.
   - Usage: Select the save you want to remove. You’ll be asked for confirmation before deletion.

## Settings

1. Change the name of a person
   → Rename any of the players listed in the config.

2. Add a new person
   → Add a player by name and Steam ID.

3. Change the ZIP destination
   → Set where exported save ZIPs will be stored.

4. Change the unzip default destination
   → Set the folder that appears by default when importing zipped saves.

5. Toggle people visibility
   → Hide or show specific players from the UI (e.g., unused Steam IDs).

6. Remove a person
   → Remove a saved player entry completely.

7. Reset player names
   → Reset names to their original defaults from when the tool was first run.

8. Toggle Auto Host Switch
   → When ON: You will be made host automatically on import if `sender_info.txt` exists.
   → When OFF: You will be prompted to choose whether to switch host.

## FILE LOCATIONS
• Saves are usually located at:
  %LOCALAPPDATA%\\..\\LocalLow\\TVGS\\Schedule I\\Saves

• Settings are stored in: settings.json

## TIPS

• Make sure your save slots are not in use by the game when switching or deleting.

**Enjoy full control over your Schedule I experience!**
