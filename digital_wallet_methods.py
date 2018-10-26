'''
Данный модуль содержит в себе методы для доступа к аккаунту и операции с БД
Автор: Роман Гаев
'''

from pymongo import MongoClient
import logging

logging.basicConfig(filename="sample.log", level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# BALANCE_LIMIT - максимальное количество средств N при котором возможен перевод (по условию задания)
# INIT_BALANCE - начальный баланс при регистрации нового пользователя
BALANCE_LIMIT = 100000
INIT_BALANCE = 0

# Данные для авторизации в БД
MONGODB_URI = "mongodb://admin:admin12345@ds141813.mlab.com:41813/digital_wallet"
client = MongoClient(MONGODB_URI)
db = client.digital_wallet


def account_routine(username):
    '''Метод запуска интерфейса личного кабинета аккаунта'''
    while True:
        try:
            logging.info("Starting account routine...")
            answer = int(
                input("\n1-Трансфер средств\n2-Баланс\n3-Внести средства\n4-Снять средства\n5-Выход из аккаунта\n"))
            if answer == 1:
                logging.info("Entering transfer dialog...")
                password = input("Подтвердите паролем:")
                receiver = input("Введите логин получателя:")
                amount = int(input("Введите сумму перевода:"))
                transfer_money(username,receiver,amount,password)

            elif answer == 2:
                logging.info("Entering balance dialog...")
                password = input("Подтвердите паролем:")
                print("Ваш баланс:")
                print(get_balance(username, password))

            elif answer == 3:
                logging.info("Entering top up...")
                amount = int(input("Введите сумму:"))
                top_up(username, amount)
            elif answer == 4:
                logging.info("Entering withdrawal...")
                amount = int(input("Введите сумму:"))
                withdraw(username,amount)
            elif answer == 5:
                logging.info("Leaving the account..")
                break
            else:
                logging.error("Wrong number...")
                print("Используйте цифры для выбора функций")
        except Exception:
            print("Ошибка ввода!")
            logging.error("IO exception...")


def password_check(username, password):
    '''Авторизация и проверка пароля пользователя'''
    logging.error("Checking password...")
    query = db.user_accounts.find_one({'username': username})
    if query is None:
        logging.error("Couldn't find the user")
        return False
    if query["password"] == password:
        logging.info("Password matches.")
        return True
    return False


def username_check(username):
    '''Проверка занятости логина в базе данных'''
    logging.info("Checking name availability")
    if db.user_accounts.find_one({'username': username}) is None:
        return True
    return False


def create_user(username, password):
    '''Создание нового пользователя в БД'''
    db.user_accounts.insert_one({'username': username, 'password': password, 'balance': INIT_BALANCE})
    logging.info("User has been created.")


def transfer_money(sender,receiver,amount,password):
    '''Перевод средств по логину получателя'''
    try:
        logging.info("Starting money transfer process.")
        receiver_query = db.user_accounts.find_one({'username': receiver})
        sender_query = db.user_accounts.find_one({'username': sender})

        # Выброс исключения при отсутствии получателя с таким именем в базе
        if receiver_query is None:
            raise ValueError

        # Выброс исключения при отсутствии средств для перевода
        elif amount > sender_query['balance'] or amount <= 0:
            raise AttributeError

        # Выброс исключения при превышении баланса(условие задания)
        elif receiver_query["balance"] > BALANCE_LIMIT:
            raise Exception

        # Выброс исключения при неверном пароле подтверждения
        if not password_check(sender, password):
            raise PermissionError

        db.user_accounts.update_one({'username': sender}, {'$inc': {'balance': -amount}}, upsert=False)
        db.user_accounts.update_one({'username': receiver}, {'$inc': {'balance': amount}}, upsert=False)
        db.transactions.insert_one({'type': 'TRANSFER','sender': sender, 'receiver': receiver, 'amount': amount})

        print("Транзакция прошла успешно")
        return True

    except PermissionError:
        print("Ошибка. Неверный пароль!")
        logging.error("Wrong password")
        return False
    except AttributeError:
        print("Ошибка.Недостаточно средств либо вы ввели неположительную сумму!")
        logging.error("Low balance/wrong amount")
        return False
    except ValueError:
        print("Ошибка.Пользователь с таким именем не существует!")
        logging.error("No such user")
        return False
    except Exception:
        print("Ошибка. Баланс получателя превышает допустимый лимит в %d!" % BALANCE_LIMIT)
        logging.error("Balance limit")
        return False


def get_balance(username, password):
    '''Запрос баланса'''
    try:
        if not password_check(username, password):
            raise PermissionError
        return db.user_accounts.find_one({'username': username})["balance"]
    except PermissionError:
        print("Ошибка. Неверный пароль!")
        logging.error("Wrong password")
        return False


def top_up(username, amount):
    '''Пополнение счета'''
    try:
        user_query = db.user_accounts.find_one({'username': username})
        # Выброс исключения при отсутствии средств для перевода
        if  amount <= 0:
            raise AttributeError
        db.user_accounts.update_one({'username': username}, {'$inc': {'balance': amount}}, upsert=False)
        db.transactions.insert_one({'type': 'TOP_UP', 'username': username, 'amount': amount})
        print("Вы успешно пополнили ваш счет")
    except AttributeError:
        print("Ошибка.Вы ввели неположительную сумму!")
        logging.error("Incorrect amount")


def withdraw(username, amount):
    '''Снятие средств'''
    try:
        user_query = db.user_accounts.find_one({'username': username})
        # Выброс исключения при отсутствии средств для перевода
        if amount > user_query['balance'] or amount <= 0:
            raise AttributeError
        db.user_accounts.update_one({'username': username}, {'$inc': {'balance': -amount}}, upsert=False)
        db.transactions.insert_one({'type': 'WITHDRAWAL', 'username': username, 'amount': amount})
        print("Вы успешно сняли средства")
    except AttributeError:
        print("Ошибка.Вы ввели неположительную сумму!")
        logging.error("Incorrect amount or unsufficient funds")