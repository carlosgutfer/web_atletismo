import psycopg2
import psycopg2.extras
import os

from .configuration_parameters import DATABASE_CONFIG

class Data_Base:

    def __init__(self):
        self._connection = None

    def get_connection(self):
        '''
            This method create the database connection if it hasn't
            been created yet and return the cursor
        '''
        if self._connection is None:
            config = DATABASE_CONFIG
            if not self.check_OS():
                # OS Linux in dockers
                self._connection = psycopg2.connect(database = config['DEFAULT']['DB_NAME'],
                                user = config['DEFAULT']['DB_USER'],
                                password = config['DEFAULT']['DB_PASSWORD'],
                                host = config['DEFAULT']['HOST'], port = config['DEFAULT']['PORT'])
            else:
                # OS Windows
                self._connection = psycopg2.connect(database = config['DEFAULT']['DB_NAME'],
                                user = config['DEFAULT']['DB_USER'],
                                password = config['DEFAULT']['DB_PASSWORD'])
        return  self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def close_connection(self):
        '''
            Delete the connection with the database
        '''
        try:
            self._connection.commit()
            self._connection.close()
        except:
            pass

    def check_OS(self):
        '''
            Func:
            
                Check if OS is windows or linux

            Output:

                0 --> Linux
                1 --> Widows
            
        '''

        path = os.getcwd()

        if path[0] == '/':
            return 0
        else:
            return 1
