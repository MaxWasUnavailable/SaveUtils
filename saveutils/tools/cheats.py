from savefile.savefile import SaveFile

description = "A collection of save game editing methods which can be considered cheats."


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
        print(f"Set money to {amount}")

    @staticmethod
    def add_money(save: SaveFile, amount: int):
        """
        Adds money to the player's current amount.
        """
        save.safe_set_value("money", save.get_value("money") + amount)
        current_money = save.get_money()
        print(f"Added {amount} to money. Current money: {current_money}")

    @staticmethod
    def remove_money(save: SaveFile, amount: int):
        """
        Removes money from the player's current amount.
        """
        MoneyCheats.set_money(save, save.get_value("money") - amount)
        current_money = save.get_money()
        print(f"Removed {amount} from money. Current money: {current_money}")

    @staticmethod
    def print_money(save: SaveFile):
        """
        Prints the player's current amount of money.
        """
        current_money = save.get_money()
        print(f"Current money: {current_money}")


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
        print(f"Set health to {amount}")

    @staticmethod
    def add_health(save: SaveFile, amount: int):
        """
        Adds health to the player's current amount.
        """
        HealthCheats.set_health(save, save.get_value("health") + amount)
        current_health = save.get_health()
        print(f"Added {amount} to health. Current health: {current_health}")

    @staticmethod
    def remove_health(save: SaveFile, amount: int):
        """
        Removes health from the player's current amount.
        """
        HealthCheats.set_health(save, save.get_value("health") - amount)
        current_health = save.get_health()
        print(f"Removed {amount} from health. Current health: {current_health}")

    @staticmethod
    def print_health(save: SaveFile):
        """
        Prints the player's current amount of health.
        """
        current_health = save.get_health()
        print(f"Current health: {current_health}")
