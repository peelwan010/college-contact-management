from loaders import (
    load_aktu_roll_list,
    get_second_year_sheets,
    load_second_year_students,
    load_first_year_contacts
)


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def main_menu():
    print("\nCollege Contact Management System")
    print("1. View AKTU Roll List")
    print("2. View Second Year Students")
    print("3. View First Year Contacts")
    print("4. Exit")
    return get_int("Enter choice: ")


def run():
    while True:
        choice = main_menu()

        if choice == 1:
            print(load_aktu_roll_list().head(20))

        elif choice == 2:
            sheets = get_second_year_sheets()
            for i, s in enumerate(sheets, 1):
                print(f"{i}. {s}")

            idx = get_int("Select sheet number: ")
            if 1 <= idx <= len(sheets):
                df = load_second_year_students(sheets[idx - 1])
                print(df.head(20))
            else:
                print("Invalid selection")

        elif choice == 3:
            print(load_first_year_contacts().head(20))

        elif choice == 4:
            print("Exiting.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run()
