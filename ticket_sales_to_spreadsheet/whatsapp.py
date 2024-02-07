import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

PROFILE_PATH = f"{os.getenv('HOME')}/.whatsappbot"

def get_driver(headless=False):
    print("get_driver")
    options = Options()
    # create profile with firefox -p
    profile_arg_param = '-profile' ;
    profile_arg_value = PROFILE_PATH
    options.add_argument(profile_arg_param)
    options.add_argument(profile_arg_value)
    os.environ['CLASS'] = 'selenium'
    if headless == True:
        os.environ['MOZ_HEADLESS'] = '1'
    driver = webdriver.Firefox(options=options)
    return driver

def open_url(driver, url):
    print(f"open_url start {url}")
    driver.get(url)
    print(f"open_url end {url}")

def wait(driver, xpath, timeout=3600):
    print(f"wait start [{xpath}, {timeout}]")
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    print(f"wait end [{xpath}, {timeout}]")

#time.sleep(2)selected_contact = driver.find_element_by_xpath("//span[@title='"+contact+"']")
#selected_contact.click()inp_xpath = '//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]'
#input_box = driver.find_element_by_xpath(inp_xpath)
#time.sleep(2)
#input_box.send_keys(text + Keys.ENTER)
#time.sleep(2)driver.quit()


def login(driver):
    open_url(driver, "https://web.whatsapp.com")

def open_chat(driver, name):
    textbox_xpath = "//div[contains(text(), 'Search or start new chat')]"
    wait(driver, textbox_xpath)
    time.sleep(3)
    search = driver.find_element(By.XPATH, textbox_xpath)
    actions = ActionChains(driver)
    actions.move_to_element(search)
    actions.click()
    actions.send_keys(name).perform()
    time.sleep(3)
    chat_xpath = f"//span[@title='{name}']"
    wait(driver, chat_xpath)
    chat = driver.find_element(By.XPATH, chat_xpath)
    chat.click()

def send_message(driver, text):
    write_xpath = "//div[contains(text(), 'Type a message')]"
    wait(driver, write_xpath)
    time.sleep(3)
    write = driver.find_element(By.XPATH, write_xpath)
    actions = ActionChains(driver)
    actions.move_to_element(write)
    actions.click()
    actions.send_keys(text).perform()
    actions.send_keys(Keys.RETURN).perform()
    #from IPython import embed; embed()

def send(message):
    driver = get_driver()
    login(driver)
    open_chat(driver, "New Super Horvat Bros.")
    send_message(driver, message)
    driver.close()

def run():
    send("[BOT]: test")

if __name__ == "__main__":
    run()
