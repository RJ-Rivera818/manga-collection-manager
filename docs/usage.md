# Usage Guide

How to use the Manga Collection Manager once it is set up. See the
[Setup Guide](setup.md) first if you have not run the program yet.

Start the program with:

```bash
python src/main.py
```

## Searching for a Series

Enter a full or partial title. Matching is not case sensitive.

- If several series match, choose one from the list.
- If only one series matches, it is selected automatically.

## Selecting an Edition

Each series can have more than one edition (for example, different
publishers or formats).

- If several editions exist, choose one from the list.
- If only one exists, it is selected automatically.
- The selected edition stays active while you manage the collection.
  Ownership is tracked separately for each edition.

## Viewing Your Collection

For the selected edition, the program shows:

- Volumes you own
- Volumes you are missing
- Collection completion percentage

## Adding and Removing Volumes

Volumes are entered as numbers, ranges, or a mix of both:

| Input | Meaning |
|-------|---------|
| `3` | Volume 3 |
| `1-5` | Volumes 1 through 5 |
| `1,3-5,8` | Volumes 1, 3, 4, 5, and 8 |

Rules:

- Duplicate volumes in one entry are only processed once.
- Invalid input (letters, bad ranges, volumes that do not exist) is rejected.
