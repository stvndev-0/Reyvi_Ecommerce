from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('last_login', 'email', 'username', 'is_staff', 'is_active',)
    search_fields = ('email', 'username', 'is_staff', 'is_active',)
    ordering = ('username',)

# Desregistrar el UserAdmin predeterminado
admin.site.unregister(User)

# Registrar el nuevo UserAdmin con el inline de Profile
admin.site.register(User, UserAdmin)