from selenium import webdriver
import time
import random
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


class Facebook():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument('--disable-notifications')

        # chrome_options.add_argument('--proxy-server=%s' % PROXY)
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(
            'chromedriver', chrome_options=chrome_options)
        browser = self.browser
        browser.get('https://facebook.com')
        browser.set_window_size(900, 700)
        time.sleep(random.randrange(4, 6))

        # declare set of users we will send messages
        self.users = set()

    # sign in to facebook account

    def auth(self, email: str, password: str):
        self.email = email
        self.password = password
        browser = self.browser
        input_email = browser.find_element_by_name('email')
        input_password = browser.find_element_by_name('pass')
        input_email.send_keys(email)
        time.sleep(random.randrange(1, 2))
        input_password.send_keys(password)
        time.sleep(random.randrange(1, 2))
        input_password.send_keys(Keys.ENTER)
        time.sleep(random.randrange(4, 6))
        try:
            error = browser.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div[1]/div/div[2]/div[2]/form/div[1]/div[1]').text
            time.sleep(2)
            browser.get('https://facebook.com')
            return
        except NoSuchElementException:
            pass
        try:
            error = browser.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div[1]/div/div[2]/div[2]/form/div/div[2]/div[2]/text()').text
            time.sleep(2)
            browser.get('https://facebook.com')
            return
        except NoSuchElementException:
            pass
        time.sleep(random.randrange(5, 7))

    def scrape_friends(self):
        browser = self.browser
        browser.set_window_size(900, 700)
        time.sleep(random.randrange(1, 2))
        browser.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[1]/div/div[2]/div[4]/div[1]/span/div/div[1]/div').click()
        time.sleep(random.randrange(5, 7))
        browser.get('https://www.facebook.com/me')

        time.sleep(random.randrange(5, 7))

        # browser.execute_script("window.scrollTo(0, 100)")
        # time.sleep(random.randrange(1, 2))
        browser.get('{}&sk=friends'.format(browser.current_url))
        # friends_quantity.click()
        time.sleep(random.randrange(12, 15))
        friends_quantity = int(browser.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a').text.split(' ')[0])
        print(friends_quantity)
        # browser.find_element_by_xpath(
        #     '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/a[3]').click()
        time.sleep(random.randrange(3, 5))
        while True:
            try:
                time.sleep(random.randrange(2, 4))
                browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 3))
                friends_list = browser.find_elements_by_xpath(
                    '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div')
                time.sleep(random.randrange(5, 6))
                for friend in friends_list:
                    try:
                        id = friend.find_element_by_xpath(
                            './/div[1]/a').get_attribute('href').split('/')[3]

                        name = friend.find_element_by_xpath(
                            './/div[2]/div[1]/a/span').text

                        if "profile.php?id=" in id:
                            id = id.strip('profile.php?id=')
                        if (id and name):
                            self.users.add((name, id))
                    except NoSuchElementException:
                        continue
                print(self.users)
                if (friends_quantity <= friends_list.__len__()):
                    browser.execute_script(
                        "window.scrollTo(0, 0);")
                    break
                try:
                    photos = browser.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[2]/div/div/div/div')
                    if (photos):
                        break
                except NoSuchElementException:
                    pass
            except StaleElementReferenceException:
                pass
        browser.refresh()
        time.sleep(random.randrange(5, 7))
        time.sleep(random.randrange(5, 7))

    def add_users_to_set(self, list: set):
        browser = self.browser
        for user in list:
            browser.get("https://facebook.com/{}".format(user))
            time.sleep(random.randrange(5, 7))
            try:
                name = browser.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/div/div/span/div/h1').text
                time.sleep(random.randrange(2, 3))
                self.users.add((name, user))
            except NoSuchElementException:
                continue

    def scrape_followers(self):
        browser = self.browser
        browser.set_window_size(900, 700)
        time.sleep(random.randrange(4, 6))
        browser.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[1]/div/div[2]/div[4]/div[1]/span/div/div[1]/div').click()
        time.sleep(random.randrange(5, 7))
        browser.get('https://www.facebook.com/me')
        # browser.execute_script(
        time.sleep(random.randrange(5, 7))
        #     "window.scrollTo(0, 500);")
        browser.get('{}&sk=followers'.format(browser.current_url))
        while True:
            try:
                time.sleep(random.randrange(2, 4))
                browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 3))

                followers_list = browser.find_elements_by_xpath(
                    '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div')
                for follower in followers_list:
                    try:
                        id = follower.find_element_by_xpath(
                            './/div[1]/a').get_attribute('href').split('/')[3]

                        name = follower.find_element_by_xpath(
                            './/div[2]/div[1]/a/span').text

                        if "profile.php?id=" in id:
                            id = id.strip('profile.php?id=')
                        if (name and id):
                            self.users.add((name, id))
                    except NoSuchElementException:
                        continue
                print(self.users)
                try:
                    photos = browser.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[2]/div/div/div/div')
                    if (photos):
                        break
                except NoSuchElementException:
                    pass

            except StaleElementReferenceException:
                pass
        time.sleep(random.randrange(5, 7))
        browser.refresh()

    def send_messages(self):
        browser = self.browser
        messages_list = ['Hello {}, this for testing', 'Hi {}, this is for testing',
                         'Hallo {}, das ist für testing', 'Hola {}, esto es para testear']

        browser.set_window_size(1200, 700)

        # browser.maximize_window()
        time.sleep(random.randrange(5, 7))
        browser.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[1]/div/div[2]/div[4]/div[1]/div[2]/span/span/div/div[1]').click()
        time.sleep(random.randrange(2, 4))
        browser.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[1]/div/div[2]/div[4]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[2]/span/a').click()

        time.sleep(random.randrange(13, 15))

        for receiver in self.users:
            browser.get(
                'https://www.facebook.com/messages/t/{}'.format(receiver[1]))

            time.sleep(random.randrange(7, 10))
            try:

                time.sleep(random.randrange(3, 4))
                try:
                    message_input = browser.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[1]/div[3]/div/div/div[2]/div/div/div[4]/div[2]/div/div/div[1]')
                except NoSuchElementException:
                    message_input = browser.find_element_by_xpath(
                        '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div[4]/div[2]/div/div/div[1]')
                message_input.click()

                def replace(message):
                    return message.format(receiver[0])

                messages_to_send = []

                for message in messages_list:
                    messages_to_send.append(replace(message=message))

                message_to_send = random.choice(messages_to_send)

                message_input.send_keys(message_to_send)
                time.sleep(random.randrange(3, 4))
                message_input.send_keys(Keys.ENTER)
                time.sleep(random.randrange(2, 3))
            except (NoSuchElementException, StaleElementReferenceException) as err:
                print(err)
        time.sleep(random.randrange(5, 7))

        # browser.quit()

    def quit(self):
        self.browser.quit()
