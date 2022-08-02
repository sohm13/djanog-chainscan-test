from django.core.management.base import BaseCommand


from blockchains.models import BSCPair, BSCPairTransaction


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Create pairs")

        