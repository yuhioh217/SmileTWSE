from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import traceback


class getAllBroker():
    def __init__(self):
        timeout = 10
        option = webdriver.ChromeOptions()
        option.add_argument(" — incognito")
        self.broswer = webdriver.Chrome(
            executable_path='/Library/Application Support/google/chromedriver', chrome_options=option)
        self.broswer.get(
            'http://kgieworld.moneydj.com/z/zg/zgb/zgb0.djhtm?')

        try:
            WebDriverWait(self.broswer, timeout).until(
                EC.visibility_of_element_located((By.XPATH, "//select[@name='sel_Broker']/option")))
        except TimeoutException:
            self.broswer.quit()

        try:
            brokers_name = [x.text for x in self.broswer.find_elements_by_xpath(
                "//select[@name='sel_Broker']/option")]
            print(brokers_name, '\n')
            brokers_id = [x.get_attribute('value') for x in self.broswer.find_elements_by_xpath(
                "//select[@name='sel_Broker']/option")]
            print(brokers_id, '\n')
            self.broswer.quit()
        except Exception as e:
            self.broswer.quit()
            traceback.print_exc()
