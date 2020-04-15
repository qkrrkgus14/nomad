# 시설 생성
# DB에 Create
import random
from datetime import datetime, timedelta
from django_seed import Seed
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from reservations import models as reservations_models
from users import models as users_models
from rooms import models as room_models

NAME = 'reservations'

class Command(BaseCommand):
    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int ,
            help=f"How Many {NAME} do you want me to tell yoy that I love you?")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = users_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(reservations_models.Reservation, number,{
            "status" :lambda x: random.choice(["pending","confirmed","canceled"]),
            "guest" : lambda x: random.choice(users),
            "room" : lambda x: random.choice(rooms),
            "check_in" : lambda x : datetime.now(),
            "check_out": lambda x: datetime.now() + timedelta(days=random.randint(3,25))
         })

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))