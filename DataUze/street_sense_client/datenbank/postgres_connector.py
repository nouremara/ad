import psycopg2
from psycopg2 import pool
import yaml

class PostgresConnector:
    def __init__(self):
        with open('config/db_config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            self.minconn = config['minconn']
            self.maxconn = config['maxconn']
            self.host = config['host']
            self.database = config['database']
            self.user = config['user']
            self.password = config['password']
            self.port = config['port']
            self.connection_pool = None

    def create_connection_pool(self):
        if not self.connection_pool:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(self.minconn, self.maxconn, host=self.host, database=self.database, user=self.user, password=self.password, port=self.port)
        return self.connection_pool

    def get_connection(self):
        return self.connection_pool.getconn()

    def return_connection(self, connection):
        self.connection_pool.putconn(connection)

    def close_all_connections(self):
        if self.connection_pool:
            self.connection_pool.closeall()
