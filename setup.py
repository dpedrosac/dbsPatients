from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import shutil


class Install_dbsPatients(install):
    """Customized setuptools install command to handle file and folder copying."""

    def run(self):
        install.run(self)
        self.copy_custom_folders_and_files()

    def copy_custom_folders_and_files(self):
        """Copy folders and handle the `.install` folder operations."""
        # Define paths
        base_dir = os.path.abspath(os.path.dirname(__file__))
        target_base_dir = os.path.join(base_dir, "output")  # Change as needed

        # Directories to copy
        dirs_to_copy = ["data"]
        os.makedirs(target_base_dir, exist_ok=True)

        # Copy folders
        for folder in dirs_to_copy:
            src = os.path.join(base_dir, folder)
            dst = os.path.join(target_base_dir, folder)
            if os.path.exists(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
                print(f"Copied {folder} to {dst}")
            else:
                print(f"Warning: {folder} not found in {base_dir}")

        # Handle ".install" folder
        install_dir = os.path.join(base_dir, ".install")
        data_dir = os.path.join(target_base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)

        if os.path.exists(install_dir):
            for file_name in os.listdir(install_dir):
                if file_name.endswith("_template.csv"):
                    src_file = os.path.join(install_dir, file_name)
                    # Remove "_template" from the file name
                    new_file_name = file_name.replace("_template", "")
                    dst_file = os.path.join(data_dir, new_file_name)
                    shutil.copy2(src_file, dst_file)
                    print(f"Copied and renamed {file_name} to {dst_file}")
        else:
            print(f"Warning: .install folder not found in {base_dir}")


setup(
    name="dbsPatients",
    version="0.1",
    packages=find_packages(), #find_packages() will automatically discover and include the packages in the folder
    package_data={"dbsPatients": [".install/*.csv"]}, # Not sure if needed as dbsPatients..install or similar
    cmdclass={
        'install': Install_dbsPatients,  # Override the default install command
            },
    include_package_data=True,
    zip_safe=False,
)