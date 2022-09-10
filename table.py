import random

import mysql.connector
from flask import Flask, render_template, request, redirect, Blueprint

from classes import transactions

table = Blueprint("table", __name__, static_folder="static", template_folder="templates")

connector = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Test1234*",
    database="transactions"


)

@table.route('/')
def hello_world():  # put application's code here
    cursor = connector.cursor()
    cursor.execute("SELECT * FROM finance_info ORDER BY transaction_date DESC LIMIT 50")

    transactionsList = []

    for record in cursor:
        transactionsObject = transactions(record[0], record[1], record[2], record[3],
                                          record[4], record[5], record[6], record[7])
        transactionsList.append(transactionsObject)

    cursor2 = connector.cursor()
    cursor2.execute("SELECT COUNT(*) FROM finance_info")

    for record in cursor2:
        totalRows = record

    cursor.close()
    cursor2.close()
    connector.commit()

    return render_template("financeTable.html", datalist=transactionsList, title="Financial Transactions",
                           totalVals=totalRows)


@table.route("/expandedTable", methods=["POST"])
def expandedTable():
    cursorAll = connector.cursor()
    cursorHalf = connector.cursor()
    cursorCustom = connector.cursor()
    cursorCounter = connector.cursor()
    cursorTotal = connector.cursor()

    cursorTotal.execute("SELECT COUNT(*) FROM finance_info")
    for record in cursorTotal:
        totalVals = record[0]

    showVals = request.form['showVals']

    valsList = []

    if showVals == "showAll":
        cursorAll.execute("SELECT * FROM finance_info ORDER BY transaction_date")

        for record in cursorAll:
            allObject = transactions(record[0], record[1], record[2], record[3],
                                     record[4], record[5], record[6], record[7])
            valsList.append(allObject)

    elif showVals == "showHalf":
        cursorCounter.execute("SELECT COUNT(*) FROM finance_info ORDER BY transaction_date")

        for record in cursorCounter:
            halfVals = int(record[0]/2)

        cursorHalf.execute('SELECT * FROM finance_info LIMIT ' + str(halfVals))

        for record in cursorHalf:
            halfObject = transactions(record[0], record[1], record[2], record[3],
                                      record[4], record[5], record[6], record[7])
            valsList.append(halfObject)

    else:
        cursorCustom.execute("SELECT * FROM finance_info  ORDER BY transaction_date LIMIT " + showVals)

        for record in cursorCustom:
            customObject = transactions(record[0], record[1], record[2], record[3],
                                        record[4], record[5], record[6], record[7])
            valsList.append(customObject)

    pageTitle = "Showing " + str(len(valsList)) + " records"

    cursorAll.close()
    cursorHalf.close()
    cursorCustom.close()
    cursorCounter.close()
    cursorTotal.close()

    return render_template("expandedTable.html", listOfValues=valsList, title=pageTitle, totalVals=totalVals)


@table.route('/createRecord')
def createRecord():
    return render_template("createRecord.html", title="title")


@table.route('/createRecordRedirect', methods=["POST"])
def createRecordRedirect():
    idCursor = connector.cursor()
    insertCursor = connector.cursor()

    ticker = request.form["ticker"]
    price = request.form['price']
    date = request.form['date']
    type = request.form['type']
    quantity = request.form['quantity']
    number = request.form['number']
    datetime = request.form['datetime']

    def createID():
        randomNumsList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        idPart1 = str(random.choice(randomNumsList))
        idPart2 = str(random.choice(randomNumsList))
        idPart3 = str(random.choice(randomNumsList))
        idPart4 = str(random.choice(randomNumsList))
        idPart5 = str(random.choice(randomNumsList))
        idFinal = int(idPart1 + idPart2 + idPart3 + idPart4 + idPart5)
        return idFinal

    idCursor.execute("select id from finance_info")

    for idVal in idCursor:
        idFinal = createID()
        if idVal == idFinal:
            continue
        else:
            break

    insertCursor.close()
    idCursor.close()
    connector.close()

    insertCursor.execute("""
    insert into finance_info (id, ticker, price, transaction_date, transaction_type, quantity, account_number, create_date)
    values('{idFinal}', '{ticker}', '{price}', '{date}', '{type}', '{quantity}', '{number}', '{datetime}')
    """).format(idFinal=idFinal, ticker=ticker, price=price, date=date, type=type, quantity=quantity, number=number, datetime=datetime)

    return redirect('/table')

# @app.route('/deleteRecord')
# def deleteRecord():
#
#     cursor = connector.cursor()
#
#     formID = request.args.get("id")
#
#     cursor.execute("select * from finance_info where id=" + str(formID))
#
#     for record in cursor:
#         transactionsObject = transactions(record[0], record[1], record[2], record[3],
#                                           record[4], record[5], record[6], record[7])
#
#     cursor.close()
#     connector.commit()
#
#     return render_template("deleteRecord.html", title="Delete a record", deleteRecord=transactionsObject)
#
# @app.route('/deleteRecordRedirect')
# def deleteRecordRedirect():
#     cursor = connector.cursor()
#
#     formID = request.args.get("idinput")
#
#     cursor.execute("delete from finance_info where id=" + str(formID))
#     cursor.close()
#     connector.commit()
#
#     return redirect("/table")


@table.route('/editRecord')
def editRecord():
    cursor = connector.cursor()

    formID = request.args.get("id")

    cursor.execute("select * from finance_info where id=" + str(formID))

    for record in cursor:
        transactionsObject = transactions(record[0], record[1], record[2], record[3],
                                          record[4], record[5], record[6], record[7])

    cursor.close()
    connector.commit()

    return render_template("editRecord.html", title="Edit a record", editRecord=transactionsObject)


@table.route('/editRecordRedirect', methods=["POST"])
def editRecordRedirect():
    cursor = connector.cursor()

    editOrDelete = request.form["editOrDelete"]
    formID = request.form["hiddenID"]
    formTicker = request.form['editTicker']
    formPrice = request.form['editPrice']
    formTransDate = request.form['editTransDate']
    formTransType = request.form['editTransType']
    formQuantity = request.form['editQuantity']
    formAccountNum = request.form['editAccountNum']
    formDateTime = request.form['editCreateDateTime']

    if editOrDelete == "edit":
        editQuery = '''\
            UPDATE finance_info SET ticker="{formTicker}", price="{formPrice}", transaction_date="{formTransDate}",
            transaction_type="{formTransType}", quantity='{formQuantity}', account_number="{formAccountNum}",
            create_date="{formDateTime}" WHERE id="{formID}"
            '''.format(formID=formID, formTicker=formTicker, formPrice=formPrice, formTransDate=formTransDate, formTransType=formTransType,
                       formQuantity=formQuantity, formAccountNum=formAccountNum, formDateTime=formDateTime)
        cursor.execute(editQuery)

    elif editOrDelete == "delete":
        cursor.execute("DELETE FROM finance_info WHERE id=" + str(formID))

    print(formID, formTicker, formPrice, formTransDate, formTransType, formQuantity, formAccountNum, formDateTime)

    return redirect('/table')