from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import yt_dlp
from tqdm import tqdm

# user input for course URL
course_url = input("Enter the course URL: ")

# Setup Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# List to store video links
video_links = []

try:
    driver.get(course_url)
    wait = WebDriverWait(driver, 10)

    # weeks
    weeks = wait.until(EC.presence_of_all_elements_located((By.XPATH, 
        "//div[contains(@class, 'unit-title')]/span[contains(translate(text(), 'WEEK', 'week'), 'week')]" # case insensitive week, live session skipped
    )))
    print(f"Total Weeks Found: {len(weeks)}")
    

    for week in tqdm(weeks, desc="Processing Weeks", unit="week"):
        print(f"Processing: {week.text}")
        ActionChains(driver).move_to_element(week).click().perform()
        time.sleep(3)  # Ensure lessons load

        # Select lessons inside the current week
        lesson_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'unit selected')]//ul[contains(@class, 'lessons-list')]//li[contains(@class, 'lesson')]")))
        print(f"Found {len(lesson_list)} lessons in {week.text}")

        for lesson in tqdm(lesson_list, desc=f"Processing Lessons in {week.text}", unit="lesson"):
            lesson_name = lesson.text.strip()
            ActionChains(driver).move_to_element(lesson).click().perform()
            time.sleep(2)  # Wait for content to load

            try:
                iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'youtube.com/embed/')]")))
                driver.switch_to.frame(iframe)
                anchor = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'ytp-impression-link') and @data-layer='8']")))
                youtube_url = anchor.get_attribute("href")
                video_links.append(youtube_url)
                print(f"{lesson_name}: {youtube_url}")
            except:
                print(f"{lesson_name}: No YouTube video found.")
            
            driver.switch_to.default_content()

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()

# output directory
output_dir = "lectures"
os.makedirs(output_dir, exist_ok=True)

# Download MP3
def download_mp3(url, counter):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_dir}/{counter}.%(ext)s',  # Unique numbering
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# tqdm for progress tracking
counter = 1  # Start from 1
for video_url in tqdm(video_links, desc="Downloading Lectures", unit="file"):
    download_mp3(video_url, counter)
    counter += 1  

print(f"All lectures downloaded to {output_dir}.")
