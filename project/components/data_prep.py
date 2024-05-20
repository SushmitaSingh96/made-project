# components/data_prep.py

import pandas as pd

class Data_prep:
    def __init__(self, data):
        self.data = data

    def data_cleaning(self):
        # Only Germany data
        deu_data = self.data[self.data['Area'] == 'Germany']
        # Separating temperature data and standard deviation data
        df_temp_change = deu_data[deu_data['Element Code'] == 7271]
        df_std_dev = deu_data[deu_data['Element Code'] == 6078]

        # Dividing temp and std deviation data into annual, seasonal, and meteorological data
        df_temp_change_annual = df_temp_change[df_temp_change['Months Code'].between(7001, 7012)]
        df_std_dev_annual = df_std_dev[df_std_dev['Months Code'].between(7001, 7012)]
        df_temp_change_seasonal = df_temp_change[df_temp_change['Months Code'].between(7016, 7019)]
        df_std_dev_seasonal = df_std_dev[df_std_dev['Months Code'].between(7016, 7019)]
        df_temp_change_met = df_temp_change[df_temp_change['Months Code'] == 7020]
        df_std_dev_met = df_std_dev[df_std_dev['Months Code'] == 7020]

        # Dropping the specified columns from each dataset
        columns_to_drop = ['Area Code', 'Area Code (M49)', 'Area', 'Months Code', 'Element Code', 'Element', 'Unit']
        df_temp_change_annual = df_temp_change_annual.drop(columns=columns_to_drop)
        df_std_dev_annual = df_std_dev_annual.drop(columns=columns_to_drop)
        df_temp_change_seasonal = df_temp_change_seasonal.drop(columns=columns_to_drop)
        df_std_dev_seasonal = df_std_dev_seasonal.drop(columns=columns_to_drop)
        df_temp_change_met = df_temp_change_met.drop(columns=columns_to_drop)
        df_std_dev_met = df_std_dev_met.drop(columns=columns_to_drop)

        return {
            'temp_change_annual': df_temp_change_annual,
            'std_dev_annual': df_std_dev_annual,
            'temp_change_seasonal': df_temp_change_seasonal,
            'std_dev_seasonal': df_std_dev_seasonal,
            'temp_change_met': df_temp_change_met,
            'std_dev_met': df_std_dev_met
        }
