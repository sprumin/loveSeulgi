from django.core.management.base import BaseCommand

from gallery.models import Album

from io import BytesIO
from selenium import webdriver

import re
import requests
import time


class Command(BaseCommand):
    help = "seulgi image crawler"

    def save_data(self, name, data):
        for row in data:
            try:
                a = Album(name=name, title=row[1], source=row[2])
                a.photo.save(name, BytesIO(requests.get(row[0]).content))

                print(f"Save Image : {row[1]}")
            except Exception as e:
                print(f"Save Error : {e.__traceback__()}")

            break

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
            break #debug

        # [0]: image_link, [1]: title, [2]: source
        images_info = re.findall(r"\"ou\":\"(.*?)\".*?\"pt\":\"(.*?)\".*?\"ru\":\"(.*?)\"", driver.page_source)

        driver.quit()

        # save model
        self.save_data("Seulgi", images_info)

    def add_arguments(self, parser):
        """ get params """
        parser.add_argument("name",
                            nargs=1,
                            type=str,
                            help="name")

    def handle(self, *args, **options):
        name = options["name"][0]

        self.crawl_google_image(name)
