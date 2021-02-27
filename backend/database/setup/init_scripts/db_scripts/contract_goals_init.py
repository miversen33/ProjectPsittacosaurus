#!/usr/bin/env python3

import sys
import psycopg2 as psql

db_uri = sys.argv[1]
db_connection = psql.connect(db_uri)
cursor = db_connection.cursor()

cursor.execute('SELECT COUNT(id) FROM contract_goals')
count, = cursor.fetchone()
if count > 0:
	sys.exit(0)
try:
	print('Restoring Table: contract_goals')
	cursor.execute("ALTER SEQUENCE contract_goals_id_seq RESTART WITH 1")
	db_connection.commit()
	print('Restored Table: contract_goals Succesfully')
except:
	sys.exit(1)
cursor.close()
db_connection.close()

