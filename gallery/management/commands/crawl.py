from django.core.management.base import BaseCommand

from selenium import webdriver


class Command(BaseCommand):
    help = "seulgi image crawler"

    def test_selenium(self, name):
        driver = webdriver.Chrome("chromedriver")
        driver.implicitly_wait(3)
        params = {
            "q": name,
            "tbm": "isch"
        }
        driver.get("https://www.google.co.kr/search?", params)

    def add_arguments(self, parser):
        """ get params """
        parser.add_argument("name",
                            nargs=1,
                            type=str,
                            help="name")

    def handle(self, *args, **options):
        name = options["name"][0]

        self.test_selenium(name)
