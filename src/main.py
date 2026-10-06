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
        print(f"Status: {result[4]}")
        return result

#series id fetch function
def series_data():
    cursor = db.cursor()

    #function call
    series = search_series()
    series_id = series[0]


    cursor.execute(
        "Select * FROM edition WHERE series_id = %s",
        (series_id,)
        )

    editions = cursor.fetchall()

#gets editions
    for edition in editions:
        edition_id = edition[0]

        cursor.execute(
            "SELECT * FROM volume WHERE edition_id = %s",
            (edition_id,)
        )

        volumes = cursor.fetchall()

    #gets volumes
        print(f"{edition[2]} - {edition[3]} - {edition[4]} volumes")

        for volume in volumes:
            volume_id = volume[0]

            cursor.execute(
                "SELECT * FROM ownership WHERE volume_id = %s",
                (volume_id,)
            )

            ownership = cursor.fetchone()
            if(ownership == None):
                print(f"Volume {volume[2]} - Missing")
            else:
                print(f"Volume {volume[2]} - Owned")


series_data()
