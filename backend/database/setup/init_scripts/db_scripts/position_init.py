#!/usr/bin/env python3

import sys
import psycopg2 as psql

db_uri = sys.argv[1]
db_connection = psql.connect(db_uri)
cursor = db_connection.cursor()

cursor.execute('SELECT COUNT(id) FROM position')
count, = cursor.fetchone()
if count > 0:
	sys.exit(0)
try:
	cursor.execute("INSERT INTO position (id,name,side) VALUES (2, 'Quarterback', 'offense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (3, 'Running Back', 'offense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (4, 'Full Back', 'offense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (5, 'Wide Receiver', 'offense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (6, 'Offensive Tackle', 'offense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (7, 'Offensive Guard', 'offense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (8, 'Center', 'offense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (9, 'Tight End', 'offense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (10, 'Cornerback', 'defense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (11, 'Free Safety', 'defense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (12, 'Strong Safety', 'defense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (13, 'Middle Linebacker', 'defense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (14, 'Outside Linebacker', 'defense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (15, 'Defensive Tackle', 'defense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (16, 'Defensive End', 'defense')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (17, 'Kicker', 'special_teams')")
	cursor.execute("INSERT INTO position (id,name,side) VALUES (18, 'Punter', 'special_teams')")
	db_connection.commit()
except:
	sys.exit(1)
cursor.close()
db_connection.close()

