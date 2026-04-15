"""Menu-driven interactive CLI loop."""


def start_menu() -> int:
    """Start a basic interactive menu loop."""
    while True:
        print("\nJOC-USB Interactive Menu")
        print("1) Run scan")
        print("2) Exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            print("Scan is available via: python -m cli.main")
        elif choice == "2":
            return 0
        else:
            print("Invalid option.")
