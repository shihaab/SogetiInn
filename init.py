import sqlite3

connection = sqlite3.connect("SogetiInn.db")
connection.isolation_level = None
cursor = connection.cursor()
    

# rooms
cursor.execute("CREATE TABLE rooms (id INTEGER, number_on_floor INTEGER, floor INTEGER, occupied INTEGER, last_cleaned TEXT, last_cleaned_employee_id INTEGER, amenities TEXT, PRIMARY KEY('id' AUTOINCREMENT))")

# cleaning employees
cursor.execute("CREATE TABLE cleaning_employees (id INTEGER, employee_number INTEGER, first_name TEXT, last_name TEXT, dob TEXT, phone_number TEXT, PRIMARY KEY('id' AUTOINCREMENT))")


# bookings
cursor.execute("CREATE TABLE bookings (id INTEGER, room_id INTEGER, client_id INTEGER, coupon_used TEXT, start_date_time TEXT, end_date_time TEXT, PRIMARY KEY('id' AUTOINCREMENT))")


# clients
cursor.execute("CREATE TABLE clients (id INTEGER, first_name TEXT, last_name TEXT, dob TEXT, phone_number TEXT, iban TEXT, PRIMARY KEY('id' AUTOINCREMENT))")

# complaints
cursor.execute("CREATE TABLE complaints (id INTEGER, booking_id INTEGER, description TEXT, PRIMARY KEY('id' AUTOINCREMENT))")

# tabs
cursor.execute("CREATE TABLE tabs (id INTEGER, booking_id TEXT, status TEXT, PRIMARY KEY('id' AUTOINCREMENT))")

# receipts
cursor.execute("CREATE TABLE receipts (id INTEGER, tab_id INTEGER, amount TEXT, currency TEXT, PRIMARY KEY('id' AUTOINCREMENT))")

