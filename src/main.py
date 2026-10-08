import os
import mysql.connector
from collection_modification import collection_mod, add_volume, remove_volume

# starts the connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("***PASSWORD***"),
    database="manga_collection"
)
print("Connected to MySQL!\n")

# search function
def search_series():

    search = input("\nWhat manga are you seaching for?: ")

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM series WHERE name = %s",
        (search,)
    )

    result = cursor.fetchone()

    if result is None:
        print("- Series not found")
        return None

    print("\n", result[1])
    print(f"Status: {result[4]}\n")
    return result

# outputs vols formated in proper ranges
def print_volume_ranges(statuses):
    if not statuses:
        return

    volume_numbers = sorted(statuses)
    start = volume_numbers[0]
    end = volume_numbers[0]
    current_status = statuses[start]

    for number in volume_numbers[1:]:
        if number == end + 1 and statuses[number] == current_status:
            end = number
        else:
            if start == end:
                print(f"Volume {start} - {current_status}")
            else:
                print(f"Volume {start}-{end} - {current_status}")

            start = number
            end = number
            current_status = statuses[number]

    if start == end:
        print(f"Volume {start} - {current_status}")
    else:
        print(f"Volume {start}-{end} - {current_status}")

# series data fetch function
def series_data(series=None, selected_edition=None):
    cursor = db.cursor()

    if series is None:
        series = search_series()

    if series is None:
        return

    series_id = series[0]

    cursor.execute(
        "SELECT * FROM edition WHERE series_id = %s",
        (series_id,)
    )

    editions = cursor.fetchall()

    if not editions:
        print("No editions found")
        return

    # gets edition
    if selected_edition is None:
        selected_edition = edition_selection(editions)
    edition_id = selected_edition[0]

    cursor.execute(
        "SELECT * FROM volume WHERE edition_id = %s",
        (edition_id,)
    )

    volumes = cursor.fetchall()

    # gets volumes
    statuses = {}

    for volume in volumes:
        volume_id = volume[0]
        volume_number = int(volume[2])

        cursor.execute(
            "SELECT * FROM ownership WHERE volume_id = %s",
            (volume_id,)
        )

        ownership = cursor.fetchone()

        if ownership is None:
            statuses[volume_number] = "Missing"
        else:
            statuses[volume_number] = "Owned"

    # vars
    owned_list = list(statuses.values())
    owned_count = owned_list.count("Owned")
    missing_count = selected_edition[4] - owned_count
    completion = owned_count / selected_edition[4]

    # output
    print(
        f"{selected_edition[2]} - "
        f"{selected_edition[3]} - "
        f"{selected_edition[4]} volumes"
    )
    print(f"You Own: {owned_count}/{selected_edition[4]} volumes")
    print(f"You are missing: {missing_count} volumes")

    if completion == 1:
        print("100% completion!!")
    else:
        print(f"Your collection is {completion:.1%} complete\n")

    print_volume_ranges(statuses)

    return selected_edition

#
def edition_selection(editions):
    print("\nAvailable Editions:")

    for i, edition in enumerate(editions, start=1):
        print(
            f"{i}. {edition[2]} - "
            f"{edition[3]} - "
            f"{edition[4]} volumes"
        )

    edition_choice = input("\nWhich edition would you like to select? ")

    while not edition_choice.isdigit() or not 1 <= int(edition_choice) <= len(editions):
        print(f"Please enter a number from 1 to {len(editions)}.")
        edition_choice = input("\nWhich edition would you like to select? ")

    selected_edition = editions[int(edition_choice) - 1]

    return selected_edition

# main
def main():
    while True:
        series = search_series()

        # Handle a failed search
        if series is None:
            user_search_choice = input(
                "\nWould you like to search again? (y/n): "
            ).lower()

            while user_search_choice not in ["y", "n"]:
                print("You must enter either 'y' or 'n'.")
                user_search_choice = input(
                    "\nWould you like to search again? (y/n): "
                ).lower()

            if user_search_choice == "y":
                continue
            else:
                print("\nHappy collecting!!")
                break

        # Work with the current series
        selected_edition = None

        while True:
            selected_edition = series_data(series, selected_edition)

            add_remove_choice = input(
                "\nWould you like to add/remove volumes from this series? (y/n): "
            ).lower()

            while add_remove_choice not in ["y", "n"]:
                print("You must enter either 'y' or 'n'.")
                add_remove_choice = input(
                    "\nWould you like to add/remove volumes from this series? (y/n): "
                ).lower()

            if add_remove_choice == "n":
                break

            collection_mod_menu_choice = collection_mod()

            while collection_mod_menu_choice not in ["1", "2"]:
                print("You must enter either '1' or '2'.")
                collection_mod_menu_choice = collection_mod()

            if collection_mod_menu_choice == "1":
                add_volume(db, selected_edition[0])

            elif collection_mod_menu_choice == "2":
                remove_volume(db, selected_edition[0])

        # Ask whether to search for another series
        user_search_choice = input(
            "\nWould you like to search for another series? (y/n): "
        ).lower()

        while user_search_choice not in ["y", "n"]:
            print("You must enter either 'y' or 'n'.")
            user_search_choice = input(
                "\nWould you like to search for another series? (y/n): "
            ).lower()

        if user_search_choice == "n":
            print("\nHappy collecting!!")
            break


main()
