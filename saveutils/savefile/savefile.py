import json
import shutil
from datetime import datetime
from logging import getLogger, StreamHandler, Formatter
from time import time
from typing import Optional


class SaveFile:
    """
    Represents a Shadows of Doubt save file.
    """

    def __init__(self, path: Optional[str] = None, verbose: bool = False) -> None:
        """
        Creates a new SaveFile instance.

        :param path: Path to the save file.
        :param verbose: Whether to enable verbose logging.
        """
        self.path = path
        self.data = None
        self.parse_time = None

        self.logger = None
        self.init_logger(verbose)

        if path:
            self.parse_file(path)

    def init_logger(self, verbose: bool = False) -> None:
        """
        Initializes the logger.

        :param verbose: Whether to enable verbose logging.
        """
        self.logger = getLogger(self.__class__.__name__)
        handler = StreamHandler()
        handler.setFormatter(Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s"))
        self.logger.addHandler(handler)

        if verbose:
            self.logger.setLevel("DEBUG")

    def parse_string(self, string: str) -> None:
        """
        Parses the save file string.

        :param string: String to parse.
        """
        self.parse_time = time()
        self.data = json.loads(string)
        self.parse_time = time() - self.parse_time
        self.logger.debug(f"Parse time: {self.parse_time}")

    def parse_file(self, path: Optional[str]) -> None:
        """
        Parses the save file.

        :param path: Path to the save file.
        """
        self.logger.debug(f"Parsing file: {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.parse_string(f.read())
        except FileNotFoundError as e:
            self.logger.exception(f"File not found: {path}")
            raise e
        except Exception as e:
            self.logger.exception(f"Failed to parse file: {path}")
            raise e

    @classmethod
    def from_string(cls, string: str) -> "SaveFile":
        """
        Creates a new SaveFile instance from a string.

        :param string: String to parse.
        """
        save = cls()
        save.parse_string(string)
        return save

    @classmethod
    def from_file(cls, path: Optional[str]) -> "SaveFile":
        """
        Creates a new SaveFile instance from a file.

        :param path: Path to the save file.
        """
        save = cls()
        save.parse_file(path)
        return save

    def to_json_string(self) -> str:
        """
        Returns the save file as a JSON string.
        """
        try:
            return json.dumps(self.data)
        except Exception as e:
            self.logger.exception(f"Failed to convert to JSON string")
            raise e

    def backup(self) -> None:
        """
        Creates a backup of the save file.
        """
        self.logger.debug(f"Creating backup of {self.path}")
        try:
            shutil.copy2(self.path, self.path + ".bak")
        except Exception as e:
            self.logger.exception(f"Failed to create backup of {self.path}")
            raise e
        self.logger.debug(f"Created backup of {self.path} as {self.path + '.bak'}")

    def save(self) -> None:
        """
        Saves the save file.
        """
        self.backup()
        self.logger.debug(f"Saving {self.path}")
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                f.write(self.to_json_string())
        except Exception as e:
            self.logger.exception(f"Failed to save {self.path}")
            raise e
        self.logger.debug(f"Saved {self.path}")

    def get_build(self) -> str:
        """
        Returns the build of the save file.
        """
        return self.data.get("build")

    def get_cityshare(self) -> str:
        """
        Returns the cityshare of the save file.
        """
        return self.data.get("cityShare")

    def get_seed(self) -> str:
        """
        Returns the seed of the save file.

        More common name wrapper for get_cityshare().
        """
        return self.get_cityshare()

    def get_savetime(self) -> datetime:
        """
        Returns the save's datetime when it was saved.
        """
        save_time = self.data.get("saveTime")
        try:
            return datetime.strptime(save_time, "%Y-%d-%m-%H-%M-%S.%f")
        except Exception as e:
            self.logger.exception(f"Failed to parse save time: {save_time}")
            raise e

    def get_gametime(self) -> float:
        """
        Returns the game time of the save file.
        """
        return self.data.get("gameTime")

    def get_case_id(self) -> int:
        """
        Returns the case ID of the save file.
        """
        return self.data.get("assignCaseID")

    def get_murder_id(self) -> int:
        """
        Returns the murder ID of the save file.
        """
        return self.data.get("assignMurderID")

    def get_gamelength(self) -> int:
        """
        Returns the current game length.
        """
        return self.data.get("gameLength")
