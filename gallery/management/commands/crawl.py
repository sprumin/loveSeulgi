from django.core.management.base import BaseCommand

from selenium import webdriver

import re
import time


class Command(BaseCommand):
    help = "seulgi image crawler"

    def crawl_google_image(self, name):
        driver = webdriver.Chrome("chromedriver")
        driver.get(f"https://www.google.co.kr/search?q={name}&tbm=isch")
        driver.implicitly_wait(3)

        last_height = driver.execute_script("return document.body.scrollHeight")
        SCROLL_PAUSE_TIME = 0.5

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)

            try:
                element = driver.find_elements_by_id("smb")[0]
                element.click()
            except:
                pass

            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

        images_info = re.findall(r"\"ou\":\"(.*?)\".*?\"pt\":\"(.*?)\".*?\"ru\":\"(.*?)\"", driver.page_source)

        for info in images_info:
            print(info)

        driver.quit()

    def add_arguments(self, parser):
        """ get params """
        parser.add_argument("name",
                            nargs=1,
                            type=str,
                            help="name")

    def handle(self, *args, **options):
        name = options["name"][0]

        self.crawl_google_image(name)
