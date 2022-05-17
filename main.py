import argparse
import requests
from pathlib import Path
import yaml

CONFIG_PATH = Path.home() / Path(".config/link-cli")
CONFIG_NAME = CONFIG_PATH / Path("config.yml")

DEFAULT_CONFIG = {"key": "<insert-key>"}
URL = "http://173.255.248.182:8000"


def load_config():
    with open(CONFIG_NAME) as file:
        return yaml.safe_load(file)


LOADED_CONFIG = load_config()
KEY = LOADED_CONFIG["key"]
HEADERS = {
    "content-type": "application/json",
    "x-api-key": KEY,
}


def make_config_dir():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.mkdir(parents=True, exist_ok=True)


def make_config_file():
    if not CONFIG_NAME.exists():
        CONFIG_NAME.touch()

        with open(CONFIG_NAME, "w") as file:
            file.write(yaml.dump(DEFAULT_CONFIG))


class Link:
    def __init__(self, cache=True):
        self.cache = cache
        self.cache_version = None

    @property
    def redirects(self):
        return requests.get(URL + "/api/redirects", headers=HEADERS).text

    @property
    def version(self):
        if self.cache_version is not None:
            return self.cache_version

        if self.cache:
            self.cache_version = requests.get(
                URL + "/api/version", headers=HEADERS
            ).text

    def newredirect(self, name, url):
        print(name, url)
        return requests.get(URL + "/api/redirects", headers=HEADERS)


def parser():
    parse = argparse.ArgumentParser()
    parse.add_argument("--api-version", help="Get version", action="store_true")
    parse.add_argument("--redirects", help="Get redirects", action="store_true")
    return parse.parse_args()


def main():
    args = parser()

    if not CONFIG_NAME.exists():
        make_config_dir()
        make_config_file()

    link = Link()

    if args.api_version:
        print(link.version)
        exit(0)

    if args.redirects:
        print(link.redirects)
        exit(0)


if __name__ == "__main__":
    main()
