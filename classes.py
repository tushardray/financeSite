class transactions:
    def __init__(self, idNum, ticker, price, transaction_date, transaction_type, quantity, account_number, create_date):
        self.__id = idNum
        self.__ticker = ticker
        self.__price = price
        self.__transaction_date = transaction_date
        self.__transaction_type = transaction_type
        self.__quantity = quantity
        self.__account_number = account_number
        self.__create_date = create_date

# GET CLASSES

    def getID(self):
        return self.__id

    def getTicker(self):
        return self.__ticker

    def getPrice(self):
        return self.__price

    def getTransDate(self):
        return self.__transaction_date

    def getTransType(self):
        return self.__transaction_type

    def getQuantity(self):
        return self.__quantity

    def getAccountNumber(self):
        return self.__account_number

    def getCreateDate(self):
        return self.__create_date





# class homeTable:
#     def __init__(self):
