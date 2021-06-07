from django.contrib import admin

from authentication.models import Usuario, Empresa, InterestedIn


class CustomerUserAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'phone')
    search_fields = ['name', 'phone']
    model = Usuario


admin.site.register(Usuario, CustomerUserAdmin)


class EmpresaAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('nome', 'razao_social', 'n_user_disponiveis')
    search_fields = ['nome', 'razao_social']
    model = Empresa


admin.site.register(Empresa, EmpresaAdmin)


class InterestedInUser(admin.ModelAdmin):
    model = InterestedIn
    list_display = ('name', 'phone', 'email')
    search_fields = ['name', 'email']

admin.site.register(InterestedIn, InterestedInUser)
