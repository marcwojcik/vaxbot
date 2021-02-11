import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4 import NavigableString


class EssexCounty:

    def check_vaccines(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.essexcovid.org/vaccine/vaccine_availability")

        table_element = driver.find_element_by_id('datatable-grouping')
        table_html = table_element.get_attribute('innerHTML')
        soup = BeautifulSoup(table_html, 'html.parser')
        table_rows = soup.find_all("tr", ["odd", "even"])

        # capture date a little globally
        date = "(No Date Found)"
        vaccines_count = 0;
        # walk through each individual row
        for row in table_rows:
            for column in row:

                if isinstance(column, NavigableString) or column == "\n":
                    continue

                if column.text.isnumeric() and (int(column.text)) > 0:
                    vaccines_count = vaccines_count + int(column.text)

        driver.close()
        return vaccines_count


class HudsonCounty:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_vaccines(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.hudsoncovidvax.org/login")
        driver.find_element_by_id("email").send_keys(self.username)
        driver.find_element_by_id("password").send_keys(self.password)
        driver.find_element_by_id("password").submit()
        driver.get("https://www.hudsoncovidvax.org/second/appt/38555")
        if not driver.page_source.__contains__("WE ARE NOT ABLE TO SCHEDULE ANY"):
            driver.close();
            return True
        else:
            driver.close();
            return False


class UnionCounty:

    def check_vaccines(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get("https://ucnjvaccine.org/index.php/vaccine/vaccine_availability")

        table_element = driver.find_element_by_id('datatable-grouping')
        table_element = table_element.find_element_by_tag_name('tbody')
        table_html = table_element.get_attribute('innerHTML')

        if 'There are no appointments at this time' not in table_html:
            soup = BeautifulSoup(table_html, 'html.parser')
            table_rows = soup.find_all('tr')

            # capture date a little globally
            date = "(No Date Found)"

            # walk through each individual row
            for row in table_rows:

                # if row only has one column, it is the date
                if len(row) == 1:
                    date = row.text
                else:
                    index = 0
                    location = ""
                    availability = ""

                    # walk through each column in the row, collect data on location and availability
                    # first col = location, second col = availability
                    for column in row:

                        if isinstance(column, NavigableString) or column == "\n":
                            continue

                        # print("index: {}, text: {}".format(index, column.text))

                        if index == 0:
                            location = column.text
                            index += 1
                        elif index == 1:
                            availability = column.text
                            index += 1

                    # now we have location and availability
                    # availability format: "XXX / XXX", split and get fist number
                    driver.close()

                    if int(availability.split()[0]) > 0:
                        print("found - date: {}, location: {}, availability: {}".format(date, location, availability))
                        return availability
                    else:
                        return "0"
        else:
            return "0"


class BergenCounty:

    def check_vaccines(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.bergencovidvaccine.com/index.php/vaccine/vaccine_availability")

        table_element = driver.find_element_by_id('datatable-grouping')
        table_element = table_element.find_element_by_tag_name('tbody')
        table_html = table_element.get_attribute('innerHTML')

        if 'There are no appointments at this time' not in table_html:
            soup = BeautifulSoup(table_html, 'html.parser')
            table_rows = soup.find_all('tr')

            # capture date a little globally
            date = "(No Date Found)"

            # walk through each individual row
            for row in table_rows:

                # if row only has one column, it is the date
                if len(row) == 1:
                    date = row.text
                else:
                    index = 0
                    location = ""
                    availability = ""

                    # walk through each column in the row, collect data on location and availability
                    # first col = location, second col = availability
                    for column in row:

                        if isinstance(column, NavigableString) or column == "\n":
                            continue

                        # print("index: {}, text: {}".format(index, column.text))

                        if index == 0:
                            location = column.text
                            index += 1
                        elif index == 1:
                            availability = column.text
                            index += 1

                    # now we have location and availability
                    # availability format: "XXX / XXX", split and get fist number
                    driver.close()

                    if int(availability.split()[0]) > 0:
                        print("found - date: {}, location: {}, availability: {}".format(date, location, availability))
                        return availability
                    else:
                        return "0"
        else:
            return "0"


class CollierCounty:

    def check_vaccines(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.eventbrite.com/o/florida-department-of-health-in-collier-county-32165407705")
        if not driver.page_source.__contains__("Sorry, there are no upcoming events"):
            return True
        else:
            return False
