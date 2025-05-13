from django.contrib import admin
from . models import MainMenu, MenuItem

class MainMenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent',)
    list_display_links = ('name',)

admin.site.register(MainMenu, MainMenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
