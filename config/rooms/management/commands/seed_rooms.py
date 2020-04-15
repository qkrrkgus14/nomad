# 시설 생성
# DB에 Create
import random
from django_seed import Seed
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "This command creates rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int ,help="How Many times do you want me to tell yoy that I love you?")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_user = user_models.User.objects.all()
        room_type = room_models.RoomType.objects.all()
        seeder.add_entity(room_models.Room, number,{
            'name' : lambda x :seeder.faker.address(),
            'host':lambda x: random.choice(all_user),
            'room_type': lambda x: random.choice(room_type),
            'guests': lambda x: random.randint(1, 20),
            'price': lambda x : random.randint(1,300),
            "beds": lambda x : random.randint(1,5),
            "bedrooms": lambda x : random.randint(1,5),
            'baths':lambda x : random.randint(1,5),
        })

        # seeder.execute() 이 코드 까지 해야 Room 생성
        # 아래의 created_photos = seeder.execute() 이 코드가 있는데
        # 이렇게 변수로 담아줘도 seeder.execute()가 동작 한다.

        ''' 여기서 부터 photo(사진) 넣는 코드 '''
        created_photos = seeder.execute()

        # created_clean -> 생성되는 id(pk)값을 얻을 수 있는 것
        created_clean = flatten(list(created_photos.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            print(pk)
            room = room_models.Room.objects.get(pk=pk)
            # 사진추가하는 방법
            for i in range(3,random.randint(10,30)): #사진갯수
                room_models.Photo.objects.create(
                    caption = seeder.faker.sentence(),
                    room = room,
                    file = f"/room_photos/{random.randint(1,31)}.webp",
                )
            #
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)  # 다대다(ManytoManyField)에서 무언가 추가하는 방법

            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)  # 다대다(ManytoManyField)에서 무언가 추가하는 방법

            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)  # 다대다(ManytoManyField)에서 무언가 추가하는 방법

        self.stdout.write(self.style.SUCCESS(f"{number} room created!"))