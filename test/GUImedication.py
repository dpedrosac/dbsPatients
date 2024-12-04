#!/usr/bin/env python3
import sys, re
import pandas as pd
import numpy as np
from PyQt5 import QtCore
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QLabel, QGridLayout, QPlainTextEdit
from utils.helper_functions import General, Content
from dependencies import FILEDIR
pd.options.mode.chained_assignment = None


class MedicationDialog(QDialog):
    """Dialog to introduce the medication at a specific date."""

    def __init__(self, visit='preoperative', parent=None): #GP: setting visit to be preoperative -> future problem?
        super(MedicationDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # ====================    Create General Layout      ====================
        self.date = visit  # ensures the right date is entered
        df_subj = Content.extract_saved_data(self.date)
        self.setWindowTitle('{} Medication of PID: {} '.format(self.date.capitalize(), int(General.read_current_subj().pid.iloc[0])))
        self.setGeometry(200, 1000, 200, 170)
        self.move(700, 250)

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # ====================    (Only) Optionbox      ====================
        self.optionbox1 = QGroupBox('Patient Medication')
        self.grid_medication = QGridLayout()
        self.medication_names = General.available_PDmedication()

        no_rows, iter_row = 9, 0  # creates nine rows of
        for idx, med in enumerate(self.medication_names):
            col = 2 if idx >= no_rows else 0
            if idx == no_rows:
                iter_row = 0
            self.grid_medication.addWidget(QLabel(med.format('')), iter_row, col)
            iter_row += 1

        # Start adding lineEdits to the created rows
        self.lineEditLevodopa_Carbidopa = QLineEdit()
        self.grid_medication.addWidget(self.lineEditLevodopa_Carbidopa, 0, 1)

        self.lineEditLevodopa_Carbidopa_CR = QLineEdit()
        self.grid_medication.addWidget(self.lineEditLevodopa_Carbidopa_CR, 1, 1)

        self.lineEditEntacapone = QLineEdit()
        self.grid_medication.addWidget(self.lineEditEntacapone, 2, 1)

        self.lineEditTolcapone = QLineEdit()
        self.grid_medication.addWidget(self.lineEditTolcapone, 3, 1)

        self.lineEditPramipexole = QLineEdit()
        self.grid_medication.addWidget(self.lineEditPramipexole, 4, 1)

        self.lineEditRopinirole = QLineEdit()
        self.grid_medication.addWidget(self.lineEditRopinirole, 5, 1)

        self.lineEditRotigotin = QLineEdit()
        self.grid_medication.addWidget(self.lineEditRotigotin, 6, 1)

        self.lineEditSelegilin_oral = QLineEdit()
        self.grid_medication.addWidget(self.lineEditSelegilin_oral, 7, 1)

        self.lineEditOther = QPlainTextEdit()
        self.grid_medication.addWidget(self.lineEditOther, 8, 1, 3, 4)

        self.lineEditSelegilin_sublingual = QLineEdit()
        self.grid_medication.addWidget(self.lineEditSelegilin_sublingual, 0, 3)

        self.lineEditRasagilin = QLineEdit()
        self.grid_medication.addWidget(self.lineEditRasagilin, 1, 3)

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
        self.button_save_return = QPushButton('Save and Return')
        self.button_save_return.clicked.connect(self.onClickedSaveReturn)

        layout_bottom.addStretch(1)
        layout_bottom.addWidget(self.button_save_return)

        hlay_bottom = QHBoxLayout()
        hlay_bottom.addStretch(2)
        hlay_bottom.addWidget(self.button_save_return)

        layout_general.addLayout(hlay_bottom, 4, 0, 1, 3)

        self.updateDisplayedMedication()  # Updates text from csv after creating the content!

    @QtCore.pyqtSlot()
    def onClickedSaveReturn(self):
        """Saves the entered information in a csv-file according to the self.date information"""

        subj_id = General.read_current_subj().id[0]  # reads data from current_subj (saved in ./tmp)
        df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')

        match = re.search(r'^(pre|intra|post)op', self.date)  # gets the condition, to ensure correct saving.
        df_items = {v.format('_{}'.format(match.group())).replace(' ', '_'): v.format('').replace(' ', '_')
                    for v in self.medication_names}

        try:
            idx2replace = df.index[df['ID'] == subj_id][0]  # looks for index at dataframe in which data shall be stored
            df_subj = df.iloc[idx2replace, :]
            first_index = False
        except IndexError:
            df_subj = pd.Series()
            df_subj['ID'] = General.read_current_subj().id[0]
            df_subj['PID_ORBIS'] = General.read_current_subj().pid[0]
            first_index = True

        for k, v in df_items.items():
            df_subj[k] = eval('self.lineEdit{}.text()'.format(v)) if v != 'Other' \
                else eval('self.lineEdit{}.toPlainText()'.format(v))
        if first_index:
            df = df.append(df_subj, ignore_index=True)
        else:
            df.iloc[idx2replace, :] = df_subj

        df = df.replace(['nan', ''], [np.nan, np.nan])
        df.to_csv(Path(f"{FILEDIR}/{self.date}.csv"), index=False)

        self.hide()

    def updateDisplayedMedication(self):
        """Displays the information extracted from the database; so everything already stored is shown"""

        df_subj = Content.extract_saved_data(self.date)
        match = re.search(r'^(pre|intra|post)op', self.date)
        df_items = {v.format('_{}'.format(match.group())).replace(' ', '_'): v.format('').replace(' ', '_')
                    for v in self.medication_names}

        if not df_subj["ID"]:
            return

        for k, v in df_items.items():
            if v != 'Other':
                eval('self.lineEdit{}.setText(str(df_subj["{}_{}"][0]))'.format(v, v, match.group())) \
                    if str(df_subj['{}_{}'.format(v, match.group())][0]) != 'nan' \
                    else eval('self.lineEdit{}.setText("")'.format(v))
            else:  # 'Other' needs a slightly different approach
                self.lineEditOther.insertPlainText(str(df_subj["{}_{}".format(v, match.group())][0])) \
                    if str(df_subj["{}_{}".format(v, match.group())][0]) != 'nan' else self.lineEditOther.insertPlainText('')

        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = MedicationDialog()
    dlg.show()
    sys.exit(app.exec_())
