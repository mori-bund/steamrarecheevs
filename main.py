# main.py
import sys
from argparse import ArgumentParser
from file_utils import load_existing_appids, save_to_csv, save_appids_without_achievements, update_no_achievements
from api_utils import get_owned_games, scrape_steam_data, resolve_vanity_url
from tqdm import tqdm
from config import STEAM_ID

def resolve_steamid(args):
	"""
	Resolve the SteamID based on provided command-line arguments.

	Args:
		args: The parsed command-line arguments.

	Returns:
		str: The resolved SteamID.

	Raises:
		ValueError: If an invalid SteamID format is provided or if the vanity URL
					couldn't be resolved to a SteamID.
	"""
	steamid = STEAM_ID

	if args.steamid:
		steamid = args.steamid

	elif args.vanity:
		steamid = resolve_vanity_url(args.vanity)

		if steamid is None:
			raise ValueError("The provided vanity URL couldn't be resolved to a SteamID.")

		return steamid

	if not steamid.isdigit() or len(steamid) != 17:
		raise ValueError("Invalid SteamID. Please check the SteamID and try again.")

	return steamid

def main():
	"""
	Steam Library Rarest Achievement Scraper to get a list of owned games with
	achievements, find the rarest achievement for each, and whether or not the
	game has been completed.

	Usage:
		python main.py [-s STEAMID] [-u]

	-s, --steamid					Specify a SteamID to search (optional).
	-v, --vanity					Specify a vanity URL to search (optional).
	-u, --update-no-achievements	Check and update no_achievements.txt

	If -u is provided, the script will update the list of appids without
	achievements by checking if any have achievements now and remove them
	if they do. This does not scan any SteamIDs for game info.

	If -s or -v is not provided, it will use the STEAM_ID from the config file.

	"""
	parser = ArgumentParser(description='Steam Library Scraper to find rarest achievements')
	group = parser.add_mutually_exclusive_group()

	group.add_argument('-s', '--steamid', type=str, help='Specify a SteamID to search (optional)')
	group.add_argument('-v', '--vanity', type=str, help='Specify a vanity URL which converts to a SteamID (optional)')
	group.add_argument('-u', '--update-no-achievements', action='store_true', help='Check and update no_achievements.txt')
	args = parser.parse_args()

	num_args_provided = sum([1 for arg in [args.steamid, args.vanity, args.update_no_achievements] if arg])
	if num_args_provided > 1:
		parser.error('Please provide exactly one of -s, -v, or -u.')

	if args.update_no_achievements:
		with open("no_achievements.txt", 'r', encoding='utf-8') as txtfile:
			appids = [int(line.strip()) for line in txtfile.readlines()]
		num_games = len(appids)
		progress_bar = tqdm(total=num_games, unit='games', ncols=100)
		update_no_achievements(appids, num_games, progress_bar)
		sys.exit()

	steamid = resolve_steamid(args)

	try:
		existing_appids = load_existing_appids(steamid)
		owned_games = get_owned_games(steamid)
	except Exception as e:
		print(f"Either the SteamID is invalid or the profile may be set to private.")
		sys.exit(1)

	progress_bar = tqdm(total=len(owned_games), unit='games', ncols=100)

	try:
		scraped_data, no_achievements = scrape_steam_data(steamid, existing_appids, owned_games, progress_bar)
	except Exception as e:
		print(f"Error scraping data: {e}")
		sys.exit(1)

	save_to_csv(scraped_data, steamid)
	save_appids_without_achievements(no_achievements)
	progress_bar.close()


if __name__ == "__main__":
	main()