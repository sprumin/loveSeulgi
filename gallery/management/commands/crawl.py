from django.core.management.base import BaseCommand

from gallery.models import Album, TrashCan

from io import BytesIO
from selenium import webdriver
from multiprocessing import Pool

import os
import re
import requests
import time
import uuid


class Command(BaseCommand):
    help = "seulgi image crawler"

    def save_data(self, datas):
        # save image data
        name = "Seulgi"
        exts = ["jpg", "jpeg", "gif", "png"] 
        
        for data in datas:
            try:
                a = Album(name=name, title=data[1].replace("\\u0027", ""), photo_link=data[0], source=data[2])
                filename = uuid.uuid4().hex
                ext = os.path.basename(data[0]).split(".")[-1]

                if not ext in exts:
                    ext = "jpg"

                if ext == "gif":
                    a.is_gif = True

                a.photo.save(f"{filename}.{ext}", BytesIO(requests.get(data[0]).content))
                print(f"Save Image : {data[1]}")

            except Exception as e:
                print(f"Save Error : {e}")


    def crawl_google_image(self, name):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=options)
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
        result = list()

        for image in images_info:
            if not Album.objects.filter(photo_link=image[0]).exists() and not TrashCan.objects.filter(photo_link=image[0]).exists():
                result.append(image)

        driver.quit()

        return result 

    def add_arguments(self, parser):
        """ get params """
        parser.add_argument("name",
                            nargs=1,
                            type=str,
                            help="name")

    def handle(self, *args, **options):
        name = options["name"][0]
        """
        pool = Pool(processes=4)
        pool.map(self.save_data, self.crawl_google_image(name))
        pool.close()
        pool.join()
        """
        self.save_data(self.crawl_google_image(name))
