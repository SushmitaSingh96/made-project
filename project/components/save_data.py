import os

class Save_data:
    def __init__(self, data):
        self.data = data
    def save_to_datadir(self):
        directory = 'data'
        if not os.path.exists(directory):
            os.makedirs(directory)

        #for dataset1
        self.data['temp_change_annual'].to_csv(os.path.join(directory, 'temp_change_annual.csv'), index=False)
        self.data['std_dev_annual'].to_csv(os.path.join(directory, 'std_dev_annual.csv'), index=False)
        self.data['temp_change_seasonal'].to_csv(os.path.join(directory, 'temp_change_seasonal.csv'), index=False)
        self.data['std_dev_seasonal'].to_csv(os.path.join(directory, 'std_dev_seasonal.csv'), index=False)
        self.data['temp_change_met'].to_csv(os.path.join(directory, 'temp_change_met.csv'), index=False)
        self.data['std_dev_met'].to_csv(os.path.join(directory, 'std_dev_met.csv'), index=False)

        print("Saved All Files")
