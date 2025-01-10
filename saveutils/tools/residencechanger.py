from logging import getLogger, StreamHandler, Formatter
from sys import getsizeof
import locale
import json
import math

from savefile.savefile import SaveFile

description = "A tool for changing one's primary residence."

logger = getLogger(__name__)
logger.setLevel("INFO")
handler = StreamHandler()
handler.setFormatter(Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s"))
logger.addHandler(handler)
locale.setlocale(locale.LC_ALL, '')

class ResidenceChanger:
    """
    A tool for changing one's primary residence.
    """
    default_cost = 20

    @staticmethod
    def output_residencies(source_save : SaveFile):
        """
        Output the player's owned apartments
        """
        original_locked = source_save.locked
        source_save.locked = True

        logger.info("Looking up player owned residences...")
        current_residence = source_save.get_residence()
        player_residences = source_save.get_apartments_owned()
        logger.info(f"Current residence: {current_residence}")
        logger.info(f"Player owned apartments: {player_residences if len(player_residences) > 0 else "None"}")

        source_save.locked = original_locked


    @staticmethod
    def change_residence(source_save : SaveFile, new_residence : int, cost : int):
        """
        Changes the player's residence to one available
        """
        original_locked = source_save.locked
        source_save.locked = True

        logger.info("Looking up player owned residences...")

        money = source_save.get_money()
        current_residence = source_save.get_residence()
        player_residences = source_save.get_apartments_owned()
        logger.info(f"Money: {money}")
        logger.info(f"Cost: {cost}")
        logger.info(f"Current residence: {current_residence}")
        logger.info(f"New residence: {new_residence}")
        logger.info(f"Player owned apartments: {player_residences if len(player_residences) > 0 else "None"}")

        # Sanity checks
        if new_residence not in player_residences:
            logger.error(f"Attempting to switch residency to apartment {new_residence} NOT owned by player.")
            return
        if cost < 0:
            logger.error(f"Cost override is negative ({cost}). City Hall will not pay you to switch residencies.")
            return
        if current_residence == new_residence:
            logger.error(f"You already live in apartment {current_residence} as your primary residency. You don't need to switch.")
            return
        if cost > money:
            logger.error(f"You don't have enough money to pay the fee. Balance: {money}. Cost: {cost}. Run the command again with the -c switch to override the cost.")
            return
        
        # We're good to go

        money -= cost
        source_save.safe_set_value("residence", new_residence)
        logger.info(f"Residence changed.")
        source_save.safe_set_value("money", money)
        logger.info(f"Fee processed.")
        source_save.locked = original_locked
        source_save.save()
        logger.info(f"File saved.")

def register_subparser(main_subparser) -> None:
    """
    Registers the residence changer subparser.
    :param main_subparser: The main parser's subparser
    """
    residence_parser = main_subparser.add_parser("residence", help=description, description=description)
    residence_parser.add_argument("-s", "--set", type=int, help="Set the amount of health your character has")
    residence_parser.add_argument('-c', '--cost', type=int, default=ResidenceChanger.default_cost, help=f"Override the default cost of {ResidenceChanger.default_cost}cr for the residency change.")

def handle_subparser(args) -> None:
    """
    Handles the residence changer subparser.
    :param args: The arguments
    """
    if args.tool == "residence":
        source_save = args.save
        target_save = SaveFile(args.output, args.verbose)

        if args.set:
            ResidenceChanger.change_residence(source_save, args.set, args.cost)
        else:
            ResidenceChanger.output_residencies(source_save)