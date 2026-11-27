def welcome_selection():
    print("\nWelcome to the Manga Collection Manager!! - (Hondana) ")
    welcome_choice = input("\nWould you like to: "
                           "\n1. Search your collection?"
                           "\n2. Search for a new series"
                           "\n> ")
    if welcome_choice not in ["1", "2"]:
        print("\nPlease enter either '1' or '2'")
        return welcome_selection()
    else:
        return welcome_choice
