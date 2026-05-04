## Asiwome Agbleze
## CMCS 111/1 - Asignment 2 Automated File Backup
## Spring 2026

# daily_backup.py
# This program creates a timestamped ZIP backup of everything
# inside the "important_files" folder.
# The backup ZIP is stored in a "backups" folder.
# It also appends a line to "backup_log.txt" describing the backup.
#
# Notes:
# - pathlib is used to work with folders and file paths
# - zipfile is used to create ZIP archives
# - datetime is used to create a timestamp for filenames and logs
# - try/except is used for simple error handling

from pathlib import Path
import zipfile
from datetime import datetime


def main():
    try:
        # 1) Set up the main paths we will use
        project_folder = Path(__file__).parent              # Folder where this script is
        important_folder = project_folder / "important_files"
        backups_folder = project_folder / "backups"
        log_file_path = project_folder / "backup_log.txt"

        # 2) Make sure the important_files folder exists
        if not important_folder.exists():
            print("Error: 'important_files' folder does not exist.")
            print("Please create it and add some files before running this script.")
            return

        # 3) Create the backups folder if it does not already exist
        backups_folder.mkdir(exist_ok=True)

        # 4) Collect all files inside important_files (files only, no subfolders)
        files_to_backup = [p for p in important_folder.iterdir() if p.is_file()]
        file_count = len(files_to_backup)

        if file_count == 0:
            print("No files found in 'important_files' to back up.")
            return

        # 5) Create a timestamp string for the ZIP filename and log
        #    Example format: 2026-01-17_2100
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

        # 6) Build the ZIP filename using the timestamp, stored in backups/
        zip_filename = f"backup_{timestamp}.zip"
        zip_path = backups_folder / zip_filename

        # 7) Create the ZIP file and add each file
        #    zipfile.ZIP_DEFLATED compresses the files.
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in files_to_backup:
                # arcname controls the path inside the ZIP file.
                # Here we keep just the file name (no full path).
                zip_file.write(file_path, arcname=file_path.name)

        # 8) Print a confirmation message for when you run the script manually
        print(
            f"Backup created: {zip_path}  "
            f"Files backed up: {file_count}"
        )

        # 9) Append one line to backup_log.txt with details
        log_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_line = (
            f"{log_timestamp} - Created backups/{zip_filename} "
            f"({file_count} files)\n"
        )

        # Open the log file in append mode so we keep previous entries.
        with log_file_path.open("a", encoding="utf-8") as log_file:
            log_file.write(log_line)

    except PermissionError as error:
        print(f"Permission error while creating backup: {error}")

    except FileNotFoundError as error:
        print(f"File not found error: {error}")

    except Exception as error:
        # Catch any other unexpected errors
        print(f"Unexpected error while running backup: {error}")


if __name__ == "__main__":
    main()