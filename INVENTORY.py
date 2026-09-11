# BASIC STOCK INVENTORY MONITORING SYSTEM
# MJ MIDDLE EASTERN HALAL RESTAURANT

LOW_STOCK = 10

# Accounts
staff_username = "staff"
staff_password = "12345"

manager_username = "manager"
manager_password = "manager123"

# Inventory

inventory = {}

# LOGIN FUNCTIONS

def staff_login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == staff_username and password == staff_password:
        print("\nStaff login successful!")
        return True
    else:
        print("Invalid username or password.")
        return False


def manager_login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == manager_username and password == manager_password:
        print("\nManager login successful!")
        return True
    else:
        print("Invalid username or password.")
        return False

# INVENTORY FUNCTIONS

def add_inventory():
    item = input("Enter item name: ").lower()

    if item == "":
        print("Item name cannot be empty.")
        return

    quantity = float(input("Enter quantity: "))
    unit = input("Enter unit (kg/pcs/L/packs): ")

    inventory[item] = {
        "quantity": quantity,
        "unit": unit
    }

    print("Item added successfully!")


def update_stock():
    item = input("Enter item name: ").lower()

    if item in inventory:

        print("1. Increase Stock")
        print("2. Decrease Stock")

        update = input("Choose an option: ")
        quantity = float(input("Enter quantity: "))

        if update == "1":

            inventory[item]["quantity"] += quantity
            print("Stock increased successfully!")

        elif update == "2":

            if quantity <= inventory[item]["quantity"]:
                inventory[item]["quantity"] -= quantity
                print("Stock decreased successfully!")
            else:
                print("Not enough stock.")

        else:
            print("Invalid choice.")

    else:
        print("Item not found.")


def search_item():
    item = input("Enter item name: ").lower()

    if item in inventory:

        print(
            "Item:", item,
            "\nQuantity:",
            inventory[item]["quantity"],
            inventory[item]["unit"]
        )

    else:
        print("Item not found.")


def view_inventory():
    print("\n===== CURRENT INVENTORY =====")

    if len(inventory) == 0:
        print("Inventory is empty.")

    else:
        for item in inventory:
            print(
                item.title(),
                "-",
                inventory[item]["quantity"],
                inventory[item]["unit"]
            )


def delete_item():
    item = input("Enter item name to delete: ").lower()

    if item in inventory:

        del inventory[item]

        print("Item deleted successfully!")

    else:
        print("Item not found.")


def check_low_stock():
    print("\n===== LOW STOCK ITEMS =====")

    found = False

    for item in inventory:

        if inventory[item]["quantity"] <= LOW_STOCK:

            print(
                item.title(),
                "-",
                inventory[item]["quantity"],
                inventory[item]["unit"],
                "- LOW STOCK"
            )

            found = True

    if found == False:
        print("No low stock items.")


def check_available_stock():
    print("\n===== AVAILABLE STOCK =====")

    for item in inventory:

        if inventory[item]["quantity"] > LOW_STOCK:

            print(
                item.title(),
                "-",
                inventory[item]["quantity"],
                inventory[item]["unit"],
                "- Available"
            )


# STAFF MENU

def staff_menu():

    while True:

        print("\n===== STAFF MENU =====")
        print("1. Add Inventory")
        print("2. Update Stock")
        print("3. Search Item")
        print("4. View Inventory")
        print("5. Delete Item")
        print("6. Check Low Stock")
        print("7. Logout")

        staff_choice = input("Choose an option: ")

        if staff_choice == "1":
            add_inventory()

        elif staff_choice == "2":
            update_stock()

        elif staff_choice == "3":
            search_item()

        elif staff_choice == "4":
            view_inventory()

        elif staff_choice == "5":
            delete_item()

        elif staff_choice == "6":
            check_low_stock()

        elif staff_choice == "7":
            print("Staff logged out.")
            break

        else:
            print("Invalid choice.")

# MANAGER MENU

def manager_menu():

    while True:

        print("\n===== MANAGER MENU =====")
        print("1. View Inventory")
        print("2. Search Item")
        print("3. Check Low Stock")
        print("4. Check Available Stock")
        print("5. Logout")

        manager_choice = input("Choose an option: ")

        if manager_choice == "1":
            view_inventory()

        elif manager_choice == "2":
            search_item()

        elif manager_choice == "3":
            check_low_stock()

        elif manager_choice == "4":
            check_available_stock()

        elif manager_choice == "5":
            print("Manager logged out.")
            break

        else:
            print("Invalid choice.")

# MAIN SYSTEM

def main():

    while True:

        print("\n==============================")
        print(" STOCK INVENTORY SYSTEM")
        print("==============================")
        print("1. Staff Login")
        print("2. Manager Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        # STAFF LOGIN
        if choice == "1":

            if staff_login():
                staff_menu()

        # MANAGER LOGIN
        elif choice == "2":

            if manager_login():
                manager_menu()

        # EXIT
        elif choice == "3":

            print("\nThank you for using the system!")
            break

        else:

            print("Invalid choice.")


# ==========================================
# RUN PROGRAM
# ==========================================

main()
