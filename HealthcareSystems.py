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



class Shoprite:

    def check_vaccines(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get("http://sr.reportsonline.com/sr/shoprite/Immunizations")
        if not driver.page_source.__contains__("There are currently no COVID-19 vaccine appointments available"):
            return True
        else:
            return False