# Setup Guide

How to install, configure, and run the Manga Collection Manager locally.

## Prerequisites

- Python 3
- MySQL server (running locally)
- Git

## 1. Clone the Repository

```bash
git clone https://github.com/RJ-Rivera818/manga-collection-manager.git
cd manga-collection-manager
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs `mysql-connector-python` and `python-dotenv`.

## 3. Configure Environment Variables

Copy `.env.example` to `.env` in the project root and fill in your MySQL
credentials:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=manga_collection
```

The `.env` file holds your password, so it is listed in `.gitignore` and
should never be committed.

## 4. Create the Database

```bash
mysql -u root -p -e "CREATE DATABASE manga_collection;"
mysql -u root -p manga_collection < database/schema.sql
```

This creates the `series`, `creator`, `series_creators`, `edition`, `volume`, and `ownership` tables.
See [Database](database.md) for details.

## 5. Create Your Catalog and Import It

The program does not include a catalog of manga. Create your own `.json` file
with your series, editions, and owned volumes, using
`database/manga_catalog.example.json` as a template. See
[Catalog File](catalog.md) for every field.
Make sure to name the file `manga_catalog.json` and place it in the /database directory 

Then load it into the database:

```bash
python src/import_catalog.py
```

## 6. Run the Program

```bash
python src/main.py
```

## Troubleshooting

- **Access denied for user:** check `DB_USER` and `DB_PASSWORD` in `.env`.
- **Unknown database:** make sure step 4 was completed and `DB_NAME`
  matches the database you created.
- **Can't connect to MySQL server:** confirm the MySQL server is running and
  `DB_HOST` is correct.
- **ModuleNotFoundError:** re-run `pip install -r requirements.txt`.
- **Search finds nothing:** make sure step 5 (import) was completed and your catalog contains the series.
- **Import fails:** check that your catalog is valid JSON and matches the format in [Catalog File](catalog.md).
