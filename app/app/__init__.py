import logging
import json
from pathlib import Path

VERSIONING_FILE = "version.json"


def get_version(directory: Path = Path(__file__).parent) -> dict:
    try:
        with open(directory / Path(VERSIONING_FILE)) as file:
            return json.load(file)
    except OSError:
        logging.warning("No version file found.")
        return {}


__version__ = get_version().get("hash")
