from pathlib import Path
from schedule import Schedule

DEFAULT = Path(__file__).with_name("courses_2023.csv")


def display(items):
    if not items:
        print("No matches found.")
        return
    for item in items:
        print(item)
    print(f"{len(items)} record(s)")


def main(path=DEFAULT):
    schedule = Schedule()
    try:
        schedule.load(path)
    except (OSError, ValueError) as exc:
        print(f"Unable to load schedule: {exc}")
        return
    print(f"Loaded {schedule.rows} rows; {schedule.duplicates} repeated keys.")
    for error in schedule.errors:
        print(error)
    while True:
        print(f"\nActive tree: {schedule.backend}")
        print("1. View all\n2. Exact key\n3. Filter courses\n4. Tree height\n5. Switch tree\n0. Exit")
        try:
            choice = input("Choice: ").strip()
            if choice == "0":
                print("Goodbye.")
                return
            elif choice == "1":
                display(schedule.items())
            elif choice == "2":
                item = schedule.find(input("Subject: "), input("Catalog: "), input("Section: "))
                display([item] if item else [])
            elif choice == "3":
                display(schedule.filter(*(input(f"{field} (blank for any): ") for field in ("Subject", "Catalog", "Section", "Instructor surname"))))
            elif choice == "4":
                print(f"{schedule.backend} height: {schedule.height()}")
            elif choice == "5":
                other = Schedule("AVL" if schedule.backend == "BST" else "BST")
                try:
                    other.load(path)
                    schedule = other
                    print(f"Switched to {schedule.backend}.")
                except (OSError, ValueError) as exc:
                    print(f"Unable to switch: {exc}")
            else:
                print("Invalid menu choice.")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return


if __name__ == "__main__":
    main()
