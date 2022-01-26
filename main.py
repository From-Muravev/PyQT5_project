import sqlite3
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import gui
from random import *


class MainClass(QDialog, gui.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_load.clicked.connect(self.loadDB)
        self.pushButton_add.clicked.connect(self.addData)
        self.pushButton_delete.clicked.connect(self.DeleteData)
        self.pushButton_update.clicked.connect(self.updateData)
        self.tableWidget.cellDoubleClicked.connect(self.selectedCell)
        self.btn.clicked.connect(self.pswd_gen)

        self.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    def loadDB(self):
        con = sqlite3.connect("users.db")
        mouse = con.cursor()
        query = "SELECT id, site, login, password FROM users"
        mouse.execute(query)
        result = mouse.fetchall()
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        con.close()

    def addData(self):
        con = sqlite3.connect("users.db")
        mouse = con.cursor()
        ID = self.lineEdit_id.text()
        login = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        site = self.lineEdit_site.text()

        insertq = """INSERT INTO users 
                  (id, site, login, password) 
                  VALUES (?, ?, ?, ?);"""
        values = [int(ID), site, login, password]
        try:
            mouse.execute(insertq, values)
            con.commit()
            con.close()
            print("Success")
        except:
            print("failed")

    def DeleteData(self):
        con = sqlite3.connect("users.db")
        mouse = con.cursor()
        ID = self.lineEdit_id.text()
        site = self.lineEdit_site.text()
        deleteq = "DELETE FROM users WHERE id = ? AND site = ?"
        values = (ID, site)
        try:
            mouse.execute(deleteq, values)
            con.commit()
            con.close()
            print("Success")
        except:
            print("failed")

    def updateData(self):
        con = sqlite3.connect("users.db")
        mouse = con.cursor()
        ID = self.lineEdit_id.text()
        login = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        site = self.lineEdit_site.text()
        updateq = "UPDATE users SET login = ?, password = ?, site = ? WHERE id = ?"
        values = (login, password, site, ID)

        try:
            mouse.execute(updateq, values)
            con.commit()
            con.close()
            print("Success")
        except:
            print("failed")

    def selectedCell(self):
        con = sqlite3.connect("users.db")
        mouse = con.cursor()
        self.index = self.tableWidget.selectedItems()

        query = "SELECT ID, site, login, password FROM users WHERE ID = ?"
        value = (self.index[0].text(),)
        mouse.execute(query, value)
        row = mouse.fetchone()

        if row:
            self.lineEdit_id.setText(str(row[0]))
            self.lineEdit_login.setText(row[2])
            self.lineEdit_password.setText(row[3])
            self.lineEdit_site.setText(row[1])

    def len_exceeded(self, s, length_of_pswd):
        if len(s) >= length_of_pswd:
            return True
        return False

    def pswd_gen(self):
        length_of_pswd = randint(8, 16)
        sm = "abcdefghijklmnopqrstuvwxyz"
        cap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num = "0123456789"
        sp_char = "$@#^&."
        pswd = ""
        while (len(pswd) < length_of_pswd):
            ran_num = randint(0, 25)
            pswd += sm[ran_num]
            if self.len_exceeded(pswd, length_of_pswd): break

            ran_num = randint(0, 25)
            pswd += cap[ran_num]
            if self.len_exceeded(pswd, length_of_pswd): break

            ran_num %= 10
            pswd += num[ran_num]
            if self.len_exceeded(pswd, length_of_pswd): break

            ran_num %= 6
            pswd += sp_char[ran_num]

        strng_pswd = list(pswd)
        shuffle(strng_pswd)
        self.ans = "".join(strng_pswd)
        self.lineEdit_password.setText(str(self.ans))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ims = MainClass()
    ims.show()
    app.exec_()
