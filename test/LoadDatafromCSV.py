import pandas as pd


# LE: changes work with python 3.11
class Data:
    def __init__(self, path: str):
        self.df_data = pd.read_csv(path)

    def get_data_from_PID(self, PID: int):
        d = self.df_data.loc[self.df_data['PID_ORBIS'] == PID]
        print("Debug: Found data for PID", PID, ":", d)  # Debugging-Ausgabe hinzugefügt
        if len(d) == 0:
            print("Debug: No data found for PID", PID)
        #       elif len(d) > 1:
        #          print("Debug: Multiple PIDs with same value")
        else:
            return d


#  def get_data_from_PID(self, PID: int):
#     d = self.df_data.loc[self.df_data['PID_ORBIS'] == PID]
#    if len(d) > 1:
#       print("multiple PIDs with same value")
#  else:
#     return d


# class Postoperative_data(Data):
#   def __init__(self, path: str, PID: int):
#      super().__init__(path)
#     self.d = self.get_data_from_PID(PID)
# TODO: Fehlerbehandlung zB. id nicht vorhanden
class Postoperative_data(Data):
    def __init__(self, path: str, PID: int):
        super().__init__(path)
        self.d = self.get_data_from_PID(PID)
        if self.d is not None:
            self.ID = self.d.loc[self.d.index[0], 'ID']
            self.PID_ORBIS = self.d.loc[self.d.index[0], "PID_ORBIS"]
        # Add similar checks for other attributes here...
        else:
            print(f"Keine Daten für PID {PID} gefunden.")
            return

        # class Postoperative_data(Data):
        #   def __init__(self, path: str, PID: int):
        #      super().__init__(path)
        #     self.d = self.get_data_from_PID(PID)
        #    if self.d is not None:
        #        self.ID = self.d.loc[self.d.index[0], 'ID']
        #        self.PID_ORBIS = self.d.loc[self.d.index[0], "PID_ORBIS"]

        #   else:
        #      print(f"Keine Daten für PID {PID} gefunden.")

        print(self.d)

        self.ID = self.d.loc[self.d.index[0], 'ID']
        self.PID_ORBIS = self.d.loc[self.d.index[0], "PID_ORBIS"]
        self.Gender = self.d.loc[self.d.index[0], "Gender"]
        self.Diagnosis_postop = self.d.loc[self.d.index[0], "Diagnosis_postop"]
        self.Date_postop = self.d.loc[self.d.index[0], "Date_postop"]
        self.Admission_NCh_postop = self.d.loc[self.d.index[0], "Admission_NCh_postop"]
        self.Admission_NR_postop = self.d.loc[self.d.index[0], "Admission_NR_postop"]
        self.Dismissal_NR_postop = self.d.loc[self.d.index[0], "Dismissal_NR_postop"]
        self.Dismissal_NCh_postop = self.d.loc[self.d.index[0], "Dismissal_NCh_postop"]
        self.Report_File_NCh_postop = self.d.loc[self.d.index[0], "Report_File_NCh_postop"]
        self.Report_File_NR_postop = self.d.loc[self.d.index[0], "Report_File_NR_postop"]
        self.Reason_postop = self.d.loc[self.d.index[0], "Reason_postop"]
        self.Using_Programmer_postop = self.d.loc[self.d.index[0], "Using_Programmer_postop"]
        self.CTscan_postop = self.d.loc[self.d.index[0], "CTscan_postop"]
        self.Battery_Replacement_postop = self.d.loc[self.d.index[0], "Battery_Replacement_postop"]
        self.Planned_Visit_postop = self.d.loc[self.d.index[0], "Planned_Visit_postop"]
        self.Qualipa_Visit_postop = self.d.loc[self.d.index[0], "Qualipa_Visit_postop"]
        self.Surgery_Date_postop = self.d.loc[self.d.index[0], "Surgery_Date_postop"]
        self.UPDRSIII_On_postop = self.d.loc[self.d.index[0], "UPDRSIII_On_postop"]
        self.UPDRSIII_Off_postop = self.d.loc[self.d.index[0], "UPDRSIII_Off_postop"]
        self.UPDRSII_postop = self.d.loc[self.d.index[0], "UPDRSII_postop"]
        self.HuY_postop = self.d.loc[self.d.index[0], "H&Y_postop"]
        self.EQ5D_postop = self.d.loc[self.d.index[0], "EQ5D_postop"]
        self.MoCa_postop = self.d.loc[self.d.index[0], "MoCa_postop"]
        self.DemTect_postop = self.d.loc[self.d.index[0], "DemTect_postop"]
        self.TSS_postop = self.d.loc[self.d.index[0], "TSS_postop"]
        self.CGIG_clinician_cargiver_postop = self.d.loc[self.d.index[0], "CGIG_clinician_cargiver_postop"]
        self.CGIG_patient_postop = self.d.loc[self.d.index[0], "CGIG_patient_postop"]
        self.MMST_postop = self.d.loc[self.d.index[0], "MMST_postop"]
        self.PDQ8_postop = self.d.loc[self.d.index[0], "PDQ8_postop"]
        self.BDI2_postop = self.d.loc[self.d.index[0], "BDI2_postop"]
        self.PDQ39_postop = self.d.loc[self.d.index[0], "PDQ39_postop"]
        self.NMSQ_postop = self.d.loc[self.d.index[0], "NMSQ_postop"]
        self.SuE_postop = self.d.loc[self.d.index[0], "S&E_postop"]
        self.LEDD_postop = self.d.loc[self.d.index[0], "LEDD_postop"]
        self.Levodopa_Carbidopa_postop = self.d.loc[self.d.index[0], "Levodopa_Carbidopa_postop"]
        self.Levodopa_Carbidopa_CR_postop = self.d.loc[self.d.index[0], "Levodopa_Carbidopa_CR_postop"]
        self.Entacapone_postop = self.d.loc[self.d.index[0], "Entacapone_postop"]
        self.Tolcapone_postop = self.d.loc[self.d.index[0], "Tolcapone_postop"]
        self.Pramipexole_postop = self.d.loc[self.d.index[0], "Pramipexole_postop"]
        self.Ropinirole_postop = self.d.loc[self.d.index[0], "Ropinirole_postop"]
        self.Rotigotin_postop = self.d.loc[self.d.index[0], "Rotigotin_postop"]
        self.Selegilin_oral_postop = self.d.loc[self.d.index[0], "Selegilin_oral_postop"]
        self.Selegilin_sublingual_postop = self.d.loc[self.d.index[0], "Selegilin_sublingual_postop"]
        self.Rasagilin_postop = self.d.loc[self.d.index[0], "Rasagilin_postop"]
        self.Amantadine_postop = self.d.loc[self.d.index[0], "Amantadine_postop"]
        self.Apomorphine_postop = self.d.loc[self.d.index[0], "Apomorphine_postop"]
        self.Piribedil_postop = self.d.loc[self.d.index[0], "Piribedil_postop"]
        self.Safinamid_postop = self.d.loc[self.d.index[0], "Safinamid_postop"]
        self.Opicapone_postop = self.d.loc[self.d.index[0], "Opicapone_postop"]
        self.Other_postop = self.d.loc[self.d.index[0], "Other_postop"]
        # perc_postop as array for easy access
        self.Perc_postop = []
        for i in range(1, 17):
            column_name = "Perc{}_postop".format(i)
            value = self.d.loc[self.d.index[0], column_name]
            self.Perc_postop.append(value)

        self.AmplL_postop = self.d.loc[self.d.index[0], "AmplL_postop"]
        self.AmplR_postop = self.d.loc[self.d.index[0], "AmplR_postop"]
        self.PWL_postop = self.d.loc[self.d.index[0], "PWL_postop"]
        self.PWR_postop = self.d.loc[self.d.index[0], "PWR_postop"]
        self.FreqL_postop = self.d.loc[self.d.index[0], "FreqL_postop"]
        self.FreqR_postop = self.d.loc[self.d.index[0], "FreqR_postop"]
        self.UPDRS1_postop = self.d.loc[self.d.index[0], "UPDRS1_postop"]
        self.UPDRS4_postop = self.d.loc[self.d.index[0], "UPDRS4_postop"]
        self.UPDRSon_postop = self.d.loc[self.d.index[0], "UPDRSon_postop"]
        self.UDDRSoff_postop = self.d.loc[self.d.index[0], "UDDRSoff_postop"]
        self.TRSon_postop = self.d.loc[self.d.index[0], "TRSon_postop"]
        self.TRSoff_postop = self.d.loc[self.d.index[0], "TRSoff_postop"]
        self.AE_postop = self.d.loc[self.d.index[0], "AE_postop"]
        self.Comments_postop = self.d.loc[self.d.index[0], "Comments_postop"]
        self.DBS_postop = self.d.loc[self.d.index[0], "DBS_postop"]
        self.HRUQ_postop = self.d.loc[self.d.index[0], "HRUQ_postop"]
        self.UPDRSOff_postop = self.d.loc[self.d.index[0], "UPDRSOff_postop"]
        self.UDDRSOn_postop = self.d.loc[self.d.index[0], "UDDRSOn_postop"]
        self.Last_Revision_postop = self.d.loc[self.d.index[0], "Last_Revision_postop"]
        self.Outpatient_Contact_postop = self.d.loc[self.d.index[0], "Outpatient_Contact_postop"]


