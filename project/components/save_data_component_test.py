import unittest
import os
from save_data import Save_data
import pandas as pd

class TestSaveData(unittest.TestCase):
    """Test suite to check if the save_to_datadir correctly creates the data directory for ds1"""
    def test_save_to_datadir(self):
        data = {
            'temp_change_annual': pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}),
            'std_dev_annual': pd.DataFrame({'C': [7, 8, 9], 'D': [10, 11, 12]}),
            'temp_change_seasonal': pd.DataFrame({'E': [13, 14, 15], 'F': [16, 17, 18]}),
            'std_dev_seasonal': pd.DataFrame({'G': [19, 20, 21], 'H': [22, 23, 24]}),
            'temp_change_met': pd.DataFrame({'I': [25, 26, 27], 'J': [28, 29, 30]}),
            'std_dev_met': pd.DataFrame({'K': [31, 32, 33], 'L': [34, 35, 36]})
        }
        data_prep = Save_data(data, 'ds1')
        data_prep.save_to_datadir()

        directory = 'data'
        self.assertTrue(os.path.exists(directory))

        expected_files = [
            'temp_change_annual.csv',
            'std_dev_annual.csv',
            'temp_change_seasonal.csv',
            'std_dev_seasonal.csv',
            'temp_change_met.csv',
            'std_dev_met.csv'
        ]

        for file in expected_files:
            self.assertTrue(os.path.exists(os.path.join(directory, file)))

if __name__ == '__main__':
    unittest.main()
