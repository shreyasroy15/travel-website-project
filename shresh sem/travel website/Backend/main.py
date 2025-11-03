from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database initialization
def init_db():
    conn = sqlite3.connect('travel.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL)''')
    
    # Create destinations table
    c.execute('''CREATE TABLE IF NOT EXISTS destinations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  description TEXT,
                  price REAL NOT NULL,
                  image_url TEXT)''')
    
    # Create hotels table
    c.execute('''CREATE TABLE IF NOT EXISTS hotels
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  location TEXT NOT NULL,
                  price_per_night REAL NOT NULL,
                  description TEXT,
                  image_url TEXT)''')
    
    # Create bookings table
    c.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  hotel_id INTEGER,
                  check_in DATE,
                  check_out DATE,
                  total_price REAL,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (hotel_id) REFERENCES hotels (id))''')
    
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# User routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        conn = sqlite3.connect('travel.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                 (data['username'], data['password'], data['email']))
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username or email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = sqlite3.connect('travel.db')
    c = conn.cursor()
    c.execute('SELECT id, username FROM users WHERE username = ? AND password = ?',
             (data['username'], data['password']))
    user = c.fetchone()
    conn.close()
    
    if user:
        return jsonify({"message": "Login successful", "user_id": user[0], "username": user[1]}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Destinations routes
@app.route('/destinations', methods=['GET'])
def get_destinations():
    conn = sqlite3.connect('travel.db')
    c = conn.cursor()
    c.execute('SELECT * FROM destinations')
    destinations = [{"id": row[0], "name": row[1], "description": row[2], 
                    "price": row[3], "image_url": row[4]} for row in c.fetchall()]
    conn.close()
    return jsonify(destinations)

@app.route('/destinations', methods=['POST'])
def add_destination():
    data = request.json
    conn = sqlite3.connect('travel.db')
    c = conn.cursor()
    c.execute('INSERT INTO destinations (name, description, price, image_url) VALUES (?, ?, ?, ?)',
             (data['name'], data['description'], data['price'], data['image_url']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Destination added successfully"}), 201

# Hotels routes
@app.route('/hotels', methods=['GET'])
def get_hotels():
    conn = sqlite3.connect('travel.db')
    c = conn.cursor()
    c.execute('SELECT * FROM hotels')
    hotels = [{"id": row[0], "name": row[1], "location": row[2], 
               "price_per_night": row[3], "description": row[4], 
               "image_url": row[5]} for row in c.fetchall()]
    conn.close()
    return jsonify(hotels)

@app.route('/hotels', methods=['POST'])
def add_hotel():
    data = request.json
    conn = sqlite3.connect('travel.db')
    c = conn.cursor()
    c.execute('INSERT INTO hotels (name, location, price_per_night, description, image_url) VALUES (?, ?, ?, ?, ?)',
             (data['name'], data['location'], data['price_per_night'], 
              data['description'], data['image_url']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Hotel added successfully"}), 201

# Booking routes
@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    try:
        conn = sqlite3.connect('travel.db')
        c = conn.cursor()
        c.execute('INSERT INTO bookings (user_id, hotel_id, check_in, check_out, total_price) VALUES (?, ?, ?, ?, ?)',
                 (data['user_id'], data['hotel_id'], data['check_in'], 
                  data['check_out'], data['total_price']))
        conn.commit()
        booking_id = c.lastrowid
        conn.close()
        return jsonify({"message": "Booking created successfully", "booking_id": booking_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/bookings/<int:user_id>', methods=['GET'])
def get_user_bookings(user_id):
    conn = sqlite3.connect('travel.db')
    c = conn.cursor()
    c.execute('''SELECT b.*, h.name, h.location FROM bookings b 
                 JOIN hotels h ON b.hotel_id = h.id 
                 WHERE b.user_id = ?''', (user_id,))
    bookings = [{"id": row[0], "user_id": row[1], "hotel_id": row[2],
                 "check_in": row[3], "check_out": row[4], "total_price": row[5],
                 "hotel_name": row[6], "hotel_location": row[7]} for row in c.fetchall()]
    conn.close()
    return jsonify(bookings)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
