# Hallo David
# Ich habe mal versucht deine Vorschläge umzusetzen aber irgendwie bekomme ich trotzdem Error-Nachrichten raus.
# Ich bin mir nicht sicher was ich falsch gemacht habe,
# "for key, value in content.items()" -> aber ich erhalte bei diesem Teil mehrere Errors leider.
# Ich habe irgendwie auch allgemeine Verständisprobleme bei dem Part.

import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication
import pandas as pd

# ===============
# OK, folgendes. Ich habe mal alles wieder in preoperative kopiert, damit wir immer die gleiche Datei bearbeiten. Ich
# hoffe, dass das nicht zu umständlich oder unübersichtlich für Dich wird. Erst einmal ein Paar kleinere Sachen. Wenn
# Du Fehler bekommst beim Programmieren, kannst DU in den sog. debug MOdus schalten also die Fehler suchen, indem Du an
# einer bestimmten Stelle stoppst. Das erreichst Du oben rechts über den grünen Käfer und indem Du ein Stop dahin
# setzt, wo Du gerne genauer schauen würdest. Um den Code im Debug MOdus zu stoppen klickst DU neben die Zeile links
# und setzt ein rotes Stop. Manchmal ist es auch sinnvoll, dass man das tut, wenn eine Variable definiert wird oder
# etwas eingelesen wird. In Deinem Fall würde ich in der  Zeile patients = pd.read_csv("preoperative_table.csv") stoppen
# und dann eine Zeile weiter laufen lassen (an meinem Rechner benutzt man dazu F8, bei dir findest Du
# die KOmbination oben unter Run -> Step Into My Code). So wie Du es hattest, hat es die csv Datei gelesen, aber keine
# sinnvolle Matrix daraus gemacht. Das kannst Du überprüfen im Debug Mode unter Debugger links unten und dann Variables.
# Schau Dir vielleicht einfach mal den Unterschied zwischen patients_old = pd.read_csv("Preoperative_CSV.csv") und
# patients = pd.read_csv("Preoperative_CSV.csv", sep=';') an.

# So wie es jetzt geschrieben ist, läuft es! Glückwunsch zu Deinem ersten Gui!!! Ich würde es aber gerne etwas anders
# aufziehen. Nachdem das also jetzt funktioniert, gehen wir einen Schritt zurück und Du erstellst erst einmal ein GUI,
# dass Du später igrendwann mit INhalt füllst. Eine Anleitung für ein GUI findest DU hier:
# https://realpython.com/python-pyqt-gui-calculator/ ich habe aber auch eine Datei eingefügt, die test_pyqt5 heißt.
# DIe knanst Du morgen einfach mal mit allen möglichen Elementen erweitern, die Dir so ein- und auffallen. Immer wieder
# speichern, neu laden, verändern, bei Fehlern debguggen, auskommentieren, usw. KÜmmer Dich nicht so sehr um das Layout,
# erst einmal ist es ok alles untereinander zu schreiben. Das machen wir später ; )


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("DBS_Patients_Preoperative.ui", self)
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 50)
        self.tableWidget.setColumnWidth(2, 270)
        self.loaddata()

    def loaddata(self):
        patients_old = pd.read_csv("Preoperative_CSV.csv")
        print(os.path.join("mnt/c/Users/Anwender/PycharmProjects/pythonProject", "Preoperative_CSV.csv"))
        patients = pd.read_csv("Preoperative_CSV.csv", sep=';')  # TODO: filename with os.path.join and include ROOTDIR
        print(patients)

        row = 0
        self.tableWidget.setRowCount(len(patients))
        for patient in patients:
            content = {
                "ID": [0, 1],
                "Gender": [1, 1],
                "Diagnosis": [2, 1],
                "First_Diagnosed": [3, 1],
                "Admission": [4, 1],
                "Dismissal": [5, 1],
                "Report": [6, 1],
                "Report:Preop": [7, 1],
                "UPDRS_On": [8, 1],
                "UPDRS_Off": [9, 1],
                "Video": [10, 1],
                "Video_File": [11, 1],
                "MRI": [12, 1],
                "fpcit_spect": [13, 1],
                "NMSQ": [14, 1],
                "MoCa": [15, 1],
                "DemTect": [16, 1],
                "MMST": [17, 1],
                "PDQ8": [18, 1],
                "BDI2": [19, 1],
                "PDQ39": [20, 1],
                "Outpat_Contact": [21, 1],
                "nch": [22, 1],
                "Briefling": [23, 1],
                "Briefling_Doctor": [24, 1],
                "DBS_Conference": [25, 1],
                "Decision_DBS": [26, 1],
                "LEDD": [27, 1],
                "Levodopa/Carbidopa": [28, 1],
                "Levodopa/Carbidopa CR": [29, 1],
                "Entacapone": [30, 1],
                "Tolcapone": [31, 1],
                "Pramipexole": [32, 1],
                "Ropinirole": [33, 1],
                "Rotigotine": [34, 1],
                "Selegiline, oral": [35, 1],
                "Selegiline, sublingual": [36, 1],
                "Rasagiline": [37, 1],
                "Amantadine": [38, 1],
                "Apomorphine": [39, 1],
                "Piribedil": [40, 1],
                "Safinamid": [41, 1],
                "Opicapone": [42, 1],
                "Other": [43, 1],
                "UPDRSII": [44, 1],
                "H&Y": [45, 1],
                "HRUQ": [46, 1],
                "EQ5D": [47, 1],
                "S&E": [48, 1],
                "icVRCS": [49, 1],
                "inexVRCS": [50, 1],
                "Notes": [51, 1]
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
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
