from django.db import models
from . import managers
# Core 앱을 만든이유 2개 DateTimeField는 모든 models의 공통된 부분이다.
# 이걸 models.py마다 쓰는거는 좋지만 프로그래밍적으로는 좋지 않은 방법이다.
# 결론 : 재사용이 가능한 common을 만들어줬다고 생각하면 된다.

# created = models.DateTimeField()
# updated = models.DateTimeField()

# Abstract -> 데이터베이스에는 나타나지 않는 모델, 그것을 "추상"모델이라고 한다.
class TimeStampeModel(models.Model):

    """ Time Stamped Model """
    created = models.DateTimeField(auto_now_add=True) #모델이 생성된 날짜
    updated = models.DateTimeField(auto_now=True)     #모델이 업데이트 된 시간
    objects = managers.CustomModelManager()

    class Meta:
        # abstract : model은 model이지만 데이터베이스에는 나타나지 않는 model
        abstract = True

