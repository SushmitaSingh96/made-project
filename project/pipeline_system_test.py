import unittest
import os
import pandas as pd
import time
from components.ingestion import Ingestion
from components.data_prep import Data_prep
from components.save_data import Save_data

class TestPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Initializing test data ingestion...")
        cls.url_ds1 = "https://bulks-faostat.fao.org/production/Environment_Temperature_change_E_Europe.zip"
        cls.url_ds2 = "https://public.emdat.be/data"

        ingestion_ds1 = Ingestion(cls.url_ds1)
        print("Testing ingestion from URL1...")
        cls.df_ds1 = ingestion_ds1.ingestion_from_url()
        print("Completed ingestion from URL1 successfully...")

        ingestion_ds2 = Ingestion(cls.url_ds2)
        print("Testing authentication and ingestion from URL2...")
        cls.df_ds2 = ingestion_ds2.authenticate_and_ingest()
        time.sleep(1)
        print("Completed ingestion from URL2 successfully...")

    def setUp(self):
        # Create the data directory if it does not exist
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # Clean up before each test
        self.clean_data_dir()

    def tearDown(self):
        # Clean up after each test
        self.clean_data_dir()

    def clean_data_dir(self):
        # Remove all files in the data directory
        for file in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def test_full_pipeline(self):
        print("Testing the full pipeline...")

        # Step 1: Prepare the datasets using ingested data from setUpClass
        prep_ds1 = Data_prep(self.df_ds1, 'ds1')
        cleaned_data_ds1 = prep_ds1.data_cleaning()
        self.assertIsInstance(cleaned_data_ds1, dict, "Data cleaning for ds1 should return a dictionary")
        self.assertEqual(len(cleaned_data_ds1), 6, "Cleaned data dictionary for ds1 should have 6 elements")

        prep_ds2 = Data_prep(self.df_ds2, 'ds2')
        cleaned_data_ds2 = prep_ds2.data_cleaning()
        self.assertIsInstance(cleaned_data_ds2, dict, "Data cleaning for ds2 should return a dictionary")
        self.assertEqual(len(cleaned_data_ds2), 2, "Cleaned data dictionary for ds2 should have 2 elements")

        # Step 2: Save the datasets
        saveds1 = Save_data(cleaned_data_ds1, "ds1")
        saveds1.save_to_datadir()
        saveds2 = Save_data(cleaned_data_ds2, "ds2")
        saveds2.save_to_datadir()

        # Step 3: Verify the saved files
        expected_files_ds1 = [
            'temp_change_annual.csv',
            'std_dev_annual.csv',
            'temp_change_seasonal.csv',
            'std_dev_seasonal.csv',
            'temp_change_met.csv',
            'std_dev_met.csv'
        ]
        for file in expected_files_ds1:
            self.assertTrue(os.path.exists(os.path.join(self.data_dir, file)), f"{file} should be saved in the data directory")

        expected_files_ds2 = [
            'temp_change_annual.csv',
            'std_dev_annual.csv'
        ]
        for file in expected_files_ds2:
            self.assertTrue(os.path.exists(os.path.join(self.data_dir, file)), f"{file} should be saved in the data directory")

        print("Full pipeline test passed.")

if __name__ == '__main__':
    unittest.main()
