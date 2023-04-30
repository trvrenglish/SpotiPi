import sqlite3
import subprocess

conn = sqlite3.connect('spotipi.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS reading
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              noise_level INT NOT NULL,
              voltage REAL NOT NULL)''')

output = subprocess.check_output(['python3', 'demo.py']).decode('utf-8')

lines = output.strip().split('\n')[::-1]

total_noise_level = 0
total_voltage = 0

line_count = 0

for line in lines:
    try:
        val, float_val = map(float, line.strip().split()[1:])
    except ValueError:
        continue
    
    total_noise_level += int(val)
    total_voltage += float_val
    line_count += 1
    
    if line_count == 10:
        break

avg_noise_level = total_noise_level // 10
avg_voltage = total_voltage / 10

c.execute('INSERT INTO reading (noise_level, voltage) VALUES (?, ?)', (avg_noise_level, avg_voltage))

c.execute('''
    DELETE FROM reading WHERE id NOT IN (
        SELECT id FROM reading ORDER BY id DESC LIMIT 5
    )
''')

conn.commit()
conn.close()
