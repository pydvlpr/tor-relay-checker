#!/bin/env python3

import os
import sys
import time
import ipaddress
from datetime import date,timedelta
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import FirefoxOptions
from selenium.common.exceptions import NoSuchElementException


class TorRelayChecker(object):
    """
        Class handles request to the Tor Metrics Website to check 
        if an ip-address is acutally a tor relay
    """

    __url_tormetrics = "https://metrics.torproject.org/rs.html#search/"
    __ipaddr = None
    __webdriver = None
    __webdriverpath = None
    __driver = None
    __relay_details = None
    __exonerator_details = None

    def __init__(self,ipaddr=None):
        """ Initializtion of Tor Relay Checker"""

        self.__ipaddr = ipaddr
        self.__setup_webdriver()

    def __setup_webdriver(self):
        """ Testing and setup available webdriver """
        
        if os.path.exists("/usr/bin/chromedriver"):
            self.__webdriver = "chrome"
            self.__webdriverpath = "/usr/bin/chromedriver"
            print("Using chromedriver")
            self.__init_webscraper("chrome")
        
        elif os.path.exists("/usr/bin/geckodriver"):
            self.__webdriver = "gecko"
            self.__webdriverpath = "/usr/bin/geckodriver"
            print("Using geckodriver")
            self.__init_webscraper("gecko")
        
        else:
            print("Please install Chrome with chromedriver or Firefox and geckodriver")
            sys.exit(2)

    def __init_webscraper(self,browser):
        """ Setup the webscraping for javascript websites """

        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument('--headless')
            self.__driver = webdriver.Chrome(self.__webdriverpath, options=options)

        if browser == "gecko":
            options = FirefoxOptions()
            options.add_argument('--headless')
            self.__driver = webdriver.Firefox(options=options)

    def set_ip(self, ipaddr):
        """ set ip-address to request """

        ipaddr = str(ipaddress.ip_address(ipaddr))
        self.__ipaddr = ipaddr
    
    def get_relay_details(self):
        """ Returns details of requested tor relay"""

        return self.__relay_details

    def get_exonerator_details(self):
        """ Returns details of exonerator request """
        
        return self.__exonerator_details

    def __request_tor_metrics_website(self, url, ipaddr):
        """ Request information of ip-address at Tor Metrics Website """

        content = None

        try:
            self.__driver.get(url+ipaddr)
            time.sleep(2)
            content = self.__driver.find_element_by_xpath(
                '//*[@id="content"]/div/div/strong')
            result = content.text
        except NoSuchElementException as e:
            content = self.__driver.find_element_by_xpath(
                '// *[@id="torstatus_results"]')
            result = content.text
            self.__relay_details = result
        except Exception as e:
            sys.exit(
                f"Error during request of information from Tor Metrics Website.\n{e}")
        self.__driver.quit()
        return result
    
    def __check_tor_metrics_website_content(self, content):
        """ Parse the content of request to Tor Metric Website """

        if "No Results found!" in content:
            return False
        else:
            return True

    def __request_exonerator(self,ipaddr,reqdate):
        """ Request information of ip-address from Exonerator website"""

        self.__exonerator_details = ""
        url = f"https://metrics.torproject.org/exonerator.html?ip={ipaddr}&timestamp={reqdate}&lang=en"
        self.__driver.get(url)
        
        content = self.__driver.find_element_by_xpath(
            '//*[@id="wrapper"]/div[6]/div[2]/div/div/div[1]')
        
        if "Result is positive" in content.text:
            print("Exonerator: True")
            content = self.__driver.find_element_by_xpath(
                '//*[@id="wrapper"]/div[6]/div[3]')
            self.__exonerator_details = content.text

        elif "Date parameter too recent" in content.text:
            print("Exonerator: Unknown")
            print("Date is too recent.")

        elif "Result is negative" in content.text:
            print("Exonerator: False")
    
        else:
            print("Something unknown happend.")

    def request_tor_metric(self):
        """ Request information from tor metrics """

        self.__init_webscraper(self.__webdriver)
        content = self.__request_tor_metrics_website(
            self.__url_tormetrics, self.__ipaddr)
        check = self.__check_tor_metrics_website_content(content)
        if check:
            result =  self.get_relay_details()
        else:
            result = ""
        return result


    def request_exonerator(self,reqdate):
        """ Request information from exonerator """

        self.__init_webscraper(self.__webdriver)
        self.__request_exonerator(self.__ipaddr, reqdate)
        return self.__exonerator_details

    def request_tor_status(self,reqdate):
        """ Run request from exonerator and tor metric informations """

        exo_result = self.request_exonerator(reqdate)
        metric_result = self.request_tor_metric()
        result = "\n".join(["Exonerator:",exo_result,"","Tor-Relay-Metric",metric_result])
        return result

    def test_run(self):
        """ Let the Tor Relay Checker work. """

        print()
        print(f"Checking ip-address {self.__ipaddr}")
        reqdate = (date.today()-timedelta(days=3)).isoformat()
        self.__init_webscraper(self.__webdriver)
        self.__request_exonerator(self.__ipaddr,reqdate)
        if self.__exonerator_details != "":
            print(self.__exonerator_details)
            print()

        self.__init_webscraper(self.__webdriver)
        content = self.__request_tor_metrics_website(self.__url_tormetrics,self.__ipaddr)
        check = self.__check_tor_metrics_website_content(content)
        print("Tor Metric: ", check)
        if check:
            print(self.get_relay_details())

    def public_test_run(self):
        """ Lets test the public request methods """

        reqdate = (date.today()-timedelta(days=3)).isoformat()
        result = self.request_tor_status(reqdate)
        print(result)


if __name__ == '__main__':
    """ Some tests"""

    trc = TorRelayChecker()
    # tor ipv4
    trc.set_ip("89.234.157.254")
    trc.test_run()
    #trc.public_test_run()

    # no relay ipv4
    trc.set_ip("89.234.157.249")
    trc.test_run()
    # tor relay ipv6 short
    trc.set_ip("2a0b:f4c1:2::252")
    trc.test_run()
    # tor relay ipv6 long
    trc.set_ip("2a0b:f4c1:0002:0000:0000:0000:0000:0253")
    trc.test_run()
    #no tor relay ipv6 long
    trc.set_ip("2a0b:f4c1:0002:0000:0000:0000:0000:0123")
    trc.test_run()

    # tor ipv4
    trc2 = TorRelayChecker("89.234.157.254")
    trc2.test_run()
