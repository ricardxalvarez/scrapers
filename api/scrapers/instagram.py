from selenium import webdriver
import time
import random
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


class Instagram():
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
        browser.get('https://instagram.com')
        browser.set_window_size(900, 700)
        time.sleep(random.randrange(5, 7))
        try:
            browser.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]').click()
        except NoSuchElementException:
            pass
        # declare set of users we will send messages
        self.users = set()

    def auth(self, username: str, password: str):
        browser = self.browser
        self.username = username
        try:
            browser.find_element_by_xpath(
                '/html/body/div[4]/div/div/button[2]'
            ).click()

            time.sleep(random.randrange(5, 7))
        except NoSuchElementException:
            print('No error')

        input_username = browser.find_element_by_name('username')
        input_password = browser.find_element_by_name('password')
        input_username.send_keys(username)
        time.sleep(random.randrange(1, 2))
        input_password.send_keys(password)
        time.sleep(random.randrange(1, 2))
        input_password.send_keys(Keys.ENTER)
        time.sleep(random.randrange(1, 2))
        try:
            error = browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[2]/p').text
            browser.quit()
            return
        except NoSuchElementException:
            print('No error')
        try:
            error = browser.find_element_by_xpath(
                '/html/body/div[1]/div/div/section/main/article/div[2]/div[1]/div[2]/form/div[2]/p').text
            browser.quit()
            return
        except NoSuchElementException:
            print('No error')
        time.sleep(random.randrange(2, 3))
        try:
            browser.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
        except NoSuchElementException:
            print('Pop out element not found')
        time.sleep(13)
        # except Exception as err:
        #     print(err)
        #     browser.quit()

    def scrape_followers(self):
        browser = self.browser
        try:
            time.sleep(random.randrange(7, 10))
            browser.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div[2]/div[7]/div/div/a').click()

            time.sleep(random.randrange(13, 15))
            #  gets the quantity this user has
            # so we can know when to stop 'while is_scrolling' loop
            try:
                followers_quantity = int(browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div/span').get_attribute('title'))
            except NoSuchElementException:
                followers_quantity = int(browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/div/span').text)
            # finds and opens followers list
            try:
                followers_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a')
            except NoSuchElementException:
                followers_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a')
            followers_button.click()

            time.sleep(random.randrange(1, 3))

            print('[Info] - Scraping...')

            is_scrolling = True
            time.sleep(random.randrange(3, 5))
            # global not_changed
            not_changed = 0
            while is_scrolling:
                if (not_changed == 2):
                    break
                time.sleep(random.randrange(1, 3))
                # scrolls down to the end
                browser.execute_script(
                    "document.evaluate('/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollTop+=document.evaluate('/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight || 200")
                time.sleep(0.1)
                # checks if loader exists, if it doesn't it means we've reached the limit of users
                # this avoids an infite loop
                try:
                    browser.find_element_by_xpath(
                        "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div")
                except NoSuchElementException:
                    not_changed = not_changed + 1
                # gets a new list of followers (10 more approximaly)
                followers = browser.find_elements_by_xpath(
                    '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div')
                #    # Getting url from href attribute
                for i in followers:
                    element = i.find_element_by_xpath(
                        ".//div[2]/div[1]/div/div/span/a")
                    if element.get_attribute('href'):
                        # adds username to followers_list set
                        self.users.add(
                            element.get_attribute('href').split("/")[3])
                    else:
                        continue
                # if this set is larger or equal than the followers quantity then will brake this loop
                if (followers_quantity <= self.users.__len__()):
                    break

            print('[Info] - Saving...')
            # await client_socket.send('{} followers scraped'.format(followers_list.__len__()))
            # print('[DONE] - Your followers are saved in followers.txt file!')

            # writes a file of the followers
            # curpath = os.path.abspath(os.curdir)
            # packet_file = "%s/%s/%s/%s.mol2" % ("__pycache__",
            #                                     "followers-{}.txt".format(username))
            # print(curpath)
            # print(os.path.join(curpath, packet_file))

            # with open(packet_file, 'w') as file:
            #     file.write('\n'.join(followers_list) + "\n")
            #     file.close()

            # with open(packet_file, 'r') as file:
            #     await client_socket.send(file)

            browser.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button').click()
            return self.users
            time.sleep(random.randrange(4, 6))
        except NoSuchElementException as err:
            print(err)
            browser.quit()

    def add_users_to_set(self, list: set):
        for user in list:
            self.users.add(user)

    def scrape_following(self):
        browser = self.browser
        try:
            # takes how many people follows you
            time.sleep(10)
            try:
                following_count = int(browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a/div/span').text)
            except NoSuchElementException:
                following_count = int(browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/div/span').text)
            # opnes ths pop out showing a list
            try:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a').click()
            except NoSuchElementException:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a').click()
            # await client_socket.send('This user has {} followers'.format(following_count))
            is_scrolling = True
            not_changed = 0
            time.sleep(random.randrange(3, 5))
            while is_scrolling:
                if (not_changed == 2):
                    break
                time.sleep(random.randrange(1, 3))
                # scrolls down to the end
                browser.execute_script(
                    "document.evaluate('/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollTop+=document.evaluate('/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                time.sleep(0.1)
                # checks if loader exists, if it doesn't it means we've reached the limit of users
                try:
                    browser.find_element_by_xpath(
                        "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[2]/div")
                except NoSuchElementException:
                    not_changed = not_changed + 1
                # gets a new list of followers (10 more approximaly)
                following = browser.find_elements_by_xpath(
                    '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div')
                for i in following:
                    try:
                        element = i.find_element_by_xpath(
                            ".//div[2]/div[1]/div/div/span/a")
                        if element.get_attribute('href'):
                            # adds username to followers_list set
                            self.users.add(
                                element.get_attribute('href').split("/")[3])
                        else:
                            continue
                    except NoSuchElementException:
                        continue
                print(following_count)
                print(self.users.__len__())

                # if this set is larger or equal than the followers quantity then will brake this loop
                if (following_count <= self.users.__len__()):
                    break
            print('[Info] - Saving...')
            # await client_socket.send('{} users scraped'.format(following_list.__len__()))
            # print('[DONE] - Your followers are saved in followers.txt file!')

            # writes a file of the followers
            # with open('following.txt', 'a') as file:
            #     file.write('\n'.join(following_list) + "\n")
        except NoSuchElementException as err:
            print(err)
            browser.quit()

    def send_messages(self):
        browser = self.browser
        try:
            # await client_socket.send('Starting to send messages')
            messages = ['Hello {}, this for testing', 'Hi {}, this is for testing',
                        'Hallo {}, das ist für testing', 'Hola {}, esto es para testear']
            # goes to inbox page
            browser.get('https://www.instagram.com/direct/inbox/')
            time.sleep(2)
            # closes pop out of turn on notifications
            try:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
            except NoSuchElementException:
                print('Turn on notifications pop out already closed')
            # open mmessage sender
            try:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button').click()
            except NoSuchElementException:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[1]/div/div[3]/button').click()
            time.sleep(random.randrange(2, 3))
            for follower in self.users:
                time.sleep(random.randrange(3, 5))
                # selects users search input
                searcher_input = browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/input')

                searcher_input.click()
                searcher_input.clear()

                time.sleep(random.randrange(4, 6))
                # searches for the user
                searcher_input.send_keys(follower)

                time.sleep(random.randrange(4, 7))
                # gets the list of results
                users = browser.find_elements_by_xpath(
                    '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div')
                # checks te list of results
                # await client_socket.send('Sending messages...')
                for user in users:
                    # get the username of each results
                    username = user.find_element_by_xpath(
                        './/div/div[2]/div[1]/div'
                    ).text
                    # checks if the result is the same as the accout we are looking for
                    if (username == follower):
                        # selects the user
                        user.find_element_by_xpath(
                            './/div').click()
                        # takes us to the dm of the user
                        browser.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div/button').click()

                        time.sleep(random.randrange(4, 6))
                        # finds the input that the message will be in
                        try:
                            message_input = browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
                        except NoSuchElementException:
                            message_input = browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')

                        message_input.click()
                        message_input.clear()
                        # sends the message to the input

                        def replace(message):
                            return message.format(follower)

                        messages_to_send = []

                        for message in messages:
                            messages_to_send.append(replace(message=message))

                        message_to_send = random.choice(messages_to_send)
                        message_input.send_keys(message_to_send)

                        time.sleep(random.randrange(1, 2))
                        # click button to send the message
                        try:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button').click()
                        except NoSuchElementException:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button').click()

                        time.sleep(3)
                        # opens again dm searcher
                        try:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button').click()
                        except NoSuchElementException:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[1]/div/div[3]/button').click()
                        break
            # await client_socket.send('Messages sent succesfully')
            browser.quit()
        except Exception as err:
            print(err)

    def quit(self):
        self.browser.quit()
