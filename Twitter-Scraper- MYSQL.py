import mysql.connector as connector
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize MySQL connection
class DBHelper:
    def __init__(self):
        self.conn = connector.connect(
            host='localhost', 
            port='port_number', 
            user='user_name', 
            password='password', 
            database='database_name'
        )
        cur = self.conn.cursor()
        
        # Create table if not exists
        query = """
        CREATE TABLE IF NOT EXISTS twitter_profiles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            profile_url VARCHAR(255) NOT NULL,
            bio TEXT,
            following_count INT UNSIGNED,
            followers_count INT UNSIGNED,
            location VARCHAR(255),
            website VARCHAR(255),
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(query)
        self.conn.commit()

    def insert_data(self, profile_url, bio, following, followers, location, website):
        cur = self.conn.cursor()
        query = """
        INSERT INTO twitter_profiles (profile_url, bio, following_count, followers_count, location, website) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (profile_url, bio, following, followers, location, website))
        self.conn.commit()

# Initialize database helper
db = DBHelper()

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run browser in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to scrape Twitter profile details
def scrape_twitter_profile(url):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    try:
        bio = driver.find_element(By.XPATH, '//div[@data-testid="UserDescription"]').text
    except:
        bio = "N/A"

    try:
        following = driver.find_element(By.XPATH, '//a[contains(@href, "/following")]/span[1]/span').text
        following = int(following.replace(",", ""))  # Convert to integer
    except:
        following = 0

    try:
        followers = driver.find_element(By.XPATH, '//a[contains(@href, "/followers")]/span[1]/span').text
        followers = int(followers.replace(",", ""))  # Convert to integer
    except:
        followers = 0

    try:
        location = driver.find_element(By.XPATH, '//span[@data-testid="UserLocation"]').text
    except:
        location = "N/A"

    try:
        website = driver.find_element(By.XPATH, '//a[@data-testid="UserUrl"]').get_attribute('href')
    except:
        website = "N/A"

    return {
        "Profile URL": url,
        "Bio": bio,
        "Following Count": following,
        "Followers Count": followers,
        "Location": location,
        "Website": website
    }

# Read Twitter profile URLs from CSV
input_csv = r'E:\\Intern\\Scripting\\twitter_links.csv'

try:
    profiles_df = pd.read_csv(input_csv, header=None)
except Exception as e:
    print(f"Error reading CSV file: {e}")
    driver.quit()
    exit()

if profiles_df.empty:
    print("The CSV file is empty. Please check the file content.")
    driver.quit()
    exit()

# Scrape and store data in MySQL
for index, row in profiles_df.iterrows():
    url = row[0]
    if pd.notnull(url):
        print(f"Scraping {url}...")
        try:
            data = scrape_twitter_profile(url)
            db.insert_data(
                data["Profile URL"],
                data["Bio"],
                data["Following Count"],
                data["Followers Count"],
                data["Location"],
                data["Website"]
            )
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

# Close the browser
driver.quit()
