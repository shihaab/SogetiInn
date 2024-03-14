import decimal
from flask import Flask, render_template, request
from faker import Faker
import sqlite3, random, string
fake = Faker()

app = Flask(__name__)

def remove_comma(input_string):
    # Find the index of the last comma and remove it
    last_comma_index = input_string.rfind(',')
    result= input_string[:last_comma_index] + input_string[last_comma_index + 1:]
    return result.replace('[', '').replace(']', '')
def clear_database():
    connection = sqlite3.connect("SogetiInn.db")
    connection.isolation_level = None
    cursor = connection.cursor()
    # drop all tables
    tables = ['rooms', 'cleaning_employees', 'bookings', 'clients', 'complaints', 'tabs', 'receipts']
    for table in tables:
        # cursor.execute("DROP TABLE IF EXISTS "+table)
        cursor.execute("DELETE FROM "+table)
    cursor.close()

def random_coupon():
    if random.randint(0,9) > 7:
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(9))
    else:
        return 'NULL'
def random_complaint():
    complaints = ["The room had a persistent musty odor that made the stay uncomfortable. Despite informing the staff, no action was taken to address the issue.",    "Upon arrival, noticed the bed sheets were stained and appeared unwashed. Requested replacement sheets, but the process was slow and inconvenient.",    "Sleep quality was severely affected by noisy neighbors, causing disturbance late into the night. The thin walls failed to provide adequate sound insulation.",    "The Wi-Fi connection was consistently slow and unreliable, making it difficult to work or stream content. Multiple complaints yielded no improvement.", "Front desk staff were unresponsive and unhelpful, failing to address concerns promptly. Customer service was lacking throughout the stay.",    "The air conditioning system in the room was broken, making the environment uncomfortably warm. Despite reporting the issue, no repairs were made.",    "Room cleaning service was inadequate, with noticeable dust and dirt in various areas. The overall cleanliness did not meet basic standards.",    "The mattress and pillows were uncomfortable, affecting sleep quality. Requested replacements, but the hotel did not provide a satisfactory solution.",    "Limited and overpriced food options in the hotel restaurant left guests unsatisfied. The menu lacked variety, and prices were disproportionately high.",    "Key cards for the room were faulty, leading to repeated issues accessing the accommodation. The inconvenience persisted despite multiple requests for assistance.",    "The shower lacked hot water, making it impossible to enjoy a comfortable bathing experience. The issue remained unresolved despite repeated complaints.",    "Persistent plumbing issues in the bathroom, including slow drainage and leaks, were reported but not addressed. This negatively impacted the overall experience.",    "Furniture in the room was outdated and worn-out, giving the accommodation an overall shabby appearance. The lack of maintenance was evident.",    "Garbage in common areas went unattended, creating an unpleasant environment. The lack of cleanliness affected the overall impression of the hotel.",    "Insufficient lighting in the room made it difficult to read or work comfortably. Despite requests for additional lighting, the issue was not resolved.",    "Check-in process was delayed, causing inconvenience for tired travelers. The staff seemed unprepared, and the overall efficiency was lacking.",    "Customer service was unhelpful and lacked genuine concern for guests' needs. Requests for information and assistance were met with indifference.",    "The swimming pool area exhibited unhygienic conditions, with dirty water and neglected maintenance. This posed health concerns for guests.",    "Toiletries provided were either missing or insufficient, leading to a lack of basic amenities. The hotel failed to meet the expected standards in this regard.",   "Guests were overcharged on the bill, with discrepancies in pricing for services and amenities. The lack of transparency in billing was concerning.",    "Limited parking spaces resulted in inconvenience for guests with vehicles. The hotel did not provide adequate alternatives or solutions.",    "Unannounced construction noise disrupted the peaceful atmosphere, causing discomfort for guests. The lack of prior notification was frustrating.",    "Room service was unsatisfactory, with delayed deliveries and missing items. Guests experienced frustration due to the lack of reliability.",   "Staff provided inaccurate information, leading to confusion and inconvenience for guests. The hotel's communication and knowledge were lacking.",    "Breakfast service was unorganized and chaotic, with long wait times and limited options. The overall dining experience fell short of expectations.",    "Minibar charges included unpleasant surprises, with discrepancies in pricing and unexpected items added to the bill. Guests felt deceived by hidden costs.",    "The TV and entertainment system in the room were faulty, detracting from the overall experience. Despite reporting the issue, no resolution was provided.",    "Room locks were unsecured or malfunctioning, posing a security risk for guests. The lack of attention to this crucial aspect raised concerns about safety.",    "Despite multiple complaints, issues remained unresolved, demonstrating a lack of commitment to guest satisfaction. The hotel management seemed unresponsive.",    "Maintenance requests went unattended, with issues in the room persisting despite reporting them. The lack of timely resolution was frustrating for guests.",    "Room insulation was inadequate, leading to noise disturbances from neighboring rooms. The lack of soundproofing affected the overall quality of the stay.",    "Public restrooms exhibited unsanitary conditions, raising hygiene concerns for guests. The lack of cleanliness in shared spaces was disappointing.",    "Unexplained power outages occurred during the stay, causing inconvenience for guests. The lack of communication and swift resolution was frustrating.",    "The hotel lacked proper COVID-19 safety measures, causing anxiety for guests concerned about health and well-being. The overall safety protocols were insufficient.",    "The heating in the room was inefficient, making the space uncomfortably cold. Despite requests for adjustments, the issue persisted.",    "The wake-up call service was unreliable, leading to missed appointments and schedules. The lack of dependability in this service was a significant inconvenience.",   "Corridors had unpleasant smells, likely due to poor ventilation or inadequate cleaning. The overall atmosphere was negatively impacted.",    "Staff displayed inattentiveness and rudeness, detracting from the overall guest experience. The lack of hospitality and courtesy was disappointing.",    "Elevators were outdated and malfunctioned frequently, causing inconvenience for guests. The lack of proper maintenance was evident.",    "Common areas had uncomfortable seating, with worn-out and poorly designed furniture. The lack of comfort affected the overall guest experience.",    "Accessibility for differently-abled guests was limited, with challenges in navigating the premises. The hotel lacked proper accommodations for all guests.",    "Housekeeping service was unresponsive and failed to address guest needs. The lack of attention to cleanliness and guest comfort was apparent.",    "Gym and fitness facilities were inadequate, with outdated equipment and limited options. The hotel did not cater to the wellness needs of guests.",    "Maintenance issues in outdoor areas went unattended, detracting from the overall appearance and appeal of the hotel premises.",    "The shuttle service was unreliable, causing delays and inconvenience for guests relying on transportation provided by the hotel.",    "Noise complaints went unattended, with disruptive sounds persisting throughout the stay. The lack of consideration for guest comfort was disappointing.",    "Room insulation was lacking, leading to uncomfortable temperatures and sounds from the surroundings. The overall sleep quality was affected.",    "Guests were greeted with an unpleasant view from the room, detracting from the overall experience. The lack of attention to aesthetics was disappointing."]
    return random.choice(complaints)
