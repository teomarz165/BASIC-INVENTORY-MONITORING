# STOCK INVENTORY MONITORING SYSTEM
# MJ Middle Eastern Halal Restaurant
#
# Type 0 or exit at any prompt to go back.

# Predetermined accounts
manager_accounts = {"manager": "manager123"}
staff_accounts = {"staff1": "staff123", "staff2": "staff456"}

# Inventory is saved using the lowercase item name
inventory = {}

# Predefined items: number -> [name, unit, minimum]
# Number 1 is always "Add New Item"
item_list = {
    "2": ["Chicken", "kg", 20],
    "3": ["Beef", "kg", 20],
    "4": ["Rice", "kg", 10],
    "5": ["Cooking Oil", "L", 4],
    "6": ["Garlic", "kg", 2],
    "7": ["Onion", "kg", 2],
    "8": ["Flour", "kg", 10],
    "9": ["Potatoes", "kg", 5]
}


# ---------- Helper functions ----------
def pause():
    input("\nPress Enter to continue...")


def is_exit(text):
    if text.lower() == "0" or text.lower() == "exit":
        return True
    return False


def yes_no(message):
    # Returns "Y", "N" or "EXIT"
    while True:
        answer = input(message).strip().upper()
        if answer == "Y":
            return "Y"
        elif answer == "N":
            return "N"
        elif is_exit(answer):
            return "EXIT"
        else:
            print("Wrong choice. Please enter Y or N.")


def valid_number(value):
    try:
        number = float(value)
        if number > 0:
            return True
        return False
    except:
        return False


def ask_quantity(message):
    # Returns the quantity, or 0 if the user exits
    while True:
        value = input(message).strip()
        if is_exit(value):
            return 0
        if valid_number(value):
            return float(value)
        print("Invalid quantity. Enter a number greater than 0.")


def show_qty(number):
    # Show 5.0 as 5
    if number == int(number):
        return str(int(number))
    return str(number)


def show_item(item):
    print("- " + item["name"] + ": " + show_qty(item["quantity"]) + " " + item["unit"])


def show_all_items():
    for key in inventory:
        show_item(inventory[key])


def is_low(item):
    # Low stock when quantity is at or below the minimum
    if item["minimum"] > 0 and item["quantity"] <= item["minimum"]:
        return True
    return False


def get_low_stock_names():
    # Returns a list of the names of items that are low on stock
    names = []
    for key in inventory:
        if is_low(inventory[key]):
            names.append(inventory[key]["name"])
    return names


def find_slot(name):
    # Find the number of an item in the predefined list
    for number in item_list:
        if item_list[number][0].lower() == name.lower():
            return number
    return ""


def next_free_slot():
    # First free number starting at 2
    number = 2
    while str(number) in item_list:
        number = number + 1
    return str(number)


# ---------- Search ----------
def search_item():
    if len(inventory) == 0:
        print("\nNo inventory items yet.")
        pause()
        return

    while True:
        print("\n--- SEARCH INVENTORY ---")
        term = input("Enter item name to search: ").strip().lower()
        if is_exit(term):
            return

        found = False
        for key in inventory:
            if term in key:
                if not found:
                    print("\nItem found:")
                found = True
                show_item(inventory[key])

        if not found:
            print("Item not found.")

        answer = yes_no("Search another item? (Y/N): ")
        if answer != "Y":
            return


