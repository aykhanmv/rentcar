from django.contrib import admin
from typing import Sequence
from django.contrib import admin, messages
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter

from user.models import (
    MyUser, 
)


# Register your models here.
class CompanyActiveListFilter(SimpleListFilter):
    title = "company employee activation status"
    parameter_name = 'company_active'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Active'),
            ('false', 'Inactive')
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(user_choices="Company",is_company_active=True)
        elif self.value() == 'false':
            return queryset.filter(user_choices="Company",is_company_active=False)

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    readonly_fields = (
        "last_activity",
        'password',
        'mail_choices'
    )
    search_fields = ("email", "first_name", "last_name")
    list_filter = (
        CompanyActiveListFilter,
    )


