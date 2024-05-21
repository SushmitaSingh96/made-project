from components.ingestion import Ingestion
from components.data_prep import Data_prep
from components.save_data import Save_data

import os

def main():
    # Ingest the dataset1
    url1 = "https://bulks-faostat.fao.org/production/Environment_Temperature_change_E_Europe.zip"
    ingestion1 = Ingestion(url1)
    df1 = ingestion1.ingestion_from_url()

    #Ingest the dataset2
    url2 = "https://public.emdat.be/data"
    ingestion2 = Ingestion(url2)
    df2 = ingestion2.authenticate_and_ingest()
    print(df2.head())
    
    # Prepare the dataset1
    datasets = Data_prep(df1)
    prepared_data = datasets.data_cleaning()

    # Save datasets1 to 'data' directory
    savedf = Save_data(prepared_data)
    savedf.save_to_datadir()



if __name__ == "__main__":
    main()
