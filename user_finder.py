import time
import os
import re
import winsound
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
frequency = 1000  # Frequency in Hertz (Hz)
duration = 1000  # Duration in milliseconds (ms)


def initialize_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.add_argument(
        "user-data-dir=C:\\Users\\mit\\AppData\\Local\\Google\\Chrome Beta\\User Data\\"
    )
    options.binary_location = (
        "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
    )
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    return driver


def extract_unique_keywords(keywords):
    # Convert keywords to lowercase
    lowercase_keywords = [word.lower() for word in keywords]

    # Convert keywords to uppercase
    uppercase_keywords = [word.upper() for word in keywords]

    # Convert keywords to title case
    titlecase_keywords = [word.capitalize() for word in keywords]

    # Remove duplicates from all three lists
    unique_lowercase_keywords = list(set(lowercase_keywords))
    unique_uppercase_keywords = list(set(uppercase_keywords))
    unique_titlecase_keywords = list(set(titlecase_keywords))

    # Combine all unique keywords into a single list
    unique_keywords = (
        unique_lowercase_keywords
        + unique_uppercase_keywords
        + unique_titlecase_keywords
    )

    return unique_keywords


def dm_sender(result_dict, url):
    with open(
        "Already_done.txt",
        "r",
    ) as All_DMs:
        DMs = All_DMs.read()
    for i in range(len(result_dict)):
        print(i, ":", result_dict[i])

    if result_dict:
        winsound.Beep(frequency, duration)
    while True:
        keys_input = input(
            "Enter the keys to include in the final list (comma-separated): "
        )
        if not keys_input:
            print("No keys entered. Please enter one or more keys or 'NA' to skip.")
            continue
        if keys_input == "NA":
            break
        # Check if the input contains only digits and commas
        if all(char.isdigit() or char == "," for char in keys_input):
            # Split the input and convert each part to an integer
            keys_list = [int(key.strip()) for key in keys_input.split(",")]

            # Check if all the integers are within the valid range
            if all(0 <= key < len(result_dict) for key in keys_list):
                break  # Exit the loop if the input is valid
            else:
                print(
                    f"Invalid input. Keys should be in the range 0 to {len(result_dict) - 1}."
                )
        else:
            print("Invalid input. Please use only digits and commas.")

    if keys_input != "NA":
        keys_list = keys_input.split(",")

        final_usernames = []
        for key in keys_list:
            key = int(key.strip())

            if key in result_dict:
                final_usernames.append(result_dict[key])

        txt_msg = "Hey.. Do you want to create a reel in 4k quality like this?" + url

        for i in range(len(final_usernames)):
            if final_usernames[i][0] not in DMs:
                driver = initialize_driver()
                driver.get("https://www.instagram.com/direct/new/?hl=en")
                time.sleep(3)
                wait = WebDriverWait(driver, 10)

                dm_icon = wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            '//div[@class="x6s0dn4 x78zum5 xdt5ytf xl56j7k"]',
                        )
                    )
                ).click()
                search_user = wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            '//*[@name="queryBox"]',
                        )
                    )
                )
                time.sleep(5)
                search_user.send_keys(final_usernames[i][0])
                time.sleep(5)
                users = driver.find_elements(
                    By.XPATH,
                    '//*[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1pi30zi x1swvt13 xwib8y2 x1y1aw1k x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]',
                )
                time.sleep(5)
                user_found = False

                for user in users:
                    uname = user.find_element(
                        By.XPATH,
                        '//*[@class="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp xo1l8bm x1roi4f4 x10wh9bi x1wdrske x8viiok x18hxmgj"]',
                    ).text
                    if uname == final_usernames[i][0]:
                        user.click()
                        user_found = True
                        break
                if not user_found:
                    print("Username has changed or does not exist.")
                    break
                Chat = driver.find_element(
                    By.XPATH,
                    '//*[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xw7yly9 xktsk01 x1yztbdb x1d52u69 x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]',
                ).click()

                time.sleep(2)

                textarea = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1i64zmx xw3qccf x1uhb9sk x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']",
                        )
                    )
                )
                textarea.click()
                time.sleep(2)
                txt_ip = driver.switch_to.active_element
                txt_ip.send_keys(txt_msg)
                time.sleep(10)

                with open(
                    "Already_done.txt",
                    "a",
                ) as All_DMs:
                    All_DMs.write(final_usernames[i][0] + "\n")
                driver.quit()
            else:
                pass
    else:
        print("No user found")


def get_reels_urls(url):
    driver = initialize_driver()
    url += "reels/"
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, "//a[@class='load-more']")
            )
            WebDriverWait(driver, 10).until(element_present)
        except:
            break

    time.sleep(2)

    reels = driver.find_elements(
        By.XPATH,
        '//a[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"]',
    )

    with open(
        "reels_urls.txt",
        "w",
    ) as f:
        NUM_URLS_TO_SCRAPE = int(os.getenv("NUM_URLS_TO_SCRAPE"))
        for i in range(11, 11 + NUM_URLS_TO_SCRAPE):  # You can adjust the range here
            href = reels[i].get_attribute("href")
            f.write(href + "\n")

    driver.quit()


def scrape_instagram_reels(keyword_list):
    with open(
        "reels_urls.txt",
        "r",
    ) as f:
        for url in f:
            driver = initialize_driver()
            driver.get(url)
            time.sleep(2)

            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//div[@class="x5yr21d xw2csxc x1odjw0f x1n2onr6"]',
                    )
                )
            )
            time.sleep(2)
            count = 5
            while count >= 0:
                ul_elements = element.find_elements(
                    By.XPATH,
                    '//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xsag5q8 xz9dl7a x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]',
                )
                driver.execute_script("arguments[0].scrollBy(0, 1000);", element)
                time.sleep(2)
                count -= 1

            sequence_number = 0
            result_dict = {}
            for ul in ul_elements:
                text = ul.text.split("\n")
                if len(text) > 3:
                    comment = text[2]
                    contains_word = any(
                        re.search(r"\b{}\b".format(word), comment, re.IGNORECASE)
                        for word in keyword_list
                    )

                    if contains_word:
                        username = text[0]

                        result_list = [username, comment]
                        result_dict[sequence_number] = result_list
                        sequence_number += 1
                else:
                    pass

            driver.quit()
            dm_sender(result_dict, url)


if __name__ == "__main__":
    keywords = os.getenv("KEYWORDS").split(",")
    unique_keywords = extract_unique_keywords(keywords)

    url = input("Enter account URL: ")
    # Define a regex pattern to match URLs starting with http or https
    url_pattern = re.compile(r"^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}(/\S*)?$")

    # Check if the URL is empty or doesn't match the pattern
    if not url or not url_pattern.match(url):
        print("Invalid URL. Please enter a valid URL starting with 'http' or 'https'.")
    else:
        get_reels_urls(url)
        scrape_instagram_reels(unique_keywords)
