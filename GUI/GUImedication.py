#!/usr/bin/env python3
import sys, os
import pandas as pd
from PyQt5 import QtCore
import numpy as np
pd.options.mode.chained_assignment = None

from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QLabel, QWidget, QGridLayout, QPlainTextEdit

from utils.helper_functions import General, Content
from dependencies import ROOTDIR, FILEDIR

class MedicationDialog(QDialog):
    """Dialog to introduce the medication at a specific date. All unrelated """

    def __init__(self, visit="preoperative", parent=None):
        super().__init__(parent)

        # ====================    Create General Layout      ====================
        self.date = visit  # ensures the right date is entered
        self.setWindowTitle('Medication of patient with DBS at {} visit'.format(visit))
        self.setGeometry(200, 100, 280, 170)
        self.move(700, 250)

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # ====================    (Only) Optionbox      ====================
        self.optionbox1 = QGroupBox('Patient Medication')
        self.grid_medication = QGridLayout()
        self.medication_names = ['Levodopa Carbidopa{}', 'Levodopa Carbidopa CR{}', 'Entacapone{}', 'Tolcapone{}',
                                 'Pramipexole{}', 'Ropinirole{}', 'Rotigotine{}', 'Selegiline oral{}', 'Other',
                                 'Selegiline sublingual{}', 'Rasagiline{}', 'Amantadine{}', 'Apomorphine{}',
                                 'Piribedil{}', 'Safinamide{}', 'Opicapone{}']
        no_rows, iter_row = 9, 0
        for idx, med in enumerate(self.medication_names):
            col = 2 if idx >= no_rows else 0
            if idx == no_rows:
                iter_row = 0
            self.grid_medication.addWidget(QLabel(med.format('')), iter_row, col)
            iter_row += 1

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

        self.lineEditSafinamide = QLineEdit()
        self.grid_medication.addWidget(self.lineEditSafinamide, 5, 3)

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

        layout_general.addLayout(hlay_bottom, 4, 0, 1,3)

        self.updatetext()# Updates text from csv after creating the content!

    @QtCore.pyqtSlot()
    def onClickedSaveReturn(self):
        """returns to calling GUI saving data whenever button is pressed """

        subj_id = General.read_current_subj().id[0] # reads data from current_subj (saved in ./tmp)
        df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')
        if df.shape[1] == 1:
            df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=';')

        idx2replace = df.index[df['ID'] == subj_id][0]  # looks for index at dataframe in which data shall be stored
        df_items = {v.format('_preop').replace(' ', '_'): v.format('').replace(' ', '_') for v in self.medication_names}
        df_subj = df.iloc[idx2replace, :]

        # TODO: to make sure nothing is entered in 'Other' separated with semicolon, comma and dots ; maybe "-"
        #  a distinct separator should be used, use replace maybe?! self.lineEditOther.toPlainText().replace(',', '-')



        #for k, v in df_items.items():
           # df_subj[k] = eval('self.lineEdit{}.text()'.format(v)) if v != 'Other' \
                #else eval('self.lineEdit{}.toPlainText()'.format(v))

        for k, v in df_items.items():
            if v != 'Other':
                df_subj[k] = eval('self.lineEdit{}.text()'.format(v))
            else:
                df_subj[k] = self.lineEditOther.toPlainText().replace(';', '-').replace(',', '-').replace('.', '-')



        df.iloc[idx2replace, :] = df_subj
        df = df.replace(['nan', ''], [np.nan, np.nan])
        df.to_csv(os.path.join(FILEDIR, "preoperative.csv"), index=False)  # saves changed data to file

        self.close()

    def updatetext(self):
        """adds information extracted from database already provided"""

        df_subj = Content.extract_saved_data(self.date)
        df_items = {v.format('_preop').replace(' ', '_'): v.format('').replace(' ', '_') for v in self.medication_names}
        for k, v in df_items.items():
            if v != 'Other':
                eval('self.lineEdit{}.setText(str(df_subj["{}_preop"][0]))'.format(v, v)) \
                    if str(df_subj['{}_preop'.format(v)][0]) != 'nan' \
                    else eval('self.lineEdit{}.setText("")'.format(v))
            else:  # 'Other' needs a slightly different approach
                self.lineEditOther.insertPlainText(str(df_subj["{}_preop".format(v)][0])) \
                    if str(df_subj["{}_preop".format(v)][0]) != 'nan' else self.lineEditOther.insertPlainText('')

        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = MedicationDialog()
    dlg.show()
    sys.exit(app.exec_())
