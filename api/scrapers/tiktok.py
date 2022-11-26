from selenium import webdriver
import time
import random
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


class Tiktok():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument('--disable-notifications')

        # chrome_options.add_argument('--proxy-server=%s' % PROXY)
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--disable-infobars")
        # chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # chrome_options.add_argument(
        #     "--user-data-dir=C:/Users/user/AppData/Local/Google/Chrome/User Data")
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(
            'chromedriver', chrome_options=chrome_options)
        browser = self.browser
        browser.get('https://tiktok.com')
        browser.set_window_size(900, 700)
        time.sleep(random.randrange(5, 8))

        self.users = set()

    def auth(self, username: str, password: str):
        browser = self.browser
        browser.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div[2]/div/a').click()
        time.sleep(random.randrange(2, 3))
        browser.find_element_by_xpath(
            '/html/body/div[7]/div[2]/div[2]').click()
        time.sleep(random.randrange(5, 8))
        browser.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div[2]/button').click()
        time.sleep(random.randrange(4, 7))
        browser.find_element_by_xpath(
            '/html/body/div[7]/div[2]/div[1]/div[1]/div/div/a[2]').click()
        time.sleep(random.randrange(4, 8))
        browser.find_element_by_xpath(
            '/html/body/div[7]/div[2]/div[2]/div[1]/div/form/div[2]/a').click()
        time.sleep(random.randrange(2, 6))
        input_username = browser.find_element_by_xpath(
            '/html/body/div[7]/div[2]/div[2]/div[1]/div/form/div[1]/input')
        input_password = browser.find_element_by_xpath(
            '/html/body/div[7]/div[2]/div[2]/div[1]/div/form/div[2]/div/input')
        input_username.send_keys(username)
        time.sleep(random.randrange(2, 5))
        input_password.send_keys(password)
        time.sleep(random.randrange(6, 10))
        input_password.send_keys(Keys.ENTER)
        time.sleep(random.randrange(4, 7))
        try:
            error = browser.find_element_by_xpath(
                '/html/body/div[6]/div[2]/div[2]/div[1]/div/form/div[3]').text
            print(error)
        except NoSuchElementException:
            pass
        time.sleep(random.randrange(4, 7))
        browser.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div[2]/div[4]').click()
        time.sleep(random.randrange(3, 4))
        browser.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div[2]/div[4]/div/ul/li[1]/a').click()

    def scrape_following(self):
        browser = self.browser
        time.sleep(random.randrange(4, 7))
        browser.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div[2]/div[4]').click()
        time.sleep(random.randrange(3, 4))
        browser.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div[2]/div[4]/div/ul/li[1]/a').click()
        browser.set_window_size(1150, 700)
        while True:
            following_accounts_list = browser.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div[4]/div')
            see_more_button_possible_list = browser.find_elements_by_xpath(
                '/html/body/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div[4]/div').text
            see_more_button = None
            for button in see_more_button_possible_list:
                try:
                    see_more_button = button.find_element_by_xpath('.//p').text
                    break
                except NoSuchElementException:
                    continue
            if (see_more_button.lowerCase() == 'see less'):
                break
            for account in following_accounts_list:
                username = account.find_element_by_xpath('.//a[2]/div/h4').text
                self.users.add(username)

    def send_messages(self):
        browser = self.browser
        time.sleep(random.randrange(4, 6))
        messages = ['Hello {}, this for testing', 'Hi {}, this is for testing',
                    'Hallo {}, das ist für testing', 'Hola {}, esto es para testear']
        for account in self.users:
            browser.get('https://www.tiktok.com/@{}'.format(account))
            time.sleep(random.randrange(4, 6))
            message_button = browser.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/a/button')
            if (message_button.text.lowerCase() == 'messages'):
                message_button.click()
                time.sleep(random.randrange(4, 6))
                input = browser.find_element_by_xpath(
                    '/html/body/div[2]/div[2]/div/div[2]/div[3]/div/div[1]/div/div/div[2]/div')
                input.click()

                def replace(message):
                    return message.format(account)

                messages_to_send = []

                for message in messages:
                    messages_to_send.append(replace(message=message))

                message_to_send = random.choice(messages_to_send)

                input.send_keys(message_to_send)
                input.send_keys(Keys.ENTER)
                time.sleep(random.randrange(4, 7))
                input.clear()
                time.sleep(random.randrange(12, 15))
            else:
                continue

    def quit(self):
        self.browser.quit()