# ---------- Add inventory ----------
def add_inventory():
    while True:
        print("\n--- ADD INVENTORY ITEM ---")
        print("1. Add New Item")
        for number in range(2, 100):
            if str(number) in item_list:
                print(str(number) + ". " + item_list[str(number)][0])
        print("0. Exit")

        choice = input("Enter choice: ").strip()
        if is_exit(choice):
            return

        new_item = False

        if choice == "1":
            name = input("Enter item name: ").strip().lower()
            if is_exit(name):
                return
            if name == "":
                print("Item name cannot be empty.")
                continue

            slot = find_slot(name)
            if slot != "":
                # Name is already in the predefined list
                name = item_list[slot][0]
                unit = item_list[slot][1]
                minimum = item_list[slot][2]
            elif name in inventory:
                unit = inventory[name]["unit"]
                minimum = 0
            else:
                unit = input("Enter unit (kg, L, pcs): ").strip()
                if is_exit(unit):
                    return
                if unit == "":
                    print("Unit cannot be empty.")
                    continue
                minimum = 0
                new_item = True

        elif choice in item_list:
            name = item_list[choice][0]
            unit = item_list[choice][1]
            minimum = item_list[choice][2]

        else:
            print("Wrong choice. Please choose from the list.")
            continue

        name = name.title()
        key = name.lower()

        if key in inventory:
            # Item already exists, add stock
            print("\n" + name + " already exists in inventory.")
            print("Current Stock: " + show_qty(inventory[key]["quantity"]) + " " + inventory[key]["unit"])

            answer = yes_no("Add stock to this item? (Y/N): ")
            if answer == "EXIT":
                return
            if answer == "Y":
                quantity = ask_quantity("Enter quantity to add: ")
                if quantity == 0:
                    return
                inventory[key]["quantity"] = inventory[key]["quantity"] + quantity
                print("\nStock added successfully.")
                print("Current Stock: " + show_qty(inventory[key]["quantity"]) + " " + inventory[key]["unit"])
        else:
            quantity = ask_quantity("Enter quantity (" + unit + "): ")
            if quantity == 0:
                return

            print("\nItem: " + name)
            print("Quantity: " + show_qty(quantity) + " " + unit)

            answer = yes_no("Confirm adding this item? (Y/N): ")
            if answer == "EXIT":
                return
            if answer == "Y":
                inventory[key] = {
                    "name": name,
                    "quantity": quantity,
                    "unit": unit,
                    "minimum": minimum
                }

                if new_item:
                    # New item also goes into the predefined list
                    slot = next_free_slot()
                    item_list[slot] = [name, unit, minimum]
                    print("\n" + name + " added successfully as number " + slot + ".")
                else:
                    print("\n" + name + " added successfully.")
            else:
                print("Item not added.")

        answer = yes_no("Add another item? (Y/N): ")
        if answer != "Y":
            return


# ---------- Decrease stock ----------
def decrease_stock():
    if len(inventory) == 0:
        print("\nNo inventory items yet.")
        pause()
        return

    while True:
        print("\n--- DECREASE STOCK ---")
        show_all_items()

        key = input("Enter item name: ").strip().lower()
        if is_exit(key):
            return
        if key not in inventory:
            print("Item not found.")
            continue

        item = inventory[key]
        print("\nItem: " + item["name"])
        print("Current Stock: " + show_qty(item["quantity"]) + " " + item["unit"])

        while True:
            quantity = ask_quantity("Enter quantity to decrease (" + item["unit"] + "): ")
            if quantity == 0:
                return
            if quantity <= item["quantity"]:
                break
            print("Cannot decrease more than the current stock.")

        answer = yes_no("Decrease " + item["name"] + " by " + show_qty(quantity) + " " + item["unit"] + "? (Y/N): ")
        if answer == "EXIT":
            return
        if answer == "Y":
            item["quantity"] = item["quantity"] - quantity
            print("\nStock decreased successfully.")
            print("Current Stock: " + show_qty(item["quantity"]) + " " + item["unit"])

            if is_low(item):
                print("WARNING: " + item["name"] + " is low on stock!")
        else:
            print("Decrease cancelled.")

        answer = yes_no("Decrease another item? (Y/N): ")
        if answer != "Y":
            return


# ---------- View inventory ----------
def view_inventory():
    print("\n--- CURRENT INVENTORY ---")

    if len(inventory) == 0:
        print("No inventory items yet.")
    else:
        show_all_items()

    pause()


# ---------- Low-stock monitoring ----------
def low_stock_monitoring():
    print("\n--- LOW-STOCK MONITORING ---")

    found = False
    no_minimum = False

    for key in inventory:
        item = inventory[key]
        if is_low(item):
            found = True
            print("- " + item["name"] + ": " + show_qty(item["quantity"]) + " " + item["unit"]
                  + " (Minimum: " + show_qty(item["minimum"]) + " " + item["unit"] + ") - LOW STOCK")
        if item["minimum"] == 0:
            no_minimum = True

    if not found:
        print("No low-stock items.")

    if no_minimum:
        print("\nNote: Some items have no minimum stock set yet.")
        print("Use Set Minimum Stock so they can be monitored.")

    pause()


