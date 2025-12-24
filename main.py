# Administrator
ROOMS_FILE = "rooms.txt"
BOOKINGS_FILE = "bookings.txt"
GUESTS_FILE = "guests.txt"
MENU_FILE = "menu.txt"
FOOD_ORDERS_FILE = "orders.txt"
REPORTS_DIR = "reports"

# Ensure all required files exist
def initialize_system():
    """Initialize the system by creating necessary files if they don't exist."""
    for file in [ROOMS_FILE, BOOKINGS_FILE, GUESTS_FILE, MENU_FILE, FOOD_ORDERS_FILE]:
        try:
            with open(file, "r") as f:
                pass
        except FileNotFoundError:
            with open(file, "w") as f:
                pass

def get_valid_number(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)  # Convert input to integer
        print("Invalid input. Please enter a number.")

# Function to load room data from file
def load_rooms():
    rooms = []
    try:
        with open(ROOMS_FILE, "r") as file:
            for line in file:
                rooms.append(line.strip().split(","))
    except FileNotFoundError:
        print("Warning: 'rooms.txt' file not found. Initializing empty room list.")
    return rooms

# Function to save room data to file
def save_rooms(rooms):
    try:
        with open(ROOMS_FILE, "w") as file:
            for room in rooms:
                file.write(",".join(room) + "\n")
    except Exception as e:
        print("Error saving room data:", e)

# Function to add a new room
def add_room():
    room_number = get_valid_number("Enter room number: ")
    room_type = input("Enter room type (Single/Double/Suite): ").strip()
    price = get_valid_number("Enter room price: ")
    availability = "Available"
    rooms = load_rooms()
    rooms.append([str(room_number), room_type, str(price), availability])
    save_rooms(rooms)
    print("Room added successfully.")

# Function to remove a room
def remove_room():
    room_number = get_valid_number("Enter room number to remove: ")
    rooms = load_rooms()
    updated_rooms = [room for room in rooms if room[0] != str(room_number)]
    if len(rooms) == len(updated_rooms):
        print("Room not found.")
    else:
        save_rooms(updated_rooms)
        print("Room removed successfully.")

# Function to update room details
def update_room():
    room_number = get_valid_number("Enter room number to update: ")
    rooms = load_rooms()
    for room in rooms:
        if room[0] == str(room_number):
            print("Current details:", room)
            room[1] = input("Enter new room type: ").strip()
            room[2] = str(get_valid_number("Enter new price: "))
            room[3] = input("Enter availability status (Available/Booked): ").strip()
            save_rooms(rooms)
            print("Room updated successfully.")
            return
    print("Room not found.")

# Function to generate a report
def generate_report():
    rooms = load_rooms()
    total_rooms = len(rooms)
    available_rooms = sum(1 for room in rooms if room[3].lower() == "available")
    booked_rooms = total_rooms - available_rooms
    print(f"Total Rooms: {total_rooms}\nAvailable Rooms: {available_rooms}\nBooked Rooms: {booked_rooms}")

# Function to view all room data
def view_all_rooms():
    rooms = load_rooms()
    if rooms:
        print("Room Number | Type | Price | Availability")
        for room in rooms:
            print(" | ".join(room))
    else:
        print("No rooms available.")

# Admin menu
def admin_menu():
    initialize_system()
    while True:
        print("\n--- Administrator Menu ---")
        print("1. Add New Room")
        print("2. Remove Room")
        print("3. Update Room Information")
        print("4. Generate Reports")
        print("5. View All Rooms")
        print("6. Exit")
        
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_room()
        elif choice == "2":
            remove_room()
        elif choice == "3":
            update_room()
        elif choice == "4":
            generate_report()
        elif choice == "5":
            view_all_rooms()
        elif choice == "6":
            print("Exiting Administrator Menu.")
            break
        else:
            print("Invalid choice. Please try again.")



#hotel_receptionist
ROOMS_FILE = "rooms.txt"
BOOKINGS_FILE = "Booking.txt"

# have to make sure the rooms exist
for file in [ROOMS_FILE, BOOKINGS_FILE]:
    try:
        with open(file, "r") as f:
            pass
    except FileNotFoundError:
        with open(file, "w") as f:
            pass

