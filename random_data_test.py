import pandas as pd
import os
import random
import string
from datetime import datetime, timedelta
from utils.helper_functions import General
from utils.data_lists import Lists
from dependencies import SYSTEMS, LEADS

class FillGeneralData:
    def __init__(self, data_dir='data', file_name='general_data.csv', num_records=100, template_path='.install/general_data_template.csv'):
        self.data_dir = data_dir
        self.file_name = file_name
        self.file_path = os.path.join(data_dir, file_name)
        self.num_records = num_records
        self.template_path = template_path
        self.genders = ['male', 'female', 'diverse']
        self.diagnoses = Lists.diagnosis
        self.side_dominance = ['right', 'left', 'unknown']
        self.ensure_data_dir_exists()
        self.template_df = self.load_template()

    def ensure_data_dir_exists(self):
        os.makedirs(self.data_dir, exist_ok=True)

    def load_template(self):
        return pd.read_csv(self.template_path)

    def random_string(self, length=10):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def random_date(self, start_date='01/01/1900', end_date='31/12/1999'):
        start = datetime.strptime(start_date, '%d/%m/%Y')
        end = datetime.strptime(end_date, '%d/%m/%Y')
        return (start + timedelta(days=random.randint(0, (end - start).days))).strftime('%d/%m/%Y')

    def generate_data(self):
        data = {
            'PID_ORBIS': [str(random.randint(1000000000, 9999999999)) for _ in range(self.num_records)],
            'surname': [self.random_string().capitalize() for _ in range(self.num_records)],
            'name': [self.random_string().capitalize() for _ in range(self.num_records)],
            'birthdate': [self.random_date() for _ in range(self.num_records)],
            'ID': [General.create_pseudonym(8) for _ in range(self.num_records)],
            'curr_no': range(0, self.num_records),
            'gender': [random.choice(self.genders) for _ in range(self.num_records)],
            'diagnosis': [random.choice(self.diagnoses) for _ in range(self.num_records)],
            'side_dominance': [random.choice(self.side_dominance) for _ in range(self.num_records)],
            'IPG_serial_number': [random.randint(10000, 99999) for _ in range(self.num_records)]
        }
        return data

    def save_to_csv(self):
        data = self.generate_data()
        df = pd.DataFrame(data)
        df = df.reindex(columns=self.template_df.columns)  # Ensure the same format as the template
        df.to_csv(self.file_path, index=False)
        print(f"Data saved to {self.file_path}")

class FillPreoperative:
    def __init__(self, data_dir='data', file_name='preoperative.csv', num_records=100,
                 template_path='.install/preoperative_template.csv'):
        self.data_dir = data_dir
        self.file_name = file_name
        self.file_path = os.path.join(data_dir, file_name)
        self.num_records = num_records
        self.template_path = template_path
        self.ensure_data_dir_exists()
        self.template_df = self.load_template()
        self.general_data = self.load_general_data()

    def ensure_data_dir_exists(self):
        os.makedirs(self.data_dir, exist_ok=True)

    def load_template(self):
        return pd.read_csv(self.template_path)

    def random_date(self, start_date='01/01/1980', end_date='31/12/2020'):
        start = datetime.strptime(start_date, '%d/%m/%Y')
        end = datetime.strptime(end_date, '%d/%m/%Y')
        return (start + timedelta(days=random.randint(0, (end - start).days))).strftime('%d/%m/%Y')

    def load_general_data(self):
        general_data_path = os.path.join(self.data_dir, 'general_data.csv')
        return pd.read_csv(general_data_path)

    def generate_data_preoperative(self):
        data = {
            'PID_ORBIS': self.general_data['PID_ORBIS'][:self.num_records],
            'surname': self.general_data['surname'][:self.num_records],
            'name': self.general_data['name'][:self.num_records],
            'birthdate': self.general_data['birthdate'][:self.num_records],
            'ID': self.general_data['ID'][:self.num_records],
            'Gender': self.general_data['gender'][:self.num_records],
            'Diagnosis_preop': self.general_data['diagnosis'][:self.num_records],
        }

        # Fill dates_preoperative fields with random dates from 1980 to 2020
        for field in Lists.dates_preoperative:
            data[field] = [self.random_date() for _ in range(self.num_records)]

        # Fill checkboxes_preoperative fields with 0 or 1
        for field in Lists.checkboxes_preoperative:
            data[field] = [random.randint(0, 1) for _ in range(self.num_records)]

        # Fill tests_preoperative fields with random integers from 1 to 8
        for field in Lists.tests_preoperative:
            data[field] = [random.randint(1, 8) for _ in range(self.num_records)]

            # Fill medication_preoperative fields with '000§mg§0' format
            for field in Lists.medication_preoperative:
                if field == 'Other_preop':
                    data[field] = "New_med§100§mg§1"
                data[field] = [f"{random.choice(range(100, 1100, 100))}§mg§{random.randint(1, 6)}" for _ in
                               range(self.num_records)]

        # Fill remaining fields with empty strings or appropriate default values
        remaining_fields = set(Lists.preoperative_template_fields) - set(data.keys())
        for field in remaining_fields:
            data[field] = ['' for _ in range(self.num_records)]

        return data

    def save_to_csv(self):
        data = self.generate_data_preoperative()
        df = pd.DataFrame(data)
        df = df.reindex(columns=self.template_df.columns)  # Ensure the same format as the template
        df.to_csv(self.file_path, index=False)
        print(f"Data saved to {self.file_path}")

