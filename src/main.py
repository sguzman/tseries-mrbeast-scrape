import requests
import shelve

# store data in a file
cache = shelve.open(".cache")


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
