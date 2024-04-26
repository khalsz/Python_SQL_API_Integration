from dataexporter.datahandler import APIDatahandler
from database.connect import connect_to_db
from database.import_csv_record import export_csv_to_table
import os
from config import dbconfig

# set environmental variables 
sql_server = dbconfig['SQL_SERVER']
postgres_username = dbconfig['POSTGRES_USERNAME']
postgres_password = dbconfig['POSTGRES_PASSWORD']
postgres_host = dbconfig['POSTGRES_HOST']

def main(url:str, csv_file_path:str, tab_name:str, db_name, data_key:str): 
    """
    Main function to execute the data pipeline process.

    Args:
        url (str): URL of the API endpoint.
        csv_file_path (str): Path to the CSV file to be saved.
        tab_name (str): Name of the database table.
        db_name (str): Name of the database.
        data_key (str): data key to be extracted from the API request json content

    Returns:
        None

    """
    try: 
       # Instantiate APIDataHandler with the provided URL     
        apidata = APIDatahandler(data_url=url)
        
        # Fetch JSON data from the API
        json_data = apidata.fetch_data()
        
        # Save JSON data to a CSV file
        apidata.save_json_to_csv(csv_file_path=csv_file_path, json_data=json_data, extract_key=data_key)
        
        # Connect to SQL Server
        sql_server_engine = connect_to_db(db_name=db_name, 
                                          server=sql_server)
        print('yes')
        # Connect to PostgreSQL Server
        postgres_server_engine = connect_to_db(username=postgres_username, password=postgres_password, 
                                               db_name=db_name, host=postgres_host)
        print('no')
        # # Export CSV data to SQL Server table
        export_csv_to_table(table_name=tab_name, engine=sql_server_engine, csv_file=csv_file_path)
        
        print('come')
        # Export CSV data to PostgreSQL table
        export_csv_to_table(table_name=tab_name, engine=postgres_server_engine, csv_file=csv_file_path)
        
        print('go')
        print('Data pipeline process successful')
        
    except Exception as e: 
        # Handle any exceptions that occur during the data pipeline process
        print(f"An error occured: {e}")
        
        
if __name__ == "__main__": 
    # Define URLs, CSV file paths, table names, and database name
    posturl = "https://dummyjson.com/posts"
    producturl = "https://dummyjson.com/products"
    postcsv_path = os.path.join(os.getcwd(), 'data/post.csv')
    productcsv_path = os.path.join(os.getcwd(), 'data/products.csv')
    post_table_name = 'posts'  
    product_table_name = "products"
    db_name = "dummyjson"
    
    # Execute main function for posts data
    main(url=posturl, csv_file_path=postcsv_path, tab_name=post_table_name, db_name=db_name, data_key='posts')
    
    # Execute main function for products data
    main(url=producturl, csv_file_path=productcsv_path, tab_name=product_table_name, db_name=db_name, data_key='products') 