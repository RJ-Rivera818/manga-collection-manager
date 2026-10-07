import mysql.connector
import random
import string

# starts the connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="USER",
    password="***PASSWORD***",
    database="manga_collection"
)
print("Connected to MySQL!\n")


# collection modification function
def collection_mod():
    print("\n")
    user_choice = input("What would you like to do? \n1. add a volume \n2. Remove a volume \n>  ")
    return user_choice

# adding volumes
def add_volume():
    prefix = "OWN"
    print("\n")

    volume_input = input("What volumes are you adding: ")
    volume_number_list = volume_input.split(",")

    cursor = db.cursor()

    for volume_number in volume_number_list:
        volume_number = volume_number.strip()

        cursor.execute(
            "SELECT * FROM volume WHERE volume_number = %s",
            (volume_number,)
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
def remove_volume():
# vars
    volume_number = input("what volumes are you removing? ")

    volume_number_list = volume_number.split(",")

    cursor = db.cursor()

    for volume_number in volume_number_list:
        volume_number = volume_number.strip()

        cursor.execute(
        "SELECT * FROM volume WHERE volume_number = %s",
        (volume_number,)
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

# search function
def search_series():

    search = input("\nWhat manga are you seaching for?: " )

    cursor = db.cursor()


    cursor.execute(
        "SELECT * FROM series WHERE name = %s",
        (search,)
)



    result = cursor.fetchone()

    if result is None:
        print("- Series not found")
        user_menu_choice = input("\nWould you like to search or another series (y/n): ")
        if user_menu_choice == "y":
            series_data()
            return None
        elif user_menu_choice == "n":
            print("\nHappy collecting!!")
    else:
        print("\n",result[1])
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
def series_data():
    cursor = db.cursor()

    #function call
    series = search_series()
    if series is None:
        return
    series_id = series[0]


    cursor.execute(
        "Select * FROM edition WHERE series_id = %s",
        (series_id,)
        )

    editions = cursor.fetchall()
    if not editions:
        print("No editions found")
        user_menu_choice = input("\nWould you like to search or another series (y/n): ")
        if user_menu_choice == "y":
            series_data()
            return None
        elif user_menu_choice == "n":
            print("\nHappy collecting!!")
        return

#gets editions
    for edition in editions:
        edition_id = edition[0]

        cursor.execute(
            "SELECT * FROM volume WHERE edition_id = %s",
            (edition_id,)
        )

        volumes = cursor.fetchall()

    #gets volumes
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



        #vars
        owned_list = list(statuses.values())
        owned_count = owned_list.count("Owned")
        missing_count = (edition[4] - owned_count)
        completion = ( owned_count / edition[4] )

        #output
        print(f"{edition[2]} - {edition[3]} - {edition[4]} volumes")
        print(f"You Own: {owned_count}/{edition[4]} volumes")
        print(f"You are missing: {missing_count} volumes")
        if (completion) == 1:
            print("100% completion!!")
        else:
            print(f"Your collection is {completion:.1%} complete\n")
        print_volume_ranges(statuses)
        user_choice = input("\nWould you like to add/remove volumes for this series (y/n): ")
        if user_choice == "y":
            collection_mod_menu_choice = collection_mod()
            if collection_mod_menu_choice == "1":
                add_volume()
                return
            elif collection_mod_menu_choice == "2":
                remove_volume()
                return
        elif user_choice == "n":
            series_data()
            return
        else:
            while user_choice != "y" and user_choice != "n":
                user_choice = input(f"You have to enter either 'y' or 'n': ")
                if user_choice == "y":
                    collection_mod_menu_choice = collection_mod()
                    if collection_mod_menu_choice == "1":
                        add_volume()
                        return
                    elif collection_mod_menu_choice == "2":
                        remove_volume()
                        return
                elif user_choice == "n":
                    series_data()
                    return


series_data()





