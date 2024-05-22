import pandas as pd

class Data_prep:
    def __init__(self, data, id):
        self.data = data
        self.id = id

    def data_cleaning(self):
        if self.id == 'ds1':
            data1 = self.dataset1_cleaning()
            return data1
        elif self.id == 'ds2':
            data2 = self.dataset2_cleaning()
            return data2
        return "Data not cleaned"

    def dataset1_cleaning(self) -> pd.DataFrame:
        # Only Germany data
        #print(self.data.head())
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
    
    def dataset2_cleaning(self) -> pd.DataFrame:
        #only Germany data
        df_deu = self.data[self.data['ISO'] == 'DEU']
        #drop columns
        columns_to_keep = ['Classification Key', 'Disaster Group','Disaster Subgroup', 'Disaster Type', 'Disaster Subtype', 'Origin', 'Associated Types', 'Magnitude','Magnitude Scale', 'Start Year', 'Start Month', 'Start Day', 'End Year','End Month', 'End Day', 'Total Deaths', 'No. Injured', 'No. Affected','Total Affected',"Insured Damage ('000 US$)", "Insured Damage, Adjusted ('000 US$)", "Total Damage ('000 US$)", "Total Damage, Adjusted ('000 US$)"]

        df_deu = df_deu[columns_to_keep]
        #out of two categories of Disaster Group: Natural and Technological, we will study only Natural Disasters
        df_deu = df_deu[df_deu['Disaster Group'] != 'Technological']
        df_deu = df_deu.drop(columns=['Disaster Group'])

        # Fill NaN values in 'Start Day' and 'End Day with 1
        df_deu['Start Day'] = df_deu['Start Day'].fillna(1)
        df_deu['End Day'] = df_deu['End Day'].fillna(1)

        # Concatenate 'Start Year', 'Start Month', and 'Start Day' columns and convert to datetime
        df_deu['Start Date'] = df_deu.apply(lambda x: pd.to_datetime(f"{int(x['Start Year'])}-{int(x['Start Month'])}-{int(x['Start Day'])}", errors='coerce'), axis=1)
        # Drop the 'Start Year', 'Start Month', and 'Start Day' columns
        df_deu.drop(columns=['Start Year', 'Start Month', 'Start Day'], inplace=True)

        #similarly, create 'End Date'
        df_deu['End Date'] = df_deu.apply(lambda x: pd.to_datetime(f"{int(x['End Year'])}-{int(x['End Month'])}-{int(x['End Day'])}", errors='coerce'), axis=1)
        # Drop the 'End Year', 'End Month', and 'End Day' columns
        df_deu.drop(columns=['End Year', 'End Month', 'End Day'], inplace=True)

        # Fill missing values in the 'Origin' column with 'Unknown'
        df_deu['Origin'] = df_deu['Origin'].fillna('Unknown')

        # Fill missing values in the 'Associated Types' column with 'Unknown'
        df_deu['Associated Types'] = df_deu['Associated Types'].fillna('Unknown')

        # List of columns to handle missing values
        columns_to_fill_with_zero = ['Magnitude', 'Total Deaths', 'No. Injured', 'No. Affected', 'Total Affected', "Insured Damage ('000 US$)", "Insured Damage, Adjusted ('000 US$)", "Total Damage ('000 US$)", "Total Damage, Adjusted ('000 US$)"]

        # Fill missing values in specified columns with 0
        df_deu[columns_to_fill_with_zero] = df_deu[columns_to_fill_with_zero].fillna(0)

        #We take the two Disaster Subgroups Meteorological and Hydrological based on the number of data points, the other categories have atmost two data points only
        df_deu_met = df_deu[df_deu['Disaster Subgroup'] == 'Meteorological']
        df_deu_hyd = df_deu[df_deu['Disaster Subgroup'] == 'Hydrological']

        return {
            'meterological_data': df_deu_met,
            'hydrological_data': df_deu_hyd
        }




        

