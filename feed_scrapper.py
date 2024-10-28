import requests 
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
from argparse import ArgumentParser
from tqdm import tqdm


class NCEpisodeScrapper:
    """
    A class to scrape episodes from the Nerdcast feed.

    Attributes:
    feed (str): The URL of the feed to scrape.
    """
    def __init__(self, feed="https://jovemnerd.com.br/feed-nerdcast/"):
        """
        The constructor for NCEpisodeScrapper class.

        Parameters:
        feed (str): The URL of the feed to scrape. Default is the Nerdcast feed.
        """
        doc = requests.get(feed)

        soup = BeautifulSoup(doc.content, "xml")

        all_episodes = soup.find_all("item")

        eps = []
        for item in all_episodes:
            # Extract the title of the episode
            title = item.find("title").text

            ep_url = item.find("link").text

            ep_date = item.find("pubDate").text
            ep_date = datetime.strptime(ep_date, "%a, %d %b %Y %H:%M:%S %z") # parse rfc 2822 
            
            enc = item.find("enclosure")
            dl_url = enc["url"]
            ep_dur = enc["length"] # duration in seconds

            idx = [m.start() for m in re.finditer("https://", dl_url)][1] # get second https-starting url in string
            dl_url = dl_url[idx:]

            ep = {
                "title": title,
                "ep_dur": ep_dur,
                "ep_url": ep_url,
                "ep_date": ep_date,
                "dl_url": dl_url,
            }
            
            eps.append(ep)

        self._ep_list_keys = list(eps[0].keys()) # get first saved episode keys for futher use in saving

        eps.reverse()
        self._episode_list = eps

    def __iter__(self):
        return iter(self._episode_list)
    
    def __getitem__(self, item):
        return self._episode_list[item]

    def save_to_csv(self, file):
        """
        Save the episode list to a CSV file.

        Parameters:
        file (str): The path to the file where the CSV will be saved.

        Returns:
        None
        """
        df = pd.DataFrame(self._episode_list, columns=self._ep_list_keys)
        df.to_csv(file, index=False)

    def total_download_size(self):
        """
        Calculate the total download size of all episodes in the episode list.

        This method iterates over the list of episodes, retrieves the download URL for each episode,
        and makes a HEAD request to get the 'Content-Length' from the response headers. It sums up
        the sizes to compute the total download size.

        Returns:
            int: The total download size of all episodes in bytes.

        Raises:
            Exception: If there is an error in making the HEAD request or retrieving the 'Content-Length'.
        """

        total_size = 0
        for ep in tqdm(self._episode_list):
            url = ep["dl_url"]
            try:
                response = requests.head(url, allow_redirects=True)
                f_size = int(response.headers.get("Content-Length", 0))
                total_size += f_size
            except Exception as e:
                print(f"Error getting size for {url}: {e}")

        return total_size
  
if __name__ == "__main__":
    parser = ArgumentParser(description="Nerdcast Episode Scraper")
    parser.add_argument(
        "-f", "--feed", type=str, default="https://jovemnerd.com.br/feed-nerdcast/",
        help="URL of the feed to scrape. Default is the Nerdcast feed."
    )
    parser.add_argument(
        "-s", "--save_file", type=str, required=True,
        help="Path to the CSV file where the episode list will be saved."
    )
    parser.add_argument(
        "-d", "--download_size", action="store_true",
        help="Calculate and print the total download size of all episodes."
    )

    args = parser.parse_args()

    nces = NCEpisodeScrapper(feed=args.feed)
    nces.save_to_csv(args.save_file)
    
    if args.download_size:
        total_size_gb = nces.total_download_size() / (1024 * 1024 * 1024)
        print(f"Total download size: {total_size_gb:.2f} GB")