from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin', 'is_active')
    list_filter = ('email', 'is_admin')
    search_fields = ('email', 'phone_number')
    ordering = ('email',)

    fieldsets = (
        ('Main', {'fields': ('full_name', 'email', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'last_login', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('full_name', 'email', 'phone_number', 'password')}),
    )

    readonly_fields = ('last_login',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


admin.site.register(User, UserAdmin)
