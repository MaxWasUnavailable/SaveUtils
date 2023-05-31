import json
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
