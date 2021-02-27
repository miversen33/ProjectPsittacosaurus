#!/usr/bin/env python3

import sys
import psycopg2 as psql

db_uri = sys.argv[1]
db_connection = psql.connect(db_uri)
cursor = db_connection.cursor()

cursor.execute('SELECT COUNT(id) FROM attribute')
count, = cursor.fetchone()
if count > 0:
	sys.exit(0)
try:
	print('Restoring Table: attribute')
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (2, 'speed', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (5, 'strength', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (6, 'carrying', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (7, 'throw_power', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (8, 'short_throw_accuracy', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (9, 'medium_throw_accuracy', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (10, 'long_throw_accuracy', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (11, 'catching', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (12, 'run_blocking', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (13, 'pass_blocking', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (14, 'finesse_block_shedding', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (15, 'power_block_shedding', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (16, 'tackling', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (17, 'man_coverage', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (18, 'zone_coverage', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (19, 'kick_power', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (20, 'short_kick_accuracy', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (21, 'medium_kick_accuracy', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (22, 'long_kick_accuracy', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (23, 'stamina', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (24, 'injury_resistance', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (28, 'agility', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (29, 'acceleration', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (30, 'awareness', True)")
	cursor.execute("INSERT INTO attribute (id,name,boostable) VALUES (31, 'intelligence', False)")
	cursor.execute("ALTER SEQUENCE attribute_id_seq RESTART WITH 31")
	db_connection.commit()
	print('Restored Table: attribute Succesfully')
except:
	sys.exit(1)
cursor.close()
db_connection.close()

