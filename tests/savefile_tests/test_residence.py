import unittest

from saveutils.savefile.savefile import SaveFile
from saveutils.tools.residencechanger import ResidenceChanger


class TestResidenceChanger(unittest.TestCase):
    """
    Tests for the SaveFile class.
    """
    save_path = 'test_saves/test.sod'
    default_money = 1000
    cost_excessive = default_money + 1000
    cost_negative = -500
    cost_free = 0
    cost_custom = 50
    original_apartment = 500
    duplicate_apartment = 500
    nonplayer_apartment = 444
    new_apartment = 600
    owned_apartments = [500, 600, 700, 800]

    def setUp(self):
        """
        Note, this is run before every test.
        Large save files can take a while to load, so keep this in mind.
        """
        self.savefile = SaveFile.from_file(self.save_path)
        self.savefile.set_value("residence", self.original_apartment)
        self.savefile.set_value("apartmentsOwned", self.owned_apartments)
        self.savefile.set_value("money", self.default_money)

    def test_initialisation(self):
        """
        Tests that the init, from_file, and from_string initialisation methods work as expected and are equivalent.
        """
        self.assertLess(ResidenceChanger.DEFAULT_COST, self.default_money)
        self.assertGreater(self.cost_excessive, self.default_money)

    def test_cost_excessive(self):
        """
        Tests some methods which get save meta information.
        """
        ResidenceChanger.change_residence(self.savefile, self.new_apartment, self.cost_excessive, skipSave=True)
        self.assertEqual(self.savefile.get_residence(), self.original_apartment)
        self.assertEqual(self.savefile.get_money(), self.default_money)

    def test_cost_negative(self):
        """
        Tests some methods which get save meta information.
        """
        ResidenceChanger.change_residence(self.savefile, self.new_apartment, self.cost_negative, skipSave=True)
        self.assertEqual(self.savefile.get_residence(), self.original_apartment)
        self.assertEqual(self.savefile.get_money(), self.default_money)

    def test_waivefee(self):
        """
        Tests some methods which get save meta information.
        """
        ResidenceChanger.change_residence(self.savefile, self.new_apartment, self.cost_free, skipSave=True)
        self.assertEqual(self.savefile.get_residence(), self.new_apartment)
        self.assertEqual(self.savefile.get_money(), self.default_money)
    
    def test_nonplayerapartment(self):
        """
        Tests some methods which get save meta information.
        """
        ResidenceChanger.change_residence(self.savefile, self.nonplayer_apartment, skipSave=True)
        self.assertEqual(self.savefile.get_residence(), self.original_apartment)
        self.assertEqual(self.savefile.get_money(), self.default_money)
    
    def test_alreadyresidency(self):
        """
        Tests some methods which get save meta information.
        """
        ResidenceChanger.change_residence(self.savefile, self.duplicate_apartment, skipSave=True)
        self.assertEqual(self.savefile.get_residence(), self.duplicate_apartment)
        self.assertEqual(self.savefile.get_money(), self.default_money)

    def test_customfee(self):
        """
        Tests some methods which get save meta information.
        """
        ResidenceChanger.change_residence(self.savefile, self.new_apartment, self.cost_custom, skipSave=True)
        self.assertEqual(self.savefile.get_residence(), self.new_apartment)
        self.assertEqual(self.savefile.get_money(), self.default_money - self.cost_custom)

    def test_default(self):
        """
        Tests some methods which get save meta information.
        """
        ResidenceChanger.change_residence(self.savefile, self.new_apartment, skipSave=True)
        self.assertEqual(self.savefile.get_residence(), self.new_apartment)
        self.assertEqual(self.savefile.get_money(), self.default_money - ResidenceChanger.DEFAULT_COST)