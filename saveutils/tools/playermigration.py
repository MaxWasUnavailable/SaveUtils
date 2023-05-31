from logging import getLogger, StreamHandler, Formatter

from savefile.savefile import SaveFile
from tools.cheats import MoneyCheats

description = "A tool for migrating a character from one save to another."

logger = getLogger(__name__)
logger.setLevel("INFO")
handler = StreamHandler()
handler.setFormatter(Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s"))
logger.addHandler(handler)


class PlayerMigration:
    """
    A tool for migrating a character from one save to another.
    """

    @staticmethod
    def migrate_player(source_save: SaveFile, target_save: SaveFile):
        """
        Migrates the player from one save to another.
        """
        original_locked = source_save.locked
        source_save.locked = True

        logger.info("Migrating player...")
        migration_data = dict()

        # First move character-specific data
        migration_data["playerFirstName"] = source_save.get_player_firstname()
        migration_data["playerSurname"] = source_save.get_player_surname()
        migration_data["playerGender"] = source_save.get_player_gender()
        migration_data["playerSkinColour"] = source_save.get_value("playerSkinColour")
        migration_data["playerBirthDay"] = source_save.get_value("playerBirthDay")
        migration_data["playerBirthMonth"] = source_save.get_value("playerBirthMonth")
        migration_data["playerBirthYear"] = source_save.get_value("playerBirthYear")
        migration_data["money"] = source_save.get_money()
        migration_data["lockpicks"] = source_save.get_lockpicks()
        migration_data["socCredit"] = source_save.get_social_credit()
        migration_data["health"] = source_save.get_health()
        migration_data["upgrades"] = source_save.get_upgrades()
        migration_data["booksRead"] = source_save.get_books_read()

        # Then move inventory data
        # First, we grab the list of interactable IDs from the target save
        interactable_ids = [interactable["id"] for interactable in target_save.get_value("interactables")]
        max_interactable_id = max(interactable_ids)

        # Then, we grab the inventory data from the source save
        migration_data["firstPersonItems"] = source_save.get_items()

        # Then, we grab the original interactables from the source save
        original_interactables = []

        for item in migration_data["firstPersonItems"]:
            interactable_id = item["interactableID"]
            if interactable_id == -1:
                # If the interactable ID is -1, we skip it
                continue

            original_interactables.append([interactable for interactable in source_save.get_value("interactables") if
                                           interactable["id"] == interactable_id][0])
            if interactable_id in interactable_ids:
                # If the interactable ID is already in use, we generate a new one
                # We do this by adding 10 to the highest interactable ID in the target save (to be extra safe)
                new_interactable_id = max_interactable_id + 10
                item["interactableID"] = new_interactable_id
                original_interactables[-1]["id"] = new_interactable_id
                max_interactable_id = new_interactable_id

            interactable_ids.append(interactable_id)

        # Then, we add the interactables to the target save. This is handled separately from the main migration loop
        # since this needs to be merged rather than overwritten.
        target_save.safe_set_value("interactables", target_save.get_value("interactables") + original_interactables)

        # To wrap things up, we move relevant meta save data
        migration_data["jobDiffLevel"] = source_save.get_value("jobDiffLevel")

        for key, value in migration_data.items():
            target_save.safe_set_value(key, value)

        # Then, we save the target save
        target_save.save()
        logger.info("Migration complete!")

        source_save.locked = original_locked

    @staticmethod
    def new_game_plus(source_save: SaveFile, target_save: SaveFile, travel_expenses: int = 20000):
        """
        Migrates the player, but only if they can afford the "travel expenses".

        Will sell all apartments for a flat 2k fee.
        """
        logger.info("Migrating to new game plus...")
        apartment_count = len(source_save.get_apartments_owned())

        total_worth = source_save.get_money() + (apartment_count * 2000)

        if total_worth < travel_expenses:
            logger.info(
                f"Player cannot afford travel expenses. Required: {travel_expenses}, Available (with apartment sales): {total_worth}")
            return

        new_money = total_worth - travel_expenses

        logger.info(
            f"Player can afford travel expenses. Required: {travel_expenses}, Available (with apartment sales): {total_worth}, New money: {new_money}")

        old_money = source_save.get_money()
        MoneyCheats.set_money(source_save, new_money)

        PlayerMigration.migrate_player(source_save, target_save)

        MoneyCheats.set_money(source_save, old_money)


def register_subparser(main_subparser) -> None:
    """
    Registers the player migration subparser.
    :param main_subparser: The main parser's subparser
    """
    migration_parser = main_subparser.add_parser("migrate", help=description, description=description)
    migration_parser.add_argument('-o', '--output', type=str, required=True, help="The output save file.")
    migration_parser.add_argument('-n', '--newgameplus', action="store_true",
                                  help="Whether to migrate the player using the new game plus system.")
    migration_parser.add_argument('-t', '--travelexpenses', type=int, default=20000,
                                  help="The travel expenses required for new game plus.")


def handle_subparser(args) -> None:
    """
    Handles the player migration subparser.
    :param args: The arguments
    """
    if args.tool == "migrate":
        source_save = args.save
        target_save = SaveFile(args.output, args.verbose)

        if args.newgameplus:
            PlayerMigration.new_game_plus(source_save, target_save, args.travelexpenses)
        else:
            PlayerMigration.migrate_player(source_save, target_save)
