import json
import shutil
from datetime import datetime
from logging import getLogger, StreamHandler, Formatter
from time import time
from typing import Optional, List, Any


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
        self.logger = getLogger(self.__class__.__name__ + str(id(self)))
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

    def save(self, path: str = None) -> None:
        """
        Saves the save file.

        :param path: Path to save to. If not specified, saves to the original path.
        """
        self.backup()

        if not path:
            path = self.path

        self.logger.debug(f"Saving {path}")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.to_json_string())
        except Exception as e:
            self.logger.exception(f"Failed to save {path}")
            raise e
        self.logger.debug(f"Saved {path}")

    def get_data_keys(self) -> List[str]:
        """
        Returns the keys of the save file's data.
        """
        return list(self.data.keys())

    def get_value(self, key: str, ignore_errors: bool = False) -> Any:
        """
        Gets a value from the save file.

        :param key: Key to get.
        :param ignore_errors: Whether to ignore errors.
        """
        self.logger.debug(f"Getting {key}")
        try:
            return self.data[key]
        except Exception as e:
            self.logger.exception(f"Failed to get {key}")
            if not ignore_errors:
                raise e
            return None

    def set_value(self, key: str, new_value: Any) -> None:
        """
        Sets a value in the save file.

        :param key: Key to set.
        :param new_value: New value to set.
        """
        self.logger.debug(f"Setting {key} to {new_value}")
        try:
            self.data[key] = new_value
        except Exception as e:
            self.logger.exception(f"Failed to set {key} to {new_value}")
            raise e

    def safe_set_value(self, key: str, new_value: Any) -> None:
        """
        Sets a value in the save file, but only if the value matches the original value's type, if the original value is None, or if the new value is None.

        :param key: Key to set.
        :param new_value: New value to set.
        """
        self.logger.debug(f"Safe setting {key} to {new_value}")
        try:
            if self.data[key] is None or type(self.data[key]) == type(new_value) or new_value is None:
                self.data[key] = new_value
            else:
                raise TypeError(f"Type mismatch: {type(self.data[key])} != {type(new_value)}")
        except Exception as e:
            self.logger.exception(f"Failed to safe set {key} to {new_value}")
            raise e

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

    def get_city_name(self) -> str:
        """
        Returns the city name of the save file.
        """
        return self.get_cityshare().split(".")[0]

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

    def get_gamelength(self) -> int:
        """
        Returns the current game length.
        """
        return self.data.get("gameLength")

    def get_player_firstname(self) -> str:
        """
        Returns the player character's first name.
        """
        return self.data.get("playerFirstName")

    def get_player_surname(self) -> str:
        """
        Returns the player character's surname.
        """
        return self.data.get("playerSurname")

    def get_player_gender(self) -> int:
        """
        Get the player character's gender.
        """
        return self.data.get("playerGender")

    def get_partner_gender(self) -> int:
        """
        Get the player character partner's gender.
        """
        return self.data.get("partnerGender")

    def get_player_birthday(self) -> List[int]:
        """
        Returns the player character's birthday.

        Format: [day, month, year]
        """
        return [self.data.get("playerBirthDay"), self.data.get("playerBirthMonth"), self.data.get("playerBirthYear")]

    def get_residence(self) -> int:
        """
        Returns the player character's residence.
        """
        return self.data.get("residence")

    def get_apartments_owned(self) -> List[int]:
        """
        Returns the player character's owned apartments.
        """
        return self.data.get("apartmentsOwned")

    def is_tutorial_enabled(self) -> bool:
        """
        Returns whether the tutorial is enabled.
        """
        return self.data.get("tutorial")

    def get_items(self) -> List[dict]:
        """
        Returns the player character's items.
        """
        return self.data.get("firstPersonItems")

    def get_player_position(self) -> dict:
        """
        Returns the player character's position.
        """
        return self.data.get("playerPos")

    def get_player_rotation(self) -> dict:
        """
        Returns the player character's rotation.
        """
        return self.data.get("playerRot")

    def get_money(self) -> int:
        """
        Returns the player's money.
        """
        return self.data.get("money")

    def get_lockpicks(self) -> int:
        """
        Returns the player's lockpicks.
        """
        return self.data.get("lockpicks")

    def get_social_credit(self) -> int:
        """
        Returns the player's social credit.
        """
        return self.data.get("socCredit")

    def get_health(self) -> float:
        """
        Returns the player's health.
        """
        return self.data.get("health")

    def get_nourishment(self) -> float:
        """
        Returns the player's nourishment.
        """
        return self.data.get("nourishment")

    def get_hydration(self) -> float:
        """
        Returns the player's hydration.
        """
        return self.data.get("hydration")

    def get_alertness(self) -> float:
        """
        Returns the player's alertness.
        """
        return self.data.get("alertness")

    def get_energy(self) -> float:
        """
        Returns the player's energy.
        """
        return self.data.get("energy")

    def get_hygiene(self) -> float:
        """
        Returns the player's hygiene.
        """
        return self.data.get("hygiene")

    def get_heat(self) -> float:
        """
        Returns the player's heat.
        """
        return self.data.get("heat")

    def get_drunk(self) -> float:
        """
        Returns the player's drunkness.
        """
        return self.data.get("drunk")

    def get_sick(self) -> float:
        """
        Returns the player's sickness.
        """
        return self.data.get("sick")

    def get_headache(self) -> float:
        """
        Returns the player's headache.
        """
        return self.data.get("headache")

    def get_wet(self) -> float:
        """
        Returns the player's wetness.
        """
        return self.data.get("wet")

    def get_broken_leg(self) -> float:
        """
        Returns the player's broken leg-ness.
        """
        return self.data.get("brokenLeg")

    def get_bruised(self) -> float:
        """
        Returns the player's bruised-ness.
        """
        return self.data.get("bruised")

    def get_black_eye(self) -> float:
        """
        Returns the player's black eye-ness.
        """
        return self.data.get("blackEye")

    def get_blacked_out(self) -> float:
        """
        Returns the player's blacked out-ness.
        """
        return self.data.get("blackedOut")

    def get_numb(self) -> float:
        """
        Returns the player's numbness.
        """
        return self.data.get("numb")

    def get_poisoned(self) -> float:
        """
        Returns the player's poisoned-ness.
        """
        return self.data.get("poisoned")

    def get_bleeding(self) -> float:
        """
        Returns the player's bleeding rate.
        """
        return self.data.get("bleeding")

    def get_well_rested(self) -> float:
        """
        Returns the player's well rested-ness.
        """
        return self.data.get("wellRested")

    def get_starch_addiction(self) -> float:
        """
        Returns the player's starch addiction.
        """
        return self.data.get("starchAddiction")

    def get_sync_disk_install(self) -> float:
        """
        Returns the player's sync disk install.
        """
        return self.data.get("syncDiskInstall")

    def get_blinded(self) -> float:
        """
        Returns the player's blindness.
        """
        return self.data.get("blinded")

    def is_crouched(self) -> bool:
        """
        Returns whether the player is crouched.
        """
        return self.data.get("crouched")

    def get_upgrades(self) -> List[dict]:
        """
        Returns the player's SyncDisk upgrades.
        """
        return self.data.get("upgrades")

    def get_keyring(self) -> List[int]:
        """
        Returns the player's keyring.
        """
        return self.data.get("keyring")

    def get_books_read(self) -> List[str]:
        """
        Returns the player's books read.
        """
        return self.data.get("booksRead")

    def get_buildings(self) -> List[dict]:
        """
        Returns buildings in the city.
        """
        return self.data.get("buildings")

    def get_companies(self) -> List[dict]:
        """
        Returns companies in the city.
        """
        return self.data.get("companies")

    def get_evidence(self) -> List[dict]:
        """
        Returns evidence.
        """
        return self.data.get("evidence")

    def get_guestPasses(self) -> List[dict]:
        """
        Returns guest passes.
        """
        return self.data.get("guestPasses")

    def get_rooms(self) -> List[dict]:
        """
        Returns rooms.
        """
        return self.data.get("rooms")

    def get_removedCityData(self) -> List[int]:
        """
        Returns removed city data.
        """
        return self.data.get("removedCityData")

    def get_addresses(self) -> List[dict]:
        """
        Returns addresses.
        """
        return self.data.get("addresses")

    def get_citizens(self) -> List[dict]:
        """
        Returns citizens.
        """
        return self.data.get("citizens")

    def get_doors(self) -> List[dict]:
        """
        Returns doors.
        """
        return self.data.get("doors")

    def get_active_cases(self) -> List[dict]:
        """
        Returns the active cases.
        """
        return self.data.get("activeCases")

    def get_crimescenes(self) -> List[dict]:
        """
        Returns the crime scenes.
        """
        return self.data.get("crimeSceneCleanup")

    def get_passcodes(self) -> List[dict]:
        """
        Returns the passcodes.
        """
        return self.data.get("passcodes")

    def get_murder_id(self) -> int:
        """
        Returns the murder ID of the save file.
        """
        return self.data.get("assignMurderID")

    def get_murders(self) -> List[dict]:
        """
        Returns the list of murders
        """
        return self.data.get("murders")

    def is_murder_routine_active(self) -> bool:
        """
        Returns whether the murderer's routine is active.
        """
        return self.data.get("murderRoutineActive")
