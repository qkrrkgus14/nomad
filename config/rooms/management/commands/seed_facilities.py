# 시설 생성
# DB에 Create

from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):
    help = "This command creates facilities"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times",help="How Many times do you want me to tell yoy that I love you?")

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in range(len(facilities)):
            room_models.Facility.objects.create(name=facilities[f])
            print(f+1, "  Create facilities : ", facilities[f])
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} facilities created!"))