from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "seulgi image crawler"

    def add_arguments(self, parser):
        """ get params """
        parser.add_argument("name",
                            nargs=1,
                            type=str,
                            help="name")

    def handle(self, *args, **options):
        name = options["name"][0]

        print(name)