# ---------- Set minimum stock ----------
def set_minimum_stock():
    if len(inventory) == 0:
        print("\nNo inventory items yet.")
        pause()
        return

    while True:
        print("\n--- SET MINIMUM STOCK ---")
        show_all_items()

        key = input("Enter item name: ").strip().lower()
        if is_exit(key):
            return
        if key not in inventory:
            print("Item not found.")
            continue

        item = inventory[key]
        minimum = ask_quantity("Enter minimum stock for " + item["name"] + " (" + item["unit"] + "): ")
        if minimum == 0:
            return

        answer = yes_no("Set minimum of " + item["name"] + " to " + show_qty(minimum) + " " + item["unit"] + "? (Y/N): ")
        if answer == "EXIT":
            return
        if answer == "Y":
            item["minimum"] = minimum

            # Keep the predefined list updated too
            slot = find_slot(item["name"])
            if slot != "":
                item_list[slot][2] = minimum

            print("Minimum stock updated successfully.")
        else:
            print("Update cancelled.")

        answer = yes_no("Set minimum stock for another item? (Y/N): ")
        if answer != "Y":
            return


# ---------- Remove inventory item ----------
def remove_inventory():
    if len(inventory) == 0:
        print("\nNo inventory items yet.")
        pause()
        return

    while True:
        print("\n--- REMOVE INVENTORY ITEM ---")
        show_all_items()

        key = input("Enter item name: ").strip().lower()
        if is_exit(key):
            return
        if key not in inventory:
            print("Item not found.")
            continue

        item = inventory[key]
        answer = yes_no("Remove " + item["name"] + "? (Y/N): ")
        if answer == "EXIT":
            return
        if answer == "Y":
            # Free its number in the predefined list
            slot = find_slot(item["name"])
            if slot != "":
                del item_list[slot]

            del inventory[key]
            print("Item removed successfully.")
        else:
            print("Removal cancelled.")

        if len(inventory) == 0:
            return

        answer = yes_no("Remove another item? (Y/N): ")
        if answer != "Y":
            return


# ---------- Menus ----------
def manager_menu():
    while True:
        print("\n===== MANAGER MENU =====")
        low_items = get_low_stock_names()
        if len(low_items) > 0:
            print("ALERT: " + str(len(low_items)) + " item(s) low on stock! Check option 3.")
            print("Low items: " + ", ".join(low_items))
        print("1. View Inventory")
        print("2. Search Inventory")
        print("3. Low-Stock Monitoring")
        print("4. Set Minimum Stock")
        print("5. Remove Inventory Item")
        print("6. Logout")

        choice = input("Enter choice: ").strip().lower()

        if choice == "1":
            view_inventory()
        elif choice == "2":
            search_item()
        elif choice == "3":
            low_stock_monitoring()
        elif choice == "4":
            set_minimum_stock()
        elif choice == "5":
            remove_inventory()
        elif choice == "6" or is_exit(choice):
            print("Logging out...")
            return
        else:
            print("Wrong choice. Please choose 1-6.")


def staff_menu():
    while True:
        print("\n===== STAFF MENU =====")
        print("1. Add Inventory")
        print("2. Decrease Stock")
        print("3. Logout")

        choice = input("Enter choice: ").strip().lower()

        if choice == "1":
            add_inventory()
        elif choice == "2":
            decrease_stock()
        elif choice == "3" or is_exit(choice):
            print("Logging out...")
            return
        else:
            print("Wrong choice. Please choose 1-3.")


# ---------- Login ----------
def manager_login():
    print("\n--- MANAGER LOGIN ---")
    print("(Enter 0 as username to go back)")

    while True:
        username = input("Username: ").strip()
        if is_exit(username):
            return
        password = input("Password: ").strip()
        if password.lower() == "exit":
            return

        if username in manager_accounts and manager_accounts[username] == password:
            print("Login successful.")
            manager_menu()
            return

        print("Invalid username or password. Please try again.")


def staff_login():
    print("\n--- STAFF LOGIN ---")
    print("(Enter 0 as username to go back)")

    while True:
        username = input("Username: ").strip()
        if is_exit(username):
            return
        password = input("Password: ").strip()
        if password.lower() == "exit":
            return

        if username in staff_accounts and staff_accounts[username] == password:
            print("Login successful.")
            staff_menu()
            return

        print("Invalid username or password. Please try again.")


# ---------- Main program ----------
def main():
    while True:
        print("\n==============================")
        print("STOCK INVENTORY MONITORING SYSTEM")
        print("MJ MIDDLE EASTERN HALAL RESTAURANT")
        print("==============================")
        print("1. Manager Login")
        print("2. Staff Login")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip().lower()

        if choice == "1":
            manager_login()
        elif choice == "2":
            staff_login()
        elif choice == "3" or is_exit(choice):
            print("\nThank you for using the system.")
            break
        else:
            print("Wrong choice. Please choose 1-3.")


main()