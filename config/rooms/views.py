'''
from math import ceil
from django.shortcuts import render, redirect
from django.core.paginator import Paginator,EmptyPage
from . import models
'''
import re
from django_countries import countries
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.urls import reverse
from . import models

class HomeView(ListView):

    """HomeView Definition """

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    # page_kwarg = 'page'
    ordering = "created"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context

    # def get(self, request,**kwargs):
    #     MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)  # 모바일 IOS, 안드로이드 체크
    #     if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
    #         print("여기다")
    #         aaa = "모바일이다"
    #     else:
    #         print("굿")
    #         aaa = "피씨다"
    #     return render(request,"rooms/room_list.html", {"aaa":aaa,})


class RoomDetail(DetailView):

    """ RoomDetail Definition"""

    model = models.Room


def search(request):
    # request.GET.get("city") 이렇게 적으면
    # html의 name="city"에 있는 value값을 체크해서
    # value 값을 얻어온다
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country","KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price",0))
    guests = int(request.GET.get("guests",0))
    bedrooms = int(request.GET.get("bedrooms",0))
    beds = int(request.GET.get("beds",0))
    baths = int(request.GET.get("baths",0))

    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    print(room_type)
    # Form에서 받아오는 것들
    form = {
        'city': city,
        "s_room_type": room_type,
        's_country': country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        # search.html에서 어떤 타입을 검색했는지 받아오기 위해
        "s_amenities":s_amenities,
        "s_facilities":s_facilities,
        "instant":instant,
        "superhost": superhost,
    }

    #

    # Choice ( RoomType Total )
    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    # 검색조건 만드는 법
    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
                    #여기서 room_type은 Room 모델의 Foreignkey다
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    print(instant,superhost)

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True


    print(s_amenities, s_facilities)
    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = models.Room.objects.filter(**filter_args)
    print(rooms)
    # DB에서 넘어오는 것들은 여기에 넣음음
    choices ={
        'countries': countries,   # 라이브러리
        "room_types": room_types,
        "amenities":amenities,
        "facilities":facilities,
    }

    return render(request, 'rooms/search.html',{
        **form, **choices,"rooms":rooms,
    })