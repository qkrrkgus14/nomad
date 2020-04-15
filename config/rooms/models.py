# 임포트 순서
# 1. 파이썬 관련, 2.Django 관련, 3. 외부패키지, 4. 애플리케이션(앱)

from django.db import models
from django.urls import reverse
from core import models as core_models
from django_countries.fields import CountryField
from users import models as user_models

"""
ForeignKey : 일대다관계
user : 일
room : 다
"""

class AbstractItem(core_models.TimeStampeModel):
    """ Abstract Item """
    name = models.CharField(max_length=80)


    class Meta:
        abstract = True

    def __str__(self):
        return self.name

# 숙소 유형(집 전체, 개인실, 호텔 객실, 다인실 --> 에어비앤비 홈페이지 참조)
class RoomType(AbstractItem):

    """RoomType Object Definition"""
    class Meta:
        verbose_name = "Room Type"
        ordering = ['created']


# 편의 시설
class Amenity(AbstractItem):

    """ Amenity Object Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


# 시설
class Facility(AbstractItem):

    """ Facility Object Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


# 객실안에서의 규칙
class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampeModel):

    """ Photo Model Definition """
    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room =  models.ForeignKey("Room", related_name="photos",on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampeModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)     # 숙소이름
    description = models.TextField()            # 숙소설명
    country = CountryField()                     # 국가
    city = models.CharField(max_length=80)      # 도시
    price = models.IntegerField()               # 가격
    address = models.CharField(max_length=140)  # 주소
    guests = models.IntegerField()              # 게스트 몇명 묵을 수 있는지
    beds = models.IntegerField()                # 침대 갯수
    bedrooms = models.IntegerField()            # 침실 (방 갯수)
    baths = models.IntegerField()               # 화장실 갯수
    check_in = models.TimeField()               # 체크인 여부 (들어오는 날짜)
    check_out = models.TimeField()              # 체크인 여부 (나가는 날짜)
    instant_book =  models.BooleanField(default=False)                  # 바로예약

    # related_name --> user가 어떻게 우리를 찾기 원합니까?
    host = models.ForeignKey("users.User", related_name="rooms",on_delete=models.CASCADE)    # 집(room) 주인

    # room_type을 ForeignKey로 쓴 이유 --> 1개만 선택 할수 있도록 하기 위함
    room_type = models.ForeignKey("RoomType", related_name="rooms",on_delete=models.SET_NULL,null=True)
    amenities = models.ManyToManyField("Amenity",related_name="rooms",blank=True)           # 편의 시설 목록
    facilities = models.ManyToManyField("Facility",related_name="rooms",blank=True)          # 시설
    house_rules = models.ManyToManyField("HouseRule",related_name="rooms",blank=True)        # 객실내에서의 규칙

    def __str__(self):
        return self.name
    
    # 모델을 건드릴때 항상 일어나는 메소드
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city) #(영어)첫번째 문자 대문자로 바꾸어줌
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={'pk':self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings+=review.rating_average()
            return round(all_ratings / len(all_reviews),2)
        return 0

    def first_photo(self):
        photo, = self.photos.all()[:1]
        return photo.file.url

"""
room(룸)은 오직 한 명의 host(주인)를 가질 수 있다. ForeignKey
amenities,facilities,house_rules  room에서 여러개를 가질 수 있다. ManyToManyField
"""