class Intraoperative_data(Data):
    def __init__(self, path: str, PID: int):
        super().__init__(path)
        self.d = self.get_data_from_PID(PID)
        if self.d is not None:
            self.ID = self.d.loc[self.d.index[0], 'ID']
            self.PID_ORBIS = self.d.loc[self.d.index[0], "PID_ORBIS"]
        # Add similar checks for other attributes here...
        else:
            print(f"Keine Daten für PID {PID} gefunden.")
            return

        self.ID = self.d.loc[0, "ID"]
        self.Gender = self.d.loc[0, "Gender"]
        self.pat_contact_intraop = self.d.loc[0, "pat_contact_intraop"]
        self.Diagnosis = self.d.loc[0, "Diagnosis"]
        self.sugery_no_intraop = self.d.loc[0, "sugery_no_intraop"]
        self.Admission_intraop = self.d.loc[0, "Admission_intraop"]
        self.Dismissal_intraop = self.d.loc[0, "Dismissal_intraop"]
        self.admission_Nch_intraop = self.d.loc[0, "admission_Nch_intraop"]
        self.dismissal_NCh_intraop = self.d.loc[0, "dismissal_NCh_intraop"]
        self.report_file_NCh_intraop = self.d.loc[0, "report_file_NCh_intraop"]
        self.report_file_NR_intraop = self.d.loc[0, "report_file_NR_intraop"]
        self.awake_intraop = self.d.loc[0, "awake_intraop"]
        self.surgery_date_intraop = self.d.loc[0, "surgery_date_intraop"]
        self.target_intraop = self.d.loc[0, "target_intraop"]
        self.electrode_intraop = self.d.loc[0, "electrode_intraop"]
        self.IPG_intraop = self.d.loc[0, "IPG_intraop"]
        self.no_traj_intraop = self.d.loc[0, "no_traj_intraop"]
        self.neur_test_intraop = self.d.loc[0, "neur_test_intraop"]

        self.targetL_intraop = []
        for i in range(1, 9):
            column_name = 'targetL{}_intraop'.format(i)
            value = self.d.loc[self.d.index[0], column_name]
            self.targetL_intraop.append(value)

        self.targetL1_intraop = self.d.loc[0, "targetL1_intraop"]
        self.targetL2_intraop = self.d.loc[0, "targetL2_intraop"]
        self.targetL3_intraop = self.d.loc[0, "targetL3_intraop"]
        self.targetL4_intraop = self.d.loc[0, "targetL4_intraop"]
        self.targetL5_intraop = self.d.loc[0, "targetL5_intraop"]
        self.targetL6_intraop = self.d.loc[0, "targetL6_intraop"]
        self.targetL7_intraop = self.d.loc[0, "targetL7_intraop"]
        self.targetL8_intraop = self.d.loc[0, "targetL8_intraop"]

        self.targetR_intraop = []
        for i in range(1, 9):
            column_name = 'targetR{}_intraop'.format(i)
            value = self.d.loc[self.d.index[0], column_name]
            self.targetR_intraop.append(value)
        self.targetR1_intraop = self.d.loc[0, "targetR1_intraop"]
        self.targetR2_intraop = self.d.loc[0, "targetR2_intraop"]
        self.targetR3_intraop = self.d.loc[0, "targetR3_intraop"]
        self.targetR4_intraop = self.d.loc[0, "targetR4_intraop"]
        self.targetR5_intraop = self.d.loc[0, "targetR5_intraop"]
        self.targetR6_intraop = self.d.loc[0, "targetR6_intraop"]
        self.targetR7_intraop = self.d.loc[0, "targetR7_intraop"]
        self.targetR8_intraop = self.d.loc[0, "targetR8_intraop"]

        self.protocol_intraop = self.d.loc[0, "protocol_intraop"]
        self.protocol_file_intraop = self.d.loc[0, "protocol_file_intraop"]
        self.op_duration_intraop = self.d.loc[0, "op_duration_intraop"]
        self.LEDD_intraop = self.d.loc[0, "LEDD_intraop"]
        self.Levodopa_Carbidopa_intraop = self.d.loc[0, "Levodopa_Carbidopa_intraop"]
        self.Levodopa_Carbidopa_CR_intraop = self.d.loc[0, "Levodopa_Carbidopa_CR_intraop"]
        self.Entacapone_intraop = self.d.loc[0, "Entacapone_intraop"]
        self.Tolcapone_intraop = self.d.loc[0, "Tolcapone_intraop"]
        self.Pramipexole_intraop = self.d.loc[0, "Pramipexole_intraop"]
        self.Ropinirole_intraop = self.d.loc[0, "Ropinirole_intraop"]
        self.Rotigotine_intraop = self.d.loc[0, "Rotigotine_intraop"]
        self.Selegiline_oral_intraop = self.d.loc[0, "Selegiline_oral_intraop"]
        self.Selegiline_sublingual_intraop = self.d.loc[0, "Selegiline_sublingual_intraop"]
        self.Rasagiline_intraop = self.d.loc[0, "Rasagiline_intraop"]
        self.Amantadine_intraop = self.d.loc[0, "Amantadine_intraop"]
        self.Apomorphine_intraop = self.d.loc[0, "Apomorphine_intraop"]
        self.Piribedil_intraop = self.d.loc[0, "Piribedil_intraop"]
        self.Safinamid_intraop = self.d.loc[0, "Safinamid_intraop"]
        self.Opicapone_intraop = self.d.loc[0, "Opicapone_intraop"]
        self.Other_intraop = self.d.loc[0, "Other_intraop"]
        self.Perc0_intraop = self.d.loc[0, "Perc0_intraop"]
        self.Perc1_intraop = self.d.loc[0, "Perc1_intraop"]
        self.Perc2_intraop = self.d.loc[0, "Perc2_intraop"]
        self.Perc3_intraop = self.d.loc[0, "Perc3_intraop"]
        self.Perc4_intraop = self.d.loc[0, "Perc4_intraop"]
        self.Perc5_intraop = self.d.loc[0, "Perc5_intraop"]
        self.Perc6_intraop = self.d.loc[0, "Perc6_intraop"]
        self.Perc7_intraop = self.d.loc[0, "Perc7_intraop"]
        self.Perc8_intraop = self.d.loc[0, "Perc8_intraop"]
        self.Perc9_intraop = self.d.loc[0, "Perc9_intraop"]
        self.Perc10_intraop = self.d.loc[0, "Perc10_intraop"]
        self.Perc11_intraop = self.d.loc[0, "Perc11_intraop"]
        self.Perc12_intraop = self.d.loc[0, "Perc12_intraop"]
        self.Perc13_intraop = self.d.loc[0, "Perc13_intraop"]
        self.Perc14_intraop = self.d.loc[0, "Perc14_intraop"]
        self.Perc15_intraop = self.d.loc[0, "Perc15_intraop"]
        self.AmplL_intraop = self.d.loc[0, "AmplL_intraop"]
        self.AmplR_intraop = self.d.loc[0, "AmplR_intraop"]
        self.PWL_intraop = self.d.loc[0, "PWL_intraop"]
        self.PWR_intraop = self.d.loc[0, "PWR_intraop"]
        self.FreqL_intraop = self.d.loc[0, "FreqL_intraop"]
        self.FreqR_intraop = self.d.loc[0, "FreqR_intraop"]
        self.CTscan_intraop = self.d.loc[0, "CTscan_intraop"]
        self.activation_visit_intraop = self.d.loc[0, "activation_visit_intraop"]
        self.implantation_visit_intraop = self.d.loc[0, "implantation_visit_intraop"]
        self.incl_qualiPA_intraop = self.d.loc[0, "incl_qualiPA_intraop"]
        self.DBS_intraop = self.d.loc[0, "DBS_intraop"]
        self.Comments_intraop = self.d.loc[0, "Comments_intraop"]


def main():
    print("Using PID:")
    data = Postoperative_data(r'C:\Users\toast\OneDrive\Desktop\GitHub\dbsPatients\data\postoperative.csv', 698767)
    if data.d is not None:
        print(data.Diagnosis_postop)
    else:
        print("Keine Daten gefunden.")


if __name__ == '__main__':
    main()
# def main():
#   data = Postoperative_data(r'data/postoperative.csv', 1399948)
#  print(data.Diagnosis_postop)
