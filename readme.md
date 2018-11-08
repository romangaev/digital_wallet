
## Электронный кошелек

### Запуск 
Для работы сервиса необходимо запустить стартовый скрипт приложения app_cli.py

### Описание содержимого:
* digital_wallet/app_cli.py - стартовый скрипт для запуска интерфейса командной строки
* digital_wallet/bank.py - модуль с основной логикой приложения и словарями имитирующими базу данных аккаунтов и транзакций
* digital_wallet/account.py - класс представляющий собой аккаунт(операции с аккаунтом синхронизированы)
* digital_wallet/transaction.py - класс транзакции
* digital_wallet/test.py - Unit тесты приложения

### Основные функиции
* Возможно пополнение баланса и снятие средств
* Возможен вход и выход из аккаунта, а также создание нового аккаунта
* Возможен перевод денег между пользователями
* Сервис работает из консоли. Для консольного интерфейса был использован стандартный python framework cmd
* Нельзя перевести пользователю деньги если на его счету больше чем N средств. N по умолчанию BALANCE_LIMIT = 100000
* Хранение данных пользователей осуществляется в NoSQL базе данных на базе сервиса mLab

### Ограничения сервиса
* Сервис не использует шифрования данных
* Для удобства и быстроты развертывания и демонстрации сервис был построен на NoSQL базе данных, в будущем предпочтительна SQL

### Python version
Python 3.6.3
