from django.contrib import admin

from contacts.models import Contact


# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'listings')
    list_display_links = ('id', 'name')
    search_fields = ('email', 'name')
    list_per_page = 25


admin.site.register(Contact, ContactAdmin)
