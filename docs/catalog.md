# Catalog File

The program does not ship with a manga catalog. Each user creates their own
`.json` file describing their series, editions, and owned volumes, and then
loads it with the import script (see the [Setup Guide](setup.md)).

Use `database/manga_catalog.example.json` as a template.

## Example

```json
{
  "series": [
    {
      "name": "Example Manga",
      "alternate_name": null,
      "creators": [
        "Example Author"
      ],
      "status": "Ongoing",
      "start_date": "2024-01-01",
      "end_date": null,
      "date_notes": "Example dates for demonstration purposes.",
      "editions": [
        {
          "name": "Standard Edition",
          "publisher": "Example Publisher",
          "format_label": "Paperback",
          "volume_count": 5,
          "owned_volumes": [1, 2, 3],
          "notes": "Example edition. Volumes 4 and 5 are not owned."
        }
      ]
    }
  ]
}
```

## Structure

The file has one top-level key, `series`, which holds a list of series.
Each series holds a list of `editions`.
fields preceded by a `*` are required  

### Series fields

| Field | Type | Description |
|-------|------|-------------|
| * `name`| string | Series title | 
| `alternate_name` | string or `null` | Another title for the series, such as a translated or original title |
| `creators` | list of strings | Names of the series creators |
| `status` | string | One of `Ongoing`, `Completed`, `Cancelled`, `Unknown`, or `On Hold` |
| `start_date` | `YYYY-MM-DD` or `null` | When publication started |
| `end_date` | `YYYY-MM-DD` or `null` | When publication ended; `null` if ongoing or unknown |
| `date_notes` | string or `null` | Notes about the dates |
| `editions` | list | The editions of this series (see below) |

### Edition fields

| Field | Type | Description |
|-------|------|-------------|
| * `name` | string | Edition name |
| `publisher` | string | Publisher name |
| `format_label` | string | Format, such as `Paperback` |
| * `volume_count` | integer | Number of volumes in the edition |
| `owned_volumes` | list of integers | Volume numbers you own in this edition |
| `notes` | string | Free-form notes |


## Tips

- Make sure the file is valid JSON: no trailing commas, and strings in
  double quotes.
- Use the exact `status` values listed above.
- Keep `owned_volumes` within the edition's volume range, from 1 to
  `volume_count`.
- Start with one or two series to confirm the import works, then add the rest.
- Keep your personal catalog out of version control if you do not want to
  publish your collection.

## How the Data Is Used

The import script reads the catalog and fills the database tables described
in [Database](database.md). Ownership is stored per volume, so each edition
is tracked separately.
