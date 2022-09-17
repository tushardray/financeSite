import mysql.connector
from flask import Flask, render_template

from table import table
from classes import transactions

connector = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Test1234*",
    database="transactions"
)

app = Flask(__name__)
app.register_blueprint(table, url_prefix="/table")


@app.route('/')
def home():
    cursorPositions = connector.cursor()
    cursorTopVals = connector.cursor()

    cursorPositions.execute("SELECT * FROM finance_info ORDER BY quantity DESC LIMIT 10")

    transactionsList = []

    for record in cursorPositions:
        transactionsObject = transactions(record[0], record[1], record[2], record[3],
                                          record[4], record[5], record[6], record[7])
        transactionsList.append(transactionsObject)

    idVal = 0
    quantityINT = 0
    priceFLO = 0

    positions = []

    return render_template("home.html", title="Home", dataList=transactionsList)




if __name__ == '__main__':
    app.run()
