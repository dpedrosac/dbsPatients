import os
import csv

def check_for_data(output_dir):
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        if files:
            print("Data is already available!")
            for filename in files:
                print(filename)
            return False
    return True

def create_csv_files_from_templates(template_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(template_dir):
        if filename.endswith('_template.csv') or filename.endswith('_template_new.csv'):
            if filename == 'postoperative_template.csv':
                pass
            else:
                if filename.endswith('_template_new.csv'):
                    new_filename = filename.replace('_template_new', '')
                    template_path = os.path.join(template_dir, filename)
                    output_path = os.path.join(output_dir, new_filename)
                else:
                    new_filename = filename.replace('_template', '')
                    template_path = os.path.join(template_dir, filename)
                    output_path = os.path.join(output_dir, new_filename)

                with open(template_path, mode='r', newline='') as template_file:
                    reader = csv.reader(template_file)
                    rows = list(reader)

                with open(output_path, mode='w', newline='') as output_file:
                    writer = csv.writer(output_file)
                    writer.writerows(rows)

if __name__ == "__main__":
    template_directory = '.install'
    output_directory = 'data'
    if check_for_data(output_directory) or input("Data folder is not empty. Do you want to override the data? (yes/no): ").lower() == 'yes':
        if True:
            if input("Are you really sure? (yes/no): ").lower() == 'yes':
                create_csv_files_from_templates(template_directory, output_directory)