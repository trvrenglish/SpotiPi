from flask import Flask, jsonify
import subprocess
import sqlite3

app = Flask(__name__)

@app.route('/')
def get_latest_reading():
    # Execute writeTable.py to insert a new row
    subprocess.run(['python', 'writeTable.py'])
    conn = sqlite3.connect('spotipi.db')
    c = conn.cursor()
    # Latest row is the one with the highest value id
    c.execute('SELECT * FROM reading ORDER BY id DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    
    latest_reading = {'id': row[0], 'timestamp': row[1], 'noise_level': row[2], 'voltage': row[3]}
    return jsonify(latest_reading)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
