
from collections import UserString
from tokenize import generate_tokens
from flask import Flask, jsonify, request
from itsdangerous import URLSafeTimedSerializer
from pymongo import MongoClient

# Συνδεση στην βαση MongoDB
client = MongoClient('db', 27017)


db = client['DigitalAirlines']
users_collection = db['users']
flights_collection = db['flights']
reservations_collection = db['reservations']

# Προσβαση στην βαση DigitalAirlines 
db = client["DigitalAirlines"]


users_collection = db["users"]
flights_collection = db["flights"]
reservations_collection = db["reservations"]

# Αποθήκευση πληροφοριών χρήστη
user_data = {
   
}
users_collection.insert_one(user_data)

# Αποθήκευση πληροφοριών πτήσης 
flight_data = {
    
}
flights_collection.insert_one(flight_data)

# Αποθήκευση πληροφοριών κράτησης 
reservation_data = {
   
}
reservations_collection.insert_one(reservation_data)

app = Flask(__name__)

users = []
logged_in_users = []
flights = []
bookings = []
admins = []
logged_in_admins = {}
reservations = [] 


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json() 
    username = data['username']
    email = data['email']
    login_code = data['login_code']
    date_of_birth = data['date_of_birth']
    country_of_origin = data['country_of_origin']
    passport_number = data['passport_number']
    
    # Έλεγχος για το αν το email υπάρχει 
    existing_email = next((user for user in users if user['email'] == email), None)
    if existing_email:
        return jsonify({'error': 'Email already exists'})
    
    # Έλεγχος για το αν υπάρχει το username
    existing_username = next((user for user in users if user['username'] == username), None)
    if existing_username:
        return jsonify({'error': 'Username already exists'})
    
    # Δημιουργία αντικειμένου  user 
    user = {
        'username': username,
        'email': email,
        'login_code': login_code,
        'date_of_birth': date_of_birth,
        'country_of_origin': country_of_origin,
        'passport_number': passport_number,
        'user_type': 'Simple User'  
    }
    
    users.append(user)  # Πρόσθεση του χρήστη σε λίστα
    
    return jsonify({'message': 'User registered successfully'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    # έλεγχος για το αν τα στοιχεία του χρήστη είναι σωστά
    user = next((user for user in users if user['email'] == email), None)
    if user and user.get('password') == password:
        # Πρόσθεση στους logged in χρήστες 
        logged_in_users.append(user)
        return jsonify({'message': 'Login successful'})
    
    return jsonify({'error': 'Invalid email or password'})



# protected endpoint
@app.route('/protected', methods=['GET'])
def protected():
    
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(' ')[1] 
        user = next((user for user in logged_in_users if user.get('token') == auth_token), None)
        if user:
            return jsonify({'message': 'Protected endpoint accessed by logged-in user'})
    
    return jsonify({'error': 'Unauthorized access'})


@app.route('/flights', methods=['GET'])
def search_flights():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date = request.args.get('date')
    
    if origin and destination and date:
        # Αναζήτηση πτήσης από προορισμό 
        result = [flight for flight in flights if flight['origin'] == origin and flight['destination'] == destination and flight['date'] == date]
    elif origin and destination:
        
        result = [flight for flight in flights if flight['origin'] == origin and flight['destination'] == destination]
    elif date:
        # Αναζήτηση πτήσης με ημερομηνία 
        result = [flight for flight in flights if flight['date'] == date]
    else:
        # Εμφάνιση όλων των διαθέσιμων πτήσεων
        result = flights
    
    return jsonify(result)



@app.route('/flights/<flight_id>', methods=['GET'])
def get_flight_details(flight_id):
    # Έλεγχος για το αν ο χρήστης είναι logged in 
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(' ')[1]  
        user = next((user for user in logged_in_users if user.get('token') == auth_token), None)
        if not user:
            return jsonify({'error': 'Unauthorized access'})
    else:
        return jsonify({'error': 'Unauthorized access'})
    
    # Αναζήτηση πτήσης με βάση το flight id
    flight = next((flight for flight in flights if flight['_id'] == flight_id), None)
    
    if not flight:
        return jsonify({'error': 'Flight not found'})
    
    return jsonify(flight)


@app.route('/flights/<flight_id>/book', methods=['POST'])
def book_ticket(flight_id):
    # Έλεγχος για το αν ο χρήστης είναι logged in 
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(' ')[1]  # Assuming Bearer token
        user = next((user for user in logged_in_users if user.get('token') == auth_token), None)
        if not user:
            return jsonify({'error': 'Unauthorized access'})
    else:
        return jsonify({'error': 'Unauthorized access'})
    
    # Αναζήτηση πτήσης με flight id
    flight = next((flight for flight in flights if flight['_id'] == flight_id), None)
    
    if not flight:
        return jsonify({'error': 'Flight not found'})
    
    data = request.get_json()
    name = data['name']
    surname = data['surname']
    passport_number = data['passport_number']
    date_of_birth = data['date_of_birth']
    email = data['email']
    ticket_class = data['ticket_class']
    
    # Δημιουργία Νέας κράτησης 
    booking = {
        'flight_id': flight_id,
        'user': user['email'],
        'name': name,
        'surname': surname,
        'passport_number': passport_number,
        'date_of_birth': date_of_birth,
        'email': email,
        'ticket_class': ticket_class
    }
    bookings.append(booking)
    
    return jsonify({'message': 'Ticket booked successfully', 'booking': booking})



@app.route('/bookings', methods=['GET'])
def get_user_bookings():
    # Έλεγχος για το αν ο χρήστης είναι logged in 
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(' ')[1]  # Assuming Bearer token
        user = next((user for user in logged_in_users if user.get('token') == auth_token), None)
        if not user:
            return jsonify({'error': 'Unauthorized access'})
    else:
        return jsonify({'error': 'Unauthorized access'})
    
    # επέλεξε τις κρατήσεις 
    user_bookings = [booking for booking in bookings if booking['user'] == user['email']]
    
    return jsonify(user_bookings)

@app.route('/bookings/<reservation_code>', methods=['GET'])
def get_booking_details(reservation_code):
    # Έλεγχος για το αν ο χρήστης είναι logged in 
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(' ')[1]  # Assuming Bearer token
        user = next((user for user in logged_in_users if user.get('token') == auth_token), None)
        if not user:
            return jsonify({'error': 'Unauthorized access'})
    else:
        return jsonify({'error': 'Unauthorized access'})
    
    # Αναζήτηση κράτησης με κωδικό κράτησης 
    booking = next((booking for booking in bookings if booking['_id'] == reservation_code and booking['user'] == user['email']), None)
    
    if not booking:
        return jsonify({'error': 'Booking not found'})
    
    return jsonify(booking)

@app.route('/bookings/<reservation_code>/cancel', methods=['DELETE'])
def cancel_booking(reservation_code):
    # Έλεγχος για το αν ο χρήστης είναι logged in 
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(' ')[1]  
        user = next((user for user in logged_in_users if user.get('token') == auth_token), None)
        if not user:
            return jsonify({'error': 'Unauthorized access'})
    else:
        return jsonify({'error': 'Unauthorized access'})
    
   # Αναζήτηση με βάση τον κωδικό κράτησης και το email 
    booking = next((booking for booking in bookings if booking['_id'] == reservation_code and booking['user'] == user['email']), None)
    
    if not booking:
        return jsonify({'error': 'Booking not found'})
    
    # Αφαίρεση κράτησης
    bookings.remove(booking)
    
    # Ενημέρωσε αριθμό διαθέσιμων πτήσεων
    flight = next((flight for flight in flights if flight['_id'] == booking['flight_id']), None)
    if flight:
        if booking['ticket_class'] == 'economy':
            flight['economy_tickets'] += 1
        elif booking['ticket_class'] == 'business':
            flight['business_tickets'] += 1
    
    return jsonify({'message': 'Booking cancelled successfully'})


@app.route('/account/delete', methods=['DELETE'])
def delete_account():
    # Έλεγχος για το αν ο χρήστης είναι logged in 
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(' ')[1] 
        user = next((user for user in logged_in_users if user.get('token') == auth_token), None)
        if not user:
            return jsonify({'error': 'Unauthorized access'})
    else:
        return jsonify({'error': 'Unauthorized access'})
    
    # Διαγραφή χρήστη
    logged_in_users.remove(user)
    
    return jsonify({'message': 'Account deleted successfully'})


@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    # Έλγχος για στοιχείων Admin 
    admin = next((admin for admin in admins if admin['email'] == email and admin['password'] == password), None)
    
    if not admin:
        return jsonify({'error': 'Invalid email or password'})
    
    # Δημιουργία token για πρόσβαση admin 
    access_token = generate_tokens()
    logged_in_admins.append({'email': admin['email'], 'token': access_token})
    
    return jsonify({'message': 'Admin logged in successfully', 'token': access_token})


@app.route('/admin/flights', methods=['POST'])
def create_flight():
    # Έλεγχος για στοιχεία admin 
    token = request.headers.get('Authorization')
    if not is_admin_logged_in(token):
        return jsonify({'error': 'Unauthorized access'})

    data = request.get_json()
    origin = data['origin']
    destination = data['destination']
    date = data['date']
    business_tickets = data['business_tickets']
    business_cost = data['business_cost']
    economy_tickets = data['economy_tickets']
    economy_cost = data['economy_cost']

    # Δημιουργία αντικειμένου πτήσης 
    flight = {
        'origin': origin,
        'destination': destination,
        'date': date,
        'business_tickets': business_tickets,
        'business_cost': business_cost,
        'economy_tickets': economy_tickets,
        'economy_cost': economy_cost
    }

    # Πρόσθεση της πτήσης στην λίστα πτήσεων 
    flights.append(flight)

    return jsonify({'message': 'Flight created successfully'})

def is_admin_logged_in(token):
    # Έλεγχος για το αν το τοκεν 
    logged_in_admin = next((admin for admin in logged_in_admins if admin['token'] == token), None)
    return logged_in_admin is not None


@app.route('/admin/flights/<flight_id>/prices', methods=['PUT'])
def update_flight_prices(flight_id):
    # Έλεγχος για αν ο admin είναι logged in 
    token = request.headers.get('Authorization')
    if not is_admin_logged_in(token):
        return jsonify({'error': 'Unauthorized access'})

    data = request.get_json()
    business_cost = data['business_cost']
    economy_cost = data['economy_cost']

    # Εύρεση πτήσης με flight id
    flight = next((f for f in flights if f['id'] == flight_id), None)
    if not flight:
        return jsonify({'error': 'Flight not found'})

    # Ενημέρωση τιμών πτήσης 
    flight['business_cost'] = business_cost
    flight['economy_cost'] = economy_cost

    return jsonify({'message': 'Flight ticket prices updated successfully'})

@app.route('/admin/flights/<flight_code>', methods=['DELETE'])
def delete_flight(flight_code):
    # Έλεγχος για αν ο admin είναι logged in 
    token = request.headers.get('Authorization')
    if not is_admin_logged_in(token):
        return jsonify({'error': 'Unauthorized access'})

    # Εύρεση πτήσης με βάση κωδικό πτήσης 
    flight = next((f for f in flights if f['code'] == flight_code), None)
    if not flight:
        return jsonify({'error': 'Flight not found'})

    # Έλεγχος για το αν υπάροχυν κρατήσεις 
    reservations = get_reservations_by_flight_code(flight_code)
    if reservations:
        return jsonify({'error': 'Cannot delete flight with existing reservations'})

    # Διαγραφή της κράτησης 
    flights.remove(flight)

    return jsonify({'message': 'Flight deleted successfully'})


def is_admin_logged_in(token):
    # Έλεγχος για το αν το token σχετίζεται με admin 
    logged_in_admin = next((admin for admin in logged_in_admins if admin['token'] == token), None)
    return logged_in_admin is not None



# Function για ανάκτηση κρατήσεων για έναν δεδομένο κωδικό πτήσης


def get_reservations_by_flight_code(flight_code):
    
    return [reservation for reservation in reservations if reservation['flight_code'] == flight_code]


# Function μέτρησης του αριθμού των κρατήσεων για μια συγκεκριμένη κατηγορία θέσεων

def count_reservations_per_class(reservations, seat_category):
    # Function to count the number of reservations for a specific seat category
    return sum(1 for reservation in reservations if reservation['seat_category'] == seat_category)


if __name__ == '__main__':
    app.run()