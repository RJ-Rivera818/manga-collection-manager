from collection_modification import collection_mod, add_volume, remove_volume
from series import search_series, print_volume_ranges, series_data, edition_selection, series_search_selection
from database_connect import database_connection



# main
def main():
    db = database_connection()

    while True:
        series = search_series(db)

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
            selected_edition = series_data(db, series, selected_edition)

            if selected_edition is None:
                break

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
