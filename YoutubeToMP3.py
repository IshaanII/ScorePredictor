import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def download_mp3(youtube_link):
    # Open the YouTube to MP3 converter website
    driver.get('https://ytmp3.cc/en13/')
    driver.implicitly_wait(0.5)

    # Find the input field for the YouTube link
    input_field = driver.find_element(By.ID, "video")

    # Find the convert button
    convert_button = driver.find_element(By.XPATH, "//*[@id='converter']/div[3]/div[2]/input")

    # Paste link and click convert button
    input_field.send_keys(youtube_link)
    convert_button.click()

    # Wait for the conversion to complete and find the download link
    time.sleep(20)  # Adjust this based on the website's conversion time
    download_button = driver.find_element(By.XPATH, "//*[@id='download']/a[1]")

    # Click the download link
    download_button.click()
    time.sleep(5)

def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+(&\w+=[\w-]+)*$'
        r'|(https?://)?(www\.)?youtu\.be/[\w-]+$', re.IGNORECASE)
    return re.match(youtube_regex, url) is not None

# Example usage
youtube_link = input("Enter the YouTube link: ")
if youtube_link and is_valid_youtube_url(youtube_link):
    download_mp3(youtube_link)

# Close the browser
driver.quit()