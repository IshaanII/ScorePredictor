from flask import Flask, render_template, request, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

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
    input_field.click()
    input_field.clear()
    input_field.send_keys(youtube_link)
    convert_button.click()

    # Wait for the conversion to complete and find the download link
    time.sleep(20)  # Seems to work consistently for videos 8mins or less
    download_button = driver.find_element(By.XPATH, "//*[@id='download']/a[1]")

    # Click the download link
    download_button.click()
    time.sleep(5)  # Time for downloading to finish

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/progress', methods=['GET', 'POST'])
def progress():
    if request.method == "POST":
        songs_input = request.form['songs']
        songs = [song.strip() for song in songs_input.split(",")]
        status = []
        for song in songs:
            download_mp3(youtube_link(song))
            status.append(song)

    # Close the browser
    driver.quit()
    return render_template('progress.html', status=status)

if __name__ == "__main__":
    app.run(debug=True)