from django.contrib import admin
from django.db.models.functions import Upper

from .models import Employee


class AgeFilter(admin.SimpleListFilter):
    title = 'Yoshi boyicha'
    parameter_name = 'ages'

    def lookups(self, request, model_admin):
        return [
            ('10-20', '10 dan 20 gacha'),
            ('20-30', '21 dan 30 gacha'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '10-20':
            return queryset.filter(age__range=[10, 20])

        if self.value() == '20-30':
            return queryset.filter(age__range=[21, 30])


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    def to_upper(self, request, queryset):
        queryset.update(first_name=Upper('first_name'),
                        last_name=Upper('last_name'))

    exclude = ['language']
    list_display = ['id', 'age', 'get_full_name_html']
    list_filter = ['gender', AgeFilter]
    search_fields = ['first_name', 'last_name']
    list_editable = ['age']
    list_per_page = 10
    actions = [to_upper]
