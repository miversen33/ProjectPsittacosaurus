from argparse import ArgumentParser
import sys
import psycopg2 as db
from argparse import ArgumentParser

argparser = ArgumentParser()
argparser.add_argument('--database', '-d', help="Database Name to connect to")
argparser.add_argument('--host', '-o', help="Database host address")
argparser.add_argument('--port', '-t', help="OPTIONAL: Host port for database connection")
argparser.add_argument('--user', '-u', help="User to connect as")
argparser.add_argument('--password', '-p', help="OPTIONAL: Authentication password")

def main(database, host, user, password, port=5432):
    # TODO(Mike): Implement creation of database level triggers
    # Plan, scrape the '../triggers directory, import every *.py file
    # and run the `script` method inside it, providing the `connection` as the db
    uri = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    connection = db.connect(uri)
    pass

if __name__ == '__main__':
    args = argparser.parse_args()
    params = dict(
        database=args.database if args.database else input('Please provide a database to connect to: '),
        host=args.host if args.host else input('Please provide host: '),
        user=args.user if args.user else input('Please provide a username: '),
        password=args.password if args.password else input('Please enter password for database connection: '),
        port=args.port if args.port else 5432
    )
    main(**params)


