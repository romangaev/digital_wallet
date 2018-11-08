import unittest

from bank import Bank

bank = Bank()
bank.create_user('romangaev', 'romangaev')
bank.create_user('ivanivanov', 'ivanivanov')


class MyTest(unittest.TestCase):

    def test_password_check_1(self):
        self.assertTrue(bank.password_check('romangaev', 'romangaev'))

    def test_password_check_2(self):
        self.assertFalse(bank.password_check('nonexisting_user', 'nonexisting_password'))

    def test_password_check_3(self):
        self.assertFalse(bank.password_check(123, 123))

    def test_username_check_1(self):
        self.assertFalse(bank.username_check('ivanivanov'))

    def test_username_check_2(self):
        self.assertTrue(bank.username_check('nonexisting_user'))

    def test_username_check_3(self):
        self.assertTrue(bank.username_check(123))

    def test_create_user(self):
        self.assertTrue(bank.username_check('new_customer'))
        bank.create_user('new_customer', 'new_password')
        self.assertFalse(bank.username_check('new_customer'))
        self.assertTrue(bank.password_check('new_customer', 'new_password'))

    def test_top_up(self):
        account = bank.user_accounts['romangaev']
        balance_1 = account.get_balance()
        account.top_up(10000)
        balance_2 = account.get_balance()
        self.assertEqual(balance_2 - balance_1, 10000)

    def test_transfer_money_1(self):
        account1 = bank.user_accounts['romangaev']
        account2 = bank.user_accounts['ivanivanov']
        sender_balance_1 = account1.get_balance()
        receiver_balance_1 = account2.get_balance()
        self.assertTrue(bank.transfer_money('romangaev', 'ivanivanov', 100, 'romangaev'))
        sender_balance_2 = account1.get_balance()
        receiver_balance_2 = account2.get_balance()
        self.assertTrue((sender_balance_1 - sender_balance_2) == 100)
        self.assertTrue((receiver_balance_2 - receiver_balance_1) == 100)

    def test_transfer_money_2(self):
        account1 = bank.user_accounts['romangaev']
        account2 = bank.user_accounts['ivanivanov']
        sender_balance_1 = account1.get_balance()
        receiver_balance_1 = account2.get_balance()
        self.assertFalse(bank.transfer_money('romangaev', 'ivanivanov', 0, 'romangaev'))
        sender_balance_2 = account1.get_balance()
        receiver_balance_2 = account2.get_balance()
        self.assertEqual(sender_balance_1, sender_balance_2)
        self.assertEqual(receiver_balance_2, receiver_balance_1)

    def test_transfer_money_3(self):
        account1 = bank.user_accounts['romangaev']
        account2 = bank.user_accounts['ivanivanov']
        sender_balance_1 = account1.get_balance()
        receiver_balance_1 = account2.get_balance()
        self.assertFalse(bank.transfer_money('romangaev', 'ivanivanov', -100, 'romangaev'))
        sender_balance_2 = account1.get_balance()
        receiver_balance_2 = account2.get_balance()
        self.assertEqual(sender_balance_1, sender_balance_2)
        self.assertEqual(receiver_balance_2, receiver_balance_1)


    def test_withdraw(self):
        account = bank.user_accounts['romangaev']
        balance_1 = account.get_balance()
        account.withdraw(500)
        balance_2 = account.get_balance()
        self.assertEqual(balance_1 - balance_2, 500)


if __name__ == "__main__":
    unittest.main()
