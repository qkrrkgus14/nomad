import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from core import managers as core_managers
from django.shortcuts import reverse
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
"""
Null = 데이터베이스에 사용(적용)되는 것
blank = form에서 사용(적용)되는 것, 보여지는 것 
"""
# Abstract -> 데이터베이스에는 나타나지 않는 모델, 그것을 "추상"모델이라고 한다.
# class User --> 내장되어있는 AbstractUser모델 재정의
class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        # (DB저장되는값, "밖으로 보여지는 값"),
        (GENDER_MALE,"Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD,'USD'),
        (CURRENCY_KRW,'KRW'),
    )


    LOGIN_EMAIL = 'email'
    LOGIN_GITHUB = 'github'
    LOGIN_KAKAO = 'kakao'

    LOGIN_CHOICES = (
        (LOGIN_EMAIL,"Email"),
        (LOGIN_GITHUB,"Github"),
        (LOGIN_KAKAO,"Kakao"),)


    objects = core_managers.CustomUserManager()

    avatar = models.ImageField(upload_to='avatars',blank=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=10,  blank=True) #CharField 한 줄 텍스트, 글자수 제한
    bio = models.TextField(blank=True) #TextField 여러줄, 글자 제한 없음
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2,  blank=True, default=LANGUAGE_KOREAN)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3,  blank=True, default=CURRENCY_KRW)
    #super host --> 인증받은 airbnb 호스트
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)
    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)


    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})


    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret":secret})
            send_mail("Verify Airbnb Account",
                      strip_tags(html_message),
                      settings.EMAIL_FROM,
                      [self.email],
                      fail_silently=False,
                      html_message=html_message,
                      )
            self.save()
        return

