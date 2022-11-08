# Hi David. Ich wusste nicht wie Du die GUI gerne haben möchtest also habe ich wieder zwei verschiedene Methoden angewendet. Ich könnte jeweils die verschiedenen
# Daten eintragen, aber da wollte ich auch nochmal fragen, wo ich am besten die "echten" Namen speichere. Wenn ich einen File mit den PID-Daten hochladen soll,
# dann muss ich auch die Original Daten irgendwo sichern, oder? 
# Ich wollte auch nochmal fragen, ob ich die Werte/Daten aus Deiner Tabelle verwenden kann, weil ich nicht sicher bin, ob ich alle Arztbriefe habe. 

import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("PID.ui", self)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(7, 150)
        self.tableWidget.setColumnWidth(8, 150)
        self.loaddata()

    def loaddata(self):
        print(os.path.join("mnt/c/Users/Anwender/PycharmProjects/pythonProject", "PID.csv"))
        patients = pd.read_csv("PID.csv", sep=';')
        print(patients)

        row = 0
        self.tableWidget.setRowCount(len(patients))
        for patient in patients:
            content = {
                "PID": [1, 1],

            }

        for key, value in content.items():
            print(key, '->', value[1])
            self.tableWidget.setItem(row, value[1], QtWidgets.QTableWidgetItem(key))
            row = row + 1


# main
app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedHeight(850)
widget.setFixedWidth(1500)
widget.show()
sys.exit(app.exec_())
