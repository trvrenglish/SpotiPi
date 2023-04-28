import sqlite3
import subprocess

conn = sqlite3.connect('spotipi.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS reading
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              noise_level INT NOT NULL,
              voltage REAL NOT NULL)''')

measurements = subprocess.run(['python3', 'demo.py'], capture_output=True, text=True)

# Parse the output into noise level and voltage readings
output_lines = measurements.stdout.strip().split('\n')
noise_level, voltage = output_lines[0].split()
noise_level = int(noise_level)
voltage = float(voltage)

# Keep only the 10 most recent rows
c.execute('''
    DELETE FROM reading WHERE id NOT IN (
        SELECT id FROM reading ORDER BY id DESC LIMIT 10
    )
''')

c.execute('INSERT INTO reading (noise_level, voltage) VALUES (?, ?)', (noise_level, voltage))

conn.commit()
conn.close()