def check_availability():
    """Displays available rooms."""
    try:
        with open(ROOMS_FILE, "r") as f:
            rooms = [line.strip().split(",") for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: Rooms file not found.")
        return

    available = [room for room in rooms if len(room) == 4 and room[3].strip().lower() == "available"]

    if available:
        print("\nAvailable Rooms:")
        for room in available:
            print(f"Room {room[0]} - {room[1]} - ${room[2]}")
    else:
        print("No available rooms.")

def book_room():
    """Handles room booking by storing guest details."""
    name = input("Guest Name: ")
    contact = input("Contact: ")

    while True:
        room_num = input("Room Number: ")
        if room_num.isdigit():
            break
        print("Invalid room number! Enter a numeric value.")

    while True:
        duration = input("Stay Duration (days): ")
        if duration.isdigit() and int(duration) > 0:
            break
        print("Invalid duration! Enter a positive number.")

    try:
        with open(ROOMS_FILE, "r") as f:
            rooms = [line.strip().split(",") for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: Rooms file not found.")
        return

    rooms = [room for room in rooms if len(room) == 4]

    try:
        with open(BOOKINGS_FILE, "r") as f:
            existing_bookings = [line.strip().split(",") for line in f]
    except FileNotFoundError:
        existing_bookings = []

    if any(len(b) >= 3 and b[2] == room_num for b in existing_bookings):
        print("Error: This room is already booked!")
        return

    for room in rooms:
        if room[0] == room_num and room[3].strip().lower() == "available":
            room[3] = "Occupied"
            with open(ROOMS_FILE, "w") as f:
                f.writelines(",".join(room) + "\n" for room in rooms)
            with open(BOOKINGS_FILE, "a") as f:
                f.write(f"{name},{contact},{room_num},{duration}\n")
            print("Room booked successfully!")
            return

    print("Room not available!")

def cancel_booking():
    """Cancels a booking and marks the room as available."""
    room_num = input("Enter Room Number to cancel booking: ")

    try:
        with open(BOOKINGS_FILE, "r") as f:
            bookings = [line.strip().split(",") for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: Bookings file not found.")
        return

    updated_bookings = [b for b in bookings if b[2] != room_num]

    with open(BOOKINGS_FILE, "w") as f:
        f.writelines(",".join(b) + "\n" for b in updated_bookings)

    try:
        with open(ROOMS_FILE, "r") as f:
            rooms = [line.strip().split(",") for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: Rooms file not found.")
        return

    for room in rooms:
        if room[0] == room_num:
            room[3] = "Available"

    with open(ROOMS_FILE, "w") as f:
        f.writelines(",".join(room) + "\n" for room in rooms)

    print("Booking canceled successfully!")

def view_bookings():
    """Displays all bookings."""
    try:
        with open(BOOKINGS_FILE, "r") as f:
            bookings = f.readlines()
    except FileNotFoundError:
        print("Error: Bookings file not found.")
        return

    if bookings:
        print("\nAll Bookings:")
        for booking in bookings:
            print(booking.strip())
    else:
        print("No bookings found.")

def receptionist_menu():
    """Displays the receptionist menu and handles choices."""
    while True:
        print("\nReceptionist Menu:")
        print("1. Check Room Availability")
        print("2. Book Room")
        print("3. Cancel Booking")
        print("4. View All Bookings")
        print("5. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            check_availability()
        elif choice == "2":
            book_room()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            view_bookings()
        elif choice == "5":
            print("Exiting receptionist menu...")
            break
        else:
            print("Invalid choice, try again.")

#guest
def exit_prog():
    print("Program exiting... Have a nice day!")

def booking_details():
    """Display guest booking details from Booking.txt"""
    try:
        with open("Booking.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("No booking details found.")

    navigate_menu()

def cancel_booking():
    """Allow guest to request a booking cancellation"""
    print("Are you sure you want to cancel the booking?")
    z = input("Enter 'Yes' for confirmation: ").strip().lower()
    
    if z == "yes":
        with open("Booking.txt", "a") as file:
            file.write("\nCANCEL_REQUEST,Pending")
        print("Your request to cancel is submitted.")

    navigate_menu()

def view_food_menu():
    """Display food menu from Menu.txt"""
    try:
        with open("Menu.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("Menu not available.")

    navigate_menu()

def order_food():
    """Allow guests to place food orders"""
    try:
        with open("Menu.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("Menu not available.")
        return

    food_items = {
        1: ("Crinkle Cut Fries", 20),
        2: ("Crispy Calamari", 40),
        3: ("Cheese Croquette", 25),
        4: ("Mojito", 12),
        5: ("Pina Colada", 15),
        6: ("Soft Drinks", 8),
        7: ("Fresh Juice", 14),
        8: ("Toffee Ice-Cream", 20),
        9: ("Flamed-Mango Crepe", 30),
        10: ("Strawberry Sundae", 22),
        11: ("Coconut Mousse", 25),
        12: ("Sweet and Sour Fish", 30),
        13: ("Garlic Chicken", 24),
        14: ("Sizzling Lamb", 45),
        15: ("Tofu Chop Suey", 25),
        16: ("Butter Chicken", 30),
        17: ("Palak Paneer", 25),
        18: ("Chicken Tandoori", 30),
        19: ("Beef Korma", 40),
        20: ("Chicken Tagliatelle", 35),
        21: ("White Sauce Cannelloni", 37),
        22: ("Bolognese Lasagna", 40),
        23: ("Creamy Mushroom Maroni", 32),
    }

    try:
        room_number = int(input("Please enter your room number: "))
        
        while True:
            try:
                ch = int(input("Select the food by number: "))
                if ch in food_items:
                    break
                else:
                    print("Invalid selection. Please enter a valid food number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        food_name, price = food_items[ch]

        while True:
            try:
                quantity = int(input(f"Enter quantity for {food_name}: "))
                if quantity > 0:
                    break
                else:
                    print("Quantity must be at least 1.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        bill = price * quantity

        print(f"Your order is: {food_name}, Quantity: {quantity}, Bill: RM{bill}")

        with open("order.txt", "a") as file:
            file.write(f"{room_number},{food_name},{quantity},{bill}\n")

    except ValueError:
        print("Invalid input. Please enter a number.")

    navigate_menu()

def view_food_orders():
    """Display all food orders"""
    print("Your current food orders are:")

    try:
        with open("orders.txt", "r") as file:
            orders = file.readlines()
            if not orders:
                print("No food orders found.")
            else:
                for order in orders:
                    data = order.strip().split(",")
                    if len(data) == 4:
                        print(f"Room {data[0]}: {data[1]} x{data[2]}, Total: RM{data[3]}")
                    else:
                        print(order.strip())
    except FileNotFoundError:
        print("No food orders found.")

    navigate_menu()

def navigate_menu():
    """Ask user if they want to return to the main menu or exit"""
    while True:
        try:
            main_menu = int(input("Enter 1 for main menu or 2 for exit: "))
            if main_menu == 1:
                guest_menu()
                break
            elif main_menu == 2:
                exit_prog()
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def guest_menu():
    """Main guest menu"""
    while True:
        print("\nGuest Menu:")
        print("1. View Booking Details")
        print("2. Cancel Booking")
        print("3. View Food Menu")
        print("4. Order Food")
        print("5. View Food Orders")
        print("6. Exit")

        try:
            choice = int(input("Please enter your choice: "))

            if choice == 1:
                booking_details()
            elif choice == 2:
                cancel_booking()
            elif choice == 3:
                view_food_menu()
            elif choice == 4:
                order_food()
            elif choice == 5:
                view_food_orders()
            elif choice == 6:
                exit_prog()
                break
            else:
                print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a number.")

#restaurant manager
def add_new_menu_item():
    try:
        item_name = input("Enter the name of the menu item: ")
        item_price = input("Enter the price of the menu item: ")
        item_category = input("Enter the category of the menu item: ")
        
        with open('menu.txt', 'a') as menu_file:
            menu_file.write(f"{item_name},{item_price},{item_category}\n")
        
        print("Menu item added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_menu_item():
    item_name = input("Enter the name of the menu item to update: ")
    updated = False
    menu_items = []

    with open("menu.txt", "r") as menu_file:
        menu_items = menu_file.readlines()

    for i, item in enumerate(menu_items):
        if item.startswith(item_name):
            new_price = input("Enter the new price: ")
            new_category = input("Enter the new category: ")
            menu_items[i] = f"{item_name},{new_price},{new_category}\n"
            updated = True
            break

    if updated:
        with open("menu.txt", "w") as menu_file:
            menu_file.writelines(menu_items)
        print("Menu item updated successfully.")
    else:
        print("Item not found.")

def view_menu():
    print("Current Menu:")
    try:
        with open("menu.txt", "r") as menu_file:
            for line in menu_file:
                print(line.strip())
    except FileNotFoundError:
        print("Menu file not found. Please add menu items first.")

def record_food_order():
    room_number = input("Enter the room number: ")
    order_items = input("Enter the items ordered (format: item_name:item_price, separated by commas): ")
    
    with open("orders.txt", "a") as orders_file:
        orders_file.write(f"{room_number},{order_items}\n")
    
    print("Order recorded successfully.")

def generate_sales_report():
    total_sales = 0
    item_count = {}
    
    try:
        with open("orders.txt", "r") as orders_file:
            for line in orders_file:
                # Split the line into room number and items
                room_number, items = line.strip().split(",", 1)
                for item in items.split(","):
                    try:
                        # Split each item into name and price
                        item_name, item_price = item.split(":")
                        total_sales += float(item_price)
                        item_count[item_name] = item_count.get(item_name, 0) + 1
                    except ValueError:
                        print(f"Error processing item: {item}. Please check the format.")
                        continue  # Skip this item and continue with the next

        print(f"Total Sales: RM{total_sales:.2f}")
        print("Most Popular Dishes:")
        for item, count in item_count.items():
            print(f"{item}: {count} orders")
    except FileNotFoundError:
        print("Orders file not found. Please record some orders first.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def restaurant_manager_menu():
    while True:
        print("\n--- Restaurant Manager Menu ---")
        print("1. Add New Menu Item")
        print("2. Update Menu Item")
        print("3. View Menu")
        print("4. Record Food Order")
        print("5. Generate Sales Report")
        print("6. Exit")

        choice = input("Select an option (1-6): ")

        if choice == '1':
            add_new_menu_item()
        elif choice == '2':
            update_menu_item()
        elif choice == '3':
            view_menu()
        elif choice == '4':
            record_food_order()
        elif choice == '5':
            generate_sales_report()
        elif choice == '6':
            print("Exiting the Restaurant Manager Menu.")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            
def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Administrator")
        print("2. Receptionist")
        print("3. Guest")
        print("4. Restaurant Manager")
        print("5. Exit")
        choice = input("Select your role: ").strip()
        if choice == "1":
            admin_menu()
        elif choice == "2":
            receptionist_menu()
        elif choice == "3":
            guest_menu() 
        elif choice == "4":
            restaurant_manager_menu()
        elif choice == "5":
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main_menu()
