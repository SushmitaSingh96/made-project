from components.ingestion import Ingestion
from components.data_prep import Data_prep
from components.save_data import Save_data

import os

def main():
    # Ingest the dataset1
    url1 = "https://bulks-faostat.fao.org/production/Environment_Temperature_change_E_Europe.zip"
    ingestion1 = Ingestion(url1)
    df1 = ingestion1.ingestion_from_url()
    #print(df1.head())

    #Ingest the dataset2
    url2 = "https://public.emdat.be/data"
    ingestion2 = Ingestion(url2)
    df2 = ingestion2.authenticate_and_ingest()
    
    #Prepare the dataset1
    datasets1 = Data_prep(df1, "ds1")
    prepared_data1 = datasets1.data_cleaning()

    #Prepare the dataset2
    datasets2 = Data_prep(df2, "ds2")
    prepared_data2 = datasets2.data_cleaning()


    # Save datasets1 to 'data' directory
    saveds1 = Save_data(prepared_data1, "ds1")
    saveds1.save_to_datadir()

    saveds2 = Save_data(prepared_data2, "ds2")
    saveds2.save_to_datadir()



if __name__ == "__main__":
    main()
