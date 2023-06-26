from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from accounts.models import Client, Domain
from users.models import CustomUser


#Register your models here.
class DomainInline(admin.TabularInline):
    model = Domain
    extra = 1

class ClientInline(admin.StackedInline):
    model = Client
    extra = 1

# @admin.register(CustomUser)
# class CustomerAdmin(TenantAdminMixin, admin.ModelAdmin):
#     inlines = [ClientInline]
#     list_display = ('username', 'email')

class ClientUserAdmin(TenantAdminMixin, admin.ModelAdmin):
    inlines = [ClientInline]

class DomainAdmin(admin.ModelAdmin):
    inlines = [DomainInline]

admin.site.register(CustomUser, ClientUserAdmin)
admin.site.register(Client, DomainAdmin)
admin.site.register(Domain)
