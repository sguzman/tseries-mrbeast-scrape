import atexit
import logging
import requests
import shelve

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


def close_cache():
    logging.info("Closing cache")
    cache.close()


atexit.register(close_cache)


# Get HTTP response from the API or from the cache
def get_or_cache(url):
    if url in cache:
        return cache[url]
    response = requests.get(url)
    cache[url] = response.json()
    return cache[url]


def main():
    url = "https://jsonplaceholder.typicode.com/posts"
    data = get_or_cache(url)
    for post in data:
        print(post["title"])


if __name__ == "__main__":
    main()
