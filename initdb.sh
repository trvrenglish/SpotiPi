rm spotipi.db
touch spotipi.db

sqlite3 spotipi.db "create table reading (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, noise_level INT NOT NULL, voltage REAL NOT NULL);"
