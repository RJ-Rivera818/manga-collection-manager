
import json
import uuid
from pathlib import Path
from getpass import getpass

import mysql.connector


def new_id():
    return uuid.uuid4().hex[:12]


def main():
    catalog_path = (
        Path(__file__).resolve().parent.parent
        / "database"
        / "manga_catalog.json"
    )

    with catalog_path.open("r", encoding="utf-8") as file:
        catalog = json.load(file)

    password = getpass("MySQL root password: ")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="manga_collection",
    )

    cursor = connection.cursor()
    creator_ids = {}
    volume_ids = {}

    try:
        # Avoid accidentally importing the catalog twice.
        cursor.execute("SELECT COUNT(*) FROM series")
        if cursor.fetchone()[0] > 0:
            raise ValueError(
                "The series table is not empty. Import cancelled."
            )

        for item in catalog["series"]:
            series_id = new_id()

            cursor.execute(
                """
                INSERT INTO series
                    (series_id, name, start_date, end_date, status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    series_id,
                    item["name"],
                    item.get("start_date"),
                    item.get("end_date"),
                    item["status"],
                ),
            )

            for creator_name in item.get("creators", []):
                if creator_name not in creator_ids:
                    creator_id = new_id()
                    creator_ids[creator_name] = creator_id

                    cursor.execute(
                        """
                        INSERT INTO creator (creator_id, name)
                        VALUES (%s, %s)
                        """,
                        (creator_id, creator_name),
                    )

                cursor.execute(
                    """
                    INSERT INTO series_creators (series_id, creator_id)
                    VALUES (%s, %s)
                    """,
                    (series_id, creator_ids[creator_name]),
                )

            for edition in item["editions"]:
                edition_id = new_id()

                cursor.execute(
                    """
                    INSERT INTO edition
                        (edition_id, series_id, name, publisher,
                         volume_count, format_label, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        edition_id,
                        series_id,
                        edition["name"],
                        edition.get("publisher"),
                        edition["volume_count"],
                        edition.get("format_label"),
                        edition.get("notes"),
                    ),
                )

                owned = {int(v) for v in edition["owned_volumes"]}
                volume_count = int(edition["volume_count"])

                # Include standard volumes and any extra owned volumes,
                # such as Jujutsu Kaisen volume 0.
                volume_numbers = set(range(1, volume_count + 1)) | owned

                for number in sorted(volume_numbers):
                    volume_id = new_id()

                    cursor.execute(
                        """
                        INSERT INTO volume
                            (volume_id, edition_id, volume_number)
                        VALUES (%s, %s, %s)
                        """,
                        (volume_id, edition_id, str(number)),
                    )

                    volume_ids[(edition_id, number)] = volume_id

                    if number in owned:
                        cursor.execute(
                            """
                            INSERT INTO ownership (ownership_id, volume_id)
                            VALUES (%s, %s)
                            """,
                            (new_id(), volume_id),
                        )

        connection.commit()

        cursor.execute("SELECT COUNT(*) FROM series")
        series_total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM edition")
        edition_total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM volume")
        volume_total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM ownership")
        owned_total = cursor.fetchone()[0]

        print("\nImport successful!")
        print(f"Series: {series_total}")
        print(f"Editions: {edition_total}")
        print(f"Volume records: {volume_total}")
        print(f"Owned volumes: {owned_total}")
        print(f"Creators: {len(creator_ids)}")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()