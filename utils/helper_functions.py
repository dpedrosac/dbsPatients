#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rstr
import csv
import os
import shutil

import pandas as pds
from dependencies import ROOTDIR, FILEDIR
from PyQt5.QtWidgets import QMessageBox


class General:
    def __init__(self, _debug=False):
        pass

    @staticmethod
    def generate_code(size_array):
        """generates a code consisting of a random combination of letters, numbers and special characters; ';' and ','
        are omitted to avoid confusion in 'csv-files' """
        re_expression = '[a-zA-Z0-9_!#%$§]{}'.format('{%s}' % str(size_array))
        return rstr.xeger(re_expression)

    @staticmethod
    def import_dataframe(filename, separator_csv=';'):
        """returns pandas dataframe from csv"""

        filename_total = os.path.join(FILEDIR, filename)
        if not os.path.isfile(filename_total):
            print('\t Filename: {} not found. Please double-check!'.format(filename_total))
        df = pds.read_csv(filename_total, sep=separator_csv, on_bad_lines='skip')

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
        """reads data from temporary information"""

        try:
            subj_details = pds.read_csv(os.path.join(ROOTDIR, 'temp', default_filename))  # Read currently used subj.
        except FileNotFoundError:
            print('Data not found! Please make sure that a file named "current_subj.csv" exists in the "temp" folder')
            subj_details = []

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
            idxPID = data_all.index[data_all['PID'] == int(pid2lookfor)].to_list()
            data_subj = data_all.iloc[idxPID]
        except FileNotFoundError:
            print('No file names {} found, creating new file from template in {}/.install '.format(file2read, ROOTDIR))
            file2write = os.path.join(ROOTDIR, '.install', '{}_template.csv'.format(flag))
            shutil.copyfile(file2read, file2write)
            data_subj = []

        return data_subj

    @staticmethod
    def synchronize_data_with_general(flag, id2lookfor, messagebox=True):
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
            file2change['Gender'].loc[int(k)] = int(df_general['Gender'].iloc[idx1])
            file2change['PID'].loc[int(k)] = int(df_general['PID_ORBIS'].iloc[idx1])

        if messagebox:
            Output.msg_box(text='There were changes in the file \n\t{} \nfor subj\n\t{}.\n Please '
                                'confirm to continue'.format('{}.csv'.format(flag),
                                                             int(df_general['PID_ORBIS'].iloc[idx1])),
                           title='Changed data in {}.csv'.format(flag), flag='Warning')
        file2change.to_csv(os.path.join(FILEDIR, '{}.csv'.format(flag)), index=False)

        return


