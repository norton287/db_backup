#!/usr/bin/python3
import configparser
import os
import datetime
import tarfile
import subprocess
import logging
import shutil

# Ensure log directory exists
log_dir = "/var/log/spindlecrank"
os.makedirs(log_dir, exist_ok=True)

# Ensure log file exists (create if not)
log_file = os.path.join(log_dir, "dbback.log")
if not os.path.exists(log_file):
    open(log_file, 'a').close()  # Create an empty log file


# Setup logging
logging.basicConfig(filename='/var/log/spindlecrank/dbback.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read INI file path from environment variable
ini_file_path = os.environ.get('MARIA_INI')
if not ini_file_path:
    raise ValueError("MARIA_INI environment variable not set")

# Read MariaDB credentials from INI file
config = configparser.ConfigParser()
config.read(ini_file_path) 

def dump_databases():
    try:
        host = config['Maria']['host']
        user = config['Maria']['user']
        password = config['Maria']['password']

        # Use a temporary file to store the SQL dump
        with open('temp_dump.sql', 'w') as f:
            command = f"mysqldump --all-databases --add-drop-table -h {host} -u {user} -p{password}"
            subprocess.run(command, shell=True, stdout=f, stderr=subprocess.PIPE, text=True, check=True)  # Check for errors
        logging.info("Database dump successful.")
        return 'temp_dump.sql'  # Return the temporary file path
    except subprocess.CalledProcessError as e:
        logging.error(f"Database dump failed: {e.stderr}")
        raise

def create_archive(sql_dump_file, backup_dir, filename):
    try:
        backup_file = os.path.join(backup_dir, filename)
        with tarfile.open(backup_file, "w:gz") as tar:
            tar.add(sql_dump_file, arcname=os.path.basename(filename[:-7]))  # Use arcname to avoid including full path
        logging.info(f"Backup archive created: {backup_file}")
    except Exception as e:
        logging.error(f"Error creating backup archive: {e}")
        raise
    finally:
        # Clean up the temporary dump file
        os.remove(sql_dump_file)

def copy_to_share(backup_dir, destination_dir, filename):
    try:
        source_file = os.path.join(backup_dir, filename)
        destination_file = os.path.join(destination_dir, filename)
        shutil.copy2(source_file, destination_file)
        logging.info(f"Backup copied to share: {destination_file}")
    except Exception as e:
        logging.error(f"Error copying backup to share: {e}")
        raise

if __name__ == "__main__":
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        backup_dir = "/backup/dump"
        destination_dir = "/share/nano/dump"
        hostname = os.uname()[1]
        filename = f"{hostname}-db-export-{timestamp}.tar.gz"
        
        os.makedirs(backup_dir, exist_ok=True)
        os.makedirs(destination_dir, exist_ok=True)  # Ensure destination directory exists

        sql_dump_file = dump_databases()
        create_archive(sql_dump_file, backup_dir, filename)
        copy_to_share(backup_dir, destination_dir, filename)

    except Exception as e:
        logging.critical(f"Critical error during backup process: {e}")
