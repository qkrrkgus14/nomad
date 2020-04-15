from django.db import models
from core import models as core_models
from rooms import models as room_models



class Review(core_models.TimeStampeModel):
    """Review Model Definition"""

    review = models.TextField()
    accuracy = models.IntegerField() #정확성
    communication = models.IntegerField() # 의사소통
    cleanliness = models.IntegerField() # 청결도
    location = models.IntegerField() #위치
    check_in = models.IntegerField() # 체크인
    value = models.IntegerField() # 가치
    user = models.ForeignKey("users.User", related_name="reviews", on_delete = models.CASCADE)
    room = models.ForeignKey("rooms.Room", related_name="reviews", on_delete = models.CASCADE)

    # room = models.ForeignKey("rooms.Room", related_name="reviews", on_delete = models.CASCADE)
    # 이 코드를 기준으로 설명하면 room 이랑 외래키로 연결되어있으니 room 모델에서 reviews로 쓰일 수 있다.

    #admin 에서 list_display에서 "__str__"로 사용 할 수 있다.
    def __str__(self):
        return f"{self.review} - {self.room}"

    # 이 함수는 admin에서 사용 가능
    def rating_average(self):
        avg = (
            self.accuracy+
            self.communication+
            self.cleanliness+
            self.location+
            self.check_in+
            self.value
        ) / 6
        return round(avg,2)

    rating_average.short_description = "Avg."
