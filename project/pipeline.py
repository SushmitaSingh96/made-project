from components.ingestion import Ingestion
from components.data_prep import Data_prep
import os

def main():
    # Ingest the data
    url = "https://bulks-faostat.fao.org/production/Environment_Temperature_change_E_Europe.zip"
    ingestion = Ingestion(url)
    df = ingestion.ingestion_from_url()
    
    # Prepare the data
    datasets = Data_prep(df)
    prepared_data = datasets.data_cleaning()
    # Save datasets to 'data' directory
    directory = 'data'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    prepared_data['temp_change_annual'].to_csv(os.path.join(directory, 'temp_change_annual.csv'), index=False)
    prepared_data['std_dev_annual'].to_csv(os.path.join(directory, 'std_dev_annual.csv'), index=False)
    prepared_data['temp_change_seasonal'].to_csv(os.path.join(directory, 'temp_change_seasonal.csv'), index=False)
    prepared_data['std_dev_seasonal'].to_csv(os.path.join(directory, 'std_dev_seasonal.csv'), index=False)
    prepared_data['temp_change_met'].to_csv(os.path.join(directory, 'temp_change_met.csv'), index=False)
    prepared_data['std_dev_met'].to_csv(os.path.join(directory, 'std_dev_met.csv'), index=False)

if __name__ == "__main__":
    main()
