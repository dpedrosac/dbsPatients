class Lists:

    # =================== General_data ====================

    diagnosis = ['Bradykinetic-rigid parkinson-syndrome (PD1)',
                                         'Tremordominant parkinson-syndrome(PD2)',
                                         'Mixed-type parkinson-syndrome (PD3)',
                                         'Dystonia (DT)',
                                         'Essential tremor (ET)', 'Equivalence type parkinson-syndrome',
                                         'Hypokinetic-rigid type parkinson-syndrome',
                                         'Akinetic-rigid type parkinson-syndrome',
                                         'Other']

    ## ================= Preoperative =====================

    preoperative_template_fields = [
        "ID", "PID_ORBIS", "Gender", "Diagnosis_preop", "First_Diagnosed_preop", "Admission_preop", "Dismissal_preop",
        "nch_preop", "Outpat_Contact_preop", "DBS_Conference_preop", "Report_preop", "Video_preop", "Video_File_preop",
        "MRI_preop", "Decision_DBS_preop", "UPDRS_On_preop", "UPDRS_Off_preop", "fpcit_spect_preop", "NMSQ_preop",
        "MoCa_preop", "DemTect_preop", "MMST_preop", "PDQ8_preop", "BDI2_preop", "PDQ39_preop", "Briefing_preop",
        "Briefing_Doctor_preop", "LEDD_preop", "Levodopa_Carbidopa_preop", "Levodopa_Carbidopa_CR_preop",
        "Entacapone_preop", "Tolcapone_preop", "Pramipexole_preop", "Ropinirole_preop", "Rotigotine_preop",
        "Selegiline_oral_preop", "Selegiline_sublingual_preop", "Rasagiline_preop", "Amantadine_preop",
        "Apomorphine_preop",
        "Piribedil_preop", "Safinamide_preop", "Opicapone_preop", "Other_preop", "UPDRSII_preop", "H&Y_preop",
        "HRUQ_preop",
        "EQ5D_preop", "S&E_preop", "icVRCS_preop", "inexVRCS_preop", "Notes_preop"
    ]

    dates_preoperative = ["First_Diagnosed_preop", "Admission_preop", "Dismissal_preop",
        "nch_preop", "Outpat_Contact_preop", "DBS_Conference_preop"]

    checkboxes_preoperative = ["Report_preop", "Decision_DBS_preop", "icVRCS_preop", "inexVRCS_preop",
                  "Video_preop", "MRI_preop", "fpcit_spect_preop"]


    tests_preoperative = ["UPDRS_On_preop", "UPDRS_Off_preop", "NMSQ_preop",
        "MoCa_preop", "DemTect_preop", "MMST_preop", "PDQ8_preop", "BDI2_preop", "PDQ39_preop", "UPDRSII_preop", "H&Y_preop",
        "HRUQ_preop", "EQ5D_preop", "S&E_preop"]


    medication_preoperative = ["Levodopa_Carbidopa_preop", "Levodopa_Carbidopa_CR_preop",
        "Entacapone_preop", "Tolcapone_preop", "Pramipexole_preop", "Ropinirole_preop", "Rotigotine_preop",
        "Selegiline_oral_preop", "Selegiline_sublingual_preop", "Rasagiline_preop", "Amantadine_preop",
        "Apomorphine_preop",
        "Piribedil_preop", "Safinamide_preop", "Opicapone_preop", "Other_preop"]

    not_used_preoperative = ['Briefing_preop', 'Briefing_Doctor_preop', 'Notes_preop', 'Video_File_preop']