def random_status():
    statuses = ['paid', 'pending', 'incomplete']
    return random.choice(statuses)
def random_number(min,max):
    return str(random.randint(min,max))
def populate():
    Faker.seed(0)
    connection = sqlite3.connect("SogetiInn.db")
    connection.isolation_level = None
    cursor = connection.cursor()
    # rooms
    number_on_floor = 0
    floor = 0
    for iteration in range(20):
        if number_on_floor > 5:
            number_on_floor = 0
            floor += 1
        cursor.execute("INSERT INTO rooms VALUES ('"+str(iteration)+"', '"+str(number_on_floor)+"', '"+str(floor)+"', '"+random_number(0,1)+"', '"+str(fake.date_this_month())+"', '"+random_number(0,9)+"', '1,2,3')")
        number_on_floor += 1

    # cleaning_employees
    for iteration in range(10):
        cursor.execute("INSERT INTO cleaning_employees VALUES ('"+str(iteration)+"', '"+random_number(1000,9999)+"', '"+fake.first_name()+"', '"+fake.last_name()+"', '"+str(fake.date_of_birth())+"', '"+fake.phone_number()+"')")

    # bookings
    for iteration in range(10):
        cursor.execute("INSERT INTO bookings VALUES ('"+str(iteration)+"', '"+random_number(0,19)+"', '"+random_number(0,29)+"', '"+random_coupon()+"', '"+str(fake.date_this_month())+"', '"+str(fake.date_this_year())+"')")

    # clients
    for iteration in range(30):
        cursor.execute("INSERT INTO clients VALUES ('"+str(iteration)+"', '"+fake.first_name()+"', '"+fake.last_name()+"', '"+str(fake.date_of_birth())+"', '"+fake.phone_number()+"', '"+fake.iban()+"')")
    
    # complaints
    for iteration in range(30):
        cursor.execute("INSERT INTO complaints VALUES  (?, ?, ?)", (str(iteration), random_number(0,9), random_complaint()))
    
    # tabs
    for iteration in range(10):
        cursor.execute("INSERT INTO tabs VALUES ('"+str(iteration)+"', '"+random_number(0,9)+"', '"+random_status()+"')")

    # receipts
    for iteration in range(30):
        cursor.execute("INSERT INTO receipts VALUES ('"+str(iteration)+"', '"+random_number(0,9)+"', '"+str(decimal.Decimal(random.randrange(155, 389))/100)+"', 'EUR')")
    cursor.close()

