from django.contrib import admin
from django.utils.html import mark_safe
from . import models
from django.contrib.auth.admin import UserAdmin
@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = (
        "id",
        "name",
        "used_by",
    )
    def used_by(self,obj):
        print(obj)
        return obj.rooms.count()



class PhotoInline(admin.TabularInline):
    model = models.Photo

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """
    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields":("name","description","country","city","address","price","room_type")}
        ),
        (
          "Times",
            {"fields":("check_in","check_out")}
        ),
        (
            "Spaces",
            {"fields": ("guests", "beds", "bedrooms", "baths")}
        ),
        (
            "More About the Space",
            {
                # "classes":("collapse",),
                "fields": ("amenities", "facilities","house_rules"),
            }
        ),
        (
            "Last Details",
            {"fields": ("host",)}
        ),

    )

    list_display =(
        "id",
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating", # models.py 에서 만들어진 함수도 이렇게 admin.py에서 list_display로 가져다가 쓸 수 있다.
    )

    list_display_links = ("name",)

    list_filter = (
        "instant_book",
        "host__superhost",
        "host__gender",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )


    ordering = ("id","name", "price", "bedrooms")

    raw_id_fields =("host",)

    search_fields = ("city","^host__username")
    # search_fields = ("^city",) 단어의 첫부분 검색
    # search_fields = ("=city",) #단어를 정확하게 검색함. 단 대소문자 구별은 하지 않음

    #manytomany 필드에서만 쓸 수 잇는것 : filter_horizontal
    filter_horizontal = (
        "amenities","facilities","house_rules",
    )

    # self : class RoomAdmin
    # obj = admin에서의 1 row(행)을 말한다. 즉 1개의 데이터, 여기서는 Room 이지!
    def count_amenities(self, obj):

        return obj.amenities.count()
    # count_amenities.short_description = "변경해보자"

    def count_photos(self,obj):
        return obj.photos.count()
    count_photos.short_description = "Photo Count"



@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__","get_thumbnail")

    def get_thumbnail(self,obj):
        # return obj.file.url
        return mark_safe(f'<img width="50px" src="{obj.file.url}"/>')
    get_thumbnail.short_description = "Thumbnail"
