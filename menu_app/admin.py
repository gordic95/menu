from django.contrib import admin
from . models import MainMenu

class MainMenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'url', 'route_name')
    list_display_links = ('title',)
    prepopulated_fields = {'url': ('title',)}



admin.site.register(MainMenu, MainMenuAdmin)
