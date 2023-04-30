from flask import Flask, jsonify
import sqlite3
import random

app = Flask(__name__)

@app.route('/')
def get_latest_reading():
    conn = sqlite3.connect('spotipi.db')
    c = conn.cursor()

    for i in range(10):
        noise_level = random.randint(50000, 150000)
        voltage = round(random.uniform(1, 2), 13)
        c.execute('INSERT INTO reading (noise_level, voltage) VALUES (?, ?)', (noise_level, voltage))
    
    c.execute('''
        DELETE FROM reading WHERE id NOT IN (
            SELECT id FROM reading ORDER BY id DESC LIMIT 10
        )
    ''')
    
    c.execute('SELECT AVG(noise_level), AVG(voltage) FROM reading')
    row = c.fetchone()
    conn.close()
    
    latest_reading = {'noise_level': row[0], 'voltage': row[1]}
    return jsonify(latest_reading)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
