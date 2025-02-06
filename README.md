# Twitter-Profile-Scraper-MYSQL
This project is a web scraper that extracts Twitter profile details and stores them in a MySQL database. It uses Selenium for web automation and MySQL for data storage.

✨ Features

✅ Scrapes Twitter profile details including bio, following count, followers count, location, and website.

✅ Uses Selenium WebDriver with Chrome in headless mode for automation.

✅ Stores the scraped data in a MySQL database for easy retrieval and analysis.

✅ Handles exceptions to avoid crashes due to missing elements on the webpage.

📌 Requirements

🐍 Python 3.x

🗄️ MySQL Database

🌐 Google Chrome & ChromeDriver

🔧 Installation

Clone the Repository

 ```git clone https://github.com/yourusername/twitter-profile-scraper.git
 cd twitter-profile-scraper
```

Install Dependencies

 `pip install -r requirements.txt`

Set Up MySQL Database

Create a MySQL database.

Update the DBHelper class with your database credentials.

The script automatically creates the required table if it doesn't exist.

⚙️ Configuration

Update the following fields in DBHelper:
```
self.conn = connector.connect(
    host='localhost', 
    port='port_number', 
    user='user_name', 
    password='password', 
    database='database_name'
)
```
🚀 Usage

Place a CSV file (twitter_links.csv) containing Twitter profile URLs in the E:\Intern\Scripting\ directory.

Run the script:

` python scraper.py`

📊 Output

🛢️ The scraped data is stored in the MySQL database under the twitter_profiles table.

📂 If the CSV file is empty or cannot be read, the script will exit gracefully with an error message.

📦 Dependencies

🔗 selenium - For automating web interactions.

🗄️ mysql-connector-python - For connecting to MySQL databases.

📊 pandas - For handling CSV file reading and data processing.

🌍 webdriver-manager - For managing the ChromeDriver installation.

⚠️ Notes

The script runs Chrome in headless mode to improve efficiency.

`--disable-gpu is used to prevent GPU-related errors in headless mode.`

The script includes error handling for missing elements on Twitter profile pages.

📜 License

This project is licensed under the MIT License.

👨‍💻 Author

Himanshu Gaur 🚀
