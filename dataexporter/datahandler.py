import requests
import csv

class APIDatahandler: 
    """
    A class to handle API data.

    Attributes:
        data_url (str): URL of the API endpoint.

    """
    def __init__(self, data_url:str):
        """
        Initializes the APIDataHandler object with the provided data URL.

        Args:
            data_url (str): URL of the API endpoint.

        Raises:
            AssertionError: If the data URL is not a valid string.

        """
        assert isinstance(data_url, str), f'{data_url} not a valid string'
        self.url = data_url
        
    def fetch_data(self): 
        """
        Fetches data from the API.

        Returns:
            dict: JSON data returned by the API, or None if an error occurs.

        """
        try: 
            reponse = requests.get(self.url)
            if reponse.status_code == 200:
                return reponse.json()
            else: 
                print(f"Error fetching data. Status code: {reponse.status_code}")
                return None
        except Exception as e: 
            raise Exception(f"Error: {e}")

    
    def save_json_to_csv(self, csv_file_path:str, json_data:dict): 
        """
        Saves JSON data to a CSV file.

        Args:
            csv_file_path (str): Path to the CSV file to be saved.
            json_data (dict): JSON data to be saved.

        Raises:
            AssertionError: If the JSON data is not a valid dictionary.
            Exception: If an error occurs while saving the CSV file.

        """
        assert isinstance(json_data, dict), "json_data not a valid dictionary"
        try: 
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file: 
                csv_data = csv.writer(csv_file)
                
                counter = 0 
                # subsetting the json data to extract needed value and loop through
                for data in list(json_data.items())[0][1]: 
                    # writing the first row of the json data to csv as header
                    if counter == 0: 
                        header = data.keys()  
                        csv_data.writerow(header)
                        counter += 1
                    csv_data.writerow(data.values())
                print("successfully saved file to csv")
        except Exception as e: 
            raise Exception(f'Error saving file to csv {e}')