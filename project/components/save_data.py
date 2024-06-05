import os

class Save_data:
    def __init__(self, data, id):
        self.data = data
        self.id = id

    def save_to_datadir(self) -> None:
        directory = 'data'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if self.id == "ds1":
            self.save_dataset1(directory)
        elif self.id == "ds2":
            self.save_dataset2(directory)

    def save_dataset1(self, directory) -> None:
        self.data['temp_change_annual'].to_csv(os.path.join(directory, 'temp_change_annual.csv'), index=False)
        self.data['std_dev_annual'].to_csv(os.path.join(directory, 'std_dev_annual.csv'), index=False)
        self.data['temp_change_seasonal'].to_csv(os.path.join(directory, 'temp_change_seasonal.csv'), index=False)
        self.data['std_dev_seasonal'].to_csv(os.path.join(directory, 'std_dev_seasonal.csv'), index=False)
        self.data['temp_change_met'].to_csv(os.path.join(directory, 'temp_change_met.csv'), index=False)
        self.data['std_dev_met'].to_csv(os.path.join(directory, 'std_dev_met.csv'), index=False)
        #print("Saved All Files")

    def save_dataset2(self, directory):
        self.data['meterological_data'].to_csv(os.path.join(directory, 'meterological_disasters.csv'), index=False)
        self.data['hydrological_data'].to_csv(os.path.join(directory, 'hydrological_disasters.csv'), index=False)
