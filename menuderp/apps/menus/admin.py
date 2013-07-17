from django.contrib import admin
from models import Food, Watch, Profile

class FoodsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['name']}),
        ('More Info',       {'fields': ['last_date', 'next_date']}), #, 'classes': ['collapse']}),
    ]
    list_display = ('name', 'num_watches', 'last_date', 'next_date')
    search_fields = ['name']

admin.site.register(Food, FoodsAdmin)

class WatchesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['food', 'frequency', 'owner']}),
    ]
    list_display = ('food', 'frequency_name', 'owner')
    search_fields = ['food', 'frequency_name', 'owner']

admin.site.register(Watch, WatchesAdmin)

class ProfilesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['user', 'pro']}),
    ]
    list_display = ('fullname', 'email', 'used_watches', 'pro', 'can_create_new_watches')
    list_filter = ['pro']
    search_fields = ['firstname', 'lastname', 'email']

admin.site.register(Profile, ProfilesAdmin)