from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import shutil

# Function to parse requirements.txt
def parse_requirements():
    """Read requirements.txt and return a list of dependencies."""
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_file):
        with open(requirements_file) as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

class CustomInstall(install):
    """Custom install command to handle copying files and folders."""

    def run(self):
        """Run the default install process and add custom steps."""
        install.run(self)  # Run standard installation
        self.copy_files_to_data_folder()

    def copy_files_to_data_folder(self):
        """Create 'data' folder and copy .install files with renaming."""
        base_dir = os.path.abspath(os.path.dirname(__file__))
        target_data_dir = os.path.join(base_dir, "data")  # Target "data" folder

        # Create 'data' folder if it does not exist
        os.makedirs(target_data_dir, exist_ok=True)
        print(f"Created or verified 'data' folder at: {target_data_dir}")

        # Source folder: .install
        install_dir = os.path.join(base_dir, ".install")

        if os.path.exists(install_dir):
            for file_name in os.listdir(install_dir):
                if file_name.endswith("_template.csv"):
                    src_file = os.path.join(install_dir, file_name)
                    new_file_name = file_name.replace("_template", "")
                    dst_file = os.path.join(target_data_dir, new_file_name)
                    shutil.copy2(src_file, dst_file)
                    print(f"Copied and renamed '{src_file}' to '{dst_file}'")
        else:
            print(f"Warning: The '.install' folder does not exist in {base_dir}")


# Setup configuration
setup(
    name="dbsPatients",
    version="0.1",
    packages=find_packages(),  # Automatically discover packages
    install_requires=parse_requirements(),  # Parse and include requirements
    cmdclass={
        'install': CustomInstall,  # Override the install command
         },
    include_package_data=True,
    zip_safe=False,
)