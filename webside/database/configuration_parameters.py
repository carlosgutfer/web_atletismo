
#############################################################
# DATABASE

FLUSH_SERVER_PORT = '7007'
WEB_IP_ADDRESS = 8000
DATABASE_CONFIG = {"DEFAULT": {
                        "DB_NAME": "postgres",
                        "DB_USER" : "postgres",
                        "DB_PASSWORD" : "admin",
                        "HOST" : "host.docker.internal",
                        "PORT": 5432
                    }} # host_linux = 127.0.0.1 works too


