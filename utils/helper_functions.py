#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

import rstr
import csv
import os
import shutil
import inspect
import pandas as pds
from pathlib import Path
from dependencies import ROOTDIR, FILEDIR
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from utils.logger import logger


# LE: changes work with python 3.11
class General:
    def __init__(self, _debug=False):
        pass

    @staticmethod
    def create_pseudonym(size_array: int) -> str:
        """generates pseudonym -- ';' and ',' are omitted to avoid confusion in 'csv-files' """
        re_expression = f'[a-zA-Z0-9_!#%$§]{{{size_array}}}'
        return rstr.xeger(re_expression)

    @staticmethod
    def available_PDmedication():
        """List w/ available medication against PD; parenthesis intended to introduce pre|intra|postoperative"""

        medication = ['Levodopa Carbidopa{}', 'Levodopa Carbidopa CR{}', 'Entacapone{}', 'Tolcapone{}',
                      'Pramipexole{}', 'Ropinirole{}', 'Rotigotin{}', 'Selegilin oral{}', 'Other{}',
                      'Selegilin sublingual{}', 'Rasagilin{}', 'Amantadine{}', 'Apomorphine{}',
                      'Piribedil{}', 'Safinamid{}', 'Opicapone{}']
        return medication

    @staticmethod
    def import_dataframe(filename: str, separator_csv: str = ',', missing_values: str = '', DEBUG=False) -> pds.DataFrame:
        """returns pandas dataframe from csv"""

        filename_total = os.path.join(FILEDIR, filename)
        if DEBUG:
            logger.debug(f"opening file: {filename_total}")

        if not os.path.isfile(filename_total):
            print(f'\t Filename: {filename_total} not found. Please double-check!')
        df = pds.read_csv(filename_total, sep=separator_csv, on_bad_lines='skip', na_values=missing_values)

        if df.shape[1] == 1:
            df = pds.read_csv(filename_total, sep=';', on_bad_lines='skip', na_values=missing_values)
        if DEBUG:
            caller1 = inspect.getouterframes(inspect.currentframe(), 2)[1][0]
            caller2 = inspect.getouterframes(inspect.currentframe(), 3)[2][0]
            logger.debug(f"{inspect.currentframe()}\n called from {caller1}\ncalled from {caller2}\n returns dataframe \n{df}")
        return df

    @staticmethod
    def write_csv_temp(df, idx, default_filename='current_subj.csv'):
        """this function is intended to write a file in which the metadata of the subject being processed is saved"""

        header = ['pid', 'id', 'idx']
        data = [int(df["PID_ORBIS"][idx[0]]), str(df["ID"][idx[0]]), idx[0]]

        with open(os.path.join(ROOTDIR, 'temp', default_filename), 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(data)

    @staticmethod
    def read_current_subj(default_filename='current_subj.csv'):
        """Reads data from temporary information"""

        file_path = Path(ROOTDIR) / 'temp' / default_filename
        try:
            subj_details = pds.read_csv(file_path)
        except FileNotFoundError:
            logger.error(f'Error: File "{file_path}" not found')
            subj_details = pds.DataFrame()

        return subj_details

    @staticmethod
    def get_data_subject(flag, pid2lookfor):
        """gets data from available dataframes for a single subject or creates empty file if not present"""

        file2read = os.path.join('{}.csv'.format(flag))
        try:
            data_all = General.import_dataframe(file2read, separator_csv=',')
            if data_all.shape[1] == 1:  # avoids problems with comma-separated vs. semicolon-separated csv-files
                data_all = General.import_dataframe(file2read, separator_csv=';')
            pid2lookfor = str(pid2lookfor).lstrip('0')  # string that is searched for in metadata file
            idxPID = data_all.index[data_all['PID_ORBIS'] == int(pid2lookfor)].to_list()
            data_subj = data_all.iloc[idxPID]
        except FileNotFoundError:  # creates empty file from template (/.install) in case of first use
            print('No file names {} found, creating new file from template in {}/.install '.format(file2read, ROOTDIR))
            file2copy = os.path.join(ROOTDIR, '.install', '{}_template.csv'.format(flag))
            shutil.copyfile(file2copy, os.path.join(FILEDIR, file2read))
            data_subj = []

        return data_subj

    @staticmethod
    def synchronize_data_with_general(flag, id2lookfor, messagebox=True, DEBUG=False):
        """adds gender and ID to where no entries were made in the csv-files"""

        df_general = General.import_dataframe('general_data.csv', separator_csv=',')
        if df_general.shape[1] == 1:  # avoids problems with comma-separated vs. semicolon-separated csv-files
            df_general = General.import_dataframe('general_data.csv', separator_csv=';')

        idx1 = df_general.index[df_general['ID'] == id2lookfor].to_list()

        file2change = General.import_dataframe('{}.csv'.format(flag), separator_csv=',')
        if file2change.shape[1] == 1:  # avoids problems with comma-separated vs. semicolon-separated csv-files
            file2change = General.import_dataframe('{}.csv'.format(flag), separator_csv=';')

        indices2change = file2change.index[file2change['ID'] == id2lookfor].to_list()
        for k in indices2change:
            # file2change['Gender'].loc[int(k)] = int(df_general['Gender'].iloc[idx1])
            file2change['PID_ORBIS'].loc[int(k)] = int(df_general['PID_ORBIS'].iloc[idx1])

        if messagebox:
            Output.msg_box(text='There were changes in the file \n\t{} \nfor subj\n\t{}.\n Please '
                                'confirm to continue'.format('{}.csv'.format(flag),
                                                             int(df_general['PID_ORBIS'].iloc[idx1])),
                           title='Changed data in {}.csv'.format(flag), flag='Warning')
        file2change.to_csv(os.path.join(FILEDIR, '{}.csv'.format(flag)), index=False)
        if DEBUG:
            logger.debug(f"file2change.csv: \n{file2change}")

        return


class Content:
    def __init__(self, _debug=False):
        pass

    @staticmethod
    def extract_postoperative_dates(condition='postoperative'):
        """ Extracts a list with all available postoperative dates for a subject"""

        subject_pid = General.read_current_subj().pid[0]
        data_frame = General.import_dataframe('{}.csv'.format(condition), separator_csv=',')

        data_frame = data_frame.loc[data_frame['PID_ORBIS'] == subject_pid]
        list_of_dates = data_frame['Reason_postop'].tolist()

        # Check if NaN is present in the list_of_dates
        if any(pds.isna(date) for date in list_of_dates):
            # Replace NaN with an empty string
            list_of_dates = ['' if pds.isna(date) else date for date in list_of_dates]

        return list_of_dates

    @staticmethod
    def extract_saved_data(condition, followup_timing=''):
        """ defines a list of columns for the csv files in the data folder; if id not found,
        dictionary remains empty"""

        subj_id = General.read_current_subj().id[0]  # reads data from curent_subj (saved in ./tmp)
        df = General.import_dataframe('{}.csv'.format(condition), separator_csv=',')
        if df.shape[1] == 1:
            df = General.import_dataframe('{}.csv'.format(condition), separator_csv=';')

        if df.shape[0] == 0:
            ID_to_add = {'PID_ORBIS': General.read_current_subj().pid[0],
                         'ID': General.read_current_subj().id[0]}  # Fill in the actual value for PID_ORBIS
            new_row_df = pds.DataFrame(ID_to_add, index=[0])
            df = df._append(new_row_df, ignore_index=True)

        # Only filter the data if the condition is "postoperative" and a follow-up interval is provided
        if followup_timing != '':
            df_subj = df[(df['Reason_postop'] == followup_timing) & (df['ID'] == subj_id)]
        else:
            df_subj = df.iloc[df.index[df['ID'] == subj_id].tolist()].to_dict('list')

        list_preop = ["ID", "PID", "Gender", "Diagnosis_preop", "First_Diagnosed_preop",
                      "Admission_preop", "Dismissal_preop", "Report_preop", "UPDRS_On_preop",
                      "UPDRS_Off_preop", "Video_preop", "Video_File_preop", "MRI_preop", "fpcit_spect_preop",
                      "NMSQ_preop", "MoCa_preop", "DemTect_preop", "MMST_preop", "PDQ8_preop",
                      "BDI2_preop", "PDQ39_preop", "Outpat_Contact_preop", "nch_preop", "Briefing_preop",
                      "Briefing_Doctor_preop", "DBS_Conference_preop", "Decision_DBS_preop", "LEDD_preop",
                      "Levodopa_Carbidopa_preop",
                      "Levodopa_Carbidopa_CR_preop", "Entacapone_preop", "Tolcapone_preop", "Pramipexole_preop",
                      "Ropinirole_preop",
                      "Rotigotine_preop", "Selegiline_oral_preop", "Selegiline_sublingual_preop",
                      "Rasagiline_preop", "Amantadine_preop", "Apomorphine_preop", "Piribedil_preop",
                      "Safinamide_preop",
                      "Opicapone_preop", "Other_preop", "UPDRSII_preop", "H&Y_preop", "HRUQ_preop",
                      "EQ5D_preop", "S&E_preop", "icVRCS_preop", "inexVRCS_preop", "Notes_preop",
                      ]

        list_intraop = ["ID", "Gender", "pat_contact_intraop", "Diagnosis", "sugery_no_intraop",
                        "Admission_intraop", "Dismissal_intraop", "admission_Nch_intraop", "dismissal_NCh_intraop",
                        "report_file_NCh_intraop",
                        "report_file_NR_intraop", "awake_intraop", "surgery_date_intraop", "target_intraop",
                        "electrode_intraop",
                        "IPG_intraop", "no_traj_intraop", "neur_test_intraop", "targetL1_intraop", "targetL2_intraop",
                        "targetL3_intraop", "targetL4_intraop", "targetL5_intraop", "targetL6_intraop",
                        "targetL7_intraop",
                        "targetL8_intraop", "targetR1_intraop", "targetR2_intraop", "targetR3_intraop",
                        "targetR4_intraop",
                        "targetR5_intraop", "targetR6_intraop", "targetR7_intraop", "targetR8_intraop",
                        "protocol_intraop",
                        "protocol_file_intraop", "op_duration_intraop", "LEDD_intraop", "Levodopa_Carbidopa_intraop",
                        "Levodopa_Carbidopa_CR_intraop",
                        "Entacapone_intraop", "Tolcapone_intraop", "Pramipexole_intraop", "Ropinirole_intraop",
                        "Rotigotine_intraop",
                        "Selegiline_oral_intraop", "Selegiline_sublingual_intraop", "Rasagiline_intraop",
                        "Amantadine_intraop", "Apomorphine_intraop",
                        "Piribedil_intraop", "Safinamid_intraop", "Opicapone_intraop", "Other_intraop", "Perc0_intraop",
                        "Perc1_intraop", "Perc2_intraop", "Perc3_intraop", "Perc4_intraop", "Perc5_intraop",
                        "Perc6_intraop", "Perc7_intraop", "Perc8_intraop", "Perc9_intraop", "Perc10_intraop",
                        "Perc11_intraop", "Perc12_intraop", "Perc13_intraop", "Perc14_intraop", "Perc15_intraop",
                        "AmplL_intraop", "AmplR_intraop", "PWL_intraop", "PWR_intraop", "FreqL_intraop",
                        "FreqR_intraop", "CTscan_intraop", "activation_visit_intraop", "implantation_visit_intraop",
                        "incl_qualiPA_intraop",
                        "DBS_intraop", "Comments_intraop"
                        ]

        list_postop = ["ID", "PID", "Gender", "Diagnosis_postop", "Date_postop",
                       "Admission_NCh_postop", "Admission_NR_postop", "Dismissal_NR_postop", "Dismissal_NCh_postop",
                       "Report_File_NCh_postop",
                       "Report_File_NR_postop", "Reason_postop", "Using_Programmer_postop", "CTscan_postop",
                       "Battery_Replacement_postop",
                       "Planned_Visit_postop", "Qualipa_Visit_postop", "Surgery_Date_postop", "UPDRSIII_On_postop",
                       "UPDRSIII_Off_postop",
                       "UPDRSII_postop", "H&Y_postop", "EQ5D_postop", "MoCa_postop", "DemTect_postop",
                       "TSS_postop", "CGIG_clinician_cargiver_postop", "CGIG_patient_postop", "MMST_postop",
                       "PDQ8_postop",
                       "BDI2_postop", "PDQ39_postop", "NMSQ_postop", "S&E_postop", "LEDD_postop",
                       "Levodopa/Carbidopa_postop", "Levodopa/Carbidopa_CR_postop", "Entacapone_postop",
                       "Tolcapone_postop", "Pramipexole_postop",
                       "Ropinirole_postop", "Rotigotine_postop", "Selegiline_oral_postop",
                       "Selegiline_sublingual_postop", "Rasagiline_postop",
                       "Amantadine_postop", "Apomorphine_postop", "Piribedil_postop", "Safinamid_postop",
                       "Ongentys_postop",
                       "Other_postop", "Perc1_postop", "Perc2_postop", "Perc3_postop", "Perc4_postop",
                       "Perc5_postop", "Perc6_postop", "Perc7_postop", "Perc8_postop", "Perc9_postop",
                       "Perc10_postop", "Perc11_postop", "Perc12_postop", "Perc13_postop", "Perc14_postop",
                       "Perc15_postop", "Perc16_postop", "AmplL_postop", "AmplR_postop", "PWL_postop",
                       "PWR_postop", "FreqL_postop", "FreqR_postop", "UPDRS1_postop", "UPDRS4_postop",
                       "UPDRSon_postop", "UDDRSoff_postop", "TRSon_postop", "TRSoff_postop", "AE_postop",
                       "Comments_postop", "DBS_postop"

                       ]
        return df_subj


class Output:
    def __init__(self, _debug=False):
        pass

    @staticmethod
    def msg_box(text='Unknown text', title='unknown title', flag='Information'):
        """helper intended to provide some sort of message box with a text and a title"""
        msgBox = QMessageBox()
        if flag == 'Information':
            msgBox.setIcon(QMessageBox.Information)
        elif flag == 'Warning':
            msgBox.setIcon(QMessageBox.Warning)
        else:
            msgBox.setIcon(QMessageBox.Critical)

        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def open_input_dialog_postoperative(self):
        """Open a message box asking for user input to determine the date after surgery"""

        result, ok = QInputDialog.getText(self, 'Input Dialog', 'Please enter the date after surgery or the event:')
        self.postoperative_date = result

        return self


class Clean:
    def __init__(self, _debug=False):
        pass

    # @staticmethod
    # def fill_missing_demographics(flag):  # TODO: this function is not used and should be removed!
    #     """very unique function without much versatility intended to fill missing data from general_data.csv to
    #     pre-/intra-/postoperative.csv in the ./data folder"""
    #
    #     file_general = General.import_dataframe('general_data.csv', separator_csv=',')
    #
    #     for index, row in file_general.iterrows():
    #         General.synchronize_data_with_general(flag, row['ID'], messagebox=False)

    @staticmethod
    def extract_subject_data(subject_id):
        """
        Extract data for a subject from a CSV file.

        Parameters:
        - subject_id (str): The ID of the subject.

        Returns:
        - df (pd.DataFrame): Extracted dataframe with the data.
        """
        # missing_values = ['n/a', 'na', '--'] # has been used in previous versions
        df = General.import_dataframe(os.path.join(FILEDIR, 'general_data.csv'))
        df = df.loc[df['ID'] == subject_id]
        return df


def check_nan(x):
    if isinstance(x, str):
        return False
    elif isinstance(x, int) or isinstance(x, float):
        return math.isnan(x)
    else:
        raise Exception("Neither string nor number")
