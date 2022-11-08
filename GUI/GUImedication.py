#!/usr/bin/env python3
import sys
from PyQt5 import QtCore

from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QLabel, QWidget, QGridLayout, QPlainTextEdit


class MedicationDialog(QDialog):
    """Dialog to introduce the medication at a specific date. All unrelated """

    def __init__(self, visit='unknown', parent=None):
        super().__init__(parent)
        self.setWindowTitle('Medication of patient with DBS at {} visit'.format(visit))
        self.setGeometry(200, 100, 280, 170)
        self.move(700, 250)

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # ====================    (Only) Optionbox      ====================
        self.optionbox1 = QGroupBox('Patient Medication')
        self.grid_medication = QGridLayout()
        medication_names = ['Levodopa/Carbidopa{}', 'Levodopa/Carbidopa CR{}', 'Entacapone {}', 'Tolcapone {}',
                            'Pramipexole {}', 'Ropinirole{}', 'Rotigotine{}', 'Selegiline oral{}', 'Other',
                            'Selegiline sublingual{}', 'Rasagiline{}', 'Amantadine{}', 'Apomorphine{}', 'Piribedil{}',
                            'Safinamid{}', 'Opicapone{}']
        no_rows, iter_row = 9, 0
        for idx, med in enumerate(medication_names):
            col = 2 if idx >= no_rows else 0
            if idx == no_rows:
                iter_row = 0
            self.grid_medication.addWidget(QLabel(med.format('')), iter_row, col)
            iter_row += 1

        self.lineEditLevodopaCarbidopa = QLineEdit()
        self.grid_medication.addWidget(self.lineEditLevodopaCarbidopa, 0, 1)

        self.lineEditLevodopaCarbidopaCR = QLineEdit()
        self.grid_medication.addWidget(self.lineEditLevodopaCarbidopaCR, 1, 1)

        self.lineEditEntacapone = QLineEdit()
        self.grid_medication.addWidget(self.lineEditEntacapone, 2, 1)

        self.lineEditTolcapone = QLineEdit()
        self.grid_medication.addWidget(self.lineEditTolcapone, 3, 1)

        self.lineEditPramipexole = QLineEdit()
        self.grid_medication.addWidget(self.lineEditPramipexole, 4, 1)

        self.lineEditRopinirole = QLineEdit()
        self.grid_medication.addWidget(self.lineEditRopinirole, 5, 1)

        self.lineEditRotigotine = QLineEdit()
        self.grid_medication.addWidget(self.lineEditRotigotine, 6, 1)

        self.lineEditSelegiline_oral = QLineEdit()
        self.grid_medication.addWidget(self.lineEditSelegiline_oral, 7, 1)

        self.lineEditOther = QPlainTextEdit()
        self.grid_medication.addWidget(self.lineEditOther, 8, 1, 3, 4)

        self.lineEditSelegiline_sublingual = QLineEdit()
        self.grid_medication.addWidget(self.lineEditSelegiline_sublingual, 0, 3)

        self.lineEditRasagiline = QLineEdit()
        self.grid_medication.addWidget(self.lineEditRasagiline, 1, 3)

        self.lineEditAmantadine = QLineEdit()
        self.grid_medication.addWidget(self.lineEditAmantadine, 2, 3)

        self.lineEditApomorphine = QLineEdit()
        self.grid_medication.addWidget(self.lineEditApomorphine, 3, 3)

        self.lineEditPiribedil = QLineEdit()
        self.grid_medication.addWidget(self.lineEditPiribedil, 4, 3)

        self.lineEditSafinamid = QLineEdit()
        self.grid_medication.addWidget(self.lineEditSafinamid, 5, 3)

        self.lineEditOpicapone = QLineEdit()
        self.grid_medication.addWidget(self.lineEditOpicapone, 6, 3)

        self.optionbox1Content = QVBoxLayout(self.optionbox1)
        layout_general.addWidget(self.optionbox1, 0, 0)

        self.optionbox1Content.addLayout(self.grid_medication)
        self.optionbox1.setLayout(self.optionbox1Content)

        # ====================    Create Content for Buttons at the Bottom      ====================
        layout_bottom = QHBoxLayout()
        self.button_save_return = QPushButton('Save settings \nand return')
        self.button_save_return.clicked.connect(self.onClickedSaveReturn)

        layout_bottom.addStretch(1)
        layout_bottom.addWidget(self.button_save_return)

        hlay_bottom = QHBoxLayout()
        hlay_bottom.addStretch(2)
        hlay_bottom.addWidget(self.button_save_return)
        #hlay_bottom.addStretch(1)

        layout_general.addLayout(hlay_bottom, 4, 0, 1,3)

    # In the next lines, actions are defined when Buttons are pressed
    @QtCore.pyqtSlot()
    def onClickedSaveReturn(self):
        """returns to calling GUI saving data whenever the (only available) button is pressed """
        # TODO: add a way to save data to csv files according to the flag (self.date) used
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = MedicationDialog()
    dlg.show()
    sys.exit(app.exec_())
