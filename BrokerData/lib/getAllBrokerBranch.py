from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import traceback


class getAllBroker():
    ''' 
      Usage:
        initial -> set config path(setConfigPath) -> fetch data(fetchData)
    '''

    def __init__(self):
        self.configPath = ""
        self.bjson = ""
        self.colArr = []

        ''' Initial Broswer '''
        option = webdriver.ChromeOptions()
        option.add_argument(" — incognito")
        self.broswer = webdriver.Chrome(
            executable_path='/Library/Application Support/google/chromedriver', chrome_options=option)

    def fetchData(self):
        self.broswer.get(
            'http://kgieworld.moneydj.com/z/zg/zgb/zgb0.djhtm?')
        self.waitForLoading(10, "//select[@name='sel_Broker']/option")
        try:
            brokers_name = self.getOptionValString("sel_Broker")
            print(brokers_name, '\n')
            brokers_id = self.getOptionValAttributes("sel_Broker")
            print(brokers_id, '\n')
            self.getEachBrokerBranch(brokers_id, brokers_name)
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

    def getEachBrokerBranch(self, brokers, brokers_name):
        for id, name in zip(brokers, brokers_name):
            url = "http://kgieworld.moneydj.com/z/zg/zgb/zgb0.djhtm?a=" + id
            self.broswer.get(url)
            try:
                branch_name = self.getOptionValString("sel_BrokerBranch")
                print(branch_name, '\n')
                branch_id = self.getOptionValAttributes("sel_BrokerBranch")
                print(branch_id, '\n')

                '''
                I will make the json file, and the format is as below:
                    {
                        "id": "xxxx",
                        "name": "xxxx",
                        "branches": [],     # id
                        "branches_name": []  # chinese
                    }
                '''
                json_obj = {
                    "id": id,
                    "name": name,
                    "branches": branch_id,
                    "branches_name": branch_name
                }
                self.dataCollection(json_obj)

            except Exception as e:
                traceback.print_exc()
                self.quitBroswer()
        print("Fetching finished...")
        if self.configPath is not None:
            with open(self.configPath, 'w', encoding='utf8') as outfile:
                json.dump(self.bjson, outfile, ensure_ascii=False)

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

    def setConfigPath(self, path):
        self.configPath = path
        print("Set the JSON config file \"" + self.configPath + "\"")
        if self.configPath is not None:
            with open(self.configPath, 'r') as reader:
                self.bjson = json.loads(reader.read())

    def dataCollection(self, broker_json):
        try:
            if self.bjson is not None and broker_json != None:
                if isinstance(self.bjson["brokers"], list):
                    self.bjson["brokers"].append(broker_json)
                    # print(self.bjson)
        except Exception as e:
            traceback.print_exc()
