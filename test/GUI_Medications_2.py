# Hallo David. Ich war mir nicht ganz sicher wie genau Du die GUI haben möchtest, daher hab ich einfach mal zwei verschiedene Ansätze verwendet.

import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("DBS_Medication.ui", self)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(7, 150)
        self.tableWidget.setColumnWidth(8, 150)
        self.loaddata()

    def loaddata(self):
        print(os.path.join("mnt/c/Users/Anwender/PycharmProjects/pythonProject", "Medication.csv"))
        patients = pd.read_csv("Medication.csv", sep=';')
        print(patients)

        row = 0
        self.tableWidget.setRowCount(len(patients))
        for patient in patients:
            content = {
                "Levodopa/Carbidopa": [1, 1],
                "Levodopa/Carbidopa CR": [2, 1],
                "Entacapone": [3, 1],
                "Tolcapone": [4, 1],
                "Pramipexole": [5, 1],
                "Ropinirole": [6, 1],
                "Rotigotine": [7, 1],
                "Selegiline oral": [8, 1],
                "Selegiline sublingual": [9, 1],
                "Rasagiline": [10, 1],
                "Amantadine": [11, 1],
                "Apomorphine": [12, 1],
                "Piribedil": [13, 1],
                "Safinamid": [14, 1],
                "Opicapone": [15, 1],
                "Ongentys": [16,1],
                "Other": [17, 1],

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
