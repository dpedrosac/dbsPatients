#!/usr/bin/env python3
import sys, re
import pandas as pd
import numpy as np
from PyQt5 import QtCore
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QLabel, QGridLayout, QPlainTextEdit, QComboBox
from utils.helper_functions import General, Content
from dependencies import FILEDIR
pd.options.mode.chained_assignment = None


class MedicationDialog(QDialog):
    """Dialog to introduce the medication at a specific date."""

    def __init__(self, visit='preoperative', parent=None):
        super(MedicationDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.date = visit
        self.inputs = {}
        self.medication_names = General.available_PDmedication()
        self.setup_ui()

    def setup_ui(self):
        self.setup_general_layout()
        self.updateDisplayedMedication()

    def setup_general_layout(self):
        df_subj = Content.extract_saved_data(self.date)
        self.setWindowTitle('{} Medication of PID: {}'.format(self.date.capitalize(), int(General.read_current_subj().pid.iloc[0])))
        self.setGeometry(200, 1000, 200, 170)
        self.move(700, 250)

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)
        self.optionbox_medication(layout_general)

    def optionbox_medication(self, layout_general):
        self.optionbox_medication = QGroupBox('Patient Medication')
        self.optionbox_medication_content = QVBoxLayout(self.optionbox_medication)
        layout_general.addWidget(self.optionbox_medication, 0, 0)

        # Add headers
        headers = ['Medication', 'Dose', 'Unit', '/Day\t']
        self.grid_medication = QGridLayout()
        self.optionbox_medication_content.addLayout(self.grid_medication)

        for col in range(2):  # Create at least 2 columns
            for i, header in enumerate(headers):
                label = QLabel(header)
                label.setAlignment(QtCore.Qt.AlignLeft)
                self.grid_medication.addWidget(label, 0, col * 4 + i)

        for idx, med in enumerate(self.medication_names):
            self.add_medication_row(idx, med)

        layout_bottom = QHBoxLayout()
        layout_ledd = QHBoxLayout()
        self.ledd_label = QLabel('LEDD:')
        self.ledd_total = QLabel('')
        layout_ledd.addWidget(self.ledd_label)
        layout_ledd.addWidget(self.ledd_total)
        layout_ledd.addStretch(1)

        self.button_calculate_ledd = QPushButton('Calculate LEDD')
        self.button_calculate_ledd.clicked.connect(self.onClickedCalculateLEDD)
        self.button_save_return = QPushButton('Save and Return')
        self.button_save_return.clicked.connect(self.onClickedSaveReturn)
        self.button_add_medication = QPushButton('Add Medication')
        self.button_add_medication.clicked.connect(lambda: self.onClickedAddMedication(len(self.inputs)))

        layout_bottom.addLayout(layout_ledd)
        layout_bottom.addStretch(1)
        layout_bottom.addWidget(self.button_calculate_ledd)
        layout_bottom.addWidget(self.button_add_medication)
        layout_bottom.addWidget(self.button_save_return)
        layout_general.addLayout(layout_bottom, 4, 0, 1, 3)

    def add_medication_row(self, idx, med):

        if idx % 10 == 0 and idx >= 20:
            print("index", idx)
            headers = ['Medication', 'Dose', 'Unit', '/Day\t']
            for i, header in enumerate(headers):
                label = QLabel(header)
                label.setAlignment(QtCore.Qt.AlignLeft)
                self.grid_medication.addWidget(label, 0, (idx//10) * 4 + i)
                #self.grid_medication.setColumnMinimumWidth(col * 4 + i + 3,100)

        col = (idx // 10) * 4
        row = (idx % 10) + 1

        if med == 'Enter new Medication':
            med_label = QLineEdit(self)
            med_label.setPlaceholderText(med)
            med_label.setFixedHeight(35)
            self.grid_medication.addWidget(med_label, row, col)
        else:
            med_label = QLabel(med.replace("{}", ""))
            med_label.setFixedHeight(35)
            self.grid_medication.addWidget(med_label, row, col)

        dose_input = QLineEdit(self)
        dose_input.setFixedSize(100, 35)
        self.grid_medication.addWidget(dose_input, row, col + 1)

        dose_unit = QLabel('mg')
        dose_unit.setFixedHeight(35)
        self.grid_medication.addWidget(dose_unit, row, col + 2)

        med_times = QLineEdit(self)
        med_times.setFixedSize(40, 35)
        self.grid_medication.addWidget(med_times, row, col + 3)

        self.inputs[idx] = (med_label, dose_input, dose_unit, med_times)

    def onClickedAddMedication(self, row):
        self.add_medication_row(row, 'Enter new Medication')


    def onClickedCalculateLEDD(self):

        conversion_factors = {"Levodopa Carbidopa": 1,  # IR
                              "Levodopa Carbidopa CR": 0.75,
                              "Levodopa (ER)": 0.5,  # missing
                              "Duodopa": 1.11,  # missing
                              "Entacapone": 0.33,  # Per dose of levodopa (LED * 0.33)
                              "Tolcapone": 0.5,  # Per dose of levodopa (LED * 0.5)
                              "Opicapone": 0.5,  # Per dose of levodopa (LED * 0.5)
                              "Selegiline oral": 10,
                              "Selegiline sublingual": 80,
                              "Rasagiline": 100,
                              "Safinamide": 1,  # Fixed LED, not dose-dependent (50mg or 100mg/d)
                              "Apomorphine": 10,
                              "Piribedil": 1,
                              "Pramipexole": 100,
                              "Ropinirole": 20,
                              "Rotigotine": 30,
                              "Amantadine": 1,
                              'Other' : 0
                              }

        total_led = 0
        total_comt = 0
        total_ledd = 0
        for idx, (med_label, dose_input, dose_unit, med_times) in self.inputs.items():
            med_name = med_label.text()
            if med_name in conversion_factors:
                factor = conversion_factors[med_name]
            else:
                factor = conversion_factors['Other']
            if 'Levodopa' in med_name:
                try:
                    dose = float(dose_input.text())
                    times_per_day = float(med_times.text())
                    led = dose * times_per_day * factor
                    total_led += led
                except ValueError:
                    pass
            elif 'capone' in med_name:
                if dose_input.text() != '':
                    try:
                        dose = total_led
                        comt = dose * factor
                        total_comt += comt
                    except ValueError:
                        pass
            else:
                try:
                    dose = float(dose_input.text())
                    times_per_day = float(med_times.text())
                    ledd = dose * times_per_day * factor
                    total_ledd += ledd
                except ValueError:
                    pass

        print(total_led)
        print(total_comt)
        print(total_ledd)
        total_ledd += total_led + total_comt
        self.ledd_total.setText(f"{total_ledd:.2f}")


    @QtCore.pyqtSlot()
    def onClickedSaveReturn(self):
        subj_id = General.read_current_subj().id[0]
        df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')

        match = re.search(r'^(pre|intra|post)op', self.date)
        df_items = {v.format('_{}'.format(match.group())).replace(' ', '_'): v.format('').replace(' ', '_')
                    for v in self.medication_names}

        print(self.inputs)
        print(self.inputs[13][0].text(), self.inputs[14][0].text())

        idx2replace = df.index[df['ID'] == subj_id][0]
        df_subj = df.iloc[idx2replace, :]
        print(self.inputs)
        print(df_items)
        print(self.date.replace("erative", ""))

        for k, v in df_items.items():
            med_label, dose_input, dose_unit, med_times = self.inputs[list(df_items.keys()).index(k)]
            if dose_input.text() and med_times.text():
                df_subj[k] = f"{dose_input.text()}§{dose_unit.text()}§{med_times.text()}"
            else:
                df_subj[k] = ""

        other_medications = ""
        if len(self.inputs) > len(df_items.keys()):
            for i in range(len(df_items.keys()), len(self.inputs)):
                med_label, dose_input, dose_unit, med_times = self.inputs[i]
                if med_label.text() and dose_input.text() and med_times.text():
                    other_medications += f"{med_label.text()}§{dose_input.text()}§{dose_unit.text()}§{med_times.text()}"
                    if i < len(self.inputs) - 1:
                        other_medications += "%"
            df_subj[f"Other_{self.date.replace("erative", "")}"] = other_medications

        self.onClickedCalculateLEDD()
        df_subj[f"LEDD_{self.date.replace('erative', '')}"] = self.ledd_total.text()

        df.iloc[idx2replace, :] = df_subj
        df = df.fillna(np.nan).infer_objects(copy=False)
        df.to_csv(Path(f"{FILEDIR}/{self.date}.csv"), index=False)

        self.close()

    def updateDisplayedMedication(self):
        df_subj = Content.extract_saved_data(self.date)
        match = re.search(r'^(pre|intra|post)op', self.date)
        df_items = {v.format('_{}'.format(match.group())).replace(' ', '_'): v.format('').replace(' ', '_')
                    for v in self.medication_names}

        if not df_subj["ID"]:
            return
        print(df_items)
        for k, v in df_items.items():
            med_label, dose_input, dose_unit, med_times = self.inputs[list(df_items.keys()).index(k)]
            if v != 'Other':
                value = str(df_subj['{}_{}'.format(v, match.group())][0])
                print(type(value))
                print(value)
                if value != 'nan':
                    dose_input.setText(value.split('§')[0])
                    med_times.setText(value.split('§')[2])
                else:
                    dose_input.setText("")
                    med_times.setText("")
            else:
                other_medications = df_subj.get(f"Other_{self.date.replace('erative', '')}")
                test = df_subj.get("Entacapone_preop")
                print(test)
                print(type(test))
                try:
                    other_medications_str = other_medications[0]
                    other_list = other_medications_str.split('%')
                    print(other_list)
                    for med in other_list:
                        med = med.replace("[]''", "")
                        if med != "":
                            med_label_text, dose_input_text, dose_unit_text, med_times_text = med.split('§')
                            self.onClickedAddMedication(len(self.inputs))
                            med_label, dose_input, dose_unit, med_times = self.inputs[len(self.inputs) - 1]
                            med_label.setText(med_label_text)
                            dose_input.setText(dose_input_text)
                            dose_unit.setCurrentText(dose_unit_text)
                            med_times.setText(med_times_text)
                except AttributeError:
                    print("Error")
                    pass
        ledd_value = df_subj[f"LEDD_{self.date.replace('erative', '')}"][0]
        if pd.notna(ledd_value):
            self.ledd_total.setText(str(ledd_value))

        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = MedicationDialog()
    dlg.show()
    sys.exit(app.exec_())