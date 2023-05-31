import argparse
from logging import getLogger, StreamHandler, Formatter

from savefile.savefile import SaveFile

description = "A collection of save game editing methods which can be considered cheats."

logger = getLogger(__name__)
logger.setLevel("INFO")
handler = StreamHandler()
handler.setFormatter(Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s"))
logger.addHandler(handler)


class MoneyCheats:
    """
    A collection of money cheats.
    """

    @staticmethod
    def set_money(save: SaveFile, amount: int):
        """
        Sets the amount of money the player has.
        """
        save.safe_set_value("money", amount)
        logger.info(f"Set money to {amount}")

    @staticmethod
    def add_money(save: SaveFile, amount: int):
        """
        Adds money to the player's current amount.
        """
        save.safe_set_value("money", save.get_value("money") + amount)
        current_money = save.get_money()
        logger.info(f"Added {amount} to money. Current money: {current_money}")

    @staticmethod
    def remove_money(save: SaveFile, amount: int):
        """
        Removes money from the player's current amount.
        """
        MoneyCheats.set_money(save, save.get_value("money") - amount)
        current_money = save.get_money()
        logger.info(f"Removed {amount} from money. Current money: {current_money}")

    @staticmethod
    def print_money(save: SaveFile):
        """
        Prints the player's current amount of money.
        """
        current_money = save.get_money()
        logger.info(f"Current money: {current_money}")


class HealthCheats:
    """
    A collection of health cheats.
    """

    @staticmethod
    def set_health(save: SaveFile, amount: int):
        """
        Sets the amount of health the player has.
        """
        save.safe_set_value("health", amount)
        logger.info(f"Set health to {amount}")

    @staticmethod
    def add_health(save: SaveFile, amount: int):
        """
        Adds health to the player's current amount.
        """
        HealthCheats.set_health(save, save.get_value("health") + amount)
        current_health = save.get_health()
        logger.info(f"Added {amount} to health. Current health: {current_health}")

    @staticmethod
    def remove_health(save: SaveFile, amount: int):
        """
        Removes health from the player's current amount.
        """
        HealthCheats.set_health(save, save.get_value("health") - amount)
        current_health = save.get_health()
        logger.info(f"Removed {amount} from health. Current health: {current_health}")

    @staticmethod
    def print_health(save: SaveFile):
        """
        Prints the player's current amount of health.
        """
        current_health = save.get_health()
        logger.info(f"Current health: {current_health}")


# Add the cheats subparser
def register_subparser(main_parser: argparse.ArgumentParser) -> None:
    """
    Registers the cheats subparser.
    :param main_parser: The main parser
    """
    cheats_parser = main_parser.add_subparsers(title="Cheats", description=description, dest="cheats")

    money_parser = cheats_parser.add_parser("money", help="Money cheats")
    money_parser.add_argument("amount", type=int, help="The amount of money to add or remove")
    money_parser.add_argument("-a", "--add", action="store_true", help="Add money to your character's bank account")
    money_parser.add_argument("-r", "--remove", action="store_true",
                              help="Remove money from your character's bank account")
    money_parser.add_argument("-s", "--set", action="store_true", help="Set the amount of money your character has")
    money_parser.add_argument("-p", "--print", action="store_true",
                              help="Print the current amount of money your character has")

    health_parser = cheats_parser.add_parser("health", help="Health cheats")
    health_parser.add_argument("amount", type=float, help="The amount of health to add or remove")
    health_parser.add_argument("-a", "--add", action="store_true", help="Add health to your character's health")
    health_parser.add_argument("-r", "--remove", action="store_true", help="Remove health from your character's health")
    health_parser.add_argument("-s", "--set", action="store_true", help="Set the amount of health your character has")
    health_parser.add_argument("-p", "--print", action="store_true",
                               help="Print the current amount of health your character has")


# Handler for the cheats subparser
def handle_subparser(args) -> None:
    """
    Handles the cheats subparser.
    :param args: The arguments
    """
    save: SaveFile = args.save

    if args.cheats == "money":
        if args.add:
            MoneyCheats.add_money(save, args.amount)
            save.save()
        elif args.remove:
            MoneyCheats.remove_money(save, args.amount)
            save.save()
        elif args.set:
            MoneyCheats.set_money(save, args.amount)
            save.save()
        elif args.print:
            MoneyCheats.print_money(save)
        else:
            logger.error("No action specified. Use -a, -r, -s, or -p.")
    elif args.cheats == "health":
        if args.add:
            HealthCheats.add_health(save, args.amount)
            save.save()
        elif args.remove:
            HealthCheats.remove_health(save, args.amount)
            save.save()
        elif args.set:
            HealthCheats.set_health(save, args.amount)
            save.save()
        elif args.print:
            HealthCheats.print_health(save)
        else:
            logger.error("No action specified. Use -a, -r, -s, or -p.")
    else:
        logger.error("No cheats specified. Use money or health.")
