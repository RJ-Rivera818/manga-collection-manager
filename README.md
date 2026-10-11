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
* `python-dotenv`

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


## 🚀 Quick Start

Follow these steps to set up and run the Manga Collection Manager locally:

### 1. Clone the Repository

```bash
git clone [https://github.com/RJ-Rivera818/manga-collection-manager.git](https://github.com/RJ-Rivera818/manga-collection-manager.git)
cd manga-collection-manager
```

### 2. Install Dependencies

Install the required packages listed in your `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory (matching your `database_connect.py` setup) and add your MySQL database credentials:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=manga_collection
```

### 4. Initialize the Database

Create your MySQL database and set up the required tables (`series`, `edition`, `volume`, `ownership`):

```bash
mysql -u root -p -e "CREATE DATABASE manga_collection;"
mysql -u root -p manga_collection < database/schema.sql
```

### 5. Populate the Database Using the `.json` Catalog

Before using the main program, you must populate your database with manga series, editions, and volume data using the provided `.json` catalog file in the `database/` folder. Run the import script:

```bash
python src/import_catalog.py
```

### 6. Run the Application

Once your database is populated, launch the main program to manage your collection:

```bash
python src/main.py
```
