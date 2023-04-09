from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager as cdm
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import json
import random

file = open('accounts.json',)
data = json.load(file)

with open('tags.txt', 'r') as tags_file:
    tags = [line.strip() for line in tags_file]


def random_comment():
    with open('comments.txt', 'r') as comments_file:
        comments = [line.strip() for line in comments_file]
    comment = random.choice(comments)
    return comment


def disabled(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return True
    else:
        return False


def main(info):
    chrome_options = webdriver.ChromeOptions()
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(service=Service(
        executable_path=cdm().install()), options=chrome_options)
    driver.set_window_size(500, 950)

    driver.get('https://instagram.com')

    # Login Initiator ---->>>>
    time.sleep(5)
    print("Logging In")
    driver.find_element(
        By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div/div/div/div/div[2]/div[3]/button[1]/div').click()
    time.sleep(2)

    username_field = driver.find_element(
        By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div/div/div/div/div[2]/form/div[1]/div[3]/div/label/input')
    username_field.send_keys(info["username"])

    time.sleep(1)

    password_field = driver.find_element(
        By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div/div/div/div/div[2]/form/div[1]/div[4]/div/label/input')
    password_field.send_keys(info["password"])

    time.sleep(1)

    driver.find_element(
        By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div/div/div/div/div[2]/form/div[1]/div[6]').click()

    time.sleep(10)

    # fetching posts ---->>>>

    tag = random.choice(tags)
    link = "https://www.instagram.com/explore/tags/" + tag

    driver.get(link)
    time.sleep(5)

    for i in range(1):
        ActionChains(driver).send_keys(Keys.END).perform()
        time.sleep(6)

    print("Fetching post details with #" + tag)
    row1 = driver.find_element(
        By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[2]/div/div[1]')
    row2 = driver.find_element(
        By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[2]/div/div[2]')

    row_link1 = row1.find_elements(By.TAG_NAME, "a")
    row_link2 = row2.find_elements(By.TAG_NAME, "a")

    row_links = row_link1 + row_link2

    url_list = []

    for i in row_links:
        if i.get_attribute('href') != None:
            url_list.append(i.get_attribute('href'))

    # Commenting to the posts ---->>>>

    for url in url_list:
        driver.get(url)
        driver.implicitly_wait(1)
        comment = random_comment()

        print("Commenting {" + comment + "} on the post with url: " + url)
        time.sleep(10)

        for i in range(1):
            ActionChains(driver).send_keys(Keys.END).perform()
            time.sleep(1)

        commentButton = driver.find_element(
            By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div/article/div/div[3]/div/div/section[1]/span[2]/button')
        time.sleep(2)
        commentButton.click()

        time.sleep(8)

        if disabled(driver, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/section/div'):
            print("Skipped --->>> Comments Disabled")
        else:
            path_textArea = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/section/div/form/div/textarea'
            WebDriverWait(driver, 50).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, path_textArea))
            )

            comment_box = driver.find_element(
                By.XPATH, path_textArea)

            WebDriverWait(driver, 50).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, path_textArea))
            )
            comment_box.click()
            comment_box.send_keys(comment)

            time.sleep(2)

            path_postButton = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/section/div/form/div/div'
            WebDriverWait(driver, 50).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, path_postButton))
            )

            post_comment = driver.find_element(
                By.XPATH, path_postButton)

            WebDriverWait(driver, 50).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, path_postButton))
            )
            post_comment.click()

            time.sleep(random.randint(5, 7, 20, 30))

    driver.close()


while True:
    for info in data:
        main(info)