class Content:
    def __init__(self, _debug=False):
        pass

    @staticmethod
    def extract_saved_data(condition):
        """ defines a list of columns for the csv files in the data folder; if id not found,
        dictionary remains empty"""

        subj_id = General.read_current_subj().id[0] # reads data from curent_subj (saved in ./tmp)
        df = General.import_dataframe('{}.csv'.format(condition), separator_csv=',')
        if df.shape[1] == 1:
            df = General.import_dataframe('{}.csv'.format(condition), separator_csv=';')
        df_subj = df.iloc[df.index[df['ID'] == subj_id].tolist()].to_dict('list')

        # Only filter the data if the condition is "postoperative" and a follow-up interval is provided
        if condition == 'postoperative' and followup_interval is not None:
            df_subj = df[df['Reason_postop'] == followup_interval]
        else:
            df_subj = df

        # Filter the data by the subject id
        df_subj = df_subj[df_subj['ID'] == subj_id]

        # Convert the filtered dataframe to a dictionary
        df_subj = df_subj.to_dict('list')



        list_preop = ["ID", "PID", "Gender", "Diagnosis_preop", "First_Diagnosed_preop",
                      "Admission_preop", "Dismissal_preop", "Report_preop", "UPDRS_On_preop",
                      "UPDRS_Off_preop", "Video_preop", "Video_File_preop", "MRI_preop", "fpcit_spect_preop",
                      "NMSQ_preop", "MoCa_preop", "DemTect_preop", "MMST_preop", "PDQ8_preop",
                      "BDI2_preop", "PDQ39_preop", "Outpat_Contact_preop", "nch_preop", "Briefing_preop",
                      "Briefing_Doctor_preop", "DBS_Conference_preop", "Decision_DBS_preop", "LEDD_preop", "Levodopa_Carbidopa_preop",
                      "Levodopa_Carbidopa_CR_preop", "Entacapone_preop", "Tolcapone_preop", "Pramipexole_preop", "Ropinirole_preop",
                      "Rotigotine_preop", "Selegiline_oral_preop", "Selegiline_sublingual_preop",
                      "Rasagiline_preop", "Amantadine_preop", "Apomorphine_preop", "Piribedil_preop", "Safinamide_preop",
                      "Opicapone_preop", "Other_preop", "UPDRSII_preop", "H&Y_preop", "HRUQ_preop",
                      "EQ5D_preop", "S&E_preop", "icVRCS_preop", "inexVRCS_preop", "Notes_preop",
                     ]

        list_intraop = ["ID", "Gender", "pat_contact_intraop", "Diagnosis", "sugery_no_intraop",
                        "Admission_intraop", "Dismissal_intraop", "admission_Nch_intraop", "dismissal_NCh_intraop", "report_file_NCh_intraop",
                        "report_file_NR_intraop", "awake_intraop", "surgery_date_intraop", "target_intraop", "electrode_intraop",
                        "IPG_intraop", "no_traj_intraop", "neur_test_intraop", "targetL1_intraop", "targetL2_intraop",
                        "targetL3_intraop", "targetL4_intraop", "targetL5_intraop", "targetL6_intraop", "targetL7_intraop",
                        "targetL8_intraop", "targetR1_intraop", "targetR2_intraop", "targetR3_intraop", "targetR4_intraop",
                        "targetR5_intraop", "targetR6_intraop", "targetR7_intraop", "targetR8_intraop", "protocol_intraop",
                        "protocol_file_intraop", "op_duration_intraop", "LEDD_intraop", "Levodopa_Carbidopa_intraop", "Levodopa_Carbidopa_CR_intraop",
                        "Entacapone_intraop", "Tolcapone_intraop", "Pramipexole_intraop", "Ropinirole_intraop", "Rotigotine_intraop",
                        "Selegiline,_oral_intraop", "Selegiline,_sublingual_intraop", "Rasagiline_intraop", "Amantadine_intraop", "Apomorphine_intraop",
                        "Piribedil_intraop", "Safinamid_intraop", "Opicapone_intraop", "Other_intraop", "Perc0_intraop",
                        "Perc1_intraop", "Perc2_intraop", "Perc3_intraop", "Perc4_intraop", "Perc5_intraop",
                        "Perc6_intraop", "Perc7_intraop", "Perc8_intraop", "Perc9_intraop", "Perc10_intraop",
                        "Perc11_intraop", "Perc12_intraop", "Perc13_intraop", "Perc14_intraop", "Perc15_intraop",
                        "AmplL_intraop", "AmplR_intraop", "PWL_intraop", "PWR_intraop", "FreqL_intraop",
                        "FreqR_intraop", "CTscan_intraop", "activation_visit_intraop", "implantation_visit_intraop", "incl_qualiPA_intraop",
                        "DBS_intraop", "Comments_intraop"
                        ]

        list_postop = ["ID", "PID", "Gender", "Diagnosis_postop", "Date_postop",
                       "Admission_NCh_postop", "Admission_NR_postop", "Dismissal_NR_postop", "Dismissal_NCh_postop", "Report_File_NCh_postop",
                       "Report_File_NR_postop", "Reason_postop", "Using_Programmer_postop", "CTscan_postop", "Battery_Replacement_postop",
                       "Planned_Visit_postop", "Qualipa_Visit_postop", "Surgery_Date_postop", "UPDRSIII_On_postop", "UPDRSIII_Off_postop",
                       "UPDRSII_postop", "H&Y_postop", "EQ5D_postop", "MoCa_postop", "DemTect_postop",
                       "TSS_postop", "CGIG_clinician_cargiver_postop", "CGIG_patient_postop", "MMST_postop", "PDQ8_postop",
                       "BDI2_postop", "PDQ39_postop", "NMSQ_postop", "S&E_postop", "LEDD_postop",
                       "Levodopa/Carbidopa_postop", "Levodopa/Carbidopa_CR_postop", "Entacapone_postop", "Tolcapone_postop", "Pramipexole_postop",
                       "Ropinirole_postop", "Rotigotine_postop", "Selegiline_oral_postop", "Selegiline_sublingual_postop", "Rasagiline_postop",
                       "Amantadine_postop", "Apomorphine_postop", "Piribedil_postop", "Safinamid_postop", "Ongentys_postop",
                       "Other_postop", "Perc1_postop", "Perc2_postop", "Perc3_postop", "Perc4_postop",
                       "Perc5_postop", "Perc6_postop", "Perc7_postop", "Perc8_postop", "Perc9_postop",
                       "Perc10_postop", "Perc11_postop", "Perc12_postop", "Perc13_postop", "Perc14_postop",
                       "Perc15_postop", "Perc16_postop", "AmplL_postop", "AmplR_postop", "PWL_postop",
                       "PWR_postop", "FreqL_postop","FreqR_postop", "UPDRS1_postop", "UPDRS4_postop",
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


class Clean:
    def __init__(self, _debug=False):
        pass

    @staticmethod
    def fill_missing_demographics(flag):
        """very unique function without much versatility intended to fill missing data from general_data.csv to
        pre-/intra-/postoperative.csv in the ./data folder"""

        file_general = General.import_dataframe('general_data.csv', separator_csv=',')
        if file_general.shape[1] == 1:  # avoids problems with comma-separated vs. semicolon-separated csv-files
            file_general = General.import_dataframe('general_data.csv', separator_csv=';')

        for index, row in file_general.iterrows():
            General.synchronize_data_with_general(flag, row['ID'], messagebox=False)

    @staticmethod
    def get_GeneralData(columns_to_extract=['PID_ORBIS', 'Gender', 'diagnosis']):
        """some data is not stored in the pre-/intra-/postoperative data, so that this function looks for the
        subject of interest and extracts this data"""

        df_general = General.import_dataframe('general_data.csv', separator_csv=',')
        if df_general.shape[1] == 1:  # avoids problems with comma-separated vs. semicolon-separated csv-files
            df_general = General.import_dataframe('general_data.csv', separator_csv=';')

        subj_id = General.read_current_subj().id[0]  # reads data from curent_subj (saved in ./tmp)

        df_extracted = df_general[columns_to_extract]
        df_subj = df_extracted.iloc[df_general.index[df_general['ID'] == subj_id].tolist()]

        return df_subj
