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

def youtube_link(song_name):
    song_name = song_name.strip().lower()
    song_name = song_name.replace(" ", "+")
    song_search = "https://www.youtube.com/results?search_query=" + song_name
    driver.get(song_search)
    driver.implicitly_wait(3)

    # Wait for search to complete and find video link
    videos = driver.find_elements(By.ID, "video-title")
    for video in videos:
        if video.get_attribute("href"):
            return video.get_attribute("href")

def download_mp3(youtube_link):
    driver.get("https://ytmp3.cc/en13/")
    driver.implicitly_wait(0.5)

    # Find the input field for the YouTube link
    input_field = driver.find_element(By.ID, "video")

    # Find the convert button
    convert_button = driver.find_element(By.XPATH, "//*[@id='converter']/div[3]/div[2]/input")

    # Paste link and click convert button
    input_field.send_keys(youtube_link)
    convert_button.click()

    # Wait for the conversion to complete and find the download link
    time.sleep(20)  # Seems to work consistently for videos 8mins or less
    download_button = driver.find_element(By.XPATH, "//*[@id='download']/a[1]")

    # Click the download link
    download_button.click()
    time.sleep(5)  # Time for downloading to finish

def main():
    songs_input = input("Enter Songs Separated By Commas: ")
    songs = [song.strip() for song in songs_input.split(",")]
    for song in songs:
        download_mp3(youtube_link(song))

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()