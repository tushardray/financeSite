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

    # for record in cursorPositions:
    #     idVal = int(record[0])
    #     # print(idVal)
    #
    #     quantityINT = int(record[1])
    #     # print(quantityINT)
    #
    #     originalPriceFLO = record[2]
    #     # print(originalPriceFLO)
    #     priceFLO = float(record[2][1:])
    #     # print(priceFLO)
    #
    #     multipliedVal = quantityINT * priceFLO
    #     # print(multipliedVal)
    #
    #     singlePos = [idVal, multipliedVal]
    #
    #     positions.append(singlePos)
    #
    # print(positions)
    #
    # for i in positions:
    #     topValString = """
    #         INSERT INTO top_vals (id, multiplied)
    #         VALUES ('{id}', '{multiplied}')
    #         """.format(id=positions[i][0], multiplied=positions[i][1])
    #
    #     cursorTopVals.execute(topValString)
    #
    # cursorPositions.close()
    # cursorTopVals.close()
    #
    # connector.commit()
    # connector.close()

    return render_template("home.html", title="Home", dataList=transactionsList)




if __name__ == '__main__':
    app.run()
