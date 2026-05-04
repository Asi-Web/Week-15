## Asiwome Agbleze
## CMSC 11/1 - Assignmet 1 (File Automation)
## Spring 2026

# csv_backup.py
# This program finds all CSV files inside the data folder,
# moves them into data/CSV_Files,
# and creates a ZIP backup named data_backup.zip.
#
# Beginner-friendly notes:
# - pathlib is used to work with folders and file paths
# - shutil is used to move files
# - zipfile is used to create the ZIP archive
# - try/except is used for basic error handling

from pathlib import Path
import shutil
import zipfile


def main():
    try:
        # Set up the main folder paths
        project_folder = Path(__file__).parent
        data_folder = project_folder / "data"
        csv_folder = data_folder / "CSV_Files"
        zip_file_path = project_folder / "data_backup.zip"

        # Make sure the data folder exists
        if not data_folder.exists():
            print("Error: The data folder does not exist.")
            return

        # Find all CSV files directly inside the data folder
        csv_files = list(data_folder.glob("*.csv"))
        print(f"Found {len(csv_files)} CSV file(s).")

        # Create the CSV_Files folder if it does not already exist
        csv_folder.mkdir(exist_ok=True)

        # Move the CSV files into data/CSV_Files
        moved_count = 0
        for file_path in csv_files:
            destination = csv_folder / file_path.name
            shutil.move(str(file_path), str(destination))
            moved_count += 1

        print(f"Moved {moved_count} CSV file(s) to {csv_folder}.")

        # Create the ZIP archive in the root folder
        with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for moved_file in csv_folder.glob("*.csv"):
                # This keeps the folder name inside the zip file
                zip_file.write(moved_file, arcname=f"CSV_Files/{moved_file.name}")

        print(f"Created archive: {zip_file_path.name}")

    except FileNotFoundError as error:
        print(f"File not found error: {error}")

    except PermissionError as error:
        print(f"Permission error: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
    