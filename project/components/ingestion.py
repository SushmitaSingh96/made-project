import requests
import zipfile
import io
import pandas as pd

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# Load environment variables from .env file
load_dotenv()

class Ingestion:
    def __init__(self, url) -> None:
        self.url = url

    def ingestion_from_url(self) -> pd.DataFrame:
        response = requests.get(self.url)      
        # Ensure the request was successful
        if response.status_code == 200:
            # Open the zip file from the response content
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                # List all files in the zip
                file_names = z.namelist()               
                # Check if the specific CSV file is in the zip
                if 'Environment_Temperature_change_E_Europe_NOFLAG.csv' in file_names:
                    # Read the specific CSV file into a pandas DataFrame
                    with z.open('Environment_Temperature_change_E_Europe_NOFLAG.csv') as f:
                        try:
                            df = pd.read_csv(f, encoding='latin-1')
                        except UnicodeDecodeError:
                            df = pd.read_csv(f, encoding='ISO-8859-1')
                        return df
                else:
                    print("CSV file not found in the zip")
                    return None
                
    def authenticate_and_ingest(self) -> pd.DataFrame:
        # Get credentials from environment variables
        USERNAME = os.getenv("EM_DAT_USERNAME")
        PASSWORD = os.getenv("EM_DAT_PASSWORD")

        # Initialize the Chrome driver
        driver = webdriver.Chrome()
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        # Navigate to the login page
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://public.emdat.be/login")

        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]'))
        )

        # Fill in the username
        username_field.send_keys(USERNAME)

        # Find the password field
        password_field = driver.find_element(By.XPATH, '//*[@id="password"]')

        # Fill in the password
        password_field.send_keys(PASSWORD)

        # Wait for the login button to be clickable and click it
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div/div[2]/div[3]/button[2]"))
        )
        ActionChains(driver).move_to_element(login_button).click().perform()

        # Wait for the login process to complete
        time.sleep(5)

        # Check if login was successful
        if "login" not in driver.current_url:
            # Navigate to the data page
            driver.get(self.url)

            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/form/div[2]/div[2]/a/span[2]'))
            )
            download_button.click()

            # Get the path of the downloaded file
            download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            file_prefix = 'public_emdat_'

            # Wait for the file to be downloaded
            downloaded_file = None
            while not downloaded_file:
                time.sleep(10)
                files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if f.startswith(file_prefix)]
                if files:
                    downloaded_file = max(files, key=os.path.getctime)

            # Wait for the file to be downloaded
            while not os.path.exists(downloaded_file):
                time.sleep(5)

            # Load the dataset into a DataFrame
            df = pd.read_excel(downloaded_file, engine='openpyxl')
            #print("DataFrame created successfully!")
            #print(df.head())
        driver.quit()
        return df