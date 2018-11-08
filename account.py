import threading
import logging


class Account:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.balance = 0

        # блокировка доступа к аккаунту на время операций
        self.lock = threading.Lock()

    def top_up(self, amount):
        # Пополнение счета
        self.lock.acquire()
        try:
            if amount <= 0:
                raise ValueError
            self.balance = self.balance + amount
            print("Вы успешно пополнили ваш счет")
        except ValueError:
            print("Ошибка.Вы ввели неположительную сумму!")
            logging.error("Incorrect amount")
        finally:
            self.lock.release()

    def withdraw(self, amount):
        # Снятие средств
        self.lock.acquire()
        try:
            # Выброс исключения при отсутствии средств для перевода
            if amount > self.balance or amount <= 0:
                raise AttributeError
            self.balance = self.balance - amount
            print("Вы успешно сняли средства")
        except AttributeError:
            print("Ошибка.Вы ввели неположительную сумму!")
            logging.error("Incorrect amount or insufficient funds")
        finally:
            self.lock.release()

    def get_balance(self):
        # Запрос баланса
        return self.balance
