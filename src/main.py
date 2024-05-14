import atexit
import logging
import requests
import shelve
from typing import List
from bs4 import BeautifulSoup

# Set up logging with timestamp and level
logging.basicConfig(
    # Put the timestamp at the beginning of each log message
    # Put level next
    format="%(levelname)s: %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

# store data in a file
cache = shelve.open(".cache")

url = "https://socialblade.com/youtube/compare/t-series/mrbeast"


def close_cache():
    logging.info("Closing cache")
    cache.close()


atexit.register(close_cache)


# Generate headers for the request
def generate_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


# Get HTTP response from the API or from the cache
def get_or_cache(url):
    if url in cache:
        return cache[url]
    response = requests.get(url, headers=generate_headers())
    cache[url] = response.text
    return cache[url]


def main():
    logging.info("Starting main")
    data: str = get_or_cache(url)
    data: BeautifulSoup = BeautifulSoup(data, "html.parser")

    # Find by id
    data = data.find("div", {"id": "subscribersYTDYGraph"})

    # Get script tag inside the div
    data = data.find("script")

    # Get the text inside the script tag
    data = data.text

    # Extract everything after the first occurrence of "Date,T-Series,MrBeast"
    data = data.split("Date,T-Series,MrBeast")[1]

    # And everything before the first occurrence of "", {"
    data = data.split(", {")[0]

    # Split on " + "
    data: List[str] = data.split(" + ")

    # Clean whitespace
    # Remove quotes
    # Remove trailing whitespace
    for i in range(len(data)):
        d = data[i]
        d = d.strip()
        d = d.replace('"', "")
        d = d[:-2]
        data[i] = d

        logging.info(d)

    # Clean first element
    data[0] = data[0][data[0].index("2") :]

    # Print data to output (with csv format)
    print("Date,T-Series,MrBeast")
    for d in data:
        print(d)

    logging.info("Ending main")


if __name__ == "__main__":
    main()
