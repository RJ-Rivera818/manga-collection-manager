# Database

The program uses a MySQL database named `manga_collection`. The schema is
defined in `database/schema.sql`, which begins with `USE manga_collection;`,
so the database must be created before the schema is loaded (see the
[Setup Guide](setup.md)).

## Tables

| Table | Purpose |
|-------|---------|
| `series` | A manga series (one title) |
| `creator` | A person who created a series (author, artist, etc.) |
| `series_creators` | Links series to creators (many-to-many) |
| `edition` | A specific edition of a series |
| `volume` | A volume within an edition |
| `ownership` | Which volumes the user owns |

## Relationships

```
creator >──< series        (through series_creators)
series  1──< edition       (a series has one or more editions)
edition 1──< volume        (an edition has one or more volumes)
volume  1──o ownership     (a volume is owned or not)
```

- A series can have many creators, and a creator can work on many series.
  The `series_creators` table connects them.
- Each edition belongs to one series, and each volume belongs to one edition.
- A volume has at most one `ownership` row. If the row exists, the volume is
  owned. Because ownership points to a volume, and each volume belongs to
  one edition, each edition is tracked separately.

## Columns

All IDs are 12-character strings (`CHAR(12)`) rather than auto-incrementing
numbers.

### `series`

| Column | Type | Description |
|--------|------|-------------|
| `series_id` | `CHAR(12)` | Primary key |
| `name` | `VARCHAR(255)` | Series title (required) |
| `start_date` | `DATE` | Publication start date (optional) |
| `end_date` | `DATE` | Publication end date (optional) |
| `status` | `ENUM` | `Ongoing`, `Completed`, `Cancelled`, `Unknown`, or `On Hold`. Defaults to `Unknown` |

### `creator`

| Column | Type | Description |
|--------|------|-------------|
| `creator_id` | `CHAR(12)` | Primary key |
| `name` | `VARCHAR(255)` | Creator name (required) |

### `series_creators`

| Column | Type | Description |
|--------|------|-------------|
| `series_id` | `CHAR(12)` | Foreign key to `series` |
| `creator_id` | `CHAR(12)` | Foreign key to `creator` |

The primary key is the pair (`series_id`, `creator_id`), so the same creator
cannot be linked to the same series twice.

### `edition`

| Column | Type | Description |
|--------|------|-------------|
| `edition_id` | `CHAR(12)` | Primary key |
| `series_id` | `CHAR(12)` | Foreign key to `series` (required) |
| `name` | `VARCHAR(255)` | Edition name (required) |
| `publisher` | `VARCHAR(255)` | Publisher (optional) |
| `volume_count` | `INT` | Number of volumes in the edition (required) |
| `format_label` | `VARCHAR(100)` | Format description (optional) |
| `notes` | `TEXT` | Free-form notes (optional) |

### `volume`

| Column | Type | Description |
|--------|------|-------------|
| `volume_id` | `CHAR(12)` | Primary key |
| `edition_id` | `CHAR(12)` | Foreign key to `edition` (required) |
| `volume_number` | `VARCHAR(255)` | Volume number, stored as text (required) |
| `notes` | `TEXT` | Free-form notes (optional) |

The pair (`edition_id`, `volume_number`) is unique, so an edition cannot
have two volumes with the same number.

### `ownership`

| Column | Type | Description |
|--------|------|-------------|
| `ownership_id` | `CHAR(12)` | Primary key |
| `volume_id` | `CHAR(12)` | Foreign key to `volume` (required, unique) |

The `UNIQUE` constraint on `volume_id` means each volume can be marked as
owned only once. The program tracks whether a volume is owned, not how many
copies exist.

## Catalog Data

Series, editions, volumes, and owned volumes are loaded from a `.json`
catalog that each user writes themselves. `src/import_catalog.py` reads it
and fills the tables above. See [Catalog File](catalog.md) for the format.
