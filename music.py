from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def play_song_on_youtube(song_name):
    # format the song name for the YouTube search query
    query = song_name.replace(" ", "+") + "+audio"

    # create a new Microsoft Edge browser instance using webdriver
    browser = webdriver.Edge()

    # navigate to the YouTube search results for the specified song
    browser.get(f"https://www.youtube.com/results?search_query={query}")

    # wait for the page to load
    time.sleep(5)

    # find the second search result and click it (the first result is usually an ad)
    search_results = browser.find_elements(By.XPATH, '//*[@id="video-title"]')
    search_results[1].click()

    # wait for the video to load and start playing
    time.sleep(5)

    # get the duration of the video
    duration = browser.execute_script("return document.getElementById('movie_player').getDuration()")

    # wait for the video to finish playing
    time.sleep(duration + 13)

    # close the browser
    browser.quit()