# API calls
@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/bookings")
def bookings():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get query parameters
    room_id = request.args.get('room_id')
    client_id = request.args.get('client_id')
    coupon_used = request.args.get('coupon_used')
    start_date_time = request.args.get('start_date_time')
    end_date_time = request.args.get('end_date_time')

    # Build the base query
    base_query = "SELECT id, room_id, client_id, coupon_used, start_date_time, end_date_time FROM bookings WHERE 1"

    # Add filters based on provided parameters
    if room_id:
        base_query += f" AND room_id = {room_id}"
    if client_id:
        base_query += f" AND client_id = {client_id}"
    if coupon_used:
        base_query += f" AND coupon_used = {coupon_used}"
    if start_date_time:
        base_query += f" AND start_date_time = {start_date_time}"
    if end_date_time:
        base_query += f" AND end_date_time = {end_date_time}"
    
    # Execute the final query
    data = cursor.execute(base_query).fetchall()
    cursor.close()
    jsonArr = []
    for iteration in data:
        jsonArr.append([{'id':iteration[0]}, {'room_id':iteration[1]}, {'client_id':iteration[2]}, {'coupon_used':iteration[3]}, {'start_date_time':iteration[4]}, {'end_date_time':iteration[5]}])
    return jsonArr

@app.route("/cleaning_employees")
def cleaning_employees():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get query parameters
    employee_number = request.args.get('employee_number')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    dob = request.args.get('dob')
    phone_number = request.args.get('phone_number')

    # Build the base query
    base_query = "SELECT id, employee_number, first_name, last_name, dob, phone_number FROM cleaning_employees WHERE 1"

    # Add filters based on provided parameters
    if employee_number:
        base_query += f" AND employee_number = {employee_number}"
    if first_name:
        base_query += f" AND first_name = {first_name}"
    if last_name:
        base_query += f" AND last_name = {last_name}"
    if dob:
        base_query += f" AND dob = {dob}"
    if phone_number:
        base_query += f" AND phone_number = {phone_number}"
    

    # Execute the final query
    data = cursor.execute(base_query).fetchall()
    cursor.close()
    jsonArr = []
    for iteration in data:
        jsonArr.append([{'id':iteration[0]}, {'employee_number':iteration[1]}, {'first_name':iteration[2]}, {'last_name':iteration[3]}, {'dob':iteration[4]}, {'phone_number':iteration[5]}])
    return jsonArr

