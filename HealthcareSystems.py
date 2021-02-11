from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Hackensack:

    def check_vaccines(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.hackensackmeridianhealth.org/covid19/")
        if not driver.page_source.__contains__("All appointments currently are full"):
            return True
        else:
            return False
        
class CentraState:

    def check_vaccines(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get("https://centrastatevac.wpengine.com/vaccine-update/")
        if not driver.page_source.__contains__("Our COVID-19 Vaccine Request form has been closed"):
            return True
        else:
            return False

