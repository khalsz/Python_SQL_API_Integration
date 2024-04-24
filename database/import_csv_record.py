import pandas as pd
from sqlalchemy import exc


def export_csv_to_table(table_name, engine, csv_file): 
    """
    Export data from a CSV file to a database table.

    Args:
        table_name (str): Name of the database table.
        engine (Engine): SQLAlchemy engine object for the database.
        csv_file (str): Path to the CSV file containing data to be exported.

    Returns:
        None

    """
    
    df = pd.read_csv(csv_file)
    
    try: 
        # Export DataFrame to the database table
        df.to_sql(table_name, engine, if_exists="append")
        
        # Fetch and print the first 5 rows from the table
        if 'postgresql' in engine.url.drivername: 
            result = engine.execute(f"select * from {table_name} limit 5").fetchall() 
        if 'mssql' in engine.url.drivername:
            result = engine.execute(f"select TOP(5) * from {table_name}").fetchall()
        for row in result: 
            print(row)
    except exc.SQLAlchemyError as e: 
        # Handle SQLAlchemy errors
        error = str(e.__dict__['orig'])
        print(error)
        return