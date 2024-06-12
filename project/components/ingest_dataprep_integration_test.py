import unittest
import time
from data_prep import Data_prep  
from ingestion import Ingestion  


class TestIngestDataPrepIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Initializing test data ingestion...")
        url_ds1 = "https://bulks-faostat.fao.org/production/Environment_Temperature_change_E_Europe.zip"
        ingestion_ds1 = Ingestion(url_ds1)
        print("Testing ingestion from URL...")
        cls.df_ds1 = ingestion_ds1.ingestion_from_url()
        print("Completed Successfully...")

        url_ds2 = "https://public.emdat.be/data"
        ingestion_ds2 = Ingestion(url_ds2)
        print("Testing authentication and ingestion...")
        cls.df_ds2 = ingestion_ds2.authenticate_and_ingest()
        time.sleep(1)
        print("Completed Successfully...")

    def test_data_cleaning_return_type(self):
        print("Testing data cleaning and return type for ds1...")
        prep_ds1 = Data_prep(self.df_ds1, 'ds1')
        cleaned_data_ds1 = prep_ds1.data_cleaning()
        self.assertIsInstance(cleaned_data_ds1, dict)
        self.assertEqual(len(cleaned_data_ds1), 6)
        print("Completed Successfully...")

        print("Testing data cleaning and return type for ds2...")
        prep_ds2 = Data_prep(self.df_ds2, 'ds2')
        cleaned_data_ds2 = prep_ds2.data_cleaning()
        self.assertIsInstance(cleaned_data_ds2, dict)
        self.assertEqual(len(cleaned_data_ds2), 2) 
        print("Completed Successfully...")

if __name__ == '__main__':
    unittest.main()
