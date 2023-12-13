# Steam Library Rarest Achievement Scraper

The Steam Library Rarest Achievement Scraper is a Python script that allows you to retrieve information about a Steam user's owned games, their rarest achievements, and whether the user has completed them. The purpose of this script was to find the games in my library that are easiest to 100%. My thinking is that if the rarest achievement has been obtained by a large percentage of players, then it is likely an easy game to 100%.

## Features

- Retrieve a list of games owned by a Steam user.
- Find the rarest achievement in each game based on global achievement percentages.
- Determine whether the user has completed all achievements for a game.
- Option to rescan games with no achievements. All are scanned to see if achievements have been added.

## Prerequisites

Before using the script, make sure you have the following:

- Python 3.x installed on your system.
- Steam API Key (available from the [Steam Developer website](https://steamcommunity.com/dev/apikey)).
- [Steam ID](https://help.steampowered.com/en/faqs/view/2816-BE67-5B69-0FEC) of the user you want to scrape. There is a command line option to scan any ID as well. **The Steam community profile MUST be public for this to work.**

## Usage

To use the script, follow these steps:

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/mori-bund/steamrarecheevs.git
   ```

2. Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

3. Set up your Steam API Key:

   - Obtain your API Key from the [Steam Developer website](https://steamcommunity.com/dev/apikey) if you don't already have one.
   - Remove the underscore from the `con_fig.py` filename in the project directory.
   - Add your API Key and [Steam ID](https://help.steampowered.com/en/faqs/view/2816-BE67-5B69-0FEC) to the `config.py` file:

     ```python
     # config.py
     API_KEY = 'your_api_key_here'
     STEAM_ID = 'your_steam_id_here'
     ```

4. Run the script:

   ```shell
   python main.py [-s STEAMID] [-v VANITY] [-u]
   ```

   - Use the `-s` option to specify a SteamID to scrape (optional). This will scrape it instead of the one in your `config.py` file.
   - Use the `-v` option to specify a Steam Vanity URL to scrape (optional). This will resolve the vanity url to a SteamID and scrape that library instead of the one in your `config.py` file.
   - Use the `-u` option to check and update the list of games with no achievements (optional). Any scanned game that doesn't have achievements is added to the `no_achievements.txt` file so the scraper knows to not bother checking those. This options rescans this list and removes the appID of any game that now has achievements. 

## Output

The script will generate CSV files containing the scraped data in a `data` directory. Each CSV file corresponds to a Steam user's library and is sorted in descending order by the rarest achievement column.

## Notes

* Please let me know if you find any bugs! I am a complete amateur and just barely know what I'm doing, but I am aware this script is not optimized at all.
* Large libraries will take a longer time to scrape the first time it is run. My 3000+ game library takes over 20 minutes to fully scrape.
* Rescanning games without achievements will also take a long time since there are well over 10,000 games in the list.
* If you scan a library that already has a CSV file saved, it will skip games already saved in the file. The script does NOT update the 100% status of a game when scanning again. I may add this functionality later.
* Steam allows some granularity with making the profile private. I probably didn't catch every nuance of this. The script will close if the profile is totally locked down, and the script will return all data except completion status if achievement data is locked down.
* I hope to add HowLongToBeat scraping some day. HLTB scraping is pretty dodgy in my experience, unfortunately.