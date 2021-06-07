from django.contrib import admin
from activity.models import Activity, QueryClient


class ActivityAdmin(admin.ModelAdmin):
    save_on_top = True
    model = Activity
    list_display = ['phone', 'status', 'cpf', 'matricula']
    list_filter = ('phone', 'status', 'cpf', 'matricula')
    search_fields = ('phone', 'status', 'cpf', 'matricula')


admin.site.register(Activity, ActivityAdmin)


class QueryClientAdmin(admin.ModelAdmin):
    save_on_top = True
    model = QueryClient
    list_display = ['cpf', 'user']
    list_filter = ('cpf', 'user')
    search_fields = ('cpf', 'user')


admin.site.register(QueryClient, QueryClientAdmin)
