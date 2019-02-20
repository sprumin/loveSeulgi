from django.core.management.base import BaseCommand

from gallery.models import Album

from io import BytesIO
from selenium import webdriver

import os
import re
import requests
import time


class Command(BaseCommand):
    help = "seulgi image crawler"

    def save_data(self, name, data):
        exts = ["jpg", "jpeg", "gif", "png"]
        for row in data: 
            try:
                a = Album(name=name, title=row[1], source=row[2])
                filename = os.path.basename(row[0])

                if not filename.split(".")[-1] in exts:
                    filename += ".jpg"

                if filename.split(".")[-1] == "gif":
                    a.is_gif = True

                a.photo.save(f"{filename}", BytesIO(requests.get(row[0]).content))

                print(f"Save Image : {row[1]}")
            except Exception as e:
                print(f"Save Error : {e}")

    def crawl_google_image(self, name):
        driver = webdriver.Chrome("chromedriver")
        driver.get(f"https://www.google.co.kr/search?q={name}&tbm=isch")
        driver.implicitly_wait(3)

        last_height = driver.execute_script("return document.body.scrollHeight")
        pause = 0.5

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)

            try:
                element = driver.find_elements_by_id("smb")[0]
                element.click()
            except:
                pass

            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

        # [0]: image_link, [1]: title, [2]: source
        images_info = re.findall(r"\"ou\":\"(.*?)\".*?\"pt\":\"(.*?)\".*?\"ru\":\"(.*?)\"", driver.page_source)
        result_images = list()
        temp_count = 0

        for image in images_info:
            if not Album.objects.filter(photo=image[0]).exists():
                driver.get(image[0])
                print(f"image has left {len(images_info) - temp_count}")
                valid = input()

                if not valid:
                    result_images.append(image)

                temp_count += 1

        driver.quit()

        # save model
        self.save_data("Seulgi", result_images)

    def add_arguments(self, parser):
        """ get params """
        parser.add_argument("name",
                            nargs=1,
                            type=str,
                            help="name")

    def handle(self, *args, **options):
        name = options["name"][0]

        self.crawl_google_image(name)
