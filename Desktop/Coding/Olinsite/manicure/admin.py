from django.contrib import admin

# Register your models here.
from .models import *


class PriceItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'pricepart')
    list_display_links = ('title',)
    search_fields = ('title',)


class AboutAdmin(admin.ModelAdmin):
    list_display = ('image', 'image_img', 'text')
    list_display_links = ('image', 'text',)
    search_fields = ('text',)


class FeedbackItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'feedback_photo', 'photo', 'text')
    list_display_links = ('name',)
    search_fields = ('name',)


class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('gallery_photo', 'photo',)
    list_display_links = ('photo',)
    #search_fields = ('name',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'phone_number', 'message')
    list_display_links = ('name',)
    search_fields = ('phone_number',)


admin.site.register(PriceItem, PriceItemAdmin)
admin.site.register(PricePart)
admin.site.register(AboutMaster, AboutAdmin)
admin.site.register(FeedbackItem, FeedbackItemAdmin)
admin.site.register(GalleryPhoto, GalleryPhotoAdmin)
admin.site.register(Contact, ContactAdmin)