@app.route("/clients")
def clients():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get query parameters
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    dob = request.args.get('dob')
    phone_number = request.args.get('phone_number')
    iban = request.args.get('iban')

    # Build the base query
    base_query = "SELECT id, first_name, last_name, dob, phone_number, iban FROM clients WHERE 1"

    # Add filters based on provided parameters
    if first_name:
        base_query += f" AND first_name = {first_name}"
    if last_name:
        base_query += f" AND last_name = {last_name}"
    if dob:
        base_query += f" AND dob = {dob}"
    if phone_number:
        base_query += f" AND phone_number = {phone_number}"
    if iban:
        base_query += f" AND iban = {iban}"

    # Execute the final query
    data = cursor.execute(base_query).fetchall()
    cursor.close()
    jsonArr = []
    for iteration in data:
        jsonArr.append([{'id':iteration[0]}, {'first_name':iteration[1]}, {'last_name':iteration[2]}, {'dob':iteration[3]}, {'phone_number':iteration[4]}, {'iban':iteration[5]}])
    return jsonArr

@app.route("/complaints")
def complaints():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get query parameters
    booking_id = request.args.get('booking_id')
    description = request.args.get('description')

    # Build the base query
    base_query = "SELECT id, tab_id, booking_id, description FROM complaints WHERE 1"

    # Add filters based on provided parameters
    if booking_id:
        base_query += f" AND booking_id = {booking_id}"
    if description:
        base_query += f" AND description = {description}"

    # Execute the final query
    data = cursor.execute(base_query).fetchall()
    cursor.close()
    jsonArr = []
    for iteration in data:
        jsonArr.append([{'id':iteration[0]}, {'booking_id':iteration[1]}, {'description':iteration[2]}])
    return jsonArr

@app.route("/receipts")
def receipts():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get query parameters
    tab_id = request.args.get('tabs_id')
    amount = request.args.get('amount')
    currency = request.args.get('currency')

    # Build the base query
    base_query = "SELECT id, tab_id, amount, currency FROM receipts WHERE 1"

    # Add filters based on provided parameters
    if tab_id:
        base_query += f" AND tabs_id = {tab_id}"
    if amount:
        base_query += f" AND amount = {amount}"
    if currency:
        base_query += f" AND currency = {currency}"

    # Execute the final query
    data = cursor.execute(base_query).fetchall()
    cursor.close()
    jsonArr = []
    for iteration in data:
        jsonArr.append([{'id':iteration[0]}, {'tab_id':iteration[1]}, {'amount':iteration[2]}, {'currency':iteration[3]}])
    return jsonArr

@app.route("/rooms")
def rooms():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get query parameters
    number_on_floor = request.args.get('number_on_floor')
    floor = request.args.get('floor')
    occupied = request.args.get('occupied')
    last_cleaned = request.args.get('last_cleaned')
    last_cleaned_employee_id = request.args.get('last_cleaned_employee_id')
    amenities = request.args.get('amenities')

    # Build the base query
    base_query = "SELECT id, number_on_floor, floor, occupied, last_cleaned, last_cleaned_employee_id, amenities FROM rooms WHERE 1"

    # Add filters based on provided parameters
    if number_on_floor:
        base_query += f" AND number_on_floor = {number_on_floor}"
    if floor:
        base_query += f" AND floor = {floor}"
    if occupied:
        base_query += f" AND occupied = {occupied}"
    if last_cleaned:
        base_query += f" AND last_cleaned = {last_cleaned}"
    if last_cleaned_employee_id:
        base_query += f" AND last_cleaned_employee_id = {last_cleaned_employee_id}"
    if amenities:
        base_query += f" AND amenities LIKE '%{amenities}%'"

    # Execute the final query
    data = cursor.execute(base_query).fetchall()
    cursor.close()
    jsonArr = []
    for iteration in data:
        jsonArr.append([{'id':iteration[0]}, {'number_on_floor':iteration[1]}, {'floor':iteration[2]}, {'occupied':iteration[3]}, {'last_cleaned':iteration[4]}, {'last_cleaned_employee_id':iteration[5]}, {'amenities':iteration[6]}])
    return jsonArr

