from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import traceback


class getAllBroker():
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument(" — incognito")
        self.broswer = webdriver.Chrome(
            executable_path='/Library/Application Support/google/chromedriver', chrome_options=option)
        self.broswer.get(
            'http://kgieworld.moneydj.com/z/zg/zgb/zgb0.djhtm?')
        self.waitForLoading(10, "//select[@name='sel_Broker']/option")
        try:
            brokers_name = self.getOptionValString("sel_Broker")
            print(brokers_name, '\n')
            brokers_id = self.getOptionValAttributes("sel_Broker")
            print(brokers_id, '\n')
            self.getEachBrokerBranch(brokers_id)
        except Exception as e:
            traceback.print_exc()
            self.quitBroswer()
        self.quitBroswer()

    def waitForLoading(self, timeout, xpath):
        timeout = timeout
        try:
            WebDriverWait(self.broswer, timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            self.quitBroswer()

    def getEachBrokerBranch(self, brokers):
        for id in brokers:
            url = "http://kgieworld.moneydj.com/z/zg/zgb/zgb0.djhtm?a=" + id
            self.broswer.get(url)
            try:
                branch_name = self.getOptionValString("sel_BrokerBranch")
                print(branch_name, '\n')
                branch_id = self.getOptionValAttributes("sel_BrokerBranch")
                print(branch_id, '\n')
            except Exception as e:
                traceback.print_exc()
                self.quitBroswer()

    def getOptionValString(self, selectName):
        valArr = [x.text for x in self.broswer.find_elements_by_xpath(
            "//select[@name='" + selectName + "']/option")]
        return valArr

    def getOptionValAttributes(self, selectName):
        valArr = [x.get_attribute('value') for x in self.broswer.find_elements_by_xpath(
            "//select[@name='" + selectName + "']/option")]
        return valArr

    def quitBroswer(self):
        self.broswer.quit()
