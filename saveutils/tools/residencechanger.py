from logging import getLogger, StreamHandler, Formatter
import locale

# Note. The import strategy is a bit inconsistent from the other tools.
# I needed it this way for PyTest to be happy in my environment. ~ BC
from saveutils.savefile.savefile import SaveFile

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
    DEFAULT_COST = 20

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
    def change_residence(source_save : SaveFile, new_residence : int, cost : int = DEFAULT_COST, target_save : SaveFile = None, skipSave : bool = False):
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

        # Important conditions to check!
        # Do NOT attempt to swap permanent residency if any of these conditions are true!
        try:
            if new_residence not in player_residences:
                logger.error(f"Attempting to switch residency to apartment {new_residence} NOT owned by player.")
                raise Exception
            if cost < 0:
                logger.error(f"Cost override is negative ({cost}). City Hall will not pay you to switch residencies.")
                raise Exception
            if current_residence == new_residence:
                logger.error(f"You already live in apartment {current_residence} as your primary residency. You don't need to switch.")
                raise Exception
            if cost > money:
                logger.error(f"You don't have enough money to pay the fee. Balance: {money}. Cost: {cost}. Run the command again with the -c switch to override the cost.")
                raise Exception
        except:
            # If we are here, then one of the above conditions are met.
            # We logged the error already.
            # We just need to do cleanup here and return
            source_save.locked = original_locked
            return
        # We're good to go. Conditions passed. Change the residency.
        source_save.safe_set_value("residence", new_residence)
        logger.info("Residence changed.")
        source_save.safe_set_value("money", money-cost)
        logger.info(f"Fee processed ({money-cost} remaining)" if cost > 0 else 'Fee waived')
        source_save.locked = original_locked
        if not skipSave: # For testing purposes, we have the option to skip writing to the file
            source_save.save(target_save)
        logger.info("File saved.")

def register_subparser(main_subparser) -> None:
    """
    Registers the residence changer subparser.
    :param main_subparser: The main parser's subparser
    """
    residence_parser = main_subparser.add_parser("residence", help=description, description=description)
    residence_parser.add_argument("-s", "--set", type=int, help="Set the player's primary residence to this ID")
    residence_parser.add_argument('-c', '--cost', type=int, default=ResidenceChanger.DEFAULT_COST, help=f"Override the default cost of {ResidenceChanger.DEFAULT_COST}cr for the residency change.")

def handle_subparser(args) -> None:
    """
    Handles the residence changer subparser.
    :param args: The arguments
    """
    if args.tool == "residence":
        if args.set:
            ResidenceChanger.change_residence(args.save, args.set, args.cost)
        else:
            ResidenceChanger.output_residencies(args.save)