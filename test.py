import unittest

from pymongo import MongoClient

import digital_wallet_methods

MONGODB_URI = "mongodb://admin:admin12345@ds141813.mlab.com:41813/digital_wallet"
client = MongoClient(MONGODB_URI)
db = client.digital_wallet


class MyTest(unittest.TestCase):
    def test_password_check_1(self):
        self.assertTrue(digital_wallet_methods.password_check('romangaev', 'romangaev'))

    def test_password_check_2(self):
        self.assertFalse(digital_wallet_methods.password_check('nonexisting_user', 'nonexisting_password'))

    def test_password_check_3(self):
        self.assertFalse(digital_wallet_methods.password_check(123, 123))

    def test_usetname_check_1(self):
        self.assertFalse(digital_wallet_methods.username_check('ivanivanov'))

    def test_usetname_check_2(self):
        self.assertTrue(digital_wallet_methods.username_check('nonexisting_user'))

    def test_usetname_check_3(self):
        self.assertTrue(digital_wallet_methods.username_check(123))

    def test_create_user(self):
        self.assertTrue(digital_wallet_methods.username_check('new_customer'))
        digital_wallet_methods.create_user('new_customer', 'new_password')
        self.assertFalse(digital_wallet_methods.username_check('new_customer'))
        self.assertTrue(digital_wallet_methods.password_check('new_customer', 'new_password'))

    def test_transfer_money_1(self):
        sender_balance_1 = digital_wallet_methods.get_balance('romangaev', 'romangaev')
        receiver_balance_1 = digital_wallet_methods.get_balance('ivanivanov', 'ivanivanov')
        self.assertTrue(digital_wallet_methods.transfer_money('romangaev', 'ivanivanov', 100, 'romangaev'))
        sender_balance_2 = digital_wallet_methods.get_balance('romangaev', 'romangaev')
        receiver_balance_2 = digital_wallet_methods.get_balance('ivanivanov', 'ivanivanov')
        self.assertTrue((sender_balance_1-sender_balance_2) == 100)
        self.assertTrue((receiver_balance_2-receiver_balance_1) == 100)
    def test_transfer_money_2(self):
        sender_balance_1 = digital_wallet_methods.get_balance('romangaev', 'romangaev')
        receiver_balance_1 = digital_wallet_methods.get_balance('ivanivanov', 'ivanivanov')
        self.assertFalse(digital_wallet_methods.transfer_money('romangaev', 'ivanivanov', 0, 'romangaev'))
        sender_balance_2 = digital_wallet_methods.get_balance('romangaev', 'romangaev')
        receiver_balance_2 = digital_wallet_methods.get_balance('ivanivanov', 'ivanivanov')
        self.assertEqual(sender_balance_1,sender_balance_2)
        self.assertEqual(receiver_balance_2,receiver_balance_1)
    def test_transfer_money_3(self):
        sender_balance_1 = digital_wallet_methods.get_balance('romangaev', 'romangaev')
        receiver_balance_1 = digital_wallet_methods.get_balance('ivanivanov', 'ivanivanov')
        self.assertFalse(digital_wallet_methods.transfer_money('romangaev', 'ivanivanov', -100, 'romangaev'))
        sender_balance_2 = digital_wallet_methods.get_balance('romangaev', 'romangaev')
        receiver_balance_2 = digital_wallet_methods.get_balance('ivanivanov', 'ivanivanov')
        self.assertEqual(sender_balance_1,sender_balance_2)
        self.assertEqual(receiver_balance_2,receiver_balance_1)

    def test_top_up(self):
        balance_1 = digital_wallet_methods.get_balance('romangaev', 'romangaev')
        digital_wallet_methods.top_up('romangaev', 500)
        balance_2 = digital_wallet_methods.get_balance('romangaev', 'romangaev')
        self.assertEqual(balance_2-balance_1, 500)
    def test_withdraw(self):
        balance_1 = digital_wallet_methods.get_balance('romangaev', 'romangaev')
        digital_wallet_methods.withdraw('romangaev', 500)
        balance_2 = digital_wallet_methods.get_balance('romangaev', 'romangaev')
        self.assertEqual(balance_1 - balance_2, 500)


if __name__ == "__main__":
    unittest.main()