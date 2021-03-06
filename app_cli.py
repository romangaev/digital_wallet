'''
Тестовое задание Сбербанк
Имитация электронного кошелька
Разработчик: Роман Гаев

Условие:
    -Реализовать сервис электронного кошелька. Из обязательного функционала только перевод денег между пользователями.
    -Дополнительно условие: нельзя перевести пользователю деньги если на его счету больше чем N средств.
    -Достаточно работы сервиса из консоли без GUI клиента.
    -Предпочтительна реализация на чистом Python либо с минимальным использования фреймворков.
    -Мы будем рады увидеть покрытие кода тестами, модульность, возможность конфигурировать проект, логирование и мониторинг.
    -Мы бы хотели чтобы при реализации вы подумали над масштабируемостью и отказоустойчивостью проекта.​

Дополнительные комментарии:
    -Сервис использует стандартный cmd framework для работы интерфейса командной строки.
Ограничения сервиса:
    -Сервис не использует шифрования данных
    -Для удобства и быстроты развертывания и демонстрации сервис был построен на NoSQL базе данных, предпочтительна SQL
'''
import cmd
import sys

from Bank import Bank

import logging

logging.basicConfig(filename="sample.log", level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class Cli(cmd.Cmd):

    def __init__(self, bank):
        #Инициализация командной строки
        cmd.Cmd.__init__(self)
        self.bank = bank
        self.prompt = "> "
        self.intro = "Добро пожаловать в Электронный Кошелёк!\nДля справки наберите 'help'"
        self.doc_header = "Доступные команды (для справки по конкретной команде наберите 'help _команда_')"
        logging.info('CLI has started')

    def do_login(self, args):
        """login - вход в аккаунт"""
        try:
            logging.info("Opened login dialog")
            username = input("Введите ваш логин:")
            password = input("Введите пароль:")

            # авторизация пользователя и запуск интерфейса аккаунта при успешной авторизации
            if bank.password_check(username, password):
                print("Успешный вход")
                bank.account_routine(username)
                logging.info("Successfully logged in")
            else:
                print("Неверный логин/пароль!")
                logging.error("Login error")
        except Exception:
            print("Ошибка ввода!")
            logging.error("Login error")

    def do_sign_up(self, args):
        """sign up - регистрация пользователя"""
        try:
            logging.info("Opened sign up dialog")
            username = input("Создайте логин:")
            if not bank.username_check(username):
                raise ValueError
            password = input("Создайте пароль:")
            bank.create_user(username, password)
            print("Вы были успешно зарегистрированы в системе!")
            logging.info("Successfully signed up")
        except ValueError:
            print("К сожалению, это имя уже занято. Пофантазируйте еще немного.")
            logging.error("Sign up error")

    def do_exit(self, line):
        """exit - выход из программы"""
        print("До скорой встречи")
        logging.info("Application terminated")
        sys.exit()


if __name__ == "__main__":
    bank = Bank()
    cli = Cli(bank)
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("завершение сеанса...")
        logging.info("Application terminated")