@app.route("/tabs")
def tabs():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get query parameters
    booking_id = request.args.get('booking_id')
    status = request.args.get('status')

    # Build the base query
    base_query = "SELECT id, booking_id, status FROM tabs WHERE 1"

    # Add filters based on provided parameters
    if booking_id:
        base_query += f" AND booking_id = {booking_id}"
    if status:
        base_query += f" AND status = {status}"

    # Execute the final query
    data = cursor.execute(base_query).fetchall()
    cursor.close()
    jsonArr = []
    for iteration in data:
        jsonArr.append([{'id':iteration[0]}, {'booking_id':iteration[1]}, {'status':iteration[2]}])
    return jsonArr

@app.route('/open-tabs') 
def open_tabs(): 
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    booking_id = request.args.get('booking_id')
        
    # Validate required parameters
    if not booking_id:
        return "Missing required parameters. Expected booking_id."

    data = cursor.execute("SELECT id, booking_id, status FROM tabs WHERE status != 'paid' AND booking_id = "+booking_id).fetchall()
    cursor.close()
    jsonArr = []
    for iteration in data:
        jsonArr.append([{'id':iteration[0]}, {'booking_id':iteration[1]}, {'status':iteration[2]}])
    return jsonArr
        
# check availibity of rooms based on the booking info. a date should be given en then rooms that are not booked on that date should show
@app.route('/available-rooms-on-date', methods=['GET', 'POST']) 
def available_rooms(): 
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()
    if request.method == 'GET': 
        date = request.args['date']
        available_rooms_ids = cursor.execute("SELECT room_id FROM bookings WHERE '"+date+"' NOT BETWEEN start_date_time AND end_date_time").fetchall()
        cursor.close()
        jsonArr = []
        for iteration in available_rooms_ids:
            jsonArr.append([{'room_id':iteration[0]}])
        return jsonArr
    else:
        cursor.close()
        return "no parameters given. Expected date in YYYY-MM-DD"


# reset db
@app.route("/reset-db")
def reset_sb():
    clear_database()
    populate()
    return "Database reset and populated!"

# checkout service
# shows the total amount of the booking
@app.route("/checkout-service", methods=['GET', 'POST']) 
def checkout_service():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    if request.method == 'GET':
        booking = request.args['booking_id']

        open_tabs = cursor.execute("SELECT id FROM tabs WHERE status != 'paid' AND booking_id = ?", (booking,)).fetchall()

        if not open_tabs:
            # No open tabs, no need to check the amount
            cursor.close()
            return "No open tabs"
        else:
            # Building dynamic SQL query with placeholders
            placeholders = ",".join(["?" for _ in open_tabs])
            query = "SELECT id, tab_id, amount, currency FROM receipts WHERE tab_id IN ({})".format(placeholders)

            # Fetching the amount using placeholders and parameters
            amount = cursor.execute(query, [tab[0] for tab in open_tabs]).fetchall()
            cursor.close()
            jsonArr = []
            for iteration in amount:
                jsonArr.append([{'id':iteration[0]}, {'tab_id':iteration[1]}, {'amount':iteration[2]}, {'currency':iteration[3]}])
            return jsonArr
    else:
        return "No parameters given. Expected booking_id"
    
# Creating data
@app.route('/create-booking')
def create_booking():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get parameters from the request
    room_id = request.args.get('room_id')
    client_id = request.args.get('client_id')
    start_date_time = request.args.get('start_date_time')
    end_date_time = request.args.get('end_date_time')
    coupon_used = request.args.get('coupon_used')

    # Validate required parameters
    if not room_id or not client_id or not start_date_time or not end_date_time:
        cursor.close()
        return "Missing required parameters. Expected room_id, client_id, start_date_time, end_date_time."

    # Build the query to insert a new booking
    query = "INSERT INTO bookings (room_id, client_id, start_date_time, end_date_time, coupon_used) VALUES (?, ?, ?, ?, ?)"

    # Execute the query with the provided parameters
    cursor.execute(query, (room_id, client_id, start_date_time, end_date_time, coupon_used))

    # Commit changes to the database
    connection.commit()
    cursor.close()

    return "Booking created successfully!"
