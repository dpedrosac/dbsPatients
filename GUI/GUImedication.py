#!/usr/bin/env python3
import sys, os
from PyQt5 import QtCore
import numpy as np

from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QLabel, QWidget, QGridLayout, QPlainTextEdit

from utils.helper_functions import General, Content
from dependencies import ROOTDIR, FILEDIR

class MedicationDialog(QDialog):
    """Dialog to introduce the medication at a specific date. All unrelated """

    def __init__(self, visit='unknown', parent=None):
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

    @QtCore.pyqtSlot()
    def onClickedSaveReturn(self):
        """returns to calling GUI saving data whenever the (only available) button is pressed """

        subj_id = General.read_current_subj().id[0] # reads data from current_subj (saved in ./tmp)
        df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')
        if df.shape[1] == 1:
            df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=';')

        idx2replace = df.index[df['ID'] == subj_id][0]  # looks for index at dataframe in which data shall be stored
        df_items = {v.format('_preop').replace(' ', '_'): v.format('').replace(' ', '_') for v in self.medication_names}
        df_subj = df.iloc[idx2replace, :]

        for k, v in df_items.items():
            df_subj[k] = eval('self.lineEdit{}.text()'.format(v)) if v != 'Other' \
                else eval('self.lineEdit{}.toPlainText()'.format(v))

        df.iloc[idx2replace, :] = df_subj
        # TODO: Marco, at this point the dumber of columns is not equal in preoperative compared to this. The reason are
        # tow columns that are wrong because something was mixed up with the selegiline_oral and selegiline_sublingual.
        # can you please make sure, the columns are right. Whenever this is done, this part should work.

        df = df.replace(['nan', ''], [np.nan, np.nan])
        df.to_csv(os.path.join(FILEDIR, "preoperative.csv"), index=False)  # saves changed data to file

        self.close()

    def updatetext(self):
        """adds information extracted from database already provided"""

        df_subj = Content.extract_saved_data(self.date)

        self.lineEditLevodopa_Carbidopa.setText(str(df_subj["Levodopa_Carbidopa_preop"][0])) \
            if str(df_subj["Levodopa_Carbidopa_preop"][0]) != 'nan' else self.lineEditLevodopa_Carbidopa.setText('')
        self.lineEditLevodopa_Carbidopa_CR.setText(str(df_subj["Levodopa_Carbidopa_CR_preop"][0])) \
            if str(df_subj["Levodopa_Carbidopa_CR_preop"][0]) != 'nan' else self.lineEditLevodopa_Carbidopa_CR.setText('')
        self.lineEditEntacapone.setText(str(df_subj["Entacapone_preop"][0])) \
            if str(df_subj["Entacapone_preop"][0]) != 'nan' else self.lineEditEntacapone.setText('')
        self.lineEditTolcapone.setText(str(df_subj["Tolcapone_preop"][0])) \
            if str(df_subj["Tolcapone_preop"][0]) != 'nan' else self.lineEditTolcapone.setText('')
        self.lineEditPramipexole.setText(str(df_subj["Pramipexole_preop"][0])) \
            if str(df_subj["Pramipexole_preop"][0]) != 'nan' else self.lineEditPramipexole.setText('')
        self.lineEditRopinirole.setText(str(df_subj["Ropinirole_preop"][0])) \
            if str(df_subj["Ropinirole_preop"][0]) != 'nan' else self.lineEditRopinirole.setText('')
        self.lineEditRotigotine.setText(str(df_subj["Rotigotine_preop"][0])) \
            if str(df_subj["Rotigotine_preop"][0]) != 'nan' else self.lineEditRotigotine.setText('')
        self.lineEditSelegiline_oral.setText(str(df_subj["Selegiline_preop"][0])) \
            if str(df_subj["Selegiline_preop"][0]) != 'nan' else self.lineEditSelegiline_oral.setText('')
        self.lineEditSelegiline_sublingual.setText(str(df_subj["_sublingual_preop"][0])) \
            if str(df_subj["_sublingual_preop"][0]) != 'nan' else self.lineEditSelegiline_sublingual.setText('')
        self.lineEditRasagiline.setText(str(df_subj["Rasagiline_preop"][0])) \
            if str(df_subj["Rasagiline_preop"][0]) != 'nan' else self.lineEditRasagiline.setText('')
        self.lineEditAmantadine.setText(str(df_subj["Amantadine_preop"][0])) \
            if str(df_subj["Amantadine_preop"][0]) != 'nan' else self.lineEditAmantadine.setText('')
        self.lineEditApomorphine.setText(str(df_subj["Apomorphine_preop"][0])) \
            if str(df_subj["Apomorphine_preop"][0]) != 'nan' else self.lineEditApomorphine.setText('')
        self.lineEditPiribedil.setText(str(df_subj["Piribedil_preop"][0])) \
            if str(df_subj["Piribedil_preop"][0]) != 'nan' else self.lineEditPiribedil.setText('')
        self.lineEditSafinamide.setText(str(df_subj["Safinamid_preop"][0])) \
            if str(df_subj["Safinamid_preop"][0]) != 'nan' else self.lineEditSafinamide.setText('')
        self.lineEditOpicapone.setText(str(df_subj["Opicapone_preop"][0])) \
            if str(df_subj["Opicapone_preop"][0]) != 'nan' else self.lineEditSafinamide.setText('')
        self.lineEditOther.setText(str(df_subj["Other_preop"][0])) \
            #if str(df_subj["Other_preop"][0]) != 'nan' else self.lineEditOther.setText('')

        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = MedicationDialog()
    dlg.show()
    sys.exit(app.exec_())
