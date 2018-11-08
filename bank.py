'''
Данный модуль содержит в себе методы для доступа к аккаунту и операции с БД
Автор: Роман Гаев
'''

import logging
from account import Account
from transaction import Transaction

logging.basicConfig(filename="sample.log", level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# BALANCE_LIMIT - максимальное количество средств N при котором возможен перевод (по условию задания)
# INIT_BALANCE - начальный баланс при регистрации нового пользователя
BALANCE_LIMIT = 100000
INIT_BALANCE = 0


class Bank:

    def __init__(self):
        self.user_accounts = {}
        self.transactions = {}

    def account_routine(self, username):
        # Метод запуска интерфейса личного кабинета аккаунт

        account = self.user_accounts[username]
        while True:
                logging.info("Starting account routine...")
                answer = int(
                    input("\n1-Трансфер средств\n2-Баланс\n3-Внести средства\n4-Снять средства\n5-Выход из аккаунта\n"))
                if answer == 1:
                    logging.info("Entering transfer dialog...")
                    password = input("Подтвердите паролем:")
                    receiver = input("Введите логин получателя:")
                    amount = int(input("Введите сумму перевода:"))
                    self.transfer_money(username, receiver, amount, password)

                elif answer == 2:
                    logging.info("Entering balance dialog...")
                    password = input("Подтвердите паролем:")
                    print("Ваш баланс:")
                    print(account.get_balance(username, password))

                elif answer == 3:
                    logging.info("Entering top up...")
                    amount = int(input("Введите сумму:"))
                    account.top_up(username, amount)
                elif answer == 4:
                    logging.info("Entering withdrawal...")
                    amount = int(input("Введите сумму:"))
                    account.withdraw(username, amount)
                elif answer == 5:
                    logging.info("Leaving the account..")
                    break
                else:
                    logging.error("Wrong number...")
                    print("Используйте цифры для выбора функций")

    def password_check(self, username, password):
        # Авторизация и проверка пароля пользователя
        logging.error("Checking password...")
        for v in self.user_accounts.values():
            if v.username == username:
                if v.password == password:
                    return True
        return False

    def username_check(self, username):
        # Проверка занятости логина в базе данных
        logging.info("Checking name availability")
        for v in self.user_accounts.values():
            if v.username == username:
                return False
        return True

    def create_user(self, username, password):
        # Создание нового пользователя в БД
        self.user_accounts[username] = Account(username, password)
        logging.info("User has been created.")

    def transfer_money(self, sender, receiver, amount, password):
        # Перевод средств по логину получател
            logging.info("Starting money transfer process.")
            sender = self.user_accounts[sender]
            receiver = self.user_accounts[receiver]

            # Выброс исключения при отсутствии получателя с таким именем в базе
            if receiver is None:
                print("Ошибка.Пользователь с таким именем не существует!")
                logging.error("No such user")
                return False

            # Выброс исключения при отсутствии средств для перевода
            elif amount > sender.balance or amount <= 0:
                print("Ошибка.Недостаточно средств либо вы ввели неположительную сумму!")
                logging.error("Low balance/wrong amount")
                return False

            # Выброс исключения при превышении баланса(условие задания)
            elif receiver.balance > BALANCE_LIMIT:
                print("Ошибка. Баланс получателя превышает допустимый лимит в %d!" % BALANCE_LIMIT)
                logging.error("Balance limit")
                return False

            # Выброс исключения при неверном пароле подтверждения
            print (self.password_check(sender.username, password))
            if not self.password_check(sender.username, password):
                print("Ошибка. Неверный пароль!")
                logging.error("Wrong password")
                return False

            sender.withdraw(amount)
            receiver.top_up(amount)

            new_trans_id = self.transactions.__len__()+1
            self.transactions[new_trans_id] = Transaction(new_trans_id,sender,receiver,'TRANSFER', amount)
            print("Транзакция прошла успешно")
            return True








