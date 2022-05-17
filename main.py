import argparse
import requests
from pathlib import Path
import yaml
import os

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

print(HEADERS)


def make_config_dir():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.mkdir(parents=True, exist_ok=True)


def make_config_file():
    if not CONFIG_NAME.exists():
        CONFIG_NAME.touch()

        with open(CONFIG_NAME, "w") as file:
            file.write(yaml.dump(DEFAULT_CONFIG))


def redirects():
    res = requests.get(URL + "/api/redirects", headers=HEADERS)
    print(res.text)


def main():
    make_config_dir()
    make_config_file()

    redirects()


if __name__ == "__main__":
    main()