# ============================ Postoperative ==============================

    postoperative_template_fields = [
        "ID", "PID_ORBIS", "Gender", "Diagnosis_postop",

        "Reason_postop",

        "Implanted_IPG", "Lead_manufacturer", "implanted_leads",

        "First_Diagnosed_postop",

        "Admission_NR_postop", "Admission_NCh_postop", "Dismissal_NR_postop", "Dismissal_NCh_postop",
        "Surgery_Date_postop", "Last_revision_postop", "Outpatient_contact_postop",

        "AE_postop",

        "Report_File_NR_postop",

        "UPDRS_On_postop", "UPDRS_Off_postop", "UPDRS1_postop", "UPDRS4_postop", "TSS_postop", "UPDRSII_postop",
        "CGIC_patient_postop", "CGIC_clinician_caregiver_postop", "NMSQ_postop", "MoCa_postop", "DemTect_postop", "MMST_postop",
        "PDQ8_postop", "BDI2_postop", "PDQ39_postop",

        "Outpat_Contact_postop",

        "Report_File_NCh_postop",

        "Briefing_postop", "Briefing_Doctor_postop", "DBS_Conference_postop", "Decision_DBS_postop",

        "LEDD_postop", "Levodopa_Carbidopa_postop",
        "Levodopa_Carbidopa_CR_postop", "Entacapone_postop", "Tolcapone_postop", "Pramipexole_postop", "Ropinirole_postop",
        "Rotigotine_postop", "Selegiline_oral_postop", "Selegiline_sublingual_postop", "Rasagiline_postop", "Amantadine_postop",
        "Apomorphine_postop", "Piribedil_postop", "Safinamide_postop", "Opicapone_postop", "Other_postop",

        "H&Y_postop","HRUQ_postop", "EQ5D_postop", "S&E_postop",

        "icVRCS_postop", "inexVRCS_postop",

        "UDDRSoff_postop", "UDDRSon_postop", "TRSon_postop", "TRSoff_postop",

        "Using_Programmer_postop", "CTscan_postop",

        "IPG_LG1_ktd", "IPG_LG2_ktd", "IPG_LG1_ano",
        "IPG_LG2_ano", "IPG_RG1_ktd", "IPG_RG2_ktd", "IPG_RG1_ano", "IPG_RG2_ano", "0_LG1_ktd", "1_LG1_ktd", "2_LG1_ktd",
        "3_LG1_ktd", "4_LG1_ktd", "5_LG1_ktd", "6_LG1_ktd", "7_LG1_ktd", "8_LG1_ktd", "9_LG1_ktd", "10_LG1_ktd", "11_LG1_ktd",
        "12_LG1_ktd", "13_LG1_ktd", "14_LG1_ktd", "15_LG1_ktd", "16_LG1_ktd", "0_LG2_ktd", "1_LG2_ktd", "2_LG2_ktd", "3_LG2_ktd",
        "4_LG2_ktd", "5_LG2_ktd", "6_LG2_ktd", "7_LG2_ktd", "8_LG2_ktd", "9_LG2_ktd", "10_LG2_ktd", "11_LG2_ktd", "12_LG2_ktd",
        "13_LG2_ktd", "14_LG2_ktd", "15_LG2_ktd", "16_LG2_ktd", "0_RG1_ktd", "1_RG1_ktd", "2_RG1_ktd", "3_RG1_ktd", "4_RG1_ktd",
        "5_RG1_ktd", "6_RG1_ktd", "7_RG1_ktd", "8_RG1_ktd", "9_RG1_ktd", "10_RG1_ktd", "11_RG1_ktd", "12_RG1_ktd", "13_RG1_ktd",
        "14_RG1_ktd", "15_RG1_ktd", "16_RG1_ktd", "0_RG2_ktd", "1_RG2_ktd", "2_RG2_ktd", "3_RG2_ktd", "4_RG2_ktd", "5_RG2_ktd",
        "6_RG2_ktd", "7_RG2_ktd", "8_RG2_ktd", "9_RG2_ktd", "10_RG2_ktd", "11_RG2_ktd", "12_RG2_ktd", "13_RG2_ktd", "14_RG2_ktd",
        "15_RG2_ktd", "16_RG2_ktd", "1a_LG1_ktd", "1b_LG1_ktd", "1c_LG1_ktd", "2a_LG1_ktd", "2b_LG1_ktd", "2c_LG1_ktd",
        "1a_LG2_ktd", "1b_LG2_ktd", "1c_LG2_ktd", "2a_LG2_ktd", "2b_LG2_ktd", "2c_LG2_ktd", "9a_RG1_ktd", "9b_RG1_ktd",
        "9c_RG1_ktd", "10a_RG1_ktd", "10b_RG1_ktd", "10c_RG1_ktd", "9a_RG2_ktd", "9b_RG2_ktd", "9c_RG2_ktd", "10a_RG2_ktd",
        "10b_RG2_ktd", "10c_RG2_ktd", "3a_LG1_ktd", "3b_LG1_ktd", "3c_LG1_ktd", "3a_LG2_ktd", "3b_LG2_ktd", "3c_LG2_ktd",
        "3a_RG1_ktd", "3b_RG1_ktd", "3c_RG1_ktd", "3a_RG2_ktd", "3b_RG2_ktd", "3c_RG2_ktd", "2a_RG1_ktd", "2b_RG1_ktd",
        "2c_RG1_ktd", "2a_RG2_ktd", "2b_RG2_ktd", "2c_RG2_ktd", "Amp_LG1", "Amp_LG2", "Freq_LG1", "Freq_LG2", "PW_LG1",
        "PW_LG2", "Amp_RG1", "Amp_RG2", "Freq_RG1", "Freq_RG2", "PW_RG1", "PW_RG2",

        "0_LG1_ano", "1_LG1_ano", "2_LG1_ano",
        "3_LG1_ano", "4_LG1_ano", "5_LG1_ano", "6_LG1_ano", "7_LG1_ano", "8_LG1_ano", "9_LG1_ano", "10_LG1_ano",
        "11_LG1_ano",
        "12_LG1_ano", "13_LG1_ano", "14_LG1_ano", "15_LG1_ano", "16_LG1_ano", "0_LG2_ano", "1_LG2_ano", "2_LG2_ano",
        "3_LG2_ano",
        "4_LG2_ano", "5_LG2_ano", "6_LG2_ano", "7_LG2_ano", "8_LG2_ano", "9_LG2_ano", "10_LG2_ano", "11_LG2_ano",
        "12_LG2_ano",
        "13_LG2_ano", "14_LG2_ano", "15_LG2_ano", "16_LG2_ano", "0_RG1_ano", "1_RG1_ano", "2_RG1_ano", "3_RG1_ano",
        "4_RG1_ano",
        "5_RG1_ano", "6_RG1_ano", "7_RG1_ano", "8_RG1_ano", "9_RG1_ano", "10_RG1_ano", "11_RG1_ano", "12_RG1_ano",
        "13_RG1_ano",
        "14_RG1_ano", "15_RG1_ano", "16_RG1_ano", "0_RG2_ano", "1_RG2_ano", "2_RG2_ano", "3_RG2_ano", "4_RG2_ano",
        "5_RG2_ano",
        "6_RG2_ano", "7_RG2_ano", "8_RG2_ano", "9_RG2_ano", "10_RG2_ano", "11_RG2_ano", "12_RG2_ano", "13_RG2_ano",
        "14_RG2_ano",
        "15_RG2_ano", "16_RG2_ano", "1a_LG1_ano", "1b_LG1_ano", "1c_LG1_ano", "2a_LG1_ano", "2b_LG1_ano", "2c_LG1_ano",
        "1a_LG2_ano", "1b_LG2_ano", "1c_LG2_ano", "2a_LG2_ano", "2b_LG2_ano", "2c_LG2_ano", "9a_RG1_ano", "9b_RG1_ano",
        "9c_RG1_ano", "10a_RG1_ano", "10b_RG1_ano", "10c_RG1_ano", "9a_RG2_ano", "9b_RG2_ano", "9c_RG2_ano",
        "10a_RG2_ano",
        "10b_RG2_ano", "10c_RG2_ano", "3a_LG1_ano", "3b_LG1_ano", "3c_LG1_ano", "3a_LG2_ano", "3b_LG2_ano",
        "3c_LG2_ano",
        "3a_RG1_ano", "3b_RG1_ano", "3c_RG1_ano", "3a_RG2_ano", "3b_RG2_ano", "3c_RG2_ano", "2a_RG1_ano", "2b_RG1_ano",
        "2c_RG1_ano", "2a_RG2_ano", "2b_RG2_ano", "2c_RG2_ano",

        "Notes_postop",

        "Planned_Visit_postop"
    ]

    dates_postoperative = ["Admission_NR_postop", "Admission_NCh_postop", "Dismissal_NR_postop", "Dismissal_NCh_postop",
        "Surgery_Date_postop", "Last_revision_postop", "Outpatient_contact_postop"]

    medication_postoperative = ["Levodopa_Carbidopa_postop",
        "Levodopa_Carbidopa_CR_postop", "Entacapone_postop", "Tolcapone_postop", "Pramipexole_postop", "Ropinirole_postop",
        "Rotigotine_postop", "Selegiline_oral_postop", "Selegiline_sublingual_postop", "Rasagiline_postop", "Amantadine_postop",
        "Apomorphine_postop", "Piribedil_postop", "Safinamide_postop", "Opicapone_postop", "Other_postop"]

    tests_postoperative = ["UPDRS_On_postop", "UPDRS_Off_postop", "UPDRS1_postop", "UPDRS4_postop", "TSS_postop", "UPDRSII_postop",
        "CGIC_patient_postop", "CGIC_clinician_caregiver_postop", "NMSQ_postop", "MoCa_postop", "DemTect_postop", "MMST_postop",
        "PDQ8_postop", "BDI2_postop", "PDQ39_postop", "H&Y_postop",
        "HRUQ_postop", "EQ5D_postop", "S&E_postop", "icVRCS_postop", "inexVRCS_postop", "UDDRSoff_postop", "UDDRSon_postop",
        "TRSon_postop", "TRSoff_postop"]

    checkboxes_postoperative = ["Report_File_NR_postop", "Report_File_NCh_postop", "Using_Programmer_postop", "CTscan_postop", "Planned_Visit_postop"]

    ae_postoperative = ["AE_postop"]

    dbs_postoperative = ["IPG_LG1_ktd", "IPG_LG2_ktd", "IPG_LG1_ano",
        "IPG_LG2_ano", "IPG_RG1_ktd", "IPG_RG2_ktd", "IPG_RG1_ano", "IPG_RG2_ano",

        "0_LG1_ktd", "1_LG1_ktd", "2_LG1_ktd",
        "3_LG1_ktd", "4_LG1_ktd", "5_LG1_ktd", "6_LG1_ktd", "7_LG1_ktd", "8_LG1_ktd", "9_LG1_ktd", "10_LG1_ktd", "11_LG1_ktd",
        "12_LG1_ktd", "13_LG1_ktd", "14_LG1_ktd", "15_LG1_ktd", "16_LG1_ktd", "0_LG2_ktd", "1_LG2_ktd", "2_LG2_ktd", "3_LG2_ktd",
        "4_LG2_ktd", "5_LG2_ktd", "6_LG2_ktd", "7_LG2_ktd", "8_LG2_ktd", "9_LG2_ktd", "10_LG2_ktd", "11_LG2_ktd", "12_LG2_ktd",
        "13_LG2_ktd", "14_LG2_ktd", "15_LG2_ktd", "16_LG2_ktd", "0_RG1_ktd", "1_RG1_ktd", "2_RG1_ktd", "3_RG1_ktd", "4_RG1_ktd",
        "5_RG1_ktd", "6_RG1_ktd", "7_RG1_ktd", "8_RG1_ktd", "9_RG1_ktd", "10_RG1_ktd", "11_RG1_ktd", "12_RG1_ktd", "13_RG1_ktd",
        "14_RG1_ktd", "15_RG1_ktd", "16_RG1_ktd", "0_RG2_ktd", "1_RG2_ktd", "2_RG2_ktd", "3_RG2_ktd", "4_RG2_ktd", "5_RG2_ktd",
        "6_RG2_ktd", "7_RG2_ktd", "8_RG2_ktd", "9_RG2_ktd", "10_RG2_ktd", "11_RG2_ktd", "12_RG2_ktd", "13_RG2_ktd", "14_RG2_ktd",
        "15_RG2_ktd", "16_RG2_ktd", "1a_LG1_ktd", "1b_LG1_ktd", "1c_LG1_ktd", "2a_LG1_ktd", "2b_LG1_ktd", "2c_LG1_ktd",
        "1a_LG2_ktd", "1b_LG2_ktd", "1c_LG2_ktd", "2a_LG2_ktd", "2b_LG2_ktd", "2c_LG2_ktd", "9a_RG1_ktd", "9b_RG1_ktd",
        "9c_RG1_ktd", "10a_RG1_ktd", "10b_RG1_ktd", "10c_RG1_ktd", "9a_RG2_ktd", "9b_RG2_ktd", "9c_RG2_ktd", "10a_RG2_ktd",
        "10b_RG2_ktd", "10c_RG2_ktd", "3a_LG1_ktd", "3b_LG1_ktd", "3c_LG1_ktd", "3a_LG2_ktd", "3b_LG2_ktd", "3c_LG2_ktd",
        "3a_RG1_ktd", "3b_RG1_ktd", "3c_RG1_ktd", "3a_RG2_ktd", "3b_RG2_ktd", "3c_RG2_ktd", "2a_RG1_ktd", "2b_RG1_ktd",
        "2c_RG1_ktd", "2a_RG2_ktd", "2b_RG2_ktd", "2c_RG2_ktd",

        "0_LG1_ano", "1_LG1_ano", "2_LG1_ano",
        "3_LG1_ano", "4_LG1_ano", "5_LG1_ano", "6_LG1_ano", "7_LG1_ano", "8_LG1_ano", "9_LG1_ano", "10_LG1_ano", "11_LG1_ano",
        "12_LG1_ano", "13_LG1_ano", "14_LG1_ano", "15_LG1_ano", "16_LG1_ano", "0_LG2_ano", "1_LG2_ano", "2_LG2_ano", "3_LG2_ano",
        "4_LG2_ano", "5_LG2_ano", "6_LG2_ano", "7_LG2_ano", "8_LG2_ano", "9_LG2_ano", "10_LG2_ano", "11_LG2_ano", "12_LG2_ano",
        "13_LG2_ano", "14_LG2_ano", "15_LG2_ano", "16_LG2_ano", "0_RG1_ano", "1_RG1_ano", "2_RG1_ano", "3_RG1_ano", "4_RG1_ano",
        "5_RG1_ano", "6_RG1_ano", "7_RG1_ano", "8_RG1_ano", "9_RG1_ano", "10_RG1_ano", "11_RG1_ano", "12_RG1_ano", "13_RG1_ano",
        "14_RG1_ano", "15_RG1_ano", "16_RG1_ano", "0_RG2_ano", "1_RG2_ano", "2_RG2_ano", "3_RG2_ano", "4_RG2_ano", "5_RG2_ano",
        "6_RG2_ano", "7_RG2_ano", "8_RG2_ano", "9_RG2_ano", "10_RG2_ano", "11_RG2_ano", "12_RG2_ano", "13_RG2_ano", "14_RG2_ano",
        "15_RG2_ano", "16_RG2_ano", "1a_LG1_ano", "1b_LG1_ano", "1c_LG1_ano", "2a_LG1_ano", "2b_LG1_ano", "2c_LG1_ano",
        "1a_LG2_ano", "1b_LG2_ano", "1c_LG2_ano", "2a_LG2_ano", "2b_LG2_ano", "2c_LG2_ano", "9a_RG1_ano", "9b_RG1_ano",
        "9c_RG1_ano", "10a_RG1_ano", "10b_RG1_ano", "10c_RG1_ano", "9a_RG2_ano", "9b_RG2_ano", "9c_RG2_ano", "10a_RG2_ano",
        "10b_RG2_ano", "10c_RG2_ano", "3a_LG1_ano", "3b_LG1_ano", "3c_LG1_ano", "3a_LG2_ano", "3b_LG2_ano", "3c_LG2_ano",
        "3a_RG1_ano", "3b_RG1_ano", "3c_RG1_ano", "3a_RG2_ano", "3b_RG2_ano", "3c_RG2_ano", "2a_RG1_ano", "2b_RG1_ano",
        "2c_RG1_ano", "2a_RG2_ano", "2b_RG2_ano", "2c_RG2_ano",
                         
        "Amp_LG1", "Amp_LG2", "Freq_LG1", "Freq_LG2", "PW_LG1",
        "PW_LG2", "Amp_RG1", "Amp_RG2", "Freq_RG1", "Freq_RG2", "PW_RG1", "PW_RG2"]

    not_used_postoperative = ["First_Diagnosed_postop", "Outpat_Contact_postop", "Briefing_postop",
                              "Briefing_Doctor_postop", "DBS_Conference_postop", "Decision_DBS_postop",
                              "Notes_postop"]


