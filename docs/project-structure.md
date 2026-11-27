# Project Structure

```
manga-collection-manager/
├── database/              # schema and example .json catalog
├── docs/                  # project documentation
├── src/
│   ├── main.py
│   ├── series.py
│   ├── collection_modification.py
│   ├── database_connect.py
│   └── import_catalog.py
├── .env.example           # template for database credentials
├── .gitignore
├── README.md
└── requirements.txt
```

## Source Files

| File | Purpose |
|------|---------|
| `main.py` | Controls the main program flow |
| `series.py` | Handles manga searching, series data, and edition selection |
| `collection_modification.py` | Handles adding and removing volumes from the collection |
| `database_connect.py` | Handles the connection to the MySQL database |
| `import_catalog.py` | Loads the user's `.json` catalog into the database |

## Other Files

| File | Purpose |
|------|---------|
| `database/schema.sql` | Creates the database tables |
| `database/manga_catalog.example.json` | Template for writing your own catalog |
| `.env.example` | Example environment variables; copy to `.env` |
| `requirements.txt` | Python dependencies |
