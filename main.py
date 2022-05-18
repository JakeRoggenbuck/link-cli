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


def make_config_dir():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.mkdir(parents=True, exist_ok=True)


def make_config_file():
    if not CONFIG_NAME.exists():
        CONFIG_NAME.touch()

        with open(CONFIG_NAME, "w") as file:
            file.write(yaml.dump(DEFAULT_CONFIG))


class Link:
    def __init__(self, headers, no_cache: bool = True):
        self.headers = headers
        self.no_cache = no_cache
        self.cache_version = None

    @property
    def redirects(self):
        return requests.get(URL + "/api/redirects", headers=self.headers).text

    @property
    def redirects_formatted(self):
        total = "number alias url"
        for line in self.redirects.split("\n"):
            if line != "":
                num, other = line.split(": ")
                name, url = other.split(" -> ")
                total += f"\n{num} {name} {url}"
        return total

    @property
    def version(self):
        if self.no_cache:
            return requests.get(URL + "/api/version", headers=self.headers).text
        else:
            if self.cache_version is not None:
                return self.cache_version
            else:
                self.cache_version = requests.get(URL + "/api/version", headers=self.headers).text
                return self.cache_version

    def newredirect(self, name, url):
        return requests.post(
            URL + "/api/newredirect",
            headers=self.headers,
            data={
                "alias": name,
                "url": url,
            },
        )

    def add_alias(self):
        name = input("alias: ")
        url = input("url: ")

        if input("Both correct? [Y/n]: ").upper() != "N":
            print(self.newredirect(name, url).text)
        else:
            print("No request made.")


def parser():
    parse = argparse.ArgumentParser(description='CLI tool for link.jr0.org')
    parse.add_argument("-p", "--api-version", help="Get version", action="store_true")
    parse.add_argument("-r", "--redirects", help="Get redirects", action="store_true")
    parse.add_argument(
        "-f", "--redirects-formatted", help="Get redirects formatted", action="store_true"
    )
    parse.add_argument("-a", "--add-alias", help="Add alias", action="store_true")
    return parse


def main():
    parse = parser()
    args = parse.parse_args()

    if not CONFIG_NAME.exists():
        make_config_dir()
        make_config_file()

    loaded_config = load_config()
    key = loaded_config["key"]
    headers = {
        "content-type": "application/json",
        "x-api-key": key,
    }

    link = Link(headers)

    if args.api_version:
        print(link.version)

    elif args.redirects:
        print(link.redirects)

    elif args.redirects_formatted:
        print(link.redirects_formatted)

    elif args.add_alias:
        link.add_alias()

    else:
        parse.print_help()


if __name__ == "__main__":
    main()
