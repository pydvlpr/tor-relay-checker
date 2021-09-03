#!/bin/env python3

import sys
import time
import ipaddress
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException


class TorRelayChecker(object):
    """
        Class handles request to the Tor Metrics Website to check 
        if an ip-address is acutally a tor relay
    """

    __url_tormetrics = "https://metrics.torproject.org/rs.html#search/"
    __ipaddr = None
    __driverpath = "/usr/bin/chromedriver"
    __driver = None

    def __init__(self):
        self.__setup_webscraper()

    def __setup_webscraper(self):
        """ Setup the webscraping for javascript websites """

        options = ChromeOptions()
        options.add_argument('--headless')
        self.__driver = webdriver.Chrome(self.__driverpath, options=options)

    def set_ip(self, ipaddr):
        """ set ip-address to request """

        ipaddr = str(ipaddress.ip_address(ipaddr))
        self.__ipaddr = ipaddr

    def __request_tor_metrics_website(self, url, ipaddr):
        """ Request information of ip-address at Tor Metrics Website """
        content = None

        try:
            self.__driver.get(url+ipaddr)
            time.sleep(2)
            content = self.__driver.find_element_by_xpath(
                '//*[@id="content"]/div/div/strong')
            result = content.text
            self.__driver.quit()
        except NoSuchElementException as e:
            result = "No match!"
        except Exception as e:
            sys.exit(
                f"Error during request of information from Tor Metrics Website.\n{e}")
        return result

    def __parse_tor_metrics_website_content(self, content):
        """ Parse the content of request to Tor Metric Website """

        if "No Results found!" in content:
            return False
        else:
            return True

    def run(self):
        """ Let the Tor Relay Checker work. """

        self.__setup_webscraper()
        content = self.__request_tor_metrics_website(
            self.__url_tormetrics, self.__ipaddr)
        print(f"Checking ip-address {self.__ipaddr}")
        check = self.__parse_tor_metrics_website_content(content)
        print("Result: ", check)


if __name__ == '__main__':

    trc = TorRelayChecker()
    # tor ipv4
    trc.set_ip("89.234.157.254")
    trc.run()
    # no relay ipv4
    trc.set_ip("89.234.157.249")
    trc.run()
    # tor relay ipv6 short
    trc.set_ip("2a0b:f4c1:2::252")
    trc.run()
    # tor relay ipv6 long
    trc.set_ip("2a0b:f4c1:0002:0000:0000:0000:0000:0253")
    trc.run()
    #no tor relay ipv6 long
    trc.set_ip("2a0b:f4c1:0002:0000:0000:0000:0000:0123")
    trc.run()
