# Create the flight table and insert data into the SQLite database

import json
import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('flight.db')
cursor = conn.cursor()

# Create the 'flight' table to store flight information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS flight (
        id INTEGER PRIMARY KEY,
        origin_city TEXT,
        destination_city TEXT,
        flight_id TEXT,
        time TEXT,
        price REAL,
        airline TEXT,
        duration TEXT
    )
''')

# load flight data from JSON file
with open('flights_data.json', 'r') as f:
    json_data = json.load(f)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('flight.db')
cursor = conn.cursor()

for flight in json_data["flights"]:
    cursor.execute('''
        INSERT OR IGNORE INTO flight (flight_id, origin_city, destination_city, time, price, airline, duration)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        flight['flight_id'],
        flight['origin_city'],
        flight['destination_city'],
        flight['time'],
        flight['price'],
        flight['airline'],
        flight['duration']
    ))

# Commit the changes and close the connection
conn.commit()
conn.close()