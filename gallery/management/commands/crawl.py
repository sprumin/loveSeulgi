from django.core.management.base import BaseCommand

from gallery.models import Album, TrashCan

from io import BytesIO
from selenium import webdriver

import os
import re
import requests
import time
import uuid


class Command(BaseCommand):
    help = "seulgi image crawler"

    def save_data(self, name, data):
        exts = ["jpg", "jpeg", "gif", "png"]
        for row in data: 
            try:
                a = Album(name=name, title=row[1], photo_link=row[0], source=row[2])
                filename = uuid.uuid4().hex
                ext = os.path.basename(row[0]).split(".")[-1]

                if not ext in exts:
                    ext = "jpg"

                if ext == "gif":
                    a.is_gif = True

                a.photo.save(f"{filename}.{ext}", BytesIO(requests.get(row[0]).content))
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
            if not Album.objects.filter(photo_link=image[0]).exists() and not TrashCan.objects.filter(photo_link=image[0]).exists():
                driver.get(image[0])
                valid = input()

                if not valid:
                    result_images.append(image)
                else:
                    t = TrashCan(photo_link=image[0])
                    t.save()

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
