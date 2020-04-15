# 편의시설
# DB에 Create

from django.core.management.base import BaseCommand
from rooms import models as room_models
# from rooms.models import Amenity

class Command(BaseCommand):
    help = "This command creates amenities"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times",help="How Many times do you want me to tell yoy that I love you?")

    def handle(self, *args, **options):
        amenities = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boarting",
            "Cable TV",
            "Carbon monoxide detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double bed",
            "En suite bathroom",
            "Free Parking",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Queen size bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke detactors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]
        for a in range(len(amenities)):
            room_models.Amenity.objects.create(name=amenities[a])
            print(a+1, "  Create amenities : ", amenities[a])
        self.stdout.write(self.style.SUCCESS("Amenities created!"))


'''
주방
샴푸
난방
에어컨
세탁기
건조기
무선 인터넷
아침식사
실내 벽난로
옷걸이
다리미
헤어드라이어
노트북 작업 공간
TV
아기 침대
유아용 식탁의자
셀프 체크인
화재 감지기
일산화탄소 감지기
욕실 단독 사용
수변
'''