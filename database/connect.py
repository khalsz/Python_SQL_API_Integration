from sqlalchemy import create_engine
import pyodbc
from sqlalchemy_utils import database_exists, create_database

def create_conn_str(username, password, db_name, server, host, driver): 
    """
    Create a connection string based on provided parameters.

    Args:
        username (str): Username for database authentication.
        password (str): Password for database authentication.
        db_name (str): Name of the database.
        server (str): Server name (for MSSQL).
        host (str): Hostname or IP address (for PostgreSQL).
        driver (str): ODBC driver name (for MSSQL).

    Returns:
        str: Connection string.

    """
    if server is None: 
        return f'postgresql+psycopg2://{username}:{password}@{host}:5432/{db_name}' 
    else: 
        return f'mssql+pyodbc://@{server}/{db_name}?driver={driver}'
    


def connect_to_db(username=None, password=None, db_name=None, 
                         server=None, host=None): 
    """
    Connect to a database.

    Args:
        username (str, optional): Username for database authentication.
        password (str, optional): Password for database authentication.
        db_name (str, optional): Name of the database.
        server (str, optional): Server name (for MSSQL).
        host (str, optional): Hostname or IP address (for PostgreSQL).

    Returns:
        Engine: SQLAlchemy engine object for the connected database.

    Raises:
        Exception: If connection fails.

    """
    try: 
        driver = pyodbc.drivers()[-1]
        # Create connection string
        conn_str = create_conn_str(username, password, db_name, server, host, driver)
        
        # Create engine
        engine = create_engine(conn_str, echo=True) 
        if not database_exists(engine.url):
            print(f"Database {db_name} does not exist, preparing to create one") 
            create_database(engine.url)
        
        # Connect to the database
        with engine.connect() as connection: 
            print(f"successfully connected to database engine")    
            
        return engine    
    
    except Exception as e: 
        raise Exception(f'Connection failed {e}')
        



