
### MariaDB Backup Script

This Python script automates the backup of all MariaDB databases on a server, compresses the backup into a tar.gz archive, and copies it to a network share. It is designed to be run regularly as a cron job.

#### Features

* **Comprehensive Backup:** Dumps all databases on the MariaDB server, including schema (structure) and data.
* **Compression:** Creates a compressed `.tar.gz` archive to save storage space.
* **Network Share Transfer:** Copies the backup archive to a specified network share for off-site storage.
* **Logging:** Logs all actions and errors to `/var/log/spindlecrank/dbback.log` for troubleshooting.
* **Error Handling:** Includes basic error handling to catch and log issues during the backup process.

#### Requirements

* **Python 3:** The script is written in Python 3 and requires the `configparser`, `os`, `datetime`, `tarfile`, `subprocess`, `logging`, and `shutil` modules.
* **MariaDB Client:** The `mysqldump` utility must be installed and accessible on the system.
* **MariaDB Credentials:** The script reads MariaDB credentials (host, user, password) from a configuration file specified by the `MARIA_INI` environment variable.
* **Backup and Share Directories:** The directories `/backup/dump` and `/share/nano/dump` must exist and be writable by the script.

#### Configuration

1. **MariaDB INI File:**
   - Create a configuration file (e.g., `mariadb.ini`) in the location specified by the `MARIA_INI` environment variable.
   - The file should have a `[Maria]` section with the following keys:
     - `host`: The hostname or IP address of the MariaDB server.
     - `user`: The MariaDB username with permission to dump all databases.
     - `password`: The password for the MariaDB user.

2. **Environment Variable:**
   - Set the `MARIA_INI` environment variable to the full path of your MariaDB configuration file.

#### Usage

1. **Cron Job:**
   - Schedule the script to run regularly using a cron job. For example, to run it daily at 3:00 AM:
     ```bash
     0 3 * * * /path/to/script/db_back.py
     ```

#### Backup File Naming

Backups are saved in the `/backup/dump` directory and copied to the `/share/nano/dump` directory. The filename format is:

```
<hostname>-db-export-<timestamp>.tar.gz
```

Where:

* `<hostname>` is the hostname of the server.
* `<timestamp>` is the date and time of the backup in the format YYYY-MM-DD-HH-MM-SS.

#### Restoration

To restore a backup:

1. **Copy:** Copy the desired `.tar.gz` backup file from the network share to the server.
2. **Extract:** Extract the archive using `tar -xzf <backup_file>`.
3. **Restore:** Use the `mysql` client to restore the databases from the extracted SQL dump file.

#### Security

* **Credentials:** Ensure that the MariaDB credentials in the configuration file are secure and have the minimum necessary privileges.
* **Network Share:** Protect the network share with appropriate access controls to prevent unauthorized access to the backups.

#### Additional Notes

* **Customization:** Modify the backup and share directories in the script if needed.
* **Error Handling:** Consider adding more robust error handling and notification mechanisms (e.g., email alerts) for production environments.
* **Retention:** Implement a backup retention policy to manage the number of backups stored on the network share.
