import sqlite3

def add_sample_data():
    conn = sqlite3.connect('travel.db')
    c = conn.cursor()
    
    # Add sample destinations
    destinations = [
        ('Paris', 'The City of Light with iconic Eiffel Tower', 999.99, '/Images/paris.jpg'),
        ('Maldives', 'Paradise islands with crystal clear waters', 1499.99, '/Images/maldives.jpg'),
        ('Tokyo', 'Modern city with rich cultural heritage', 1299.99, '/Images/tokyo.jpg')
    ]
    
    c.executemany('INSERT INTO destinations (name, description, price, image_url) VALUES (?, ?, ?, ?)', destinations)
    
    # Add sample hotels
    hotels = [
        ('Grand Paris Hotel', 'Paris', 299.99, 'Luxury hotel near Eiffel Tower', '/Images/paris-hotel.jpg'),
        ('Maldives Resort & Spa', 'Maldives', 599.99, 'Overwater villas with ocean view', '/Images/maldives-hotel.jpg'),
        ('Tokyo Skyline Hotel', 'Tokyo', 399.99, 'Modern hotel in Shinjuku district', '/Images/tokyo-hotel.jpg')
    ]
    
    c.executemany('INSERT INTO hotels (name, location, price_per_night, description, image_url) VALUES (?, ?, ?, ?, ?)', hotels)
    
    conn.commit()
    conn.close()
    print("Sample data added successfully!")

if __name__ == '__main__':
    add_sample_data()