class FillPostoperative:
    def __init__(self, data_dir='data', file_name='postoperative.csv', num_records=100, template_path='.install/postoperative_template.csv'):
        self.data_dir = data_dir
        self.file_name = file_name
        self.file_path = os.path.join(data_dir, file_name)
        self.num_records = num_records
        self.template_path = template_path
        self.ensure_data_dir_exists()
        self.template_df = self.load_template()
        self.general_data = self.load_general_data()

    def ensure_data_dir_exists(self):
        os.makedirs(self.data_dir, exist_ok=True)

    def load_template(self):
        return pd.read_csv(self.template_path)

    def random_date(self, start_date='01/01/1980', end_date='31/12/2020'):
        start = datetime.strptime(start_date, '%d/%m/%Y')
        end = datetime.strptime(end_date, '%d/%m/%Y')
        return (start + timedelta(days=random.randint(0, (end - start).days))).strftime('%d/%m/%Y')

    def load_general_data(self):
        general_data_path = os.path.join(self.data_dir, 'general_data.csv')
        return pd.read_csv(general_data_path)

    def generate_data_postoperative(self):
        data = {
            'PID_ORBIS': [],
            'surname': [],
            'name': [],
            'birthdate': [],
            'ID': [],
            'Gender': [],
            'Diagnosis_postop': [],
            'Reason_postop': [],
            'Implanted_IPG': [],
            'Lead_manufacturer': [],
            'implanted_leads': []
        }

        for i in range(self.num_records):
            # Choose random Implanted_IPG and implanted_leads for each ID
            implanted_ipg = random.choice(SYSTEMS)
            implanted_leads = random.choice(list(LEADS.keys()))
            lead_manufacturer = LEADS[implanted_leads]['Manufacturer']

            leads_settings_general = ["IPG_LG1_ktd", "IPG_LG2_ktd", "IPG_LG1_ano", "IPG_LG2_ano",
                              "IPG_RG1_ktd", "IPG_RG2_ktd", "IPG_RG1_ano", "IPG_RG2_ano",
                              "Amp_LG1", "Amp_LG2", "Freq_LG1", "Freq_LG2", "PW_LG1",
                              "PW_LG2", "Amp_RG1", "Amp_RG2", "Freq_RG1", "Freq_RG2", "PW_RG1", "PW_RG2"
                              ]
            leads_settings = []

            for num in LEADS[implanted_leads]['Contacts_name'][0]:
                for side in ['LG1', 'LG2', 'RG1', 'RG2']:
                    for polarity in ['ano', 'ktd']:
                        lead_name = f'{num}_{side}_{polarity}'
                        leads_settings.append(lead_name)

            for num in LEADS[implanted_leads]['Contacts_name'][1]:
                for side in ['LG1', 'LG2', 'RG1', 'RG2']:
                    for polarity in ['ano', 'ktd']:
                        lead_name = f'{num}_{side}_{polarity}'
                        leads_settings.append(lead_name)

            for _ in range(5):  # Create 5 datasets for each ID
                data['PID_ORBIS'].append(self.general_data['PID_ORBIS'][i])
                data['surname'].append(self.general_data['surname'][i])
                data['name'].append(self.general_data['name'][i])
                data['birthdate'].append(self.general_data['birthdate'][i])
                data['ID'].append(self.general_data['ID'][i])
                data['Gender'].append(self.general_data['gender'][i])
                data['Diagnosis_postop'].append(self.general_data['diagnosis'][i])
                data['Reason_postop'].append(self.random_date())
                data['Implanted_IPG'].append(implanted_ipg)
                data['Lead_manufacturer'].append(lead_manufacturer)
                data['implanted_leads'].append(implanted_leads)

                # Fill dates_postoperative fields with random dates from 1980 to 2020
                for field in Lists.dates_postoperative:
                    if field not in data:
                        data[field] = []
                    data[field].append(self.random_date())

                # Fill checkboxes_postoperative fields with 0 or 1
                for field in Lists.checkboxes_postoperative:
                    if field not in data:
                        data[field] = []
                    data[field].append(random.randint(0, 1))

                # Fill tests_postoperative fields with random integers from 1 to 8
                for field in Lists.tests_postoperative:
                    if field not in data:
                        data[field] = []
                    data[field].append(random.randint(1, 8))

                # Fill medication_postoperative fields with 'AAA§mg§B' format
                for field in Lists.medication_postoperative:
                    if field not in data:
                        data[field] = []
                    if field == 'Other_postop':
                        data[field].append("New_med§100§mg§1")
                    else:
                        data[field].append(f"{random.choice(range(100, 1100, 100))}§mg§{random.randint(1, 6)}")

                for field in Lists.dbs_postoperative:
                    if field not in data:
                        data[field] = []
                    if field in leads_settings or field in leads_settings_general:
                        data[field].append(random.randint(1, 10))
                    else:
                        data[field].append('')

        # Fill remaining fields with empty strings or appropriate default values
        remaining_fields = set(Lists.postoperative_template_fields) - set(data.keys())
        for field in remaining_fields:
            data[field] = []
            for _ in range(self.num_records):
                for i in range(5):
                    data[field].append('')

        return data

    def save_to_csv(self):
        data = self.generate_data_postoperative()
        df = pd.DataFrame(data)
        df = df.reindex(columns=self.template_df.columns)  # Ensure the same format as the template
        df.to_csv(self.file_path, index=False)
        print(f"Data saved to {self.file_path}")

class FillIntraoperative:
    def __init__(self, data_dir='data', file_name='intraoperative.csv', num_records=100, template_path='.install/intraoperative_template.csv'):
        self.data_dir = data_dir
        self.file_name = file_name
        self.file_path = os.path.join(data_dir, file_name)
        self.num_records = num_records
        self.template_path = template_path
        self.ensure_data_dir_exists()
        self.template_df = self.load_template()
        self.general_data = self.load_general_data()

    def ensure_data_dir_exists(self):
        os.makedirs(self.data_dir, exist_ok=True)

    def load_template(self):
        return pd.read_csv(self.template_path)

    def random_date(self, start_date='01/01/1980', end_date='31/12/2020'):
        start = datetime.strptime(start_date, '%d/%m/%Y')
        end = datetime.strptime(end_date, '%d/%m/%Y')
        return (start + timedelta(days=random.randint(0, (end - start).days))).strftime('%d/%m/%Y')

    def load_general_data(self):
        general_data_path = os.path.join(self.data_dir, 'general_data.csv')
        return pd.read_csv(general_data_path)

    def generate_data_intraoperative(self):

        testing_neur_list = ['Oehrn/Weber', 'Pedrosa', 'Waldthaler', 'Other']
        target_list = ['STN', 'GPi', 'VLp', 'Other']

        data = {
            'PID_ORBIS': [],
            'surname': [],
            'name': [],
            'birthdate': [],
            'ID': [],
            'Gender': [],
            'Diagnosis_preop': [],
            'Implanted_IPG': [],
            'Lead_manufacturer': [],
            'implanted_leads': []
        }

        for i in range(self.num_records):
            # Choose random Implanted_IPG and implanted_leads for each ID
            implanted_ipg = random.choice(SYSTEMS)
            implanted_leads = random.choice(list(LEADS.keys()))
            lead_manufacturer = LEADS[implanted_leads]['Manufacturer']

            leads_settings_general = ["IPG_LG1_ktd", "IPG_LG2_ktd", "IPG_LG1_ano", "IPG_LG2_ano",
                                      "IPG_RG1_ktd", "IPG_RG2_ktd", "IPG_RG1_ano", "IPG_RG2_ano",
                                      "Amp_LG1", "Amp_LG2", "Freq_LG1", "Freq_LG2", "PW_LG1",
                                      "PW_LG2", "Amp_RG1", "Amp_RG2", "Freq_RG1", "Freq_RG2", "PW_RG1", "PW_RG2"
                                      ]
            leads_settings = []

            for num in LEADS[implanted_leads]['Contacts_name'][0]:
                for side in ['LG1', 'LG2', 'RG1', 'RG2']:
                    for polarity in ['ano', 'ktd']:
                        lead_name = f'{num}_{side}_{polarity}'
                        leads_settings.append(lead_name)

            for num in LEADS[implanted_leads]['Contacts_name'][1]:
                for side in ['LG1', 'LG2', 'RG1', 'RG2']:
                    for polarity in ['ano', 'ktd']:
                        lead_name = f'{num}_{side}_{polarity}'
                        leads_settings.append(lead_name)


            data['PID_ORBIS'].append(self.general_data['PID_ORBIS'][i])
            data['surname'].append(self.general_data['surname'][i])
            data['name'].append(self.general_data['name'][i])
            data['birthdate'].append(self.general_data['birthdate'][i])
            data['ID'].append(self.general_data['ID'][i])
            data['Gender'].append(self.general_data['gender'][i])
            data['Diagnosis_preop'].append(self.general_data['diagnosis'][i])
            data['Implanted_IPG'].append(implanted_ipg)
            data['Lead_manufacturer'].append(lead_manufacturer)
            data['implanted_leads'].append(implanted_leads)

            # Fill dates_intraoperative fields with random dates from 1980 to 2020
            for field in Lists.dates_intraoperative:
                if field not in data:
                    data[field] = []
                data[field].append(self.random_date())

            # Fill checkboxes_intraoperative fields with 0 or 1
            for field in Lists.checkboxes_intraoperative:
                if field not in data:
                    data[field] = []
                data[field].append(random.randint(0, 1))

            for field in Lists.lineedits_intraoperative:
                if field not in data:
                    data[field] = []
                data[field].append(random.choice(range(1, 120)))

            # Fill tests_intraoperative fields with random integers from 1 to 8
            for field in Lists.listwidgets_intraoperative:
                if field not in data:
                    data[field] = []
                if field == 'target_intraop':
                    data[field].append(random.choice(target_list))
                else:
                    data[field].append(random.choice(testing_neur_list))

            # Fill medication_intraoperative fields with 'AAA§mg§B' format
            for field in Lists.medication_intraoperative:
                if field not in data:
                    data[field] = []
                if field == 'Other_intraop':
                    data[field].append("New_med§100§mg§1")
                else:
                    data[field].append(f"{random.choice(range(100, 1100, 100))}§mg§{random.randint(1, 6)}")



            for field in Lists.dbs_intraoperative:
                if field not in data:
                    data[field] = []
                if field in leads_settings or field in leads_settings_general:
                    data[field].append(random.randint(1, 10))
                else:
                    data[field].append('')

            # Fill remaining fields with empty strings or appropriate default values
            remaining_fields = set(Lists.intraoperative_template_fields) - set(data.keys())
            for field in remaining_fields:
                data[field] = []
                for _ in range(self.num_records):
                        data[field].append('')

        return data

    def save_to_csv(self):
        data = self.generate_data_intraoperative()
        df = pd.DataFrame(data)
        df = df.reindex(columns=self.template_df.columns)  # Ensure the same format as the template
        df.to_csv(self.file_path, index=False)
        print(f"Data saved to {self.file_path}")


if __name__ == '__main__':
    if input("Do you want to override the data? (yes/no): ").lower() == 'yes':
        while True:
            sample_patients = input("How many Entries?: ")
            try:
                sample_patients = int(sample_patients)
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        filler = FillGeneralData(num_records=sample_patients)
        filler.save_to_csv()

        filler_preoperative = FillPreoperative(num_records=sample_patients)
        filler_preoperative.save_to_csv()

        filler_postoperative = FillPostoperative(num_records=sample_patients)
        filler_postoperative.save_to_csv()

        filler_intraoperative = FillIntraoperative(num_records=sample_patients)
        filler_intraoperative.save_to_csv()