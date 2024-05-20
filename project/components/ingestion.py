import requests
import zipfile
import io
import pandas as pd

class Ingestion:
    def __init__(self, url) -> None:
        self.url = url

    def ingestion_from_url(self) -> pd.DataFrame:
        response = requests.get(self.url)      
        # Ensure the request was successful
        if response.status_code == 200:
            # Open the zip file from the response content
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                # List all files in the zip
                file_names = z.namelist()               
                # Check if the specific CSV file is in the zip
                if 'Environment_Temperature_change_E_Europe_NOFLAG.csv' in file_names:
                    # Read the specific CSV file into a pandas DataFrame
                    with z.open('Environment_Temperature_change_E_Europe_NOFLAG.csv') as f:
                        try:
                            df = pd.read_csv(f, encoding='latin-1')
                        except UnicodeDecodeError:
                            df = pd.read_csv(f, encoding='ISO-8859-1')
                        return df
                else:
                    print("CSV file not found in the zip")
                    return None

