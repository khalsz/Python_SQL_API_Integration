import pandas as pd
from sqlalchemy import exc
from sqlalchemy import  text


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
        df.to_sql(table_name, con=engine, if_exists="replace", index_label='id', index=False)
         
        # instantiating engine connection
        with engine.connect() as connection: 
            if 'postgresql' in engine.url.drivername: 
                # Fetch top 5 rows from postgresql table
                result = connection.execute(text(f"select * from {table_name} limit 5")).fetchall() 
            if 'mssql' in engine.url.drivername:
                # Fetch top 5 rows from sql server table
                result = connection.execute(text(f"select top(5)* from {table_name}")).fetchall()
            # converting queried data to dataframe
            queried_df = pd.DataFrame(result, columns=df.columns)
            print(queried_df)
    except exc.SQLAlchemyError as e: 
        # Handle SQLAlchemy errors
        raise Exception(f"Error: {e}")