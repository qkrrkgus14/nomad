# 시설 생성
# DB에 Create
import random
from django_seed import Seed
from django.core.management.base import BaseCommand
from reviews import models as review_models
from users import models as users_models
from rooms import models as room_models

class Command(BaseCommand):
    help = "This command creates reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int ,help="How Many reviews do you want me to tell yoy that I love you?")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = users_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(review_models.Review, number,{
            "accuracy" : lambda x : random.randint(0,6),
            "communication" :lambda x : random.randint(0,6),
            "cleanliness" :lambda x : random.randint(0,6),
            "location" :lambda x : random.randint(0,6),
            "check_in" :lambda x : random.randint(0,6),
            "value" :lambda x : random.randint(0,6),
            "room" : lambda x: random.choice(rooms),
            "user" : lambda x: random.choice(users),
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews created!"))