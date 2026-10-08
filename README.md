# Manga Collection Manager

Made using Python and **MySQL**.

## Description

This is a program I made to better organize and catalog my home manga collection. It keeps track of series, editions within those series, and volumes within each edition. Version 1 allows the user to search for manga, select editions, and manage owned volumes.

## Features

### Search

* Users can **search for manga by full or partial title**.
* Select from multiple matching series.
* Automatically select a series when only one result is found.

### Editions

* Select between different editions of a series.
* Automatically select an edition when only one is available.
* Keep the selected edition while managing the collection.

### Collection Display

* View owned and missing volumes.
* View collection completion percentage.

### Adding and Removing Volumes

* Add or remove individual volumes.
* Add or remove multiple volumes at once.
* Add or remove volume ranges such as `1-5`.
* Combine individual volumes and ranges such as `1,3-5,8`.

### Input Validation

* Prevent duplicate volume entries from being processed.
* Validate invalid volume input.
* Track ownership separately for each edition.

## Requirements

* Python 3
* MySQL
* `mysql-connector-python`

## Project Structure

* `main.py` - Controls the main program flow.
* `series.py` - Handles manga searching, series data, and edition selection.
* `collection_modification.py` - Handles adding and removing volumes from the collection.
* `database_connect.py` - Handles the connection to the MySQL database.

## Database Setup

This program uses a MySQL database named `manga_collection`.

The database currently contains four tables:

* `series`
* `edition`
* `volume`
* `ownership`

## Database Connection Setup

The program uses an environment variable to store the database password instead of storing it directly in the source code.

The environment variable name must match the name passed to `os.getenv()` in `database_connect.py`.

For example, if your code uses `os.getenv("***PASSWORD***")`, configure the environment variable as follows:

```text
***PASSWORD***=Your_Password
```

Replace `Your_Password` with your actual MySQL password in your local environment. **Never put your actual password in this README or commit it to GitHub.**

The database connection is configured in `database_connect.py`.
