import mysql.connector


#starts the connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="USER",
    password="***PASSWORD***",
    database="manga_collection"
)
print("Connected to MySQL!\n")

#search function
def search_series():
    search = input("What manga are you seaching for?: " )

    cursor = db.cursor()


    cursor.execute(
        "SELECT * FROM series WHERE name = %s",
        (search,)
)



    result = cursor.fetchone()

    if result is None:
        print("Series not found")
        return None
    else:
        print("\n",result[1])
        print(f"Status: {result[4]}\n")
        return result

#outputs vols formated in proper ranges
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

#series data fetch function
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
            print(f"Your collection is {completion:.1%} complete")










series_data()