@app.route('/create-client')
def create_client():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get parameters from the request
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    dob = request.args.get('dob')
    phone_number = request.args.get('phone_number')
    iban = request.args.get('iban')

    # Validate required parameters
    if not first_name or not last_name or not dob or not phone_number or not iban:
        cursor.close()
        return "Missing required parameters. Expected first_name, last_name, dob, phone_number, iban."

    # Build the query to insert a new client
    query = "INSERT INTO clients (first_name, last_name, dob, phone_number, iban) VALUES (?, ?, ?, ?, ?)"

    # Execute the query with the provided parameters
    cursor.execute(query, (first_name, last_name, dob, phone_number, iban))

    # Commit changes to the database
    connection.commit()
    cursor.close()

    return "Client created successfully!"
@app.route('/create-tab')
def create_tab():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get parameters from the request
    booking_id = request.args.get('booking_id')
    status = request.args.get('status')

    # Validate required parameters
    if not booking_id or not status:
        cursor.close()
        return "Missing required parameters. Expected booking_id, status."

    # Build the query to insert a new tab
    query = "INSERT INTO tabs (booking_id, status) VALUES (?, ?)"

    # Execute the query with the provided parameters
    cursor.execute(query, (booking_id, status))

    # Commit changes to the database
    connection.commit()
    cursor.close()

    return "Tab created successfully!"
@app.route('/create-receipt')
def create_receipt():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get parameters from the request
    tab_id = request.args.get('tab_id')
    amount = request.args.get('amount')
    currency = request.args.get('currency')

    # Validate required parameters
    if not tab_id or not amount or not currency:
        cursor.close()
        return "Missing required parameters. Expected tab_id, amount, currency."

    # Build the query to insert a new receipt
    query = "INSERT INTO receipts (tab_id, amount, currency) VALUES (?, ?, ?)"

    # Execute the query with the provided parameters
    cursor.execute(query, (tab_id, amount, currency))

    # Commit changes to the database
    connection.commit()
    cursor.close()

    return "Receipt created successfully!"
@app.route('/remove-receipt')
def remove_receipt():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get parameter from the request
    id = request.args.get('id')

    # Validate required parameter
    if not id:
        cursor.close()
        return "Missing required parameter. Expected id."

    # Build the query to remove the receipt
    query = "DELETE FROM receipts WHERE id = ?"

    # Execute the query with the provided parameter
    cursor.execute(query, (id,))

    # Commit changes to the database
    connection.commit()
    cursor.close()

    return "Receipt removed successfully!"
@app.route('/remove-client')
def remove_client():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get parameter from the request
    id = request.args.get('id')

    # Validate required parameter
    if not id:
        cursor.close()
        return "Missing required parameter. Expected id."

    # Build the query to remove the receipt
    query = "DELETE FROM clients WHERE id = ?"

    # Execute the query with the provided parameter
    cursor.execute(query, (id,))

    # Commit changes to the database
    connection.commit()
    cursor.close()

    return "Client removed successfully!"
@app.route('/remove-room')
def remove_rooms():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get parameter from the request
    id = request.args.get('id')

    # Validate required parameter
    if not id:
        cursor.close()
        return "Missing required parameter. Expected id."

    # Build the query to remove the receipt
    query = "DELETE FROM rooms WHERE id = ?"

    # Execute the query with the provided parameter
    cursor.execute(query, (id,))

    # Commit changes to the database
    connection.commit()
    cursor.close()

    return "Room removed successfully!"

