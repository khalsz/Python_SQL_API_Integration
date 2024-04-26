from sqlalchemy import create_engine, text
import pyodbc
from sqlalchemy_utils import database_exists, create_database

def create_conn_str(db_name, username=None, password=None,  server=None, 
                    host=None, driver=None): 

    """
    Create a connection string based on provided parameters.

    Args:
        username (str, optional): Username for database authentication.
        password (str, optional): Password for database authentication.
        db_name (str): Name of the database.
        server (str, optional): Server name (for MSSQL).
        host (str, optional): Hostname or IP address (for PostgreSQL).
        driver (str, optional): ODBC driver name (for MSSQL).

    Returns:
        str: Connection string.

    """
    if server is None: 
        return f'postgresql+psycopg2://{username}:{password}@{host}:5432/{db_name}' 
    else: 
        return f'mssql+pyodbc://@{server}/{db_name}?driver={driver}'


def sql_connect (server, driver, db_name): 
    """
    Connect to a SQL Server database.

    Args:
        server (str): Server name for connecting to SQL Server.
        driver (str): ODBC driver name.
        db_name (str): Name of the database.

    Returns:
        Engine: SQLAlchemy engine object for the connected database.

    Raises:
        Exception: If connection fails.
    """
    try: 
        # Connecting to the default master database to ensure initial connection
        conn_str = create_conn_str(server=server, driver=driver, db_name='master')
        engine = create_engine(conn_str, echo=True, isolation_level = "AUTOCOMMIT")
        
        # checking database existing and creating one if not 
        with engine.connect() as connection: 
            db_exists = connection.execute(text(f"select name from sys.databases where name = '{db_name}'")).fetchone()
            if db_exists is None: 
                print(f"Database {db_name} does not exist, preparing to create one")
                connection.execute(text(f"create database {db_name}"))
                
        # Create new connection string and engine with database name with AUTOCOMMIT isolation level
        conn_str = create_conn_str(server=server, db_name=db_name, driver=driver)
        engine = create_engine(conn_str, echo=True, isolation_level = "AUTOCOMMIT") 
        
        return engine
    except Exception as e: 
        raise Exception(f"Error: {e}")
                
def postgreql_connect(username, password, db_name, host): 
    """
    Connect to a PostgreSQL database.

    Args:
        username (str): Username for database authentication.
        password (str): Password for database authentication.
        db_name (str): Name of the database.
        host (str): Hostname or IP address of the PostgreSQL server.

    Returns:
        Engine: SQLAlchemy engine object for the connected database.

    Raises:
        Exception: If connection fails.
    """
    try:
        # Construct the connection string
        connstr = create_conn_str(username=username, password=password, db_name=db_name, host=host)
        
        # Create the SQLAlchemy engine with AUTOCOMMIT isolation level
        engine = create_engine(connstr, echo=True, isolation_level = "AUTOCOMMIT")
        
        # checking database existing and creating one if not exist
        if not database_exists(engine.url):
            print(f"Database {db_name} does not exist, preparing to create one") 
            create_database(engine.url)    
            
        return engine
    except Exception as e: 
        raise Exception(f"Error: {e}")
                
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
        # Extracting sql server database driver name
        driver = pyodbc.drivers()[-1]
        if server is None:
            # Connecting to postgresql server database
            engine = postgreql_connect(username, password, db_name, host)
        else: 
            # Connecting to sql server database
            engine = sql_connect (server, driver, db_name)
        
        # Connect to the database
        with engine.connect() as connection: 
            print(f"successfully connected to database engine: {connection}")    
            
        return engine    
    
    except Exception as e: 
        raise Exception(f'Connection failed {e}')
        



