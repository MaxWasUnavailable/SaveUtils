import unittest

from saveutils.savefile.savefile import SaveFile


class TestSaveFile(unittest.TestCase):
    """
    Tests for the SaveFile class.
    """
    save_path = './test_saves/test.sod'

    def setUp(self):
        """
        Note, this is run before every test.
        Large save files can take a while to load, so keep this in mind.
        """
        self.savefile = SaveFile.from_file(self.save_path)

    def test_initialisation(self):
        """
        Tests that the init, from_file, and from_string initialisation methods work as expected and are equivalent.
        """
        save_file = open(self.save_path, 'r', encoding='utf-8')
        save_string = save_file.read()
        save_file.close()

        savefile_from_init = SaveFile(self.save_path)
        savefile_from_file = SaveFile.from_file(self.save_path)
        savefile_from_string = SaveFile.from_string(save_string)

        self.assertIsNotNone(savefile_from_init.data)
        self.assertIsNotNone(savefile_from_init.get_build())

        self.assertEqual(savefile_from_init.data, savefile_from_file.data)
        self.assertEqual(savefile_from_init.data, savefile_from_string.data)

    def test_get_save_info(self):
        """
        Tests some methods which get save meta information.
        """
        self.assertEqual(self.savefile.get_build(), '33.19')
        self.assertEqual(self.savefile.get_cityshare(), "Test City.0.3319.YQ5DzKtQP5s00vzs")
        self.assertEqual(self.savefile.get_seed(), self.savefile.get_cityshare())

    def test_get_player_info(self):
        """
        Tests some methods which get player information.
        """
        self.assertEqual(self.savefile.get_player_firstname(), 'Test')
        self.assertEqual(self.savefile.get_player_surname(), 'Tester')
        self.assertEqual(self.savefile.get_player_birthday(), [19, 12, 1947])
        self.assertEqual(self.savefile.is_crouched(), False)
        self.assertEqual(len(self.savefile.get_apartments_owned()), 0)
        self.assertEqual(len(self.savefile.get_active_cases()), 0)

    def test_get_city_info(self):
        """
        Tests some methods which get city information.
        """
        self.assertEqual(len(self.savefile.get_murders()), 1)
        self.assertEqual(len(self.savefile.get_citizens()), 278)
