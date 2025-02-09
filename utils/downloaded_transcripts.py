import time
import os
import urllib.request as url
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from tqdm.auto import tqdm
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transcript_download.log'),
        logging.StreamHandler()
    ]
)

def main():
    logging.info("Starting transcript download process")
    
    # Take user input for course URL
    course_url = input("Enter the course URL: ")
    logging.info(f"Course URL received: {course_url}")
    
    # O/P Directory
    transcripts_path = "./transcripts/"
    logging.info(f"Creating output directory at {transcripts_path}")
    os.makedirs(transcripts_path, exist_ok=True)

    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    logging.info("Initializing Chrome driver in headless mode")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        logging.info(f"Navigating to course URL: {course_url}")
        driver.get(course_url)
        time.sleep(5)  # Wait for the website to load

        logging.info("Clicking Downloads button")
        download_button = driver.find_element(By.XPATH, "//span[@class='tab']")
        download_button.click()
        time.sleep(2)

        logging.info("Clicking View Transcripts button")
        view_transcripts_button = driver.find_element(By.XPATH, "/html/body/app-root/app-course-details/main/section/app-course-detail-ui/div/div[3]/app-course-downloads/div/div[2]/div[1]/h3[1]")
        view_transcripts_button.click()
        time.sleep(2)

        chapter_list = driver.find_elements(By.CLASS_NAME, "c-name")
        chapter_count = len(chapter_list)
        logging.info(f"Found {chapter_count} chapters")

        # Loop through each chapter
        for i in tqdm(range(chapter_count - 1), desc="Processing chapters"):
            logging.info(f"Processing chapter {i+1}/{chapter_count-1}")
            
            # Scroll to the language button before clicking
            language_button = driver.find_element(By.XPATH, f"/html/body/app-root/app-course-details/main/section/app-course-detail-ui/div/div[3]/app-course-downloads/div/div[2]/div[2]/div[{i+2}]/div[1]/app-nptel-dropdown/div/span")
            driver.execute_script("arguments[0].scrollIntoView(true);", language_button)
            time.sleep(1)
            ActionChains(driver).move_to_element(language_button).click().perform()
            time.sleep(2)

            # Scroll to the English button before clicking
            english_button = driver.find_element(By.XPATH, f"/html/body/app-root/app-course-details/main/section/app-course-detail-ui/div/div[3]/app-course-downloads/div/div[2]/div[2]/div[{i+2}]/div[1]/app-nptel-dropdown/ul/li")
            driver.execute_script("arguments[0].scrollIntoView(true);", english_button)
            time.sleep(1)
            ActionChains(driver).move_to_element(english_button).click().perform()

        logging.info("Collecting PDF download links")
        drive_links = driver.find_elements(By.XPATH, "//a[contains(@href,'drive.google.com')]")
        pdf_links = [link.get_attribute("href") for link in drive_links]
        logging.info(f"Found {len(pdf_links)} PDF links")

        # Download each PDF file and save it to the transcripts directory
        chapter_name = 1
        for i in tqdm(range(len(pdf_links) - 1), desc="Downloading PDFs"):
            link = pdf_links[i]
            filename = link.split('/')[5]
            download_url = f"https://drive.google.com/uc?id={filename}&export=download"
            final_path = f'{transcripts_path}{chapter_name}.pdf'
            
            logging.info(f"Downloading PDF {chapter_name} to {final_path}")
            try:
                url.urlretrieve(download_url, final_path)
                logging.info(f"Successfully downloaded PDF {chapter_name}")
            except Exception as e:
                logging.error(f"Failed to download PDF {chapter_name}: {str(e)}")
            
            chapter_name += 1

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        logging.info("Closing browser")
        driver.quit()

if __name__ == "__main__":
    main()
