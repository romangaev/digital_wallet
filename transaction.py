import threading


class Transaction:
    def __init__(self, trans_id, sender, receiver, type, amount):
        self.trans_id = trans_id
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.amount = amount
        self.lock = threading.RLock()
