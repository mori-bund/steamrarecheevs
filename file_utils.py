# file_utils.py
import csv
import os
import pandas as pd
from api_utils import get_game_achievement_data

DATA_DIR = 'data'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def load_existing_appids(steamid):
    """
    Get a list of AppIDs that have already been scanned. Gets them from an
    existing CSV (if there is one) and from a list of games known to have
    no achievements.

    Args:
        steamid (str): The SteamID of the user.

    Returns:
        set: A set of previously scraped Steam AppIDs.
    """
    csv_filename = os.path.join(DATA_DIR, f"{steamid}.csv")
    txt_filename = "no_achievements.txt"
    existing_appids = set()
    
    if os.path.isfile(csv_filename):
        with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader, None)  # Skip the header row
            for row in csv_reader:
                appid = int(row[0])
                existing_appids.add(appid)

    if os.path.isfile(txt_filename):
        with open(txt_filename, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                appid = int(row[0])
                existing_appids.add(appid)
    
    return existing_appids

def save_to_csv(data, steamid):
    """
    Save scraped data to a CSV file for each unique SteamID. Appends to the
    file if it already exists, and creates the file if it doesn't. Sorts
    the csv by rarest achievement when finished.

    Args:
        data (list): List of data to be saved to the CSV file.
        steamid (str): The SteamID of the user.
    """
    csv_filename = os.path.join(DATA_DIR, f"{steamid}.csv")

    file_exists = os.path.isfile(csv_filename)

    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        if not file_exists:
            csv_writer.writerow(['AppID', 'Title', 'Rarest Achievement %', 'Completed'])

        for row in data:
            csv_writer.writerow(row)

    df = pd.read_csv(csv_filename)
    df = df.sort_values(by='Rarest Achievement %', ascending=False)
    df.to_csv(csv_filename, index=False)

def save_appids_without_achievements(appids):
    """
    Adds a list of appids without achievements to the text file.

    Args:
        appids (list): List of appids without achievements.
    """
    txt_filename = "no_achievements.txt"

    with open(txt_filename, 'a', encoding='utf-8') as txtfile:
        for appid in appids:
            txtfile.write(str(appid) + '\n')

def update_no_achievements(appids, num_games, progress_bar):
    """
    Update the list of appids without achievements. This is done with an
    optional flag at runtime.

    Args:
        appids (list): List of appids without achievements.
        num_games (int): The total number of appids to be updated.
        progress_bar (tqdm.tqdm): Progress bar for tracking progress.
    """
    updated_appids = []
    for appid in appids:
        if get_game_achievement_data(appid) == None:
            updated_appids.append(appid)
            num_games -= 1
        progress_bar.update(1)
        
    with open("no_achievements.txt", 'w', encoding='utf-8') as txtfile:
        for appid in updated_appids:
            txtfile.write(str(appid) + '\n')

    print(f"Removed {num_games} appid(s) that now have achievements.")