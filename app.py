from flask import Flask, jsonify
import sqlite3
import random
import subprocess

app = Flask(__name__)

@app.route('/')
def get_latest_reading():
    conn = sqlite3.connect('spotipi.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS reading
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  noise_level INT NOT NULL,
                  voltage REAL NOT NULL)''')

    process = subprocess.Popen(['python', '-u', 'measure.py'], stdout=subprocess.PIPE)
    output = process.stdout

    for i in range(10):
        line = output.readline().decode().strip()
        if line:
            noise_level, voltage = map(float, line.split())
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