# ================================= Intraoperative ========================================
    intraoperative_template_fields = [
        "ID", "PID_ORBIS", "Gender", "Diagnosis_preop", "Implanted_IPG", "Lead_manufacturer", "implanted_leads",
        "pat_contact_intraop", "sugery_no_intraop", "Admission_intraop", "Dismissal_intraop", "admission_Nch_intraop",
        "dismissal_NCh_intraop", "report_file_NCh_intraop", "report_file_NR_intraop", "awake_intraop",
        "surgery_date_intraop",
        "target_intraop", "no_traj_intraop", "neur_test_intraop", "protocol_intraop", "protocol_file_intraop",
        "op_duration_intraop", "LEDD_intraop", "Levodopa_Carbidopa_intraop", "Levodopa_Carbidopa_CR_intraop",
        "Entacapone_intraop", "Tolcapone_intraop", "Pramipexole_intraop", "Ropinirole_intraop", "Rotigotine_intraop",
        "Selegiline_oral_intraop", "Selegiline_sublingual_intraop", "Rasagiline_intraop", "Amantadine_intraop",
        "Apomorphine_intraop", "Piribedil_intraop", "Safinamide_intraop", "Opicapone_intraop", "Other_intraop",
        "CTscan_intraop", "activation_visit_intraop", "implantation_visit_intraop", "incl_qualiPA_intraop",
        "DBS_intraop",
        "IPG_LG1_ktd", "IPG_LG2_ktd", "IPG_LG1_ano", "IPG_LG2_ano", "IPG_RG1_ktd", "IPG_RG2_ktd", "IPG_RG1_ano",
        "IPG_RG2_ano",
        "0_LG1_ktd", "1_LG1_ktd", "2_LG1_ktd", "3_LG1_ktd", "4_LG1_ktd", "5_LG1_ktd", "6_LG1_ktd", "7_LG1_ktd",
        "8_LG1_ktd",
        "9_LG1_ktd", "10_LG1_ktd", "11_LG1_ktd", "12_LG1_ktd", "13_LG1_ktd", "14_LG1_ktd", "15_LG1_ktd", "16_LG1_ktd",
        "0_LG2_ktd", "1_LG2_ktd", "2_LG2_ktd", "3_LG2_ktd", "4_LG2_ktd", "5_LG2_ktd", "6_LG2_ktd", "7_LG2_ktd",
        "8_LG2_ktd",
        "9_LG2_ktd", "10_LG2_ktd", "11_LG2_ktd", "12_LG2_ktd", "13_LG2_ktd", "14_LG2_ktd", "15_LG2_ktd", "16_LG2_ktd",
        "0_RG1_ktd", "1_RG1_ktd", "2_RG1_ktd", "3_RG1_ktd", "4_RG1_ktd", "5_RG1_ktd", "6_RG1_ktd", "7_RG1_ktd",
        "8_RG1_ktd",
        "9_RG1_ktd", "10_RG1_ktd", "11_RG1_ktd", "12_RG1_ktd", "13_RG1_ktd", "14_RG1_ktd", "15_RG1_ktd", "16_RG1_ktd",
        "0_RG2_ktd", "1_RG2_ktd", "2_RG2_ktd", "3_RG2_ktd", "4_RG2_ktd", "5_RG2_ktd", "6_RG2_ktd", "7_RG2_ktd",
        "8_RG2_ktd",
        "9_RG2_ktd", "10_RG2_ktd", "11_RG2_ktd", "12_RG2_ktd", "13_RG2_ktd", "14_RG2_ktd", "15_RG2_ktd", "16_RG2_ktd",
        "1a_LG1_ktd", "1b_LG1_ktd", "1c_LG1_ktd", "2a_LG1_ktd", "2b_LG1_ktd", "2c_LG1_ktd", "1a_LG2_ktd", "1b_LG2_ktd",
        "1c_LG2_ktd", "2a_LG2_ktd", "2b_LG2_ktd", "2c_LG2_ktd", "9a_RG1_ktd", "9b_RG1_ktd", "9c_RG1_ktd", "10a_RG1_ktd",
        "10b_RG1_ktd", "10c_RG1_ktd", "9a_RG2_ktd", "9b_RG2_ktd", "9c_RG2_ktd", "10a_RG2_ktd", "10b_RG2_ktd",
        "10c_RG2_ktd",
        "3a_LG1_ktd", "3b_LG1_ktd", "3c_LG1_ktd", "3a_LG2_ktd", "3b_LG2_ktd", "3c_LG2_ktd", "3a_RG1_ktd", "3b_RG1_ktd",
        "3c_RG1_ktd", "3a_RG2_ktd", "3b_RG2_ktd", "3c_RG2_ktd", "2a_RG1_ktd", "2b_RG1_ktd", "2c_RG1_ktd", "2a_RG2_ktd",
        "2b_RG2_ktd", "2c_RG2_ktd", "0_LG1_ano", "1_LG1_ano", "2_LG1_ano", "3_LG1_ano", "4_LG1_ano", "5_LG1_ano",
        "6_LG1_ano",
        "7_LG1_ano", "8_LG1_ano", "9_LG1_ano", "10_LG1_ano", "11_LG1_ano", "12_LG1_ano", "13_LG1_ano", "14_LG1_ano",
        "15_LG1_ano", "16_LG1_ano", "0_LG2_ano", "1_LG2_ano", "2_LG2_ano", "3_LG2_ano", "4_LG2_ano", "5_LG2_ano",
        "6_LG2_ano",
        "7_LG2_ano", "8_LG2_ano", "9_LG2_ano", "10_LG2_ano", "11_LG2_ano", "12_LG2_ano", "13_LG2_ano", "14_LG2_ano",
        "15_LG2_ano", "16_LG2_ano", "0_RG1_ano", "1_RG1_ano", "2_RG1_ano", "3_RG1_ano", "4_RG1_ano", "5_RG1_ano",
        "6_RG1_ano",
        "7_RG1_ano", "8_RG1_ano", "9_RG1_ano", "10_RG1_ano", "11_RG1_ano", "12_RG1_ano", "13_RG1_ano", "14_RG1_ano",
        "15_RG1_ano", "16_RG1_ano", "0_RG2_ano", "1_RG2_ano", "2_RG2_ano", "3_RG2_ano", "4_RG2_ano", "5_RG2_ano",
        "6_RG2_ano",
        "7_RG2_ano", "8_RG2_ano", "9_RG2_ano", "10_RG2_ano", "11_RG2_ano", "12_RG2_ano", "13_RG2_ano", "14_RG2_ano",
        "15_RG2_ano", "16_RG2_ano", "1a_LG1_ano", "1b_LG1_ano", "1c_LG1_ano", "2a_LG1_ano", "2b_LG1_ano", "2c_LG1_ano",
        "1a_LG2_ano", "1b_LG2_ano", "1c_LG2_ano", "2a_LG2_ano", "2b_LG2_ano", "2c_LG2_ano", "9a_RG1_ano", "9b_RG1_ano",
        "9c_RG1_ano", "10a_RG1_ano", "10b_RG1_ano", "10c_RG1_ano", "9a_RG2_ano", "9b_RG2_ano", "9c_RG2_ano",
        "10a_RG2_ano",
        "10b_RG2_ano", "10c_RG2_ano", "3a_LG1_ano", "3b_LG1_ano", "3c_LG1_ano", "3a_LG2_ano", "3b_LG2_ano",
        "3c_LG2_ano",
        "3a_RG1_ano", "3b_RG1_ano", "3c_RG1_ano", "3a_RG2_ano", "3b_RG2_ano", "3c_RG2_ano", "2a_RG1_ano", "2b_RG1_ano",
        "2c_RG1_ano", "2a_RG2_ano", "2b_RG2_ano", "2c_RG2_ano", "Amp_LG1", "Amp_LG2", "Freq_LG1", "Freq_LG2", "PW_LG1",
        "PW_LG2", "Amp_RG1", "Amp_RG2", "Freq_RG1", "Freq_RG2", "PW_RG1", "PW_RG2"
    ]

    dates_intraoperative = ["surgery_date_intraop", "Admission_intraop", "Dismissal_intraop", "admission_Nch_intraop",
        "dismissal_NCh_intraop"]

    checkboxes_intraoperative = ["report_file_NCh_intraop", "report_file_NR_intraop", "awake_intraop", "protocol_intraop"]

    listwidgets_intraoperative = ["target_intraop", "neur_test_intraop"]

    medication_intraoperative = ["Levodopa_Carbidopa_intraop", "Levodopa_Carbidopa_CR_intraop",
        "Entacapone_intraop", "Tolcapone_intraop", "Pramipexole_intraop", "Ropinirole_intraop", "Rotigotine_intraop",
        "Selegiline_oral_intraop", "Selegiline_sublingual_intraop", "Rasagiline_intraop", "Amantadine_intraop",
        "Apomorphine_intraop", "Piribedil_intraop", "Safinamide_intraop", "Opicapone_intraop", "Other_intraop"]

    dbs_intraoperative = ["0_LG1_ktd", "1_LG1_ktd", "2_LG1_ktd", "3_LG1_ktd", "4_LG1_ktd", "5_LG1_ktd", "6_LG1_ktd", "7_LG1_ktd",
        "8_LG1_ktd",
        "9_LG1_ktd", "10_LG1_ktd", "11_LG1_ktd", "12_LG1_ktd", "13_LG1_ktd", "14_LG1_ktd", "15_LG1_ktd", "16_LG1_ktd",
        "0_LG2_ktd", "1_LG2_ktd", "2_LG2_ktd", "3_LG2_ktd", "4_LG2_ktd", "5_LG2_ktd", "6_LG2_ktd", "7_LG2_ktd",
        "8_LG2_ktd",
        "9_LG2_ktd", "10_LG2_ktd", "11_LG2_ktd", "12_LG2_ktd", "13_LG2_ktd", "14_LG2_ktd", "15_LG2_ktd", "16_LG2_ktd",
        "0_RG1_ktd", "1_RG1_ktd", "2_RG1_ktd", "3_RG1_ktd", "4_RG1_ktd", "5_RG1_ktd", "6_RG1_ktd", "7_RG1_ktd",
        "8_RG1_ktd",
        "9_RG1_ktd", "10_RG1_ktd", "11_RG1_ktd", "12_RG1_ktd", "13_RG1_ktd", "14_RG1_ktd", "15_RG1_ktd", "16_RG1_ktd",
        "0_RG2_ktd", "1_RG2_ktd", "2_RG2_ktd", "3_RG2_ktd", "4_RG2_ktd", "5_RG2_ktd", "6_RG2_ktd", "7_RG2_ktd",
        "8_RG2_ktd",
        "9_RG2_ktd", "10_RG2_ktd", "11_RG2_ktd", "12_RG2_ktd", "13_RG2_ktd", "14_RG2_ktd", "15_RG2_ktd", "16_RG2_ktd",
        "1a_LG1_ktd", "1b_LG1_ktd", "1c_LG1_ktd", "2a_LG1_ktd", "2b_LG1_ktd", "2c_LG1_ktd", "1a_LG2_ktd", "1b_LG2_ktd",
        "1c_LG2_ktd", "2a_LG2_ktd", "2b_LG2_ktd", "2c_LG2_ktd", "9a_RG1_ktd", "9b_RG1_ktd", "9c_RG1_ktd", "10a_RG1_ktd",
        "10b_RG1_ktd", "10c_RG1_ktd", "9a_RG2_ktd", "9b_RG2_ktd", "9c_RG2_ktd", "10a_RG2_ktd", "10b_RG2_ktd",
        "10c_RG2_ktd",
        "3a_LG1_ktd", "3b_LG1_ktd", "3c_LG1_ktd", "3a_LG2_ktd", "3b_LG2_ktd", "3c_LG2_ktd", "3a_RG1_ktd", "3b_RG1_ktd",
        "3c_RG1_ktd", "3a_RG2_ktd", "3b_RG2_ktd", "3c_RG2_ktd", "2a_RG1_ktd", "2b_RG1_ktd", "2c_RG1_ktd", "2a_RG2_ktd",
        "2b_RG2_ktd", "2c_RG2_ktd", "0_LG1_ano", "1_LG1_ano", "2_LG1_ano", "3_LG1_ano", "4_LG1_ano", "5_LG1_ano",
        "6_LG1_ano",
        "7_LG1_ano", "8_LG1_ano", "9_LG1_ano", "10_LG1_ano", "11_LG1_ano", "12_LG1_ano", "13_LG1_ano", "14_LG1_ano",
        "15_LG1_ano", "16_LG1_ano", "0_LG2_ano", "1_LG2_ano", "2_LG2_ano", "3_LG2_ano", "4_LG2_ano", "5_LG2_ano",
        "6_LG2_ano",
        "7_LG2_ano", "8_LG2_ano", "9_LG2_ano", "10_LG2_ano", "11_LG2_ano", "12_LG2_ano", "13_LG2_ano", "14_LG2_ano",
        "15_LG2_ano", "16_LG2_ano", "0_RG1_ano", "1_RG1_ano", "2_RG1_ano", "3_RG1_ano", "4_RG1_ano", "5_RG1_ano",
        "6_RG1_ano",
        "7_RG1_ano", "8_RG1_ano", "9_RG1_ano", "10_RG1_ano", "11_RG1_ano", "12_RG1_ano", "13_RG1_ano", "14_RG1_ano",
        "15_RG1_ano", "16_RG1_ano", "0_RG2_ano", "1_RG2_ano", "2_RG2_ano", "3_RG2_ano", "4_RG2_ano", "5_RG2_ano",
        "6_RG2_ano",
        "7_RG2_ano", "8_RG2_ano", "9_RG2_ano", "10_RG2_ano", "11_RG2_ano", "12_RG2_ano", "13_RG2_ano", "14_RG2_ano",
        "15_RG2_ano", "16_RG2_ano", "1a_LG1_ano", "1b_LG1_ano", "1c_LG1_ano", "2a_LG1_ano", "2b_LG1_ano", "2c_LG1_ano",
        "1a_LG2_ano", "1b_LG2_ano", "1c_LG2_ano", "2a_LG2_ano", "2b_LG2_ano", "2c_LG2_ano", "9a_RG1_ano", "9b_RG1_ano",
        "9c_RG1_ano", "10a_RG1_ano", "10b_RG1_ano", "10c_RG1_ano", "9a_RG2_ano", "9b_RG2_ano", "9c_RG2_ano",
        "10a_RG2_ano",
        "10b_RG2_ano", "10c_RG2_ano", "3a_LG1_ano", "3b_LG1_ano", "3c_LG1_ano", "3a_LG2_ano", "3b_LG2_ano",
        "3c_LG2_ano",
        "3a_RG1_ano", "3b_RG1_ano", "3c_RG1_ano", "3a_RG2_ano", "3b_RG2_ano", "3c_RG2_ano", "2a_RG1_ano", "2b_RG1_ano",
        "2c_RG1_ano", "2a_RG2_ano", "2b_RG2_ano", "2c_RG2_ano",
        "IPG_LG1_ktd", "IPG_LG2_ktd", "IPG_LG1_ano", "IPG_LG2_ano", "IPG_RG1_ktd", "IPG_RG2_ktd",
        "IPG_RG1_ano", "IPG_RG2_ano", "Amp_LG1", "Amp_LG2", "Freq_LG1", "Freq_LG2", "PW_LG1",
        "PW_LG2", "Amp_RG1", "Amp_RG2", "Freq_RG1", "Freq_RG2", "PW_RG1", "PW_RG2"]

    lineedits_intraoperative = ["no_traj_intraop", "op_duration_intraop"]

    not_used_intraoperative = ["pat_contact_intraop", "sugery_no_intraop", "protocol_file_intraop", "CTscan_intraop", "activation_visit_intraop",
    "implantation_visit_intraop", "incl_qualiPA_intraop", "DBS_intraop"]