@app.route('/update-receipt')
def update_receipt():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get parameters from the request
    id = request.args.get('id')
    amount = request.args.get('new_amount')
    currency = request.args.get('new_currency')

    # Validate required parameters
    if not id or (not amount and not currency):
        cursor.close()
        return "Missing required parameters. Expected id and at least one of new_amount or new_currency."

    # Build the query to update the receipt
    query = "UPDATE receipts SET"

    # Include new_amount if provided
    if amount:
        query += " amount = ?,"
    # Include new_currency if provided
    if currency:
        query += " currency = ?,"
    
    # Remove the trailing comma
    query = query.rstrip(',')

    # Append the WHERE clause
    query += " WHERE id = ?"

    # Gather values for the query execution
    values = []
    if amount:
        values.append(amount)
    if currency:
        values.append(currency)
    values.append(id)

    # Execute the query with the provided parameters
    cursor.execute(query, tuple(values))

    # Commit changes to the database
    connection.commit()
    cursor.close()

    return "Receipt updated successfully!"

@app.route('/update-room')
def update_room():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get parameters from the request
    id = request.args.get('id')
    number_on_floor = request.args.get('number_on_floor')
    floor = request.args.get('floor')
    occupied = request.args.get('occupied')
    last_cleaned = request.args.get('last_cleaned')
    last_cleaned_employee_id = request.args.get('last_cleaned_employee_id')
    amenities = request.args.get('amenities')

    # Validate required parameters
    if not id or (not number_on_floor and not floor and not occupied and not last_cleaned and not last_cleaned_employee_id and not amenities):
        cursor.close()
        return "Missing required parameters. Expected id and at least one of number_on_floor or floor or occupied or last_cleaned or last_cleaned_employee_id or amenities."

    # Build the query to update the receipt
    query = "UPDATE rooms SET"

    # Include parameters if provided
    if number_on_floor:
        query += " number_on_floor = ?,"
    if floor:
        query += " floor = ?,"
    if occupied:
        query += " occupied = ?,"
    if last_cleaned:
        query += " last_cleaned = ?,"
    if last_cleaned_employee_id:
        query += " last_cleaned_employee_id = ?,"
    if amenities:
        query += " amenities = ?,"
    
    # Remove the trailing comma
    query = query.rstrip(',')

    # Append the WHERE clause
    query += " WHERE id = ?"

    # Gather values for the query execution
    values = []
    if number_on_floor:
        values.append(number_on_floor)
    if floor:
        values.append(floor)
    if occupied:
        values.append(occupied)
    if last_cleaned:
        values.append(last_cleaned)
    if last_cleaned_employee_id:
        values.append(last_cleaned_employee_id)
    if amenities:
        values.append(amenities)
    values.append(id)

    # Execute the query with the provided parameters
    cursor.execute(query, tuple(values))

    # Commit changes to the database
    connection.commit()
    cursor.close()

    return "Room updated successfully!"
@app.route('/update-booking')
def update_booking():
    connection = sqlite3.connect("SogetiInn.db")
    cursor = connection.cursor()

    # Get parameters from the request
    id = request.args.get('id')
    client_id = request.args.get('client_id')
    coupon_used = request.args.get('coupon_used')
    start_date_time = request.args.get('start_date_time')
    end_date_time = request.args.get('end_date_time')

    # Validate required parameters
    if not id or (not client_id and not coupon_used and not start_date_time and not end_date_time):
        cursor.close()
        return "Missing required parameters. Expected id and at least one of client_id coupon_used start_date_time end_date_time."

    # Build the query to update the receipt
    query = "UPDATE bookings SET"

    # Include parameters if provided
    if client_id:
        query += " client_id = ?,"
    if coupon_used:
        query += " coupon_used = ?,"
    if start_date_time:
        query += " start_date_time = ?,"
    if end_date_time:
        query += " end_date_time = ?,"
    
    # Remove the trailing comma
    query = query.rstrip(',')

    # Append the WHERE clause
    query += " WHERE id = ?"

    # Gather values for the query execution
    values = []
    if client_id:
        values.append(client_id)
    if coupon_used:
        values.append(coupon_used)
    if start_date_time:
        values.append(start_date_time)
    if end_date_time:
        values.append(end_date_time)
    values.append(id)

    # Execute the query with the provided parameters
    cursor.execute(query, tuple(values))

    # Commit changes to the database
    connection.commit()
    cursor.close()

    return "Booking updated successfully!"