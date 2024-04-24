# Data Migrator

## Overview
The Data Migrator is a Python project designed to fetch data from API endpoints, save it to CSV files, and export it to both SQL Server and PostgreSQL databases. It consists of several modules that handle different aspects of the data pipeline process.

## Features
- Fetch data from API endpoints.
- Save JSON data to CSV files.
- Connect to SQL Server and PostgreSQL databases.
- Export CSV data to database tables.

## Project Structure
- `dataexporter/`: Main package containing the data handling modules.
  - `datahandler.py`: Module to handle API data fetching and CSV file saving.
- `database/`: Package containing modules for database interaction.
  - `connect.py`: Module to connect to SQL Server and PostgreSQL databases.
  - `import_csv_record.py`: Module to export CSV data to database tables.
- `main_data_pipeline.py`: Main script to execute the data pipeline process.
- `README.txt`: Readme file providing an overview of the project.

## Usage
1. Set up your environment by installing the required Python packages listed in `requirements.txt`.
2. Configure your database connection parameters and API endpoints in the `main_data_pipeline.py` script.
3. Run the `main_data_pipeline.py` script to execute the data pipeline process.
4. Check the console output for status messages and errors.
5. Verify the data in your SQL Server and PostgreSQL databases.

## Configuration
- Database Connection: Set up environment variables for SQL Server and PostgreSQL connection parameters (`SQL_SERVER`, `POSTGRES_USERNAME`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`).
- API Endpoints: Define the URLs of the API endpoints to fetch data from in the `main.py` script.

## Dependencies
- Python 3.x
- requests
- pandas
- SQLAlchemy
- pyodbc
- sqlalchemy-utils


