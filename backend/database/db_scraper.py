#!/usr/bin/env python3

from pathlib import Path
from subprocess import run
import sys

# TODO(Mike): If you care enough, make this a function. If you dont, then dont, thats ok too
try:
    import psycopg2 as psql
except ImportError:
    print('Unable to start, missing psycopg2')
    do_install = input('Attempt psycopg2 install? ')
    if do_install:
        print('Attempting install')
        try:
            run(['/usr/bin/env', 'python3', '-m', 'pip', 'install', 'psycopg2-binary'])
        except:
            print('Unable to install psycopg2.')
            print('Please run the following command to install psycopg2')
            print('/usr/bin/env python3 -m pip install psycopg2-binary')
            sys.exit(1)
    else:
        print('Please run the following command to install psycopg2')
        print('/usr/bin/env python3 -m pip install psycopg2-binary')
        sys.exit(1)

_PYTHON_STUB = \
'''#!/usr/bin/env python3

import sys
import psycopg2 as psql

db_uri = sys.argv[1]
db_connection = psql.connect(db_uri)
cursor = db_connection.cursor()

'''

_GET_TABLE_COLS_QUERY = '''
SELECT 
    column_name 
FROM information_schema.columns 
WHERE
    table_schema='public' 
    AND table_name=%s
'''

_READ_TABLES = [
    'attribute',
    'base_attribute',
    'contract_goals',
    'position',
    'subposition',
]


if len(sys.argv) < 3:
    print('Missing Database URI or Script Save location. Please review provided params and run again')
    sys.exit(1)

if not sys.argv[1].startswith('postgres'):
    print(f'Invalid uri provided. Provided URI {sys.argv[1]}')
    sys.exit(2)

uri = sys.argv[1]
save_location = Path(sys.argv[2])

if not save_location.exists():
    save_location.mkdir(parents=True)

db_connection = psql.connect(uri)

cursor = db_connection.cursor()

for table in _READ_TABLES:
    # TODO(Mike): Probably want some sort of logic here so we can restore tables in the correct order. Or figure out how to use this in conjuction with
    # pg_dump?
    print(f'Scanning Table {table}...')
    f = f'{save_location}/{table}_init.py'
    cursor.execute(_GET_TABLE_COLS_QUERY, (table, ))
    columns = [row[0] for row in cursor.fetchall()]
    print(f'''    Found columns [{','.join(columns)}]''')
    cursor.execute(f'SELECT {",".join(columns)} FROM {table} ORDER BY id ASC')

    with open(f, 'w') as out_file:
        print(f'    Writing to file {f}')
        out_file.write(_PYTHON_STUB)
        out_file.write(f'''cursor.execute('SELECT COUNT(id) FROM {table}')\n''')
        out_file.write(f'''count, = cursor.fetchone()\n''')
        out_file.write(f'''if count > 0:\n''')
        out_file.write(f'''\tsys.exit(0)\n''')
        out_file.write(f'''try:\n''')
        out_file.write(f'''\tprint('Restoring Table: {table}')\n''')
        id = 1
        for row in cursor.fetchall():
            insert_query = f'''\tcursor.execute("INSERT INTO {table} ({','.join(columns)}) VALUES ('''
            processed_values = 0
            id = row[0]
            for value in row:
                if processed_values > 0:
                    insert_query +=  ', '
                if isinstance(value, str):
                    insert_query += f"'{value}'"
                else:
                    insert_query += str(value)
                processed_values += 1
            insert_query += ')")\n'
            out_file.write(insert_query)
        out_file.write(f'\tcursor.execute("ALTER SEQUENCE {table}_id_seq RESTART WITH {id}")\n')
        out_file.write('\tdb_connection.commit()\n')
        out_file.write(f'''\tprint('Restored Table: {table} Succesfully')\n''')
        out_file.write('except:\n')
        out_file.write('\tsys.exit(1)\n')
        out_file.write('cursor.close()\n')
        out_file.write('db_connection.close()\n\n')
        print("    Finished file creation")
    print(f"    Making file: {f} executable")
    Path(f).chmod(0o755)
    print(f"Succesfully created table initilization script {f}")