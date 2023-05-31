from savefile.savefile import SaveFile

description = "A tool for migrating a character from one save to another."


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

        print("Migrating player...")
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
        print("Migration complete!")

        source_save.locked = original_locked
