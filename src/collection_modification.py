import random
import string

# collection modification function
def collection_mod():
    print("\n")
    user_collection_choice = input("What would you like to do? \n1. add a volume \n2. Remove a volume \n>  ")
    return user_collection_choice

# adding volumes
def add_volume(db, edition_id):
    prefix = "OWN"
    print("\n")

    volume_input = input("What volumes are you adding: ")
    volume_number_list = volume_input.split(",")

    cursor = db.cursor()

    for volume_number in volume_number_list:
        volume_number = volume_number.strip()

        cursor.execute(
            "SELECT * FROM volume WHERE edition_id = %s AND volume_number = %s",
            (edition_id, volume_number,)
        )

        volume = cursor.fetchone()

        if volume is None:
            print(f"Volume {volume_number} not found")
            continue

        volume_id = volume[0]

        cursor.execute(
            "SELECT * FROM ownership WHERE volume_id = %s",
            (volume_id,)
        )

        ownership = cursor.fetchone()

        if ownership is None:
            ownership_id = prefix + "".join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=9
                )
            )

            cursor.execute(
                "INSERT INTO Ownership (volume_id, ownership_id) VALUES (%s, %s)",
                (volume_id, ownership_id)
            )

            print(f"Volume {volume_number} added successfully!")
        else:
            print(f"You already own Volume {volume_number}!")

    db.commit()

# removing volumes
def remove_volume(db, edition_id):
# vars
    volume_number = input("what volumes are you removing? ")

    volume_number_list = volume_number.split(",")

    cursor = db.cursor()

    for volume_number in volume_number_list:
        volume_number = volume_number.strip()

        cursor.execute(
        "SELECT * FROM volume WHERE edition_id =%s AND volume_number = %s",
        (edition_id, volume_number,)
        )

        volume = cursor.fetchone()

        if volume is None:
            print(f"Volume {volume_number} not found")
            continue

        volume_id = volume[0]

        cursor.execute(
            "SELECT * FROM ownership WHERE volume_id = %s",
            (volume_id,)
        )

        ownership = cursor.fetchone()

        if ownership is None:
            print(f"Volume {volume_number} not in collection")
        else:
            cursor.execute(
        "DELETE FROM ownership WHERE volume_id = %s",
    (volume_id,)
            )
            print(f"Volume {volume_number} removed successfully!")
    db.commit()