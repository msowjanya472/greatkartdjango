from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    model = Account

    # Fields to display in the admin list view
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_superuser')

    # Fields editable directly in list view
    list_editable = ('is_staff', 'is_superuser')

    # Fields that are searchable in admin
    search_fields = ('email', 'username', 'first_name', 'last_name')

    # Default ordering
    ordering = ('email',)

    # Fields shown on the user detail page
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )

    # Fields shown when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )

# Register the Account model with custom admin
admin.site.register(Account, AccountAdmin